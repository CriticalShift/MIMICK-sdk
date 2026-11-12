from mimick.appliance.v1 import common_pb2 as _common_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SoftwareReadRequest(_message.Message):
    __slots__ = ("handle", "timeout_ms")
    HANDLE_FIELD_NUMBER: _ClassVar[int]
    TIMEOUT_MS_FIELD_NUMBER: _ClassVar[int]
    handle: _common_pb2.PeripheralHandle
    timeout_ms: int
    def __init__(self, handle: _Optional[_Union[_common_pb2.PeripheralHandle, _Mapping]] = ..., timeout_ms: _Optional[int] = ...) -> None: ...

class SoftwareReadResponse(_message.Message):
    __slots__ = ("status", "output", "exit_code")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_FIELD_NUMBER: _ClassVar[int]
    EXIT_CODE_FIELD_NUMBER: _ClassVar[int]
    status: _common_pb2.Status
    output: bytes
    exit_code: int
    def __init__(self, status: _Optional[_Union[_common_pb2.Status, _Mapping]] = ..., output: _Optional[bytes] = ..., exit_code: _Optional[int] = ...) -> None: ...

class SoftwareWriteRequest(_message.Message):
    __slots__ = ("handle", "data", "timeout_ms")
    HANDLE_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    TIMEOUT_MS_FIELD_NUMBER: _ClassVar[int]
    handle: _common_pb2.PeripheralHandle
    data: bytes
    timeout_ms: int
    def __init__(self, handle: _Optional[_Union[_common_pb2.PeripheralHandle, _Mapping]] = ..., data: _Optional[bytes] = ..., timeout_ms: _Optional[int] = ...) -> None: ...

class SoftwareWriteResponse(_message.Message):
    __slots__ = ("status", "bytes_written", "exit_code")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    BYTES_WRITTEN_FIELD_NUMBER: _ClassVar[int]
    EXIT_CODE_FIELD_NUMBER: _ClassVar[int]
    status: _common_pb2.Status
    bytes_written: int
    exit_code: int
    def __init__(self, status: _Optional[_Union[_common_pb2.Status, _Mapping]] = ..., bytes_written: _Optional[int] = ..., exit_code: _Optional[int] = ...) -> None: ...
