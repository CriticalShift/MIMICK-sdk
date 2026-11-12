from mimick.appliance.v1 import common_pb2 as _common_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ChardevSendRequest(_message.Message):
    __slots__ = ("handle", "data")
    HANDLE_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    handle: _common_pb2.PeripheralHandle
    data: bytes
    def __init__(self, handle: _Optional[_Union[_common_pb2.PeripheralHandle, _Mapping]] = ..., data: _Optional[bytes] = ...) -> None: ...

class ChardevSendResponse(_message.Message):
    __slots__ = ("status", "bytes_written")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    BYTES_WRITTEN_FIELD_NUMBER: _ClassVar[int]
    status: _common_pb2.Status
    bytes_written: int
    def __init__(self, status: _Optional[_Union[_common_pb2.Status, _Mapping]] = ..., bytes_written: _Optional[int] = ...) -> None: ...

class ChardevRecvRequest(_message.Message):
    __slots__ = ("handle", "max_bytes", "timeout_ms", "expect_pattern")
    HANDLE_FIELD_NUMBER: _ClassVar[int]
    MAX_BYTES_FIELD_NUMBER: _ClassVar[int]
    TIMEOUT_MS_FIELD_NUMBER: _ClassVar[int]
    EXPECT_PATTERN_FIELD_NUMBER: _ClassVar[int]
    handle: _common_pb2.PeripheralHandle
    max_bytes: int
    timeout_ms: int
    expect_pattern: str
    def __init__(self, handle: _Optional[_Union[_common_pb2.PeripheralHandle, _Mapping]] = ..., max_bytes: _Optional[int] = ..., timeout_ms: _Optional[int] = ..., expect_pattern: _Optional[str] = ...) -> None: ...

class ChardevRecvResponse(_message.Message):
    __slots__ = ("status", "data", "matched", "received_at")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    MATCHED_FIELD_NUMBER: _ClassVar[int]
    RECEIVED_AT_FIELD_NUMBER: _ClassVar[int]
    status: _common_pb2.Status
    data: bytes
    matched: bool
    received_at: _common_pb2.Timestamp
    def __init__(self, status: _Optional[_Union[_common_pb2.Status, _Mapping]] = ..., data: _Optional[bytes] = ..., matched: _Optional[bool] = ..., received_at: _Optional[_Union[_common_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class ChardevReadStreamRequest(_message.Message):
    __slots__ = ("handle", "frame_size")
    HANDLE_FIELD_NUMBER: _ClassVar[int]
    FRAME_SIZE_FIELD_NUMBER: _ClassVar[int]
    handle: _common_pb2.PeripheralHandle
    frame_size: int
    def __init__(self, handle: _Optional[_Union[_common_pb2.PeripheralHandle, _Mapping]] = ..., frame_size: _Optional[int] = ...) -> None: ...

class ChardevReadFrame(_message.Message):
    __slots__ = ("status", "data", "frame_index", "captured_at")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    FRAME_INDEX_FIELD_NUMBER: _ClassVar[int]
    CAPTURED_AT_FIELD_NUMBER: _ClassVar[int]
    status: _common_pb2.Status
    data: bytes
    frame_index: int
    captured_at: _common_pb2.Timestamp
    def __init__(self, status: _Optional[_Union[_common_pb2.Status, _Mapping]] = ..., data: _Optional[bytes] = ..., frame_index: _Optional[int] = ..., captured_at: _Optional[_Union[_common_pb2.Timestamp, _Mapping]] = ...) -> None: ...
