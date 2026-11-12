"""Run events: OTLP log records the Cloud's run materializer builds the run from.

Each record carries the run, a client-made event id, this emitter's id, and how
many events the emitter has sent so far. The Cloud applies a record once by its
id, and holds a run's final values until every count up to the highest has
arrived. Records go to the Controller's collector over OTLP/HTTP, whose
disk-backed queue carries them to the Cloud. With no collector reachable, such
as on a developer's machine, each record is printed instead.
"""

from __future__ import annotations

import atexit
import socket
import sys
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from dataclasses import dataclass, field

from opentelemetry.proto.collector.logs.v1 import logs_service_pb2
from opentelemetry.proto.common.v1 import common_pb2
from opentelemetry.proto.logs.v1 import logs_pb2
from opentelemetry.proto.resource.v1 import resource_pb2

# The names in this module are the run event vocabulary, a contract with the
# Cloud defined in MIMICK-Cloud's common/pkg/otelattrs.
SCOPE = "mimickd/task"
SERVICE_NAME = "mimickd"
SYSTEM_ACTOR_ID = "0de1f857-d141-566d-93ce-f07e8bb30720"

PLAN = "mimick.task.plan"
START = "mimick.task.start"
STOP = "mimick.task.stop"
MESSAGE = "mimick.task.message"
OBSERVE = "mimick.task.observe"
ATTACH = "mimick.task.attach"

SEVERITY = {
    "debug": (logs_pb2.SEVERITY_NUMBER_DEBUG, "DEBUG"),
    "info": (logs_pb2.SEVERITY_NUMBER_INFO, "INFO"),
    "warn": (logs_pb2.SEVERITY_NUMBER_WARN, "WARN"),
    "error": (logs_pb2.SEVERITY_NUMBER_ERROR, "ERROR"),
}

# How long a record may wait to be batched with others.
_FLUSH_INTERVAL = 0.2
_DIAL_TIMEOUT = 0.4
_POST_TIMEOUT = 10.0


@dataclass
class Event:
    name: str
    body: str
    level: str = "info"
    task_id: str = ""
    attrs: dict[str, str] = field(default_factory=dict)
    # The user's key/value data, stored under mimick.task.data.<key>.
    data: dict[str, str] = field(default_factory=dict)
    time_ns: int = 0


class Emitter:
    """Numbers and sends one run's events from this process."""

    def __init__(self, collector: str, run_id: str = "", session_id: str = "", sink=None):
        self.run_id = run_id
        self.session_id = session_id
        self.emitter_id = str(uuid.uuid4())
        self._count = 0
        self._lock = threading.Lock()
        self._sink = sink if sink is not None else _sink_for(collector)

    def emit(self, *events: Event) -> None:
        with self._lock:
            for e in events:
                self._count += 1
                e.attrs["mimick.event.id"] = str(uuid.uuid4())
                e.attrs["mimick.emitter.id"] = self.emitter_id
                e.attrs["mimick.event.count"] = str(self._count)
                if self.run_id:
                    e.attrs["mimick.run.id"] = self.run_id
                e.time_ns = e.time_ns or time.time_ns()
                self._sink.put(e, self.session_id)

    def emit_sample(self, e: Event) -> None:
        """Sends a monitor sample. Samples are not numbered: they stay in the
        log store, and the run's own records are what the count accounts for."""
        if self.run_id:
            e.attrs["mimick.run.id"] = self.run_id
        e.time_ns = e.time_ns or time.time_ns()
        self._sink.put(e, self.session_id)

    def flush(self, timeout: float = _POST_TIMEOUT) -> None:
        self._sink.flush(timeout)


def _sink_for(collector: str):
    if _reachable(collector):
        return _OTLPSink(collector)
    return _PrintSink()


def _reachable(endpoint: str) -> bool:
    u = urllib.parse.urlsplit(endpoint)
    if not u.hostname:
        return False
    port = u.port or (443 if u.scheme == "https" else 80)
    try:
        with socket.create_connection((u.hostname, port), timeout=_DIAL_TIMEOUT):
            return True
    except OSError:
        return False


class _PrintSink:
    def put(self, e: Event, session_id: str) -> None:
        line = e.body
        if e.name == MESSAGE:
            line = f"[{e.level}] {e.body}"
            if e.data:
                line += " " + " ".join(f"{k}={v}" for k, v in sorted(e.data.items()))
        elif e.name == PLAN:
            line = "Declared plan " + e.attrs.get("mimick.plan.digest", "")
        print(line, file=sys.stderr if e.level in ("warn", "error") else sys.stdout)

    def flush(self, timeout: float) -> None:
        pass


def record(e: Event, session_id: str) -> logs_pb2.LogRecord:
    """The OTLP log record of one event, as the Go CLI writes it."""
    number, text = SEVERITY.get(e.level, SEVERITY["info"])
    attrs = {"mimick.user.id": SYSTEM_ACTOR_ID}
    if session_id:
        attrs["mimick.session.id"] = session_id
    if e.task_id:
        attrs["mimick.task.id"] = e.task_id
    attrs.update({k: v for k, v in e.attrs.items() if v != ""})
    attrs.update({"mimick.task.data." + k: v for k, v in e.data.items()})
    return logs_pb2.LogRecord(
        time_unix_nano=e.time_ns,
        observed_time_unix_nano=e.time_ns,
        severity_number=number,
        severity_text=text,
        event_name=e.name,
        body=common_pb2.AnyValue(string_value=e.body),
        attributes=[
            common_pb2.KeyValue(key=k, value=common_pb2.AnyValue(string_value=v)) for k, v in sorted(attrs.items())
        ],
    )


class _OTLPSink:
    """Batches records and posts them on a background thread.

    Records are sent in the order they were numbered. Org and Controller
    identity are left off the resource: the collector stamps its own.
    """

    def __init__(self, collector: str):
        self._url = collector.rstrip("/").removesuffix("/v1/logs") + "/v1/logs"
        self._pending: list[logs_pb2.LogRecord] = []
        self._cond = threading.Condition()
        self._sending = False
        self._thread = threading.Thread(target=self._run, name="mimick-events", daemon=True)
        self._thread.start()
        atexit.register(self.flush, _POST_TIMEOUT)

    def put(self, e: Event, session_id: str) -> None:
        with self._cond:
            self._pending.append(record(e, session_id))
            self._cond.notify_all()

    def flush(self, timeout: float) -> None:
        deadline = time.monotonic() + timeout
        with self._cond:
            self._cond.notify_all()
            while self._pending or self._sending:
                left = deadline - time.monotonic()
                if left <= 0:
                    print(f"mimick: {len(self._pending)} run events were not sent", file=sys.stderr)
                    return
                self._cond.wait(left)

    def _run(self) -> None:
        while True:
            with self._cond:
                while not self._pending:
                    self._cond.wait()
                self._cond.wait(_FLUSH_INTERVAL)
                batch, self._pending = self._pending, []
                self._sending = True
            try:
                self._post(batch)
            finally:
                with self._cond:
                    self._sending = False
                    self._cond.notify_all()

    def _post(self, batch: list[logs_pb2.LogRecord]) -> None:
        req = logs_service_pb2.ExportLogsServiceRequest(
            resource_logs=[
                logs_pb2.ResourceLogs(
                    resource=resource_pb2.Resource(
                        attributes=[
                            common_pb2.KeyValue(
                                key="service.name", value=common_pb2.AnyValue(string_value=SERVICE_NAME)
                            )
                        ]
                    ),
                    scope_logs=[
                        logs_pb2.ScopeLogs(scope=common_pb2.InstrumentationScope(name=SCOPE), log_records=batch)
                    ],
                )
            ]
        )
        http = urllib.request.Request(
            self._url,
            data=req.SerializeToString(),
            headers={"Content-Type": "application/x-protobuf"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(http, timeout=_POST_TIMEOUT) as resp:
                resp.read()
        except (urllib.error.URLError, OSError) as err:
            print(f"mimick: could not send {len(batch)} run events to the collector: {err}", file=sys.stderr)
