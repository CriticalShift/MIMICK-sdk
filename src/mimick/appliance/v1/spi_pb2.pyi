from mimick.appliance.v1 import common_pb2 as _common_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SpiMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SPI_MODE_UNSPECIFIED: _ClassVar[SpiMode]
    SPI_MODE_0: _ClassVar[SpiMode]
    SPI_MODE_1: _ClassVar[SpiMode]
    SPI_MODE_2: _ClassVar[SpiMode]
    SPI_MODE_3: _ClassVar[SpiMode]

class CsIdleState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CS_IDLE_STATE_UNSPECIFIED: _ClassVar[CsIdleState]
    CS_IDLE_STATE_HIGH: _ClassVar[CsIdleState]
    CS_IDLE_STATE_LOW: _ClassVar[CsIdleState]

class CsControl(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CS_CONTROL_UNSPECIFIED: _ClassVar[CsControl]
    CS_CONTROL_AUTO: _ClassVar[CsControl]
    CS_CONTROL_ASSERT: _ClassVar[CsControl]
    CS_CONTROL_HOLD: _ClassVar[CsControl]
    CS_CONTROL_RELEASE: _ClassVar[CsControl]
SPI_MODE_UNSPECIFIED: SpiMode
SPI_MODE_0: SpiMode
SPI_MODE_1: SpiMode
SPI_MODE_2: SpiMode
SPI_MODE_3: SpiMode
CS_IDLE_STATE_UNSPECIFIED: CsIdleState
CS_IDLE_STATE_HIGH: CsIdleState
CS_IDLE_STATE_LOW: CsIdleState
CS_CONTROL_UNSPECIFIED: CsControl
CS_CONTROL_AUTO: CsControl
CS_CONTROL_ASSERT: CsControl
CS_CONTROL_HOLD: CsControl
CS_CONTROL_RELEASE: CsControl

class SpiSetConfigRequest(_message.Message):
    __slots__ = ("handle", "mode", "freq_hz", "bit_order", "cs_idle", "flush_after_read")
    HANDLE_FIELD_NUMBER: _ClassVar[int]
    MODE_FIELD_NUMBER: _ClassVar[int]
    FREQ_HZ_FIELD_NUMBER: _ClassVar[int]
    BIT_ORDER_FIELD_NUMBER: _ClassVar[int]
    CS_IDLE_FIELD_NUMBER: _ClassVar[int]
    FLUSH_AFTER_READ_FIELD_NUMBER: _ClassVar[int]
    handle: _common_pb2.PeripheralHandle
    mode: SpiMode
    freq_hz: int
    bit_order: _common_pb2.BitOrder
    cs_idle: CsIdleState
    flush_after_read: bool
    def __init__(self, handle: _Optional[_Union[_common_pb2.PeripheralHandle, _Mapping]] = ..., mode: _Optional[_Union[SpiMode, str]] = ..., freq_hz: _Optional[int] = ..., bit_order: _Optional[_Union[_common_pb2.BitOrder, str]] = ..., cs_idle: _Optional[_Union[CsIdleState, str]] = ..., flush_after_read: _Optional[bool] = ...) -> None: ...

class SpiSetConfigResponse(_message.Message):
    __slots__ = ("status", "actual_freq_hz")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    ACTUAL_FREQ_HZ_FIELD_NUMBER: _ClassVar[int]
    status: _common_pb2.Status
    actual_freq_hz: int
    def __init__(self, status: _Optional[_Union[_common_pb2.Status, _Mapping]] = ..., actual_freq_hz: _Optional[int] = ...) -> None: ...

class SpiGetConfigRequest(_message.Message):
    __slots__ = ("handle",)
    HANDLE_FIELD_NUMBER: _ClassVar[int]
    handle: _common_pb2.PeripheralHandle
    def __init__(self, handle: _Optional[_Union[_common_pb2.PeripheralHandle, _Mapping]] = ...) -> None: ...

class SpiGetConfigResponse(_message.Message):
    __slots__ = ("status", "mode", "freq_hz", "bit_order", "cs_idle", "flush_after_read")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    MODE_FIELD_NUMBER: _ClassVar[int]
    FREQ_HZ_FIELD_NUMBER: _ClassVar[int]
    BIT_ORDER_FIELD_NUMBER: _ClassVar[int]
    CS_IDLE_FIELD_NUMBER: _ClassVar[int]
    FLUSH_AFTER_READ_FIELD_NUMBER: _ClassVar[int]
    status: _common_pb2.Status
    mode: SpiMode
    freq_hz: int
    bit_order: _common_pb2.BitOrder
    cs_idle: CsIdleState
    flush_after_read: bool
    def __init__(self, status: _Optional[_Union[_common_pb2.Status, _Mapping]] = ..., mode: _Optional[_Union[SpiMode, str]] = ..., freq_hz: _Optional[int] = ..., bit_order: _Optional[_Union[_common_pb2.BitOrder, str]] = ..., cs_idle: _Optional[_Union[CsIdleState, str]] = ..., flush_after_read: _Optional[bool] = ...) -> None: ...

class SpiWriteRequest(_message.Message):
    __slots__ = ("handle", "data")
    HANDLE_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    handle: _common_pb2.PeripheralHandle
    data: bytes
    def __init__(self, handle: _Optional[_Union[_common_pb2.PeripheralHandle, _Mapping]] = ..., data: _Optional[bytes] = ...) -> None: ...

class SpiWriteResponse(_message.Message):
    __slots__ = ("status", "bytes_written")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    BYTES_WRITTEN_FIELD_NUMBER: _ClassVar[int]
    status: _common_pb2.Status
    bytes_written: int
    def __init__(self, status: _Optional[_Union[_common_pb2.Status, _Mapping]] = ..., bytes_written: _Optional[int] = ...) -> None: ...

class SpiReadRequest(_message.Message):
    __slots__ = ("handle", "size")
    HANDLE_FIELD_NUMBER: _ClassVar[int]
    SIZE_FIELD_NUMBER: _ClassVar[int]
    handle: _common_pb2.PeripheralHandle
    size: int
    def __init__(self, handle: _Optional[_Union[_common_pb2.PeripheralHandle, _Mapping]] = ..., size: _Optional[int] = ...) -> None: ...

class SpiReadResponse(_message.Message):
    __slots__ = ("status", "data")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    status: _common_pb2.Status
    data: bytes
    def __init__(self, status: _Optional[_Union[_common_pb2.Status, _Mapping]] = ..., data: _Optional[bytes] = ...) -> None: ...

class SpiTransferRequest(_message.Message):
    __slots__ = ("handle", "mosi_data")
    HANDLE_FIELD_NUMBER: _ClassVar[int]
    MOSI_DATA_FIELD_NUMBER: _ClassVar[int]
    handle: _common_pb2.PeripheralHandle
    mosi_data: bytes
    def __init__(self, handle: _Optional[_Union[_common_pb2.PeripheralHandle, _Mapping]] = ..., mosi_data: _Optional[bytes] = ...) -> None: ...

class SpiTransferResponse(_message.Message):
    __slots__ = ("status", "miso_data", "bytes_transferred")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    MISO_DATA_FIELD_NUMBER: _ClassVar[int]
    BYTES_TRANSFERRED_FIELD_NUMBER: _ClassVar[int]
    status: _common_pb2.Status
    miso_data: bytes
    bytes_transferred: int
    def __init__(self, status: _Optional[_Union[_common_pb2.Status, _Mapping]] = ..., miso_data: _Optional[bytes] = ..., bytes_transferred: _Optional[int] = ...) -> None: ...

class SpiWriteBitsRequest(_message.Message):
    __slots__ = ("handle", "bits", "bit_count")
    HANDLE_FIELD_NUMBER: _ClassVar[int]
    BITS_FIELD_NUMBER: _ClassVar[int]
    BIT_COUNT_FIELD_NUMBER: _ClassVar[int]
    handle: _common_pb2.PeripheralHandle
    bits: int
    bit_count: int
    def __init__(self, handle: _Optional[_Union[_common_pb2.PeripheralHandle, _Mapping]] = ..., bits: _Optional[int] = ..., bit_count: _Optional[int] = ...) -> None: ...

class SpiWriteBitsResponse(_message.Message):
    __slots__ = ("status",)
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: _common_pb2.Status
    def __init__(self, status: _Optional[_Union[_common_pb2.Status, _Mapping]] = ...) -> None: ...

class SpiReadBitsRequest(_message.Message):
    __slots__ = ("handle", "bit_count")
    HANDLE_FIELD_NUMBER: _ClassVar[int]
    BIT_COUNT_FIELD_NUMBER: _ClassVar[int]
    handle: _common_pb2.PeripheralHandle
    bit_count: int
    def __init__(self, handle: _Optional[_Union[_common_pb2.PeripheralHandle, _Mapping]] = ..., bit_count: _Optional[int] = ...) -> None: ...

class SpiReadBitsResponse(_message.Message):
    __slots__ = ("status", "bits")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    BITS_FIELD_NUMBER: _ClassVar[int]
    status: _common_pb2.Status
    bits: int
    def __init__(self, status: _Optional[_Union[_common_pb2.Status, _Mapping]] = ..., bits: _Optional[int] = ...) -> None: ...

class SpiTransferStreamRequest(_message.Message):
    __slots__ = ("handle", "mosi_data", "read_size", "cs_control", "seq")
    HANDLE_FIELD_NUMBER: _ClassVar[int]
    MOSI_DATA_FIELD_NUMBER: _ClassVar[int]
    READ_SIZE_FIELD_NUMBER: _ClassVar[int]
    CS_CONTROL_FIELD_NUMBER: _ClassVar[int]
    SEQ_FIELD_NUMBER: _ClassVar[int]
    handle: _common_pb2.PeripheralHandle
    mosi_data: bytes
    read_size: int
    cs_control: CsControl
    seq: int
    def __init__(self, handle: _Optional[_Union[_common_pb2.PeripheralHandle, _Mapping]] = ..., mosi_data: _Optional[bytes] = ..., read_size: _Optional[int] = ..., cs_control: _Optional[_Union[CsControl, str]] = ..., seq: _Optional[int] = ...) -> None: ...

class SpiTransferStreamResponse(_message.Message):
    __slots__ = ("status", "miso_data", "seq", "captured_at")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    MISO_DATA_FIELD_NUMBER: _ClassVar[int]
    SEQ_FIELD_NUMBER: _ClassVar[int]
    CAPTURED_AT_FIELD_NUMBER: _ClassVar[int]
    status: _common_pb2.Status
    miso_data: bytes
    seq: int
    captured_at: _common_pb2.Timestamp
    def __init__(self, status: _Optional[_Union[_common_pb2.Status, _Mapping]] = ..., miso_data: _Optional[bytes] = ..., seq: _Optional[int] = ..., captured_at: _Optional[_Union[_common_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class SpiReadStreamRequest(_message.Message):
    __slots__ = ("handle", "frame_size", "max_frames", "interval_us")
    HANDLE_FIELD_NUMBER: _ClassVar[int]
    FRAME_SIZE_FIELD_NUMBER: _ClassVar[int]
    MAX_FRAMES_FIELD_NUMBER: _ClassVar[int]
    INTERVAL_US_FIELD_NUMBER: _ClassVar[int]
    handle: _common_pb2.PeripheralHandle
    frame_size: int
    max_frames: int
    interval_us: int
    def __init__(self, handle: _Optional[_Union[_common_pb2.PeripheralHandle, _Mapping]] = ..., frame_size: _Optional[int] = ..., max_frames: _Optional[int] = ..., interval_us: _Optional[int] = ...) -> None: ...

class SpiReadStreamFrame(_message.Message):
    __slots__ = ("status", "miso_data", "frame_index", "captured_at", "overflow")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    MISO_DATA_FIELD_NUMBER: _ClassVar[int]
    FRAME_INDEX_FIELD_NUMBER: _ClassVar[int]
    CAPTURED_AT_FIELD_NUMBER: _ClassVar[int]
    OVERFLOW_FIELD_NUMBER: _ClassVar[int]
    status: _common_pb2.Status
    miso_data: bytes
    frame_index: int
    captured_at: _common_pb2.Timestamp
    overflow: bool
    def __init__(self, status: _Optional[_Union[_common_pb2.Status, _Mapping]] = ..., miso_data: _Optional[bytes] = ..., frame_index: _Optional[int] = ..., captured_at: _Optional[_Union[_common_pb2.Timestamp, _Mapping]] = ..., overflow: _Optional[bool] = ...) -> None: ...
