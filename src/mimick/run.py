"""The run object model: a Run, and the Steps (node runs) inside it.

    with run.start(plan) as r:
        with r.step("flash") as s:
            s.observe("vbat", 4.21)

Each step writes a start record when it opens and a stop record when it
closes, with the outcome its body set, or fail when an observation or a child
failed, or error when an exception escaped. Calls to mimickd made inside a step
are recorded under it. The rules match the Go CLI's `mimick task` verbs.
"""

from __future__ import annotations

import math
import re
import sys
import threading
import uuid
from collections.abc import Iterator
from typing import Any

from mimick import correlation, env as _env, events
from mimick.plan import Measure, Node, Plan, canonicalize, digest, measure, node, plan  # noqa: F401

PASS, FAIL, ERROR, ABORTED, SKIP, INCONCLUSIVE = "pass", "fail", "error", "aborted", "skip", "inconclusive"
# A node its framework gives no outcome, such as an OpenHTF group.
NONE = "none"
ERROR_SOURCES = ("dut", "test", "infrastructure")
_CODE = re.compile(r"^[A-Z0-9_]+$")

# Best to worst, for a parent's or the run's worst outcome.
_RANK = {SKIP: 1, PASS: 2, INCONCLUSIVE: 3, ABORTED: 4, FAIL: 5, ERROR: 6}

_STOP_VERB = {NONE: "ended", PASS: "passed", FAIL: "failed", SKIP: "skipped", ERROR: "errored", ABORTED: "aborted",
              INCONCLUSIVE: "was inconclusive"}


def _worst(latest: dict[tuple, tuple[str, bool]]) -> tuple[str, bool]:
    """The worst latest outcome among steps, and whether any was marginal. A
    retry replaces the attempt before it, so a step that passed on its second
    try fails nothing."""
    result, marginal = "", False
    for r, m in latest.values():
        if _RANK.get(r, 0) > _RANK.get(result, 0):
            result = r
        marginal = marginal or m
    return result, marginal


def node_key(name: str) -> str:
    """The key a step named name gets when nothing gives it one, as the CLI derives it."""
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def start(plan: Plan | None = None, *, environ: dict[str, str] | None = None, sink=None) -> Run:
    """Opens the run described by the environment, declaring plan when given."""
    e = _env.from_environ(environ)
    _env.activate(e)
    return Run(e, plan, events.Emitter(e.collector, e.run_id, e.session_id, sink=sink))


class Run:
    def __init__(self, environment: _env.Env, plan: Plan | None, emitter: events.Emitter):
        self.env = environment
        self.plan = plan
        self.emitter = emitter
        self._lock = threading.Lock()
        self._open: list[Step] = []
        self._attempts: dict[tuple, int] = {}
        # The latest outcome of each top-level step, by attempt series.
        self._top: dict[tuple, tuple[str, bool]] = {}
        self._closed = False

    @property
    def dut(self) -> _env.Dut:
        return self.env.dut

    def __enter__(self) -> Run:
        if self.plan is not None:
            canonical, _ = canonicalize(self.plan.canonical())
            self.emitter.emit(events.Event(
                events.PLAN, canonical.decode("utf-8"), attrs={"mimick.plan.digest": digest(canonical)}))
        return self

    def __exit__(self, exc_type, exc, tb) -> bool:
        if exc is not None:
            reason = f"{exc_type.__name__}: {exc}"
            self._abandon(ERROR, reason, source="test")
            self.end(ERROR, reason)
        else:
            self._abandon(ABORTED, "The run ended with this step open")
            self.end()
        self.emitter.flush()
        return False

    def _abandon(self, result: str, reason: str, source: str = "") -> None:
        with self._lock:
            still_open = list(reversed(self._open))
        for s in still_open:
            if not s.closed:
                s._close(result, reason, source=source)

    def end(self, outcome: str = "", reason: str = "", marginal: bool = False) -> None:
        """Closes the run itself. The outcome defaults to the worst top-level one."""
        if self._closed:
            return
        self._closed = True
        top, top_marginal = _worst(self._top)
        result = outcome or top or PASS
        marginal = result == PASS and (marginal or top_marginal)
        attrs = {"mimick.task.result": result, "mimick.task.marginal": str(marginal).lower()}
        if reason:
            attrs["mimick.task.reason"] = reason
        body = f"Run ended: {result}" + (f": {reason}" if reason else "")
        self.emitter.emit(events.Event(events.STOP, body, level="error" if result in (FAIL, ERROR) else "info",
                                       attrs=attrs))

    def step(self, key: str = "", name: str = "", kind: str = "", attempt: int = 0,
             iteration: dict[str, str] | None = None) -> Step:
        """A node run, opened by `with`. key defaults to the slug of name."""
        if not key:
            if not name:
                raise ValueError("a step needs a key or a name")
            key = node_key(name)
        declared = self.plan.find(key) if self.plan else None
        return Step(self, key, name or (declared.name if declared else "") or key,
                    kind or (declared.kind if declared else "") or "task", attempt, dict(iteration or {}), declared)

    def retry(self, key: str = "", name: str = "", tries: int = 3, **kwargs) -> Iterator[Step]:
        """Attempts of one step until one passes, at most tries of them.

            for s in r.retry("flash", tries=3):
                with s:
                    flash()

        An exception in an attempt before the last is recorded on that attempt
        and does not leave the loop.
        """
        for i in range(tries):
            s = self.step(key, name, **kwargs)
            s._swallow = i < tries - 1
            yield s
            if s.outcome == PASS:
                return

    def log(self, message: str, level: str = "info", code: str = "", **data: Any) -> None:
        """A message on the innermost open step, or on the run."""
        _message(self, self.current_id(), message, level, code, data)

    def current_id(self) -> str:
        return correlation.current()

    def _next_attempt(self, key: str, iteration: dict[str, str], given: int) -> int:
        series = (key, tuple(sorted(iteration.items())))
        with self._lock:
            n = given or self._attempts.get(series, 0) + 1
            self._attempts[series] = max(self._attempts.get(series, 0), n)
            return n


def _message(r: Run, task_id: str, message: str, level: str, code: str, data: dict[str, Any]) -> None:
    if level not in events.SEVERITY:
        raise ValueError(f"level must be one of {', '.join(events.SEVERITY)}")
    if code and not _CODE.match(code):
        raise ValueError(f"diagnosis code {code!r} must be upper-case letters, digits and underscores")
    attrs = {"mimick.code": code} if code else {}
    r.emitter.emit(events.Event(events.MESSAGE, message, level=level, task_id=task_id, attrs=attrs,
                                data={k: str(v) for k, v in data.items()}))


class Step:
    def __init__(self, run: Run, key: str, name: str, kind: str, attempt: int, iteration: dict[str, str],
                 declared: Node | None):
        self.run = run
        self.key, self.name, self.kind = key, name, kind
        self.id = str(uuid.uuid4())
        self.parent: Step | None = None
        self.attempt = attempt
        self.iteration = iteration
        self.declared = declared
        self.outcome = ""
        self.closed = False
        self._set: tuple[str, str, str, tuple[str, ...], bool] | None = None
        self._failed_observations: list[str] = []
        self._marginal = False
        # The latest outcome of each child step, by attempt series.
        self._children: dict[tuple, tuple[str, bool]] = {}
        self._swallow = False
        self._reset = None

    # -- lifecycle ------------------------------------------------------------

    def __enter__(self) -> Step:
        self.begin()
        self._reset = correlation._current.set(self.id)
        return self

    def begin(self) -> Step:
        """Opens the step without making it the context's current one, for an
        adapter that opens and closes steps from threads other than the test's.
        Close it with end()."""
        r = self.run
        with r._lock:
            self.parent = r._open[-1] if r._open else None
            r._open.append(self)
        self.attempt = r._next_attempt(self.key, self.iteration, self.attempt)
        attrs = {
            "mimick.task.name": self.name,
            "mimick.task.node": self.key,
            "mimick.task.kind": self.kind,
            "mimick.task.attempt": str(self.attempt),
        }
        if self.parent is not None:
            attrs["mimick.task.parent"] = self.parent.id
        for k, v in self.iteration.items():
            attrs["mimick.task.iteration." + k] = str(v)
        r.emitter.emit(events.Event(events.START, f'Started task "{self.name}"', task_id=self.id, attrs=attrs))
        return self

    def end(self, result: str, reason: str = "", marginal: bool = False, source: str = "",
            codes: tuple[str, ...] = ()) -> None:
        """Closes the step with the outcome its framework reported, as is: no
        failed observation or child turns a pass into a fail."""
        if not self.closed:
            self._close(result, reason, source=source, codes=codes, marginal=marginal, derive=False)

    def __exit__(self, exc_type, exc, tb) -> bool:
        if self._reset is not None:
            correlation._current.reset(self._reset)
            self._reset = None
        if self.closed:
            return False
        if exc is not None:
            result, reason, source, codes, marginal = self._set or (ERROR, "", "test", (), False)
            if result not in (FAIL, ERROR):
                result, source = ERROR, "test"
            self._close(result, reason or f"{exc_type.__name__}: {exc}", source=source, codes=codes)
            return self._swallow
        result, reason, source, codes, marginal = self._set or (PASS, "", "", (), False)
        self._close(result, reason, source=source, codes=codes, marginal=marginal)
        return False

    # -- outcome --------------------------------------------------------------

    def fail(self, reason: str = "", source: str = "", codes: tuple[str, ...] = ()) -> None:
        self._set_outcome(FAIL, reason, source, codes)

    def error(self, reason: str = "", source: str = "", codes: tuple[str, ...] = ()) -> None:
        self._set_outcome(ERROR, reason, source, codes)

    def skip(self, reason: str = "") -> None:
        self._set_outcome(SKIP, reason)

    def abort(self, reason: str = "") -> None:
        self._set_outcome(ABORTED, reason)

    def inconclusive(self, reason: str = "") -> None:
        self._set_outcome(INCONCLUSIVE, reason)

    def passed(self, marginal: bool = False) -> None:
        self._set_outcome(PASS, marginal=marginal)

    def _set_outcome(self, result: str, reason: str = "", source: str = "", codes: tuple[str, ...] = (),
                     marginal: bool = False) -> None:
        if source and source not in ERROR_SOURCES:
            raise ValueError(f"source must be one of {', '.join(ERROR_SOURCES)}")
        if source and result not in (FAIL, ERROR):
            raise ValueError("source applies only to a fail or an error")
        for c in codes:
            if not _CODE.match(c):
                raise ValueError(f"diagnosis code {c!r} must be upper-case letters, digits and underscores")
        self._set = (result, reason, source, tuple(codes), marginal)

    def _close(self, result: str, reason: str = "", source: str = "", codes: tuple[str, ...] = (),
               marginal: bool = False, derive: bool = True) -> None:
        r = self.run
        if derive and result == PASS:
            why = ""
            if self._failed_observations:
                why = "observation " + ", ".join(self._failed_observations) + " failed"
            elif _worst(self._children)[0] in (FAIL, ERROR):
                why = f"a child step {_worst(self._children)[0]}ed"
            if why:
                result, reason = FAIL, reason or "Passed, but " + why
                print(f'mimick: "{self.name}" is recorded as failed: {why}', file=sys.stderr)
        if derive:
            marginal = result == PASS and (marginal or self._marginal or _worst(self._children)[1])
        out: list[events.Event] = []
        for c in codes:
            out.append(events.Event(events.MESSAGE, reason or "Diagnosis " + c, level="error", task_id=self.id,
                                    attrs={"mimick.code": c}))
        if not codes and result in (FAIL, ERROR):
            out.append(events.Event(events.MESSAGE, reason or "Task failed", level="error", task_id=self.id))
        attrs = {"mimick.task.name": self.name, "mimick.task.result": result,
                 "mimick.task.marginal": str(marginal).lower()}
        if reason:
            attrs["mimick.task.reason"] = reason
        if source:
            attrs["mimick.task.error_source"] = source
        body = f'Task "{self.name}" {_STOP_VERB.get(result, "stopped")}' + (f": {reason}" if reason else "")
        out.append(events.Event(events.STOP, body, level="error" if result in (FAIL, ERROR) else "info",
                                task_id=self.id, attrs=attrs))
        r.emitter.emit(*out)
        self.outcome, self.closed = result, True
        with r._lock:
            if self in r._open:
                r._open.remove(self)
            series = (self.key, tuple(sorted(self.iteration.items())))
            latest = self.parent._children if self.parent is not None else r._top
            latest[series] = (result, marginal)

    # -- results --------------------------------------------------------------

    def observe(self, name: str, value: Any, unit: str = "", lower: float | None = None,
                upper: float | None = None, marginal: tuple[float | None, float | None] | None = None,
                coords: dict[str, str] | None = None, verdict: bool | str = True) -> str:
        """Records one value and returns its verdict: pass, fail, marginal or unset.

        A value the plan declares takes its unit and limits from the plan, and
        the arguments override them. A failed verdict makes the step fail.
        verdict=False records no verdict, and a verdict string, such as one a
        test framework already judged, is recorded as given.
        """
        decl: Measure | None = None
        if self.declared is not None:
            decl = next((o for o in self.declared.observations if o.name == name), None)
        typ, text, number = _value_type(value)
        unit = unit or (decl.unit if decl else "")
        lo = lower if lower is not None else (decl.lower if decl else None)
        hi = upper if upper is not None else (decl.upper if decl else None)
        mlo, mhi = marginal if marginal else ((decl.marginal or (None, None)) if decl else (None, None))
        result = "unset"
        if isinstance(verdict, str):
            if verdict not in ("pass", "fail", "marginal", "unset"):
                raise ValueError("verdict must be pass, fail, marginal or unset")
            result = verdict
        elif verdict and typ == "num":
            result = _judge(number, lo, hi, mlo, mhi)
        attrs = {"mimick.observation.name": name, "mimick.observation.value": text,
                 "mimick.observation.type": typ, "mimick.observation.verdict": result}
        if unit:
            attrs["mimick.observation.unit"] = unit
        if lower is not None:
            attrs["mimick.observation.lower"] = _num_text(lower)
        if upper is not None:
            attrs["mimick.observation.upper"] = _num_text(upper)
        for k, v in (coords or {}).items():
            attrs["mimick.observation.coords." + k] = str(v)
        if result == "fail":
            self._failed_observations.append(name)
            print(f"mimick: {name}={text} is outside its limits", file=sys.stderr)
        elif result == "marginal":
            self._marginal = True
            print(f"mimick: {name}={text} is outside its marginal limits", file=sys.stderr)
        body = f"Observed {name}={text}" + (f" {unit}" if unit else "") + \
            (f" ({result})" if result in ("fail", "marginal") else "")
        self.run.emitter.emit(events.Event(events.OBSERVE, body, level="warn" if result == "fail" else "info",
                                           task_id=self.id, attrs=attrs))
        return result

    def log(self, message: str, level: str = "info", code: str = "", **data: Any) -> None:
        _message(self.run, self.id, message, level, code, data)

    def attach(self, path: str, name: str = "", media_type: str = "") -> str:
        """Uploads a file and attaches it to this step. Returns its file id."""
        from mimick import files

        return files.attach(self.run, self.id, path, name, media_type)

    # Steps nested in this one; a convenience for `with s.step(...)`.
    def step(self, *args, **kwargs) -> Step:
        return self.run.step(*args, **kwargs)


def _value_type(value: Any) -> tuple[str, str, float]:
    if isinstance(value, bool):
        return "bool", str(value).lower(), 0.0
    if isinstance(value, (int, float)) and math.isfinite(value):
        return "num", _num_text(value), float(value)
    text = str(value)
    if text in ("true", "false"):
        return "bool", text, 0.0
    try:
        f = float(text)
        if math.isfinite(f):
            return "num", text, f
    except ValueError:
        pass
    return "text", text, 0.0


def _num_text(v: float) -> str:
    return str(int(v)) if isinstance(v, float) and v.is_integer() else str(v)


def _judge(v: float, lower, upper, mlower, mupper) -> str:
    if lower is None and upper is None and mlower is None and mupper is None:
        return "unset"
    if (lower is not None and v < lower) or (upper is not None and v > upper):
        return "fail"
    if (mlower is not None and v < mlower) or (mupper is not None and v > mupper):
        return "marginal"
    return "pass"
