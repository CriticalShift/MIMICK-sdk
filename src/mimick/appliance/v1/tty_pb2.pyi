from mimick.appliance.v1 import common_pb2 as _common_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TerminalSize(_message.Message):
    __slots__ = ("cols", "rows")
    COLS_FIELD_NUMBER: _ClassVar[int]
    ROWS_FIELD_NUMBER: _ClassVar[int]
    cols: int
    rows: int
    def __init__(self, cols: _Optional[int] = ..., rows: _Optional[int] = ...) -> None: ...

class TtyClientMessage(_message.Message):
    __slots__ = ("open", "input", "resize", "ping")
    OPEN_FIELD_NUMBER: _ClassVar[int]
    INPUT_FIELD_NUMBER: _ClassVar[int]
    RESIZE_FIELD_NUMBER: _ClassVar[int]
    PING_FIELD_NUMBER: _ClassVar[int]
    open: TtyOpen
    input: TtyInput
    resize: TtyResize
    ping: Ping
    def __init__(self, open: _Optional[_Union[TtyOpen, _Mapping]] = ..., input: _Optional[_Union[TtyInput, _Mapping]] = ..., resize: _Optional[_Union[TtyResize, _Mapping]] = ..., ping: _Optional[_Union[Ping, _Mapping]] = ...) -> None: ...

class TtyOpen(_message.Message):
    __slots__ = ("handle", "requested_size")
    HANDLE_FIELD_NUMBER: _ClassVar[int]
    REQUESTED_SIZE_FIELD_NUMBER: _ClassVar[int]
    handle: _common_pb2.PeripheralHandle
    requested_size: TerminalSize
    def __init__(self, handle: _Optional[_Union[_common_pb2.PeripheralHandle, _Mapping]] = ..., requested_size: _Optional[_Union[TerminalSize, _Mapping]] = ...) -> None: ...

class TtyInput(_message.Message):
    __slots__ = ("data",)
    DATA_FIELD_NUMBER: _ClassVar[int]
    data: bytes
    def __init__(self, data: _Optional[bytes] = ...) -> None: ...

class TtyResize(_message.Message):
    __slots__ = ("size",)
    SIZE_FIELD_NUMBER: _ClassVar[int]
    size: TerminalSize
    def __init__(self, size: _Optional[_Union[TerminalSize, _Mapping]] = ...) -> None: ...

class Ping(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class TtyServerMessage(_message.Message):
    __slots__ = ("opened", "history", "output", "resize", "pong", "error")
    OPENED_FIELD_NUMBER: _ClassVar[int]
    HISTORY_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_FIELD_NUMBER: _ClassVar[int]
    RESIZE_FIELD_NUMBER: _ClassVar[int]
    PONG_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    opened: TtyOpened
    history: TtyHistory
    output: TtyOutput
    resize: TtyNegotiatedResize
    pong: Pong
    error: TtyError
    def __init__(self, opened: _Optional[_Union[TtyOpened, _Mapping]] = ..., history: _Optional[_Union[TtyHistory, _Mapping]] = ..., output: _Optional[_Union[TtyOutput, _Mapping]] = ..., resize: _Optional[_Union[TtyNegotiatedResize, _Mapping]] = ..., pong: _Optional[_Union[Pong, _Mapping]] = ..., error: _Optional[_Union[TtyError, _Mapping]] = ...) -> None: ...

class TtyOpened(_message.Message):
    __slots__ = ("handle", "negotiated_size", "fixed_size", "recording")
    HANDLE_FIELD_NUMBER: _ClassVar[int]
    NEGOTIATED_SIZE_FIELD_NUMBER: _ClassVar[int]
    FIXED_SIZE_FIELD_NUMBER: _ClassVar[int]
    RECORDING_FIELD_NUMBER: _ClassVar[int]
    handle: _common_pb2.PeripheralHandle
    negotiated_size: TerminalSize
    fixed_size: bool
    recording: bool
    def __init__(self, handle: _Optional[_Union[_common_pb2.PeripheralHandle, _Mapping]] = ..., negotiated_size: _Optional[_Union[TerminalSize, _Mapping]] = ..., fixed_size: _Optional[bool] = ..., recording: _Optional[bool] = ...) -> None: ...

class TtyHistory(_message.Message):
    __slots__ = ("size", "data", "captured_at")
    SIZE_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    CAPTURED_AT_FIELD_NUMBER: _ClassVar[int]
    size: TerminalSize
    data: bytes
    captured_at: _common_pb2.Timestamp
    def __init__(self, size: _Optional[_Union[TerminalSize, _Mapping]] = ..., data: _Optional[bytes] = ..., captured_at: _Optional[_Union[_common_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class TtyOutput(_message.Message):
    __slots__ = ("data",)
    DATA_FIELD_NUMBER: _ClassVar[int]
    data: bytes
    def __init__(self, data: _Optional[bytes] = ...) -> None: ...

class TtyNegotiatedResize(_message.Message):
    __slots__ = ("size",)
    SIZE_FIELD_NUMBER: _ClassVar[int]
    size: TerminalSize
    def __init__(self, size: _Optional[_Union[TerminalSize, _Mapping]] = ...) -> None: ...

class Pong(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class TtyError(_message.Message):
    __slots__ = ("code", "message")
    CODE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    code: str
    message: str
    def __init__(self, code: _Optional[str] = ..., message: _Optional[str] = ...) -> None: ...

class WatchTtyRequest(_message.Message):
    __slots__ = ("handle", "requested_size")
    HANDLE_FIELD_NUMBER: _ClassVar[int]
    REQUESTED_SIZE_FIELD_NUMBER: _ClassVar[int]
    handle: _common_pb2.PeripheralHandle
    requested_size: TerminalSize
    def __init__(self, handle: _Optional[_Union[_common_pb2.PeripheralHandle, _Mapping]] = ..., requested_size: _Optional[_Union[TerminalSize, _Mapping]] = ...) -> None: ...

class SendTtyInputRequest(_message.Message):
    __slots__ = ("handle", "data")
    HANDLE_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    handle: _common_pb2.PeripheralHandle
    data: bytes
    def __init__(self, handle: _Optional[_Union[_common_pb2.PeripheralHandle, _Mapping]] = ..., data: _Optional[bytes] = ...) -> None: ...

class SendTtyInputResponse(_message.Message):
    __slots__ = ("status",)
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: _common_pb2.Status
    def __init__(self, status: _Optional[_Union[_common_pb2.Status, _Mapping]] = ...) -> None: ...

class GetTtyHistoryRequest(_message.Message):
    __slots__ = ("handle", "max_bytes")
    HANDLE_FIELD_NUMBER: _ClassVar[int]
    MAX_BYTES_FIELD_NUMBER: _ClassVar[int]
    handle: _common_pb2.PeripheralHandle
    max_bytes: int
    def __init__(self, handle: _Optional[_Union[_common_pb2.PeripheralHandle, _Mapping]] = ..., max_bytes: _Optional[int] = ...) -> None: ...

class GetTtyHistoryResponse(_message.Message):
    __slots__ = ("status", "size", "data", "captured_at")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    SIZE_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    CAPTURED_AT_FIELD_NUMBER: _ClassVar[int]
    status: _common_pb2.Status
    size: TerminalSize
    data: bytes
    captured_at: _common_pb2.Timestamp
    def __init__(self, status: _Optional[_Union[_common_pb2.Status, _Mapping]] = ..., size: _Optional[_Union[TerminalSize, _Mapping]] = ..., data: _Optional[bytes] = ..., captured_at: _Optional[_Union[_common_pb2.Timestamp, _Mapping]] = ...) -> None: ...
