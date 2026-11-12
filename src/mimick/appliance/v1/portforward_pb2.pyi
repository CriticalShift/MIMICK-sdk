from mimick.appliance.v1 import common_pb2 as _common_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ForwardClientMessage(_message.Message):
    __slots__ = ("open", "data", "close_write")
    OPEN_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    CLOSE_WRITE_FIELD_NUMBER: _ClassVar[int]
    open: ForwardOpen
    data: ForwardData
    close_write: ForwardCloseWrite
    def __init__(self, open: _Optional[_Union[ForwardOpen, _Mapping]] = ..., data: _Optional[_Union[ForwardData, _Mapping]] = ..., close_write: _Optional[_Union[ForwardCloseWrite, _Mapping]] = ...) -> None: ...

class ForwardServerMessage(_message.Message):
    __slots__ = ("opened", "data", "close_write", "error")
    OPENED_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    CLOSE_WRITE_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    opened: ForwardOpened
    data: ForwardData
    close_write: ForwardCloseWrite
    error: ForwardError
    def __init__(self, opened: _Optional[_Union[ForwardOpened, _Mapping]] = ..., data: _Optional[_Union[ForwardData, _Mapping]] = ..., close_write: _Optional[_Union[ForwardCloseWrite, _Mapping]] = ..., error: _Optional[_Union[ForwardError, _Mapping]] = ...) -> None: ...

class ForwardOpen(_message.Message):
    __slots__ = ("host", "port", "via")
    HOST_FIELD_NUMBER: _ClassVar[int]
    PORT_FIELD_NUMBER: _ClassVar[int]
    VIA_FIELD_NUMBER: _ClassVar[int]
    host: str
    port: int
    via: _common_pb2.PeripheralHandle
    def __init__(self, host: _Optional[str] = ..., port: _Optional[int] = ..., via: _Optional[_Union[_common_pb2.PeripheralHandle, _Mapping]] = ...) -> None: ...

class ForwardOpened(_message.Message):
    __slots__ = ("status", "local_addr", "remote_addr")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    LOCAL_ADDR_FIELD_NUMBER: _ClassVar[int]
    REMOTE_ADDR_FIELD_NUMBER: _ClassVar[int]
    status: _common_pb2.Status
    local_addr: str
    remote_addr: str
    def __init__(self, status: _Optional[_Union[_common_pb2.Status, _Mapping]] = ..., local_addr: _Optional[str] = ..., remote_addr: _Optional[str] = ...) -> None: ...

class ForwardData(_message.Message):
    __slots__ = ("data",)
    DATA_FIELD_NUMBER: _ClassVar[int]
    data: bytes
    def __init__(self, data: _Optional[bytes] = ...) -> None: ...

class ForwardCloseWrite(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ForwardError(_message.Message):
    __slots__ = ("status",)
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: _common_pb2.Status
    def __init__(self, status: _Optional[_Union[_common_pb2.Status, _Mapping]] = ...) -> None: ...
