"""The runbook environment: what the Controller's runner tells the container.

Inside a runbook the runner sets MIMICK_* variables. Outside one, such as on a
developer's machine, every value is empty and the SDK prints what it would
record instead of sending it.
"""

from __future__ import annotations

import os
import threading
from dataclasses import dataclass, field

import grpc

DEFAULT_COLLECTOR = "http://127.0.0.1:4318"

# The DUT variables the runner sets for itself, so a DUT field with one of these
# names cannot shadow them.
_DUT_RESERVED = {"MIMICK_DUT_ID", "MIMICK_DUT_TYPE", "MIMICK_DUT_REVISION"}


@dataclass(frozen=True)
class Dut:
    """The DUT the run tests, as the Station records it."""

    id: str = ""
    type: str = ""
    revision: str = ""
    # The DUT Type's field values, keyed by lower-case field name.
    fields: dict[str, str] = field(default_factory=dict)

    def __getattr__(self, name: str) -> str:
        try:
            return self.fields[name]
        except KeyError:
            raise AttributeError(name) from None


@dataclass(frozen=True)
class Env:
    endpoint: str = ""
    collector: str = DEFAULT_COLLECTOR
    run_id: str = ""
    run_token: str = ""
    session_id: str = ""
    dut: Dut = field(default_factory=Dut)

    @property
    def in_runbook(self) -> bool:
        return bool(self.endpoint and self.run_id)


def from_environ(environ: dict[str, str] | None = None) -> Env:
    env = os.environ if environ is None else environ
    fields = {
        key[len("MIMICK_DUT_") :].lower(): value
        for key, value in env.items()
        if key.startswith("MIMICK_DUT_") and key not in _DUT_RESERVED
    }
    return Env(
        endpoint=env.get("MIMICK_ENDPOINT", ""),
        collector=env.get("MIMICK_OTLP_ENDPOINT") or DEFAULT_COLLECTOR,
        run_id=env.get("MIMICK_RUN_ID", ""),
        run_token=env.get("MIMICK_RUN_TOKEN", ""),
        session_id=env.get("MIMICK_SESSION_ID", ""),
        dut=Dut(
            id=env.get("MIMICK_DUT_ID", ""),
            type=env.get("MIMICK_DUT_TYPE", ""),
            revision=env.get("MIMICK_DUT_REVISION", ""),
            fields=fields,
        ),
    )


_lock = threading.Lock()
_channel: grpc.Channel | None = None
_channel_target = ""
_active: Env | None = None


def activate(env: Env) -> None:
    """Makes env the one stubs use when given none: the open run's."""
    global _active
    _active = env


def channel(env: Env | None = None) -> grpc.Channel:
    """The one channel to mimickd that every stub shares.

    It carries the step-correlation interceptor, so a call made inside a step
    is recorded under that step.
    """
    from mimick import correlation

    global _channel, _channel_target
    env = env or _active or from_environ()
    if not env.endpoint:
        raise RuntimeError("MIMICK_ENDPOINT is not set: peripherals are reachable only inside a runbook")
    with _lock:
        if _channel is None or _channel_target != env.endpoint:
            if _channel is not None:
                _channel.close()
            raw = grpc.insecure_channel(env.endpoint)
            _channel = grpc.intercept_channel(raw, correlation.Interceptor(env.run_token))
            _channel_target = env.endpoint
        return _channel


def reset() -> None:
    """Closes the shared channel, so the next call reads the environment again."""
    global _channel, _channel_target, _active
    with _lock:
        if _channel is not None:
            _channel.close()
        _channel, _channel_target, _active = None, "", None
