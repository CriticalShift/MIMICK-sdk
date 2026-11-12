"""Monitors: a value sampled on an interval while a step runs.

    with s.monitor("vbat_v", every=0.1, unit="V", lower=3.6, gpio=None,
                   software=("meter0", r"([0-9.]+) V")):
        boot()

A Controller-side monitor asks mimickd to sample one of the Station's
peripherals, with steady timing independent of the test. An in-process
monitor calls a function of the test. Either way each sample is a row of the
step, judged against the limits, and stopping the monitor records one series
observation judged over its worst sample. A step stops its open monitors when
it closes.
"""

from __future__ import annotations

import datetime as dt
import threading
import time
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from mimick import env as _env, events

if TYPE_CHECKING:
    from mimick.run import Step

_WORST = {"unset": 0, "pass": 1, "marginal": 2, "fail": 3}


@dataclass
class Series:
    """What a stopped monitor recorded."""

    count: int = 0
    errors: int = 0
    first: dt.datetime | None = None
    last: dt.datetime | None = None
    min: float | None = None
    max: float | None = None
    verdict: str = "unset"
    # (time, value) pairs, oldest first.
    samples: list[tuple[dt.datetime, float]] = field(default_factory=list)


def judge(v: float, lower, upper, marginal) -> str:
    from mimick.run import _judge

    mlo, mhi = marginal or (None, None)
    return _judge(v, lower, upper, mlo, mhi)


class Monitor:
    def __init__(self, step: Step, name: str, every: float, unit: str, lower, upper, marginal,
                 source: Callable[[], float] | None, controller: dict | None):
        if every < 0.01:
            raise ValueError("a monitor samples at most every 10 ms")
        self.step, self.name, self.every, self.unit = step, name, every, unit
        self.lower, self.upper, self.marginal = lower, upper, marginal
        self.series: Series | None = None
        self._source, self._controller = source, controller
        self._stop = threading.Event()
        self._thread: threading.Thread | None = None
        self._local = Series()
        self._id = ""

    # -- lifecycle ------------------------------------------------------------

    def start(self) -> Monitor:
        if self._controller is not None:
            from mimick.appliance.v1 import run_report_pb2, run_report_pb2_grpc

            req = run_report_pb2.StartMonitorRequest(
                name=self.name, node_run_id=self.step.id, every_ms=int(self.every * 1000), unit=self.unit,
                **{k: v for k, v in (("lower", self.lower), ("upper", self.upper)) if v is not None},
                **_marginal_kwargs(self.marginal), **self._controller)
            stub = run_report_pb2_grpc.RunReportServiceStub(_env.channel(self.step.run.env))
            self._id = stub.StartMonitor(req).id
        else:
            self._thread = threading.Thread(target=self._sample_loop, name=f"mimick-monitor-{self.name}",
                                            daemon=True)
            self._thread.start()
        self.step._monitors.append(self)
        return self

    def stop(self) -> Series:
        if self.series is not None:
            return self.series
        if self._controller is not None:
            from mimick.appliance.v1 import run_report_pb2, run_report_pb2_grpc

            stub = run_report_pb2_grpc.RunReportServiceStub(_env.channel(self.step.run.env))
            got = stub.StopMonitor(run_report_pb2.StopMonitorRequest(id=self._id))
            series = Series(
                count=got.count, errors=got.errors,
                first=_time(got.first) if got.count else None, last=_time(got.last) if got.count else None,
                min=got.min if got.count else None, max=got.max if got.count else None,
                verdict=got.verdict or "unset",
                samples=[(_time(s.at), s.value) for s in got.samples])
        else:
            self._stop.set()
            if self._thread is not None:
                self._thread.join()
            series = self._local
        self.series = series
        if self in self.step._monitors:
            self.step._monitors.remove(self)
        self._record(series)
        return series

    def __enter__(self) -> Monitor:
        return self

    def __exit__(self, *exc) -> bool:
        self.stop()
        return False

    # -- in-process sampling --------------------------------------------------

    def _sample_loop(self) -> None:
        next_at = time.monotonic()
        while not self._stop.is_set():
            self._sample_once()
            next_at += self.every
            self._stop.wait(max(0.0, next_at - time.monotonic()))

    def _sample_once(self) -> None:
        s = self._local
        try:
            v = float(self._source())
        except Exception:  # noqa: BLE001 - a failed sample is counted, not raised into the test
            s.errors += 1
            return
        now = dt.datetime.now(dt.timezone.utc)
        verdict = judge(v, self.lower, self.upper, self.marginal)
        s.count += 1
        s.first = s.first or now
        s.last = now
        s.min = v if s.min is None else min(s.min, v)
        s.max = v if s.max is None else max(s.max, v)
        if _WORST[verdict] > _WORST[s.verdict]:
            s.verdict = verdict
        s.samples.append((now, v))
        del s.samples[:-10000]
        self.step.run.emitter.emit_sample(events.Event(
            events.OBSERVE, f"Sampled {self.name}={v:g}" + (f" {self.unit}" if self.unit else ""),
            task_id=self.step.id, attrs=sample_attrs(self.name, v, self.unit, verdict)))

    # -- the series record ----------------------------------------------------

    def _record(self, s: Series) -> None:
        attrs = {
            "mimick.observation.name": self.name,
            "mimick.observation.verdict": s.verdict,
            "mimick.observation.series.rows": str(s.count),
        }
        if self.unit:
            attrs["mimick.observation.unit"] = self.unit
        if self.lower is not None:
            attrs["mimick.observation.lower"] = repr(float(self.lower))
        if self.upper is not None:
            attrs["mimick.observation.upper"] = repr(float(self.upper))
        if s.first and s.last:
            attrs["mimick.observation.series.from"] = s.first.isoformat()
            attrs["mimick.observation.series.to"] = s.last.isoformat()
        body = f"Monitored {self.name}: {s.count} samples"
        if s.count:
            body += f", {s.min:g} to {s.max:g}" + (f" {self.unit}" if self.unit else "")
        if s.verdict in ("fail", "marginal"):
            body += f" ({s.verdict})"
        if s.verdict == "fail":
            self.step._failed_observations.append(self.name)
        elif s.verdict == "marginal":
            self.step._marginal = True
        self.step.run.emitter.emit(events.Event(events.OBSERVE, body, level="warn" if s.verdict == "fail" else "info",
                                                task_id=self.step.id, attrs=attrs))


def sample_attrs(name: str, v: float, unit: str, verdict: str) -> dict[str, str]:
    attrs = {
        "mimick.observation.name": name,
        "mimick.observation.value": repr(float(v)),
        "mimick.observation.type": "num",
        "mimick.observation.verdict": verdict,
        "mimick.observation.sample": "true",
    }
    if unit:
        attrs["mimick.observation.unit"] = unit
    return attrs


def _marginal_kwargs(marginal) -> dict:
    if not marginal:
        return {}
    lo, hi = marginal
    out = {}
    if lo is not None:
        out["marginal_lower"] = lo
    if hi is not None:
        out["marginal_upper"] = hi
    return out


def _time(ts) -> dt.datetime:
    return dt.datetime.fromtimestamp(ts.seconds + ts.nanos / 1e9, tz=dt.timezone.utc)


def controller_source(gpio=None, relay=None, software=None) -> dict:
    """The StartMonitorRequest source for one Station peripheral.

    gpio=(location, pin), relay=(location, channel), or software=location or
    (location, pattern), where a location is an interface such as io0.gpio0.
    mimickd opens it while the monitor runs.
    """
    from mimick.appliance.v1 import run_report_pb2

    given = [x for x in (gpio, relay, software) if x is not None]
    if len(given) != 1:
        raise ValueError("give exactly one of gpio, relay or software")
    if gpio is not None:
        location, pin = gpio
        return {"gpio_pin": run_report_pb2.GpioPinSource(location=location, pin=pin)}
    if relay is not None:
        location, channel = relay
        return {"relay_channel": run_report_pb2.RelayChannelSource(location=location, channel=channel)}
    location, pattern = (software, "") if isinstance(software, str) else software
    return {"software_read": run_report_pb2.SoftwareReadSource(location=location, pattern=pattern)}
