"""Live reporting of an OpenHTF test.

A watcher thread follows OpenHTF's live test state, the mechanism its station
GUI uses (`TestState.asdict_with_event()`), and an output callback reports the
final record. Nothing in OpenHTF is patched.

A phase's step opens when the phase starts. It closes once the next phase has
started or the test ended: OpenHTF changes a repeated phase's earlier attempt
from FAIL to SKIP only after recording it, so the outcome is read once it
settles. A group, section, subtest or branch opens when the first phase under
it starts, and closes when one outside it starts.
"""

from __future__ import annotations

import logging
import re
import sys
import threading
from typing import Any

import openhtf as htf

from mimick import correlation, files, run as mrun
from mimick.openhtf.plan import Walked, walk

_PHASE_OUTCOMES = {"PASS": mrun.PASS, "FAIL": mrun.FAIL, "SKIP": mrun.SKIP, "ERROR": mrun.ERROR}
_SUBTEST_OUTCOMES = {"PASS": mrun.PASS, "FAIL": mrun.FAIL, "STOP": mrun.ABORTED}
_TEST_OUTCOMES = {"PASS": mrun.PASS, "FAIL": mrun.FAIL, "ERROR": mrun.ERROR, "TIMEOUT": mrun.ERROR,
                  "ABORTED": mrun.ABORTED}
_LEVELS = [(logging.ERROR, "error"), (logging.WARNING, "warn"), (logging.INFO, "info")]
_NOT_CODE = re.compile(r"[^A-Z0-9_]+")


def execute(test: htf.Test, *, environ: dict[str, str] | None = None, sink=None, **kwargs: Any) -> bool:
    """Runs test.execute(**kwargs) and reports it to MIMICK. Returns what
    execute returns: whether the test passed."""
    with Reporter(test, environ=environ, sink=sink):
        return test.execute(**kwargs)


def _name(value) -> str:
    return getattr(value, "name", str(value))


class Reporter:
    """Reports one execution of one test. Use as a context manager around
    test.execute()."""

    def __init__(self, test: htf.Test, *, environ: dict[str, str] | None = None, sink=None):
        self.test = test
        self.walked: Walked = walk(test)
        self.run = mrun.start(self.walked.plan, environ=environ, sink=sink)
        self._lock = threading.RLock()
        self._containers: list[tuple[str, mrun.Step]] = []
        # id() of a PhaseRecord to its open step, and the records already closed.
        self._phases: dict[int, mrun.Step] = {}
        self._closed_records: set[int] = set()
        self._checkpoints_done = 0
        self._current_phase: mrun.Step | None = None
        self._finished = threading.Event()
        self._watcher = threading.Thread(target=self._watch, name="mimick-openhtf", daemon=True)
        self._handler = _LogHandler(self)

    # -- lifecycle ------------------------------------------------------------

    def __enter__(self) -> Reporter:
        self.run.__enter__()
        if self.run.dut.id:
            self.test.configure(default_dut_id=self.run.dut.id)
        self.test.add_output_callbacks(self._on_record)
        logging.getLogger("openhtf").addHandler(self._handler)
        self._watcher.start()
        return self

    def __exit__(self, exc_type, exc, tb) -> bool:
        self._finished.set()
        self._watcher.join(timeout=5)
        logging.getLogger("openhtf").removeHandler(self._handler)
        with self._lock:
            if exc is not None:
                reason = f"{exc_type.__name__}: {exc}"
                self._close_all(mrun.ERROR, reason)
                self.run.end(mrun.ERROR, reason)
            else:
                self._close_all()
                self.run.end()
        correlation.set_fallback("")
        self.run.emitter.flush()
        return False

    def _on_record(self, record) -> None:
        """OpenHTF's output callback: the settled record of the whole test."""
        with self._lock:
            self._sync(record, None, final=True)
            self._close_all(record=record)
            outcome = _TEST_OUTCOMES.get(_name(record.outcome), mrun.ERROR)
            reason = "; ".join(f"{d.code}: {d.description}" if d.description else str(d.code)
                               for d in (record.outcome_details or []))
            self.run.end(outcome, reason, marginal=bool(getattr(record, "marginal", False)))
        self._finished.set()

    # -- watching -------------------------------------------------------------

    def catch_up(self) -> mrun.Step | None:
        """Reports what has changed so far, and returns the running phase's step.
        The log handler calls it from the phase's thread, so a line logged
        before the watcher noticed the phase still lands under it."""
        state = self.test.state
        with self._lock:
            if state is not None and not self._finished.is_set():
                try:
                    self._sync(state.test_record, getattr(state, "running_phase_state", None), final=False)
                except Exception as err:  # noqa: BLE001 - a reporting fault must not stop the test
                    print(f"mimick: could not report a step: {err}", file=sys.stderr)
            return self._current_phase

    def _watch(self) -> None:
        while not self._finished.is_set():
            state = self.test.state
            if state is None:
                self._finished.wait(0.05)
                continue
            try:
                _, changed = state.asdict_with_event()
            except RuntimeError:
                # The live dicts change while OpenHTF builds the snapshot.
                continue
            try:
                with self._lock:
                    self._sync(state.test_record, getattr(state, "running_phase_state", None), final=False)
            except Exception as err:  # noqa: BLE001 - a reporting fault must not stop the test
                print(f"mimick: could not report a step: {err}", file=sys.stderr)
            changed.wait(0.5)

    def _sync(self, record, running, final: bool) -> None:
        """Reports what changed in the record since the last call, in time order."""
        if self.run._closed:
            return
        running_record = getattr(running, "phase_record", None)
        phases = list(record.phases)
        items: list[tuple[int, int, Any]] = []
        for i, pr in enumerate(phases):
            if id(pr) in self._closed_records:
                continue
            settled = final or i < len(phases) - 1 or (running_record is not None and running_record is not pr)
            items.append((pr.start_time_millis or 0, 0, ("phase", pr, settled)))
        if running_record is not None and id(running_record) not in self._phases \
                and id(running_record) not in self._closed_records:
            items.append((running_record.start_time_millis or 0, 0, ("phase", running_record, False)))
        checkpoints = list(getattr(record, "checkpoints", []) or [])
        for cp in checkpoints[self._checkpoints_done:]:
            items.append((cp.evaluated_millis or 0, 1, ("checkpoint", cp, True)))
        self._checkpoints_done = len(checkpoints)
        for _, _, (kind, obj, settled) in sorted(items, key=lambda x: (x[0], x[1])):
            if kind == "phase":
                self._phase(obj, settled, record)
            else:
                self._checkpoint(obj, record)

    # -- nodes ----------------------------------------------------------------

    def _enter_ancestors(self, ancestors: list[str], record) -> None:
        """Closes the open containers the next node is not inside, innermost
        first, then opens the ones it is inside."""
        while self._containers and self._containers[-1][0] not in ancestors:
            self._close_container(record)
        open_keys = [k for k, _ in self._containers]
        for key in ancestors:
            if key not in open_keys:
                kind, name = self.walked.nodes[key]
                step = self.run.step(key, name=name, kind=kind).begin()
                self._containers.append((key, step))

    def _close_container(self, record) -> None:
        key, step = self._containers.pop()
        kind, name = self.walked.nodes[key]
        result, marginal = mrun.NONE, False
        if kind == "subtest" and record is not None:
            for sr in getattr(record, "subtests", []) or []:
                if sr.name == name:
                    result = _SUBTEST_OUTCOMES.get(_name(sr.outcome), mrun.NONE)
                    marginal = bool(getattr(sr, "marginal", False))
        step.end(result, marginal=marginal)

    def _close_all(self, result: str = mrun.ABORTED, reason: str = "The test ended with this step open",
                   record=None) -> None:
        for step in list(self._phases.values()):
            step.end(result, reason)
        self._phases.clear()
        while self._containers:
            self._close_container(record)

    def _phase(self, pr, settled: bool, record) -> None:
        key = self.walked.phases.get(pr.descriptor_id) or pr.name
        step = self._phases.get(id(pr))
        if step is None:
            self._enter_ancestors(self.walked.ancestors.get(key, []), record)
            step = self.run.step(key, name=pr.name, kind="phase").begin()
            self._phases[id(pr)] = step
            self._current_phase = step
            correlation.set_fallback(step.id)
        if not settled:
            return
        self._finish_phase(step, pr)
        del self._phases[id(pr)]
        self._closed_records.add(id(pr))
        if self._current_phase is step:
            self._current_phase = None
            correlation.set_fallback("")

    def _finish_phase(self, step: mrun.Step, pr) -> None:
        for name, m in (pr.measurements or {}).items():
            self._measurement(step, name, m)
        for name, att in (pr.attachments or {}).items():
            self._attachment(step, name, att)
        failure_codes = tuple(_code(d) for d in (pr.failure_diagnosis_results or []))
        for d in pr.diagnosis_results or []:
            if d not in (pr.failure_diagnosis_results or []):
                step.log(f"Diagnosis {_code(d)}", level="warn", code=_code(d))
        outcome = _PHASE_OUTCOMES.get(_name(pr.outcome), mrun.ERROR)
        step.end(outcome, _reason(pr, outcome), marginal=bool(getattr(pr, "marginal", False)), codes=failure_codes)

    def _measurement(self, step: mrun.Step, name: str, m) -> None:
        outcome = _name(m.outcome)
        if outcome == "PASS":
            verdict = "marginal" if getattr(m, "marginal", False) else "pass"
        elif outcome in ("FAIL", "UNSET", "PARTIALLY_SET"):
            verdict = "fail"
        else:
            verdict = "unset"
        unit = ""
        if m.units is not None:
            unit = m.units.suffix or m.units.name or ""
        value = m.measured_value
        if not getattr(value, "is_value_set", False):
            # A declared value that was never recorded fails its phase.
            step.observe(name, "", unit=unit, verdict=verdict)
            return
        dims = getattr(m, "dimensions", None)
        if dims:
            names = [d.name or f"d{i}" for i, d in enumerate(dims)]
            for coords, v in value:
                step.observe(name, v, unit=unit, verdict=verdict,
                             coords={n: str(c) for n, c in zip(names, coords)})
        else:
            step.observe(name, value.value, unit=unit, verdict=verdict)

    def _attachment(self, step: mrun.Step, name: str, att) -> None:
        if not self.run.env.endpoint:
            print(f"mimick: attachment {name} not sent: there is no Station outside a runbook", file=sys.stderr)
            return
        try:
            files.attach_bytes(self.run, step.id, name, att.data, att.mimetype or "")
        except Exception as err:  # noqa: BLE001 - a lost attachment must not stop the test
            print(f"mimick: could not attach {name}: {err}", file=sys.stderr)

    def _checkpoint(self, cp, record) -> None:
        key = self.walked.checkpoints.get(cp.name, cp.name)
        self._enter_ancestors(self.walked.ancestors.get(key, []), record)
        step = self.run.step(key, name=cp.name, kind="checkpoint").begin()
        result = getattr(cp.result, "phase_result", None)
        verdict = _name(result) if result is not None else ""
        if verdict == "CONTINUE":
            step.end(mrun.PASS)
        elif verdict == "SKIP":
            step.end(mrun.SKIP)
        elif verdict in ("STOP", "FAIL_SUBTEST"):
            step.end(mrun.FAIL, "Stopped the test" if verdict == "STOP" else "Failed the subtest")
        else:
            step.end(mrun.ERROR, f"The checkpoint raised: {result}")


def _code(diag_result) -> str:
    code = _NOT_CODE.sub("_", _name(diag_result).upper()).strip("_")
    return code or "DIAGNOSIS"


def _reason(pr, outcome: str) -> str:
    result = getattr(pr, "result", None)
    exc = getattr(result, "phase_result", None)
    if outcome == mrun.ERROR and exc is not None and hasattr(exc, "exc_type"):
        return f"{exc.exc_type.__name__}: {exc.exc_val}"
    if outcome == mrun.FAIL:
        failed = [n for n, m in (pr.measurements or {}).items() if _name(m.outcome) != "PASS"]
        if failed:
            return "Measurement " + ", ".join(failed) + " failed"
    return ""


class _LogHandler(logging.Handler):
    """Sends records from the `openhtf` logger tree to the step that logged."""

    def __init__(self, reporter: Reporter):
        super().__init__(level=logging.INFO)
        self.reporter = reporter

    def emit(self, record: logging.LogRecord) -> None:
        name = record.name
        if ".phase." not in name and ".plug." not in name:
            return  # OpenHTF's own bookkeeping
        level = next((lv for n, lv in _LEVELS if record.levelno >= n), "info")
        try:
            step = self.reporter.catch_up()
            mrun._message(self.reporter.run, step.id if step else "", record.getMessage(), level, "",
                          {"source": name.rsplit(".", 1)[-1]})
        except Exception:  # noqa: BLE001 - logging must never raise into the test
            self.handleError(record)
