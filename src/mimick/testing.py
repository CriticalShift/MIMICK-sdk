"""Test doubles: a fake collector and a fake mimickd, so a test of the SDK, or
of a customer's test, runs with no Station.

    with testing.FakeBench() as bench:
        with run.start(environ=bench.environ) as r:
            with r.step("flash") as s:
                s.observe("vbat", 4.1)
        bench.collector.records   # every run event, decoded
"""

from __future__ import annotations

import http.server
import threading
from concurrent import futures
from dataclasses import dataclass, field

import grpc
from opentelemetry.proto.collector.logs.v1 import logs_service_pb2

from mimick import env as _env
from mimick.appliance.v1 import (
    common_pb2,
    gpio_pb2,
    gpio_pb2_grpc,
    peripheral_pb2,
    peripheral_pb2_grpc,
    run_report_pb2,
    run_report_pb2_grpc,
)


@dataclass
class Record:
    """One OTLP log record the fake collector received."""

    event_name: str
    body: str
    severity: str
    attrs: dict[str, str]


class FakeCollector:
    """An OTLP/HTTP logs receiver on a free loopback port."""

    def __init__(self):
        self.records: list[Record] = []
        self._lock = threading.Lock()
        collector = self

        class Handler(http.server.BaseHTTPRequestHandler):
            def do_POST(self):
                body = self.rfile.read(int(self.headers.get("Content-Length", 0)))
                req = logs_service_pb2.ExportLogsServiceRequest()
                req.ParseFromString(body)
                with collector._lock:
                    for rl in req.resource_logs:
                        for sl in rl.scope_logs:
                            for lr in sl.log_records:
                                collector.records.append(Record(
                                    lr.event_name, lr.body.string_value, lr.severity_text,
                                    {kv.key: kv.value.string_value for kv in lr.attributes}))
                self.send_response(200)
                self.send_header("Content-Type", "application/x-protobuf")
                self.end_headers()
                self.wfile.write(logs_service_pb2.ExportLogsServiceResponse().SerializeToString())

            def log_message(self, *args):
                pass

        self._server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        self.endpoint = f"http://127.0.0.1:{self._server.server_address[1]}"
        self._thread = threading.Thread(target=self._server.serve_forever, daemon=True)
        self._thread.start()

    def named(self, event_name: str) -> list[Record]:
        with self._lock:
            return [r for r in self.records if r.event_name == event_name]

    def close(self):
        self._server.shutdown()
        self._server.server_close()


@dataclass
class StoredFile:
    name: str
    media_type: str
    data: bytes
    task_id: str


@dataclass
class GpioCall:
    method: str
    task_id: str


class _RunReport(run_report_pb2_grpc.RunReportServiceServicer):
    def __init__(self, bench: FakeBench):
        self.bench = bench

    def UploadFile(self, request_iterator, context):
        md = dict(context.invocation_metadata())
        if md.get("x-mimick-run-token") != self.bench.run_token:
            context.abort(grpc.StatusCode.PERMISSION_DENIED, "the call needs the current run's MIMICK_RUN_TOKEN")
        name, media_type, data = "", "", b""
        for i, chunk in enumerate(request_iterator):
            if i == 0:
                name, media_type = chunk.name, chunk.media_type
            data += chunk.data
        file_id = f"00000000-0000-4000-8000-{len(self.bench.files) + 1:012d}"
        self.bench.files[file_id] = StoredFile(name, media_type, data, md.get("x-mimick-task-id", ""))
        import hashlib

        return run_report_pb2.UploadFileResponse(file_id=file_id, size=len(data),
                                                 sha256=hashlib.sha256(data).hexdigest())


    def StartMonitor(self, request, context):
        md = dict(context.invocation_metadata())
        if md.get("x-mimick-run-token") != self.bench.run_token:
            context.abort(grpc.StatusCode.PERMISSION_DENIED, "the call needs the current run's MIMICK_RUN_TOKEN")
        monitor_id = f"monitor-{len(self.bench.monitors) + 1}"
        self.bench.monitors[monitor_id] = request
        return run_report_pb2.Monitor(id=monitor_id)

    def StopMonitor(self, request, context):
        if request.id not in self.bench.monitors:
            context.abort(grpc.StatusCode.NOT_FOUND, "no such monitor")
        self.bench.stopped.append(request.id)
        samples = [run_report_pb2.MonitorSample(at=common_pb2.Timestamp(seconds=1700000000 + i), value=v)
                   for i, v in enumerate(self.bench.monitor_values)]
        values = self.bench.monitor_values
        return run_report_pb2.MonitorSeries(
            count=len(values), first=samples[0].at if samples else None, last=samples[-1].at if samples else None,
            min=min(values) if values else 0, max=max(values) if values else 0,
            verdict=self.bench.monitor_verdict, samples=samples)


class _Gpio(gpio_pb2_grpc.GpioServiceServicer):
    def __init__(self, bench: FakeBench):
        self.bench = bench

    def ReadPin(self, request, context):
        md = dict(context.invocation_metadata())
        self.bench.gpio_calls.append(GpioCall("ReadPin", md.get("x-mimick-task-id", "")))
        return gpio_pb2.GpioReadPinResponse(level=self.bench.pin_levels.get(request.pin, gpio_pb2.PIN_LEVEL_LOW))


class _Peripheral(peripheral_pb2_grpc.PeripheralServiceServicer):
    def __init__(self, bench: FakeBench):
        self.bench = bench

    def Open(self, request, context):
        self.bench.opened.append(request.location)
        return peripheral_pb2.OpenResponse(handle=common_pb2.PeripheralHandle(id=f"handle-{len(self.bench.opened)}"))

    def Close(self, request, context):
        return peripheral_pb2.CloseResponse()


@dataclass
class FakeBench:
    """A fake collector and a fake mimickd, with the environment a runbook gets."""

    run_id: str = "run-1"
    run_token: str = "token-1"
    session_id: str = "session-1"
    dut: dict[str, str] = field(default_factory=dict)
    files: dict[str, StoredFile] = field(default_factory=dict)
    gpio_calls: list[GpioCall] = field(default_factory=list)
    pin_levels: dict[int, int] = field(default_factory=dict)
    monitors: dict = field(default_factory=dict)
    stopped: list[str] = field(default_factory=list)
    monitor_values: list[float] = field(default_factory=lambda: [1.0, 2.0, 3.0])
    monitor_verdict: str = "pass"
    opened: list[str] = field(default_factory=list)

    def __enter__(self) -> FakeBench:
        self.collector = FakeCollector()
        self._server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
        run_report_pb2_grpc.add_RunReportServiceServicer_to_server(_RunReport(self), self._server)
        gpio_pb2_grpc.add_GpioServiceServicer_to_server(_Gpio(self), self._server)
        peripheral_pb2_grpc.add_PeripheralServiceServicer_to_server(_Peripheral(self), self._server)
        port = self._server.add_insecure_port("127.0.0.1:0")
        self._server.start()
        self.endpoint = f"127.0.0.1:{port}"
        self.environ = {
            "MIMICK_ENDPOINT": self.endpoint,
            "MIMICK_OTLP_ENDPOINT": self.collector.endpoint,
            "MIMICK_RUN_ID": self.run_id,
            "MIMICK_RUN_TOKEN": self.run_token,
            "MIMICK_SESSION_ID": self.session_id,
            **{"MIMICK_DUT_" + k.upper(): v for k, v in self.dut.items()},
        }
        _env.reset()
        return self

    def __exit__(self, *exc) -> None:
        _env.reset()
        self._server.stop(None)
        self.collector.close()
