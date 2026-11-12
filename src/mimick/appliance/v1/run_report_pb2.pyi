from mimick.appliance.v1 import common_pb2 as _common_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class FileChunk(_message.Message):
    __slots__ = ("name", "media_type", "data")
    NAME_FIELD_NUMBER: _ClassVar[int]
    MEDIA_TYPE_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    name: str
    media_type: str
    data: bytes
    def __init__(self, name: _Optional[str] = ..., media_type: _Optional[str] = ..., data: _Optional[bytes] = ...) -> None: ...

class UploadFileResponse(_message.Message):
    __slots__ = ("file_id", "size", "sha256")
    FILE_ID_FIELD_NUMBER: _ClassVar[int]
    SIZE_FIELD_NUMBER: _ClassVar[int]
    SHA256_FIELD_NUMBER: _ClassVar[int]
    file_id: str
    size: int
    sha256: str
    def __init__(self, file_id: _Optional[str] = ..., size: _Optional[int] = ..., sha256: _Optional[str] = ...) -> None: ...

class StartMonitorRequest(_message.Message):
    __slots__ = ("name", "node_run_id", "every_ms", "unit", "lower", "upper", "marginal_lower", "marginal_upper", "gpio_pin", "relay_channel", "software_read")
    NAME_FIELD_NUMBER: _ClassVar[int]
    NODE_RUN_ID_FIELD_NUMBER: _ClassVar[int]
    EVERY_MS_FIELD_NUMBER: _ClassVar[int]
    UNIT_FIELD_NUMBER: _ClassVar[int]
    LOWER_FIELD_NUMBER: _ClassVar[int]
    UPPER_FIELD_NUMBER: _ClassVar[int]
    MARGINAL_LOWER_FIELD_NUMBER: _ClassVar[int]
    MARGINAL_UPPER_FIELD_NUMBER: _ClassVar[int]
    GPIO_PIN_FIELD_NUMBER: _ClassVar[int]
    RELAY_CHANNEL_FIELD_NUMBER: _ClassVar[int]
    SOFTWARE_READ_FIELD_NUMBER: _ClassVar[int]
    name: str
    node_run_id: str
    every_ms: int
    unit: str
    lower: float
    upper: float
    marginal_lower: float
    marginal_upper: float
    gpio_pin: GpioPinSource
    relay_channel: RelayChannelSource
    software_read: SoftwareReadSource
    def __init__(self, name: _Optional[str] = ..., node_run_id: _Optional[str] = ..., every_ms: _Optional[int] = ..., unit: _Optional[str] = ..., lower: _Optional[float] = ..., upper: _Optional[float] = ..., marginal_lower: _Optional[float] = ..., marginal_upper: _Optional[float] = ..., gpio_pin: _Optional[_Union[GpioPinSource, _Mapping]] = ..., relay_channel: _Optional[_Union[RelayChannelSource, _Mapping]] = ..., software_read: _Optional[_Union[SoftwareReadSource, _Mapping]] = ...) -> None: ...

class GpioPinSource(_message.Message):
    __slots__ = ("location", "pin")
    LOCATION_FIELD_NUMBER: _ClassVar[int]
    PIN_FIELD_NUMBER: _ClassVar[int]
    location: str
    pin: int
    def __init__(self, location: _Optional[str] = ..., pin: _Optional[int] = ...) -> None: ...

class RelayChannelSource(_message.Message):
    __slots__ = ("location", "channel")
    LOCATION_FIELD_NUMBER: _ClassVar[int]
    CHANNEL_FIELD_NUMBER: _ClassVar[int]
    location: str
    channel: int
    def __init__(self, location: _Optional[str] = ..., channel: _Optional[int] = ...) -> None: ...

class SoftwareReadSource(_message.Message):
    __slots__ = ("location", "pattern")
    LOCATION_FIELD_NUMBER: _ClassVar[int]
    PATTERN_FIELD_NUMBER: _ClassVar[int]
    location: str
    pattern: str
    def __init__(self, location: _Optional[str] = ..., pattern: _Optional[str] = ...) -> None: ...

class Monitor(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class StopMonitorRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class MonitorSample(_message.Message):
    __slots__ = ("at", "value")
    AT_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    at: _common_pb2.Timestamp
    value: float
    def __init__(self, at: _Optional[_Union[_common_pb2.Timestamp, _Mapping]] = ..., value: _Optional[float] = ...) -> None: ...

class MonitorSeries(_message.Message):
    __slots__ = ("count", "errors", "first", "last", "min", "max", "verdict", "samples")
    COUNT_FIELD_NUMBER: _ClassVar[int]
    ERRORS_FIELD_NUMBER: _ClassVar[int]
    FIRST_FIELD_NUMBER: _ClassVar[int]
    LAST_FIELD_NUMBER: _ClassVar[int]
    MIN_FIELD_NUMBER: _ClassVar[int]
    MAX_FIELD_NUMBER: _ClassVar[int]
    VERDICT_FIELD_NUMBER: _ClassVar[int]
    SAMPLES_FIELD_NUMBER: _ClassVar[int]
    count: int
    errors: int
    first: _common_pb2.Timestamp
    last: _common_pb2.Timestamp
    min: float
    max: float
    verdict: str
    samples: _containers.RepeatedCompositeFieldContainer[MonitorSample]
    def __init__(self, count: _Optional[int] = ..., errors: _Optional[int] = ..., first: _Optional[_Union[_common_pb2.Timestamp, _Mapping]] = ..., last: _Optional[_Union[_common_pb2.Timestamp, _Mapping]] = ..., min: _Optional[float] = ..., max: _Optional[float] = ..., verdict: _Optional[str] = ..., samples: _Optional[_Iterable[_Union[MonitorSample, _Mapping]]] = ...) -> None: ...
