from mimick.appliance.v1 import common_pb2 as _common_pb2
from mimick.appliance.v1 import tty_pb2 as _tty_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ShellSessionState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SHELL_SESSION_STATE_UNSPECIFIED: _ClassVar[ShellSessionState]
    SHELL_SESSION_STATE_STARTING: _ClassVar[ShellSessionState]
    SHELL_SESSION_STATE_RUNNING: _ClassVar[ShellSessionState]
SHELL_SESSION_STATE_UNSPECIFIED: ShellSessionState
SHELL_SESSION_STATE_STARTING: ShellSessionState
SHELL_SESSION_STATE_RUNNING: ShellSessionState

class ShellSessionHandle(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class OpenShellSessionRequest(_message.Message):
    __slots__ = ("image", "command", "privileged", "requested_size")
    IMAGE_FIELD_NUMBER: _ClassVar[int]
    COMMAND_FIELD_NUMBER: _ClassVar[int]
    PRIVILEGED_FIELD_NUMBER: _ClassVar[int]
    REQUESTED_SIZE_FIELD_NUMBER: _ClassVar[int]
    image: str
    command: _containers.RepeatedScalarFieldContainer[str]
    privileged: bool
    requested_size: _tty_pb2.TerminalSize
    def __init__(self, image: _Optional[str] = ..., command: _Optional[_Iterable[str]] = ..., privileged: _Optional[bool] = ..., requested_size: _Optional[_Union[_tty_pb2.TerminalSize, _Mapping]] = ...) -> None: ...

class OpenShellSessionResponse(_message.Message):
    __slots__ = ("status", "handle")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    HANDLE_FIELD_NUMBER: _ClassVar[int]
    status: _common_pb2.Status
    handle: ShellSessionHandle
    def __init__(self, status: _Optional[_Union[_common_pb2.Status, _Mapping]] = ..., handle: _Optional[_Union[ShellSessionHandle, _Mapping]] = ...) -> None: ...

class ListShellSessionsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListShellSessionsResponse(_message.Message):
    __slots__ = ("sessions",)
    SESSIONS_FIELD_NUMBER: _ClassVar[int]
    sessions: _containers.RepeatedCompositeFieldContainer[ShellSessionSummary]
    def __init__(self, sessions: _Optional[_Iterable[_Union[ShellSessionSummary, _Mapping]]] = ...) -> None: ...

class ShellSessionSummary(_message.Message):
    __slots__ = ("handle", "image", "image_digest", "command", "privileged", "opened_by_user_id", "opened_at", "watcher_count", "state")
    HANDLE_FIELD_NUMBER: _ClassVar[int]
    IMAGE_FIELD_NUMBER: _ClassVar[int]
    IMAGE_DIGEST_FIELD_NUMBER: _ClassVar[int]
    COMMAND_FIELD_NUMBER: _ClassVar[int]
    PRIVILEGED_FIELD_NUMBER: _ClassVar[int]
    OPENED_BY_USER_ID_FIELD_NUMBER: _ClassVar[int]
    OPENED_AT_FIELD_NUMBER: _ClassVar[int]
    WATCHER_COUNT_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    handle: ShellSessionHandle
    image: str
    image_digest: str
    command: _containers.RepeatedScalarFieldContainer[str]
    privileged: bool
    opened_by_user_id: str
    opened_at: _common_pb2.Timestamp
    watcher_count: int
    state: ShellSessionState
    def __init__(self, handle: _Optional[_Union[ShellSessionHandle, _Mapping]] = ..., image: _Optional[str] = ..., image_digest: _Optional[str] = ..., command: _Optional[_Iterable[str]] = ..., privileged: _Optional[bool] = ..., opened_by_user_id: _Optional[str] = ..., opened_at: _Optional[_Union[_common_pb2.Timestamp, _Mapping]] = ..., watcher_count: _Optional[int] = ..., state: _Optional[_Union[ShellSessionState, str]] = ...) -> None: ...

class WatchShellSessionRequest(_message.Message):
    __slots__ = ("handle", "requested_size")
    HANDLE_FIELD_NUMBER: _ClassVar[int]
    REQUESTED_SIZE_FIELD_NUMBER: _ClassVar[int]
    handle: ShellSessionHandle
    requested_size: _tty_pb2.TerminalSize
    def __init__(self, handle: _Optional[_Union[ShellSessionHandle, _Mapping]] = ..., requested_size: _Optional[_Union[_tty_pb2.TerminalSize, _Mapping]] = ...) -> None: ...

class ShellServerMessage(_message.Message):
    __slots__ = ("pulling", "opened", "history", "output", "resize", "closed", "error", "heartbeat")
    PULLING_FIELD_NUMBER: _ClassVar[int]
    OPENED_FIELD_NUMBER: _ClassVar[int]
    HISTORY_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_FIELD_NUMBER: _ClassVar[int]
    RESIZE_FIELD_NUMBER: _ClassVar[int]
    CLOSED_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    HEARTBEAT_FIELD_NUMBER: _ClassVar[int]
    pulling: ShellPulling
    opened: ShellOpened
    history: ShellHistory
    output: ShellOutput
    resize: ShellNegotiatedResize
    closed: ShellClosed
    error: ShellError
    heartbeat: ShellHeartbeat
    def __init__(self, pulling: _Optional[_Union[ShellPulling, _Mapping]] = ..., opened: _Optional[_Union[ShellOpened, _Mapping]] = ..., history: _Optional[_Union[ShellHistory, _Mapping]] = ..., output: _Optional[_Union[ShellOutput, _Mapping]] = ..., resize: _Optional[_Union[ShellNegotiatedResize, _Mapping]] = ..., closed: _Optional[_Union[ShellClosed, _Mapping]] = ..., error: _Optional[_Union[ShellError, _Mapping]] = ..., heartbeat: _Optional[_Union[ShellHeartbeat, _Mapping]] = ...) -> None: ...

class ShellPulling(_message.Message):
    __slots__ = ("image", "downloaded_bytes", "total_bytes")
    IMAGE_FIELD_NUMBER: _ClassVar[int]
    DOWNLOADED_BYTES_FIELD_NUMBER: _ClassVar[int]
    TOTAL_BYTES_FIELD_NUMBER: _ClassVar[int]
    image: str
    downloaded_bytes: int
    total_bytes: int
    def __init__(self, image: _Optional[str] = ..., downloaded_bytes: _Optional[int] = ..., total_bytes: _Optional[int] = ...) -> None: ...

class ShellOpened(_message.Message):
    __slots__ = ("handle", "negotiated_size", "image", "image_digest", "privileged")
    HANDLE_FIELD_NUMBER: _ClassVar[int]
    NEGOTIATED_SIZE_FIELD_NUMBER: _ClassVar[int]
    IMAGE_FIELD_NUMBER: _ClassVar[int]
    IMAGE_DIGEST_FIELD_NUMBER: _ClassVar[int]
    PRIVILEGED_FIELD_NUMBER: _ClassVar[int]
    handle: ShellSessionHandle
    negotiated_size: _tty_pb2.TerminalSize
    image: str
    image_digest: str
    privileged: bool
    def __init__(self, handle: _Optional[_Union[ShellSessionHandle, _Mapping]] = ..., negotiated_size: _Optional[_Union[_tty_pb2.TerminalSize, _Mapping]] = ..., image: _Optional[str] = ..., image_digest: _Optional[str] = ..., privileged: _Optional[bool] = ...) -> None: ...

class ShellHistory(_message.Message):
    __slots__ = ("size", "data", "captured_at")
    SIZE_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    CAPTURED_AT_FIELD_NUMBER: _ClassVar[int]
    size: _tty_pb2.TerminalSize
    data: bytes
    captured_at: _common_pb2.Timestamp
    def __init__(self, size: _Optional[_Union[_tty_pb2.TerminalSize, _Mapping]] = ..., data: _Optional[bytes] = ..., captured_at: _Optional[_Union[_common_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class ShellOutput(_message.Message):
    __slots__ = ("data",)
    DATA_FIELD_NUMBER: _ClassVar[int]
    data: bytes
    def __init__(self, data: _Optional[bytes] = ...) -> None: ...

class ShellNegotiatedResize(_message.Message):
    __slots__ = ("size",)
    SIZE_FIELD_NUMBER: _ClassVar[int]
    size: _tty_pb2.TerminalSize
    def __init__(self, size: _Optional[_Union[_tty_pb2.TerminalSize, _Mapping]] = ...) -> None: ...

class ShellClosed(_message.Message):
    __slots__ = ("exit_code", "closed_by_request")
    EXIT_CODE_FIELD_NUMBER: _ClassVar[int]
    CLOSED_BY_REQUEST_FIELD_NUMBER: _ClassVar[int]
    exit_code: int
    closed_by_request: bool
    def __init__(self, exit_code: _Optional[int] = ..., closed_by_request: _Optional[bool] = ...) -> None: ...

class ShellError(_message.Message):
    __slots__ = ("code", "message")
    CODE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    code: str
    message: str
    def __init__(self, code: _Optional[str] = ..., message: _Optional[str] = ...) -> None: ...

class ShellHeartbeat(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class SendShellInputRequest(_message.Message):
    __slots__ = ("handle", "data")
    HANDLE_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    handle: ShellSessionHandle
    data: bytes
    def __init__(self, handle: _Optional[_Union[ShellSessionHandle, _Mapping]] = ..., data: _Optional[bytes] = ...) -> None: ...

class SendShellInputResponse(_message.Message):
    __slots__ = ("status",)
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: _common_pb2.Status
    def __init__(self, status: _Optional[_Union[_common_pb2.Status, _Mapping]] = ...) -> None: ...

class ResizeShellSessionRequest(_message.Message):
    __slots__ = ("handle", "size")
    HANDLE_FIELD_NUMBER: _ClassVar[int]
    SIZE_FIELD_NUMBER: _ClassVar[int]
    handle: ShellSessionHandle
    size: _tty_pb2.TerminalSize
    def __init__(self, handle: _Optional[_Union[ShellSessionHandle, _Mapping]] = ..., size: _Optional[_Union[_tty_pb2.TerminalSize, _Mapping]] = ...) -> None: ...

class ResizeShellSessionResponse(_message.Message):
    __slots__ = ("status", "negotiated_size")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    NEGOTIATED_SIZE_FIELD_NUMBER: _ClassVar[int]
    status: _common_pb2.Status
    negotiated_size: _tty_pb2.TerminalSize
    def __init__(self, status: _Optional[_Union[_common_pb2.Status, _Mapping]] = ..., negotiated_size: _Optional[_Union[_tty_pb2.TerminalSize, _Mapping]] = ...) -> None: ...

class CloseShellSessionRequest(_message.Message):
    __slots__ = ("handle",)
    HANDLE_FIELD_NUMBER: _ClassVar[int]
    handle: ShellSessionHandle
    def __init__(self, handle: _Optional[_Union[ShellSessionHandle, _Mapping]] = ...) -> None: ...

class CloseShellSessionResponse(_message.Message):
    __slots__ = ("status",)
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: _common_pb2.Status
    def __init__(self, status: _Optional[_Union[_common_pb2.Status, _Mapping]] = ...) -> None: ...
