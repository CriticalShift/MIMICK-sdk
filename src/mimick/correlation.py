"""Step correlation: every call made inside a step is recorded under it.

The current node run lives in a context variable. A channel interceptor sends
it as x-mimick-task-id on each call to mimickd, which stamps it on the rows the
call causes. The run token travels on every call as well, for the services that
require it.
"""

from __future__ import annotations

import contextvars
from collections.abc import Iterator
from contextlib import contextmanager

import grpc

TASK_ID_KEY = "x-mimick-task-id"
RUN_TOKEN_KEY = "x-mimick-run-token"

_current: contextvars.ContextVar[str] = contextvars.ContextVar("mimick_node_run", default="")

# The node run for a thread with nothing in its context, such as a thread a test
# framework starts for each step. A framework adapter sets it as steps run.
_fallback = ""


def current() -> str:
    """The node run id calls are recorded under, or ''."""
    return _current.get() or _fallback


def set_fallback(node_run_id: str) -> None:
    """Sets the node run a call is recorded under when its context names none."""
    global _fallback
    _fallback = node_run_id


@contextmanager
def within(node_run_id: str) -> Iterator[None]:
    token = _current.set(node_run_id)
    try:
        yield
    finally:
        _current.reset(token)


class _Details(grpc.ClientCallDetails):
    def __init__(self, base: grpc.ClientCallDetails, metadata: list[tuple[str, str]]):
        self.method = base.method
        self.timeout = base.timeout
        self.metadata = metadata
        self.credentials = base.credentials
        self.wait_for_ready = base.wait_for_ready
        self.compression = base.compression


class Interceptor(
    grpc.UnaryUnaryClientInterceptor,
    grpc.UnaryStreamClientInterceptor,
    grpc.StreamUnaryClientInterceptor,
    grpc.StreamStreamClientInterceptor,
):
    def __init__(self, run_token: str = ""):
        self._run_token = run_token

    def _details(self, details: grpc.ClientCallDetails) -> grpc.ClientCallDetails:
        metadata = [
            (k, v) for k, v in (details.metadata or []) if k not in (TASK_ID_KEY, RUN_TOKEN_KEY)
        ]
        if node_run := current():
            metadata.append((TASK_ID_KEY, node_run))
        if self._run_token:
            metadata.append((RUN_TOKEN_KEY, self._run_token))
        return _Details(details, metadata)

    def intercept_unary_unary(self, continuation, details, request):
        return continuation(self._details(details), request)

    def intercept_unary_stream(self, continuation, details, request):
        return continuation(self._details(details), request)

    def intercept_stream_unary(self, continuation, details, request_iterator):
        return continuation(self._details(details), request_iterator)

    def intercept_stream_stream(self, continuation, details, request_iterator):
        return continuation(self._details(details), request_iterator)
