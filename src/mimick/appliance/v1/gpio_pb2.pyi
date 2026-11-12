from mimick.appliance.v1 import common_pb2 as _common_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PinGroup(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PIN_GROUP_UNSPECIFIED: _ClassVar[PinGroup]
    PIN_GROUP_LOW: _ClassVar[PinGroup]
    PIN_GROUP_HIGH: _ClassVar[PinGroup]

class PinDirection(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PIN_DIRECTION_UNSPECIFIED: _ClassVar[PinDirection]
    PIN_DIRECTION_INPUT: _ClassVar[PinDirection]
    PIN_DIRECTION_OUTPUT: _ClassVar[PinDirection]

class ActiveLevel(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ACTIVE_LEVEL_UNSPECIFIED: _ClassVar[ActiveLevel]
    ACTIVE_LEVEL_HIGH: _ClassVar[ActiveLevel]
    ACTIVE_LEVEL_LOW: _ClassVar[ActiveLevel]

class DriveMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DRIVE_MODE_UNSPECIFIED: _ClassVar[DriveMode]
    DRIVE_MODE_PUSH_PULL: _ClassVar[DriveMode]
    DRIVE_MODE_OPEN_DRAIN: _ClassVar[DriveMode]
    DRIVE_MODE_OPEN_SOURCE: _ClassVar[DriveMode]

class PinPull(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PIN_PULL_UNSPECIFIED: _ClassVar[PinPull]
    PIN_PULL_NONE: _ClassVar[PinPull]
    PIN_PULL_UP: _ClassVar[PinPull]
    PIN_PULL_DOWN: _ClassVar[PinPull]

class DriveStrength(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DRIVE_STRENGTH_UNSPECIFIED: _ClassVar[DriveStrength]
    DRIVE_STRENGTH_2MA: _ClassVar[DriveStrength]
    DRIVE_STRENGTH_4MA: _ClassVar[DriveStrength]
    DRIVE_STRENGTH_8MA: _ClassVar[DriveStrength]
    DRIVE_STRENGTH_16MA: _ClassVar[DriveStrength]

class SlewRate(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SLEW_RATE_UNSPECIFIED: _ClassVar[SlewRate]
    SLEW_RATE_SLOW: _ClassVar[SlewRate]
    SLEW_RATE_FAST: _ClassVar[SlewRate]

class PinLevel(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PIN_LEVEL_UNSPECIFIED: _ClassVar[PinLevel]
    PIN_LEVEL_LOW: _ClassVar[PinLevel]
    PIN_LEVEL_HIGH: _ClassVar[PinLevel]

class EdgeType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    EDGE_TYPE_UNSPECIFIED: _ClassVar[EdgeType]
    EDGE_TYPE_RISING: _ClassVar[EdgeType]
    EDGE_TYPE_FALLING: _ClassVar[EdgeType]
    EDGE_TYPE_BOTH: _ClassVar[EdgeType]
PIN_GROUP_UNSPECIFIED: PinGroup
PIN_GROUP_LOW: PinGroup
PIN_GROUP_HIGH: PinGroup
PIN_DIRECTION_UNSPECIFIED: PinDirection
PIN_DIRECTION_INPUT: PinDirection
PIN_DIRECTION_OUTPUT: PinDirection
ACTIVE_LEVEL_UNSPECIFIED: ActiveLevel
ACTIVE_LEVEL_HIGH: ActiveLevel
ACTIVE_LEVEL_LOW: ActiveLevel
DRIVE_MODE_UNSPECIFIED: DriveMode
DRIVE_MODE_PUSH_PULL: DriveMode
DRIVE_MODE_OPEN_DRAIN: DriveMode
DRIVE_MODE_OPEN_SOURCE: DriveMode
PIN_PULL_UNSPECIFIED: PinPull
PIN_PULL_NONE: PinPull
PIN_PULL_UP: PinPull
PIN_PULL_DOWN: PinPull
DRIVE_STRENGTH_UNSPECIFIED: DriveStrength
DRIVE_STRENGTH_2MA: DriveStrength
DRIVE_STRENGTH_4MA: DriveStrength
DRIVE_STRENGTH_8MA: DriveStrength
DRIVE_STRENGTH_16MA: DriveStrength
SLEW_RATE_UNSPECIFIED: SlewRate
SLEW_RATE_SLOW: SlewRate
SLEW_RATE_FAST: SlewRate
PIN_LEVEL_UNSPECIFIED: PinLevel
PIN_LEVEL_LOW: PinLevel
PIN_LEVEL_HIGH: PinLevel
EDGE_TYPE_UNSPECIFIED: EdgeType
EDGE_TYPE_RISING: EdgeType
EDGE_TYPE_FALLING: EdgeType
EDGE_TYPE_BOTH: EdgeType

class PinConfig(_message.Message):
    __slots__ = ("pin", "direction", "active_level", "drive_strength", "slew_rate", "drive_mode", "pull")
    PIN_FIELD_NUMBER: _ClassVar[int]
    DIRECTION_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_LEVEL_FIELD_NUMBER: _ClassVar[int]
    DRIVE_STRENGTH_FIELD_NUMBER: _ClassVar[int]
    SLEW_RATE_FIELD_NUMBER: _ClassVar[int]
    DRIVE_MODE_FIELD_NUMBER: _ClassVar[int]
    PULL_FIELD_NUMBER: _ClassVar[int]
    pin: int
    direction: PinDirection
    active_level: ActiveLevel
    drive_strength: DriveStrength
    slew_rate: SlewRate
    drive_mode: DriveMode
    pull: PinPull
    def __init__(self, pin: _Optional[int] = ..., direction: _Optional[_Union[PinDirection, str]] = ..., active_level: _Optional[_Union[ActiveLevel, str]] = ..., drive_strength: _Optional[_Union[DriveStrength, str]] = ..., slew_rate: _Optional[_Union[SlewRate, str]] = ..., drive_mode: _Optional[_Union[DriveMode, str]] = ..., pull: _Optional[_Union[PinPull, str]] = ...) -> None: ...

class PinValue(_message.Message):
    __slots__ = ("pin", "level")
    PIN_FIELD_NUMBER: _ClassVar[int]
    LEVEL_FIELD_NUMBER: _ClassVar[int]
    pin: int
    level: PinLevel
    def __init__(self, pin: _Optional[int] = ..., level: _Optional[_Union[PinLevel, str]] = ...) -> None: ...

class GpioListPinsRequest(_message.Message):
    __slots__ = ("handle",)
    HANDLE_FIELD_NUMBER: _ClassVar[int]
    handle: _common_pb2.PeripheralHandle
    def __init__(self, handle: _Optional[_Union[_common_pb2.PeripheralHandle, _Mapping]] = ...) -> None: ...

class PinInfo(_message.Message):
    __slots__ = ("pin", "name", "group", "protocol_shared", "config", "level", "physical_pin", "configured")
    PIN_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    GROUP_FIELD_NUMBER: _ClassVar[int]
    PROTOCOL_SHARED_FIELD_NUMBER: _ClassVar[int]
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    LEVEL_FIELD_NUMBER: _ClassVar[int]
    PHYSICAL_PIN_FIELD_NUMBER: _ClassVar[int]
    CONFIGURED_FIELD_NUMBER: _ClassVar[int]
    pin: int
    name: str
    group: PinGroup
    protocol_shared: bool
    config: PinConfig
    level: PinLevel
    physical_pin: int
    configured: bool
    def __init__(self, pin: _Optional[int] = ..., name: _Optional[str] = ..., group: _Optional[_Union[PinGroup, str]] = ..., protocol_shared: _Optional[bool] = ..., config: _Optional[_Union[PinConfig, _Mapping]] = ..., level: _Optional[_Union[PinLevel, str]] = ..., physical_pin: _Optional[int] = ..., configured: _Optional[bool] = ...) -> None: ...

class GpioListPinsResponse(_message.Message):
    __slots__ = ("status", "pins")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    PINS_FIELD_NUMBER: _ClassVar[int]
    status: _common_pb2.Status
    pins: _containers.RepeatedCompositeFieldContainer[PinInfo]
    def __init__(self, status: _Optional[_Union[_common_pb2.Status, _Mapping]] = ..., pins: _Optional[_Iterable[_Union[PinInfo, _Mapping]]] = ...) -> None: ...

class GpioSetConfigRequest(_message.Message):
    __slots__ = ("handle", "pins")
    HANDLE_FIELD_NUMBER: _ClassVar[int]
    PINS_FIELD_NUMBER: _ClassVar[int]
    handle: _common_pb2.PeripheralHandle
    pins: _containers.RepeatedCompositeFieldContainer[PinConfig]
    def __init__(self, handle: _Optional[_Union[_common_pb2.PeripheralHandle, _Mapping]] = ..., pins: _Optional[_Iterable[_Union[PinConfig, _Mapping]]] = ...) -> None: ...

class GpioSetConfigResponse(_message.Message):
    __slots__ = ("status", "updated_pins")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    UPDATED_PINS_FIELD_NUMBER: _ClassVar[int]
    status: _common_pb2.Status
    updated_pins: _containers.RepeatedCompositeFieldContainer[PinConfig]
    def __init__(self, status: _Optional[_Union[_common_pb2.Status, _Mapping]] = ..., updated_pins: _Optional[_Iterable[_Union[PinConfig, _Mapping]]] = ...) -> None: ...

class GpioGetConfigRequest(_message.Message):
    __slots__ = ("handle", "pin_ids")
    HANDLE_FIELD_NUMBER: _ClassVar[int]
    PIN_IDS_FIELD_NUMBER: _ClassVar[int]
    handle: _common_pb2.PeripheralHandle
    pin_ids: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, handle: _Optional[_Union[_common_pb2.PeripheralHandle, _Mapping]] = ..., pin_ids: _Optional[_Iterable[int]] = ...) -> None: ...

class GpioGetConfigResponse(_message.Message):
    __slots__ = ("status", "pins")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    PINS_FIELD_NUMBER: _ClassVar[int]
    status: _common_pb2.Status
    pins: _containers.RepeatedCompositeFieldContainer[PinConfig]
    def __init__(self, status: _Optional[_Union[_common_pb2.Status, _Mapping]] = ..., pins: _Optional[_Iterable[_Union[PinConfig, _Mapping]]] = ...) -> None: ...

class GpioWritePinRequest(_message.Message):
    __slots__ = ("handle", "pin", "level")
    HANDLE_FIELD_NUMBER: _ClassVar[int]
    PIN_FIELD_NUMBER: _ClassVar[int]
    LEVEL_FIELD_NUMBER: _ClassVar[int]
    handle: _common_pb2.PeripheralHandle
    pin: int
    level: PinLevel
    def __init__(self, handle: _Optional[_Union[_common_pb2.PeripheralHandle, _Mapping]] = ..., pin: _Optional[int] = ..., level: _Optional[_Union[PinLevel, str]] = ...) -> None: ...

class GpioWritePinResponse(_message.Message):
    __slots__ = ("status",)
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: _common_pb2.Status
    def __init__(self, status: _Optional[_Union[_common_pb2.Status, _Mapping]] = ...) -> None: ...

class GpioWritePinsRequest(_message.Message):
    __slots__ = ("handle", "pins")
    HANDLE_FIELD_NUMBER: _ClassVar[int]
    PINS_FIELD_NUMBER: _ClassVar[int]
    handle: _common_pb2.PeripheralHandle
    pins: _containers.RepeatedCompositeFieldContainer[PinValue]
    def __init__(self, handle: _Optional[_Union[_common_pb2.PeripheralHandle, _Mapping]] = ..., pins: _Optional[_Iterable[_Union[PinValue, _Mapping]]] = ...) -> None: ...

class GpioWritePinsResponse(_message.Message):
    __slots__ = ("status",)
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: _common_pb2.Status
    def __init__(self, status: _Optional[_Union[_common_pb2.Status, _Mapping]] = ...) -> None: ...

class GpioReadPinRequest(_message.Message):
    __slots__ = ("handle", "pin")
    HANDLE_FIELD_NUMBER: _ClassVar[int]
    PIN_FIELD_NUMBER: _ClassVar[int]
    handle: _common_pb2.PeripheralHandle
    pin: int
    def __init__(self, handle: _Optional[_Union[_common_pb2.PeripheralHandle, _Mapping]] = ..., pin: _Optional[int] = ...) -> None: ...

class GpioReadPinResponse(_message.Message):
    __slots__ = ("status", "level", "sampled_at")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    LEVEL_FIELD_NUMBER: _ClassVar[int]
    SAMPLED_AT_FIELD_NUMBER: _ClassVar[int]
    status: _common_pb2.Status
    level: PinLevel
    sampled_at: _common_pb2.Timestamp
    def __init__(self, status: _Optional[_Union[_common_pb2.Status, _Mapping]] = ..., level: _Optional[_Union[PinLevel, str]] = ..., sampled_at: _Optional[_Union[_common_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class GpioReadPinsRequest(_message.Message):
    __slots__ = ("handle",)
    HANDLE_FIELD_NUMBER: _ClassVar[int]
    handle: _common_pb2.PeripheralHandle
    def __init__(self, handle: _Optional[_Union[_common_pb2.PeripheralHandle, _Mapping]] = ...) -> None: ...

class GpioReadPinsResponse(_message.Message):
    __slots__ = ("status", "pin_states", "raw_value", "sampled_at")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    PIN_STATES_FIELD_NUMBER: _ClassVar[int]
    RAW_VALUE_FIELD_NUMBER: _ClassVar[int]
    SAMPLED_AT_FIELD_NUMBER: _ClassVar[int]
    status: _common_pb2.Status
    pin_states: _containers.RepeatedCompositeFieldContainer[PinValue]
    raw_value: int
    sampled_at: _common_pb2.Timestamp
    def __init__(self, status: _Optional[_Union[_common_pb2.Status, _Mapping]] = ..., pin_states: _Optional[_Iterable[_Union[PinValue, _Mapping]]] = ..., raw_value: _Optional[int] = ..., sampled_at: _Optional[_Union[_common_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class GpioTristateRequest(_message.Message):
    __slots__ = ("handle",)
    HANDLE_FIELD_NUMBER: _ClassVar[int]
    handle: _common_pb2.PeripheralHandle
    def __init__(self, handle: _Optional[_Union[_common_pb2.PeripheralHandle, _Mapping]] = ...) -> None: ...

class GpioTristateResponse(_message.Message):
    __slots__ = ("status",)
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: _common_pb2.Status
    def __init__(self, status: _Optional[_Union[_common_pb2.Status, _Mapping]] = ...) -> None: ...

class PinWatchConfig(_message.Message):
    __slots__ = ("pin", "edge", "debounce_us")
    PIN_FIELD_NUMBER: _ClassVar[int]
    EDGE_FIELD_NUMBER: _ClassVar[int]
    DEBOUNCE_US_FIELD_NUMBER: _ClassVar[int]
    pin: int
    edge: EdgeType
    debounce_us: int
    def __init__(self, pin: _Optional[int] = ..., edge: _Optional[_Union[EdgeType, str]] = ..., debounce_us: _Optional[int] = ...) -> None: ...

class GpioWatchStreamRequest(_message.Message):
    __slots__ = ("handle", "pins", "poll_interval_us", "max_events")
    HANDLE_FIELD_NUMBER: _ClassVar[int]
    PINS_FIELD_NUMBER: _ClassVar[int]
    POLL_INTERVAL_US_FIELD_NUMBER: _ClassVar[int]
    MAX_EVENTS_FIELD_NUMBER: _ClassVar[int]
    handle: _common_pb2.PeripheralHandle
    pins: _containers.RepeatedCompositeFieldContainer[PinWatchConfig]
    poll_interval_us: int
    max_events: int
    def __init__(self, handle: _Optional[_Union[_common_pb2.PeripheralHandle, _Mapping]] = ..., pins: _Optional[_Iterable[_Union[PinWatchConfig, _Mapping]]] = ..., poll_interval_us: _Optional[int] = ..., max_events: _Optional[int] = ...) -> None: ...

class GpioPinEvent(_message.Message):
    __slots__ = ("status", "pin", "level", "edge", "occurred_at", "event_index", "snapshot")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    PIN_FIELD_NUMBER: _ClassVar[int]
    LEVEL_FIELD_NUMBER: _ClassVar[int]
    EDGE_FIELD_NUMBER: _ClassVar[int]
    OCCURRED_AT_FIELD_NUMBER: _ClassVar[int]
    EVENT_INDEX_FIELD_NUMBER: _ClassVar[int]
    SNAPSHOT_FIELD_NUMBER: _ClassVar[int]
    status: _common_pb2.Status
    pin: int
    level: PinLevel
    edge: EdgeType
    occurred_at: _common_pb2.Timestamp
    event_index: int
    snapshot: _containers.RepeatedCompositeFieldContainer[PinValue]
    def __init__(self, status: _Optional[_Union[_common_pb2.Status, _Mapping]] = ..., pin: _Optional[int] = ..., level: _Optional[_Union[PinLevel, str]] = ..., edge: _Optional[_Union[EdgeType, str]] = ..., occurred_at: _Optional[_Union[_common_pb2.Timestamp, _Mapping]] = ..., event_index: _Optional[int] = ..., snapshot: _Optional[_Iterable[_Union[PinValue, _Mapping]]] = ...) -> None: ...

class GpioSyncRequest(_message.Message):
    __slots__ = ("handle", "write_pins", "seq")
    HANDLE_FIELD_NUMBER: _ClassVar[int]
    WRITE_PINS_FIELD_NUMBER: _ClassVar[int]
    SEQ_FIELD_NUMBER: _ClassVar[int]
    handle: _common_pb2.PeripheralHandle
    write_pins: _containers.RepeatedCompositeFieldContainer[PinValue]
    seq: int
    def __init__(self, handle: _Optional[_Union[_common_pb2.PeripheralHandle, _Mapping]] = ..., write_pins: _Optional[_Iterable[_Union[PinValue, _Mapping]]] = ..., seq: _Optional[int] = ...) -> None: ...

class GpioSyncResponse(_message.Message):
    __slots__ = ("status", "pin_states", "seq", "sampled_at")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    PIN_STATES_FIELD_NUMBER: _ClassVar[int]
    SEQ_FIELD_NUMBER: _ClassVar[int]
    SAMPLED_AT_FIELD_NUMBER: _ClassVar[int]
    status: _common_pb2.Status
    pin_states: _containers.RepeatedCompositeFieldContainer[PinValue]
    seq: int
    sampled_at: _common_pb2.Timestamp
    def __init__(self, status: _Optional[_Union[_common_pb2.Status, _Mapping]] = ..., pin_states: _Optional[_Iterable[_Union[PinValue, _Mapping]]] = ..., seq: _Optional[int] = ..., sampled_at: _Optional[_Union[_common_pb2.Timestamp, _Mapping]] = ...) -> None: ...
