from mimick.appliance.v1 import common_pb2 as _common_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PeripheralState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PERIPHERAL_STATE_UNSPECIFIED: _ClassVar[PeripheralState]
    PERIPHERAL_STATE_PRESENT: _ClassVar[PeripheralState]
    PERIPHERAL_STATE_ABSENT: _ClassVar[PeripheralState]
    PERIPHERAL_STATE_UNUSED: _ClassVar[PeripheralState]
PERIPHERAL_STATE_UNSPECIFIED: PeripheralState
PERIPHERAL_STATE_PRESENT: PeripheralState
PERIPHERAL_STATE_ABSENT: PeripheralState
PERIPHERAL_STATE_UNUSED: PeripheralState

class ListPeripheralsRequest(_message.Message):
    __slots__ = ("transport_filter", "protocol_filter", "include_absent")
    TRANSPORT_FILTER_FIELD_NUMBER: _ClassVar[int]
    PROTOCOL_FILTER_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_ABSENT_FIELD_NUMBER: _ClassVar[int]
    transport_filter: _common_pb2.TransportType
    protocol_filter: _common_pb2.ProtocolType
    include_absent: bool
    def __init__(self, transport_filter: _Optional[_Union[_common_pb2.TransportType, str]] = ..., protocol_filter: _Optional[_Union[_common_pb2.ProtocolType, str]] = ..., include_absent: _Optional[bool] = ...) -> None: ...

class PeripheralStatus(_message.Message):
    __slots__ = ("session_open", "current_handle", "absent_reason", "state")
    SESSION_OPEN_FIELD_NUMBER: _ClassVar[int]
    CURRENT_HANDLE_FIELD_NUMBER: _ClassVar[int]
    ABSENT_REASON_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    session_open: bool
    current_handle: _common_pb2.PeripheralHandle
    absent_reason: str
    state: PeripheralState
    def __init__(self, session_open: _Optional[bool] = ..., current_handle: _Optional[_Union[_common_pb2.PeripheralHandle, _Mapping]] = ..., absent_reason: _Optional[str] = ..., state: _Optional[_Union[PeripheralState, str]] = ...) -> None: ...

class PeripheralEntry(_message.Message):
    __slots__ = ("location", "name", "interface", "descriptor", "status", "peripheral", "hardware_location", "member_of")
    LOCATION_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    INTERFACE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTOR_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    PERIPHERAL_FIELD_NUMBER: _ClassVar[int]
    HARDWARE_LOCATION_FIELD_NUMBER: _ClassVar[int]
    MEMBER_OF_FIELD_NUMBER: _ClassVar[int]
    location: str
    name: str
    interface: _common_pb2.Interface
    descriptor: _common_pb2.PeripheralDescriptor
    status: PeripheralStatus
    peripheral: str
    hardware_location: str
    member_of: str
    def __init__(self, location: _Optional[str] = ..., name: _Optional[str] = ..., interface: _Optional[_Union[_common_pb2.Interface, _Mapping]] = ..., descriptor: _Optional[_Union[_common_pb2.PeripheralDescriptor, _Mapping]] = ..., status: _Optional[_Union[PeripheralStatus, _Mapping]] = ..., peripheral: _Optional[str] = ..., hardware_location: _Optional[str] = ..., member_of: _Optional[str] = ...) -> None: ...

class ListPeripheralsResponse(_message.Message):
    __slots__ = ("status", "peripherals")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    PERIPHERALS_FIELD_NUMBER: _ClassVar[int]
    status: _common_pb2.Status
    peripherals: _containers.RepeatedCompositeFieldContainer[PeripheralEntry]
    def __init__(self, status: _Optional[_Union[_common_pb2.Status, _Mapping]] = ..., peripherals: _Optional[_Iterable[_Union[PeripheralEntry, _Mapping]]] = ...) -> None: ...

class RefreshPeripheralsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class RefreshPeripheralsResponse(_message.Message):
    __slots__ = ("status", "peripherals")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    PERIPHERALS_FIELD_NUMBER: _ClassVar[int]
    status: _common_pb2.Status
    peripherals: _containers.RepeatedCompositeFieldContainer[PeripheralEntry]
    def __init__(self, status: _Optional[_Union[_common_pb2.Status, _Mapping]] = ..., peripherals: _Optional[_Iterable[_Union[PeripheralEntry, _Mapping]]] = ...) -> None: ...

class OpenRequest(_message.Message):
    __slots__ = ("location", "timeout_ms")
    LOCATION_FIELD_NUMBER: _ClassVar[int]
    TIMEOUT_MS_FIELD_NUMBER: _ClassVar[int]
    location: str
    timeout_ms: int
    def __init__(self, location: _Optional[str] = ..., timeout_ms: _Optional[int] = ...) -> None: ...

class OpenResponse(_message.Message):
    __slots__ = ("status", "handle", "location", "interface", "descriptor")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    HANDLE_FIELD_NUMBER: _ClassVar[int]
    LOCATION_FIELD_NUMBER: _ClassVar[int]
    INTERFACE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTOR_FIELD_NUMBER: _ClassVar[int]
    status: _common_pb2.Status
    handle: _common_pb2.PeripheralHandle
    location: str
    interface: _common_pb2.Interface
    descriptor: _common_pb2.PeripheralDescriptor
    def __init__(self, status: _Optional[_Union[_common_pb2.Status, _Mapping]] = ..., handle: _Optional[_Union[_common_pb2.PeripheralHandle, _Mapping]] = ..., location: _Optional[str] = ..., interface: _Optional[_Union[_common_pb2.Interface, _Mapping]] = ..., descriptor: _Optional[_Union[_common_pb2.PeripheralDescriptor, _Mapping]] = ...) -> None: ...

class CloseRequest(_message.Message):
    __slots__ = ("handle",)
    HANDLE_FIELD_NUMBER: _ClassVar[int]
    handle: _common_pb2.PeripheralHandle
    def __init__(self, handle: _Optional[_Union[_common_pb2.PeripheralHandle, _Mapping]] = ...) -> None: ...

class CloseResponse(_message.Message):
    __slots__ = ("status",)
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: _common_pb2.Status
    def __init__(self, status: _Optional[_Union[_common_pb2.Status, _Mapping]] = ...) -> None: ...

class PeripheralConfig(_message.Message):
    __slots__ = ("name", "timeout_ms")
    NAME_FIELD_NUMBER: _ClassVar[int]
    TIMEOUT_MS_FIELD_NUMBER: _ClassVar[int]
    name: str
    timeout_ms: int
    def __init__(self, name: _Optional[str] = ..., timeout_ms: _Optional[int] = ...) -> None: ...

class PeripheralGetConfigRequest(_message.Message):
    __slots__ = ("handle",)
    HANDLE_FIELD_NUMBER: _ClassVar[int]
    handle: _common_pb2.PeripheralHandle
    def __init__(self, handle: _Optional[_Union[_common_pb2.PeripheralHandle, _Mapping]] = ...) -> None: ...

class PeripheralGetConfigResponse(_message.Message):
    __slots__ = ("status", "location", "interface", "descriptor", "config")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    LOCATION_FIELD_NUMBER: _ClassVar[int]
    INTERFACE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTOR_FIELD_NUMBER: _ClassVar[int]
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    status: _common_pb2.Status
    location: str
    interface: _common_pb2.Interface
    descriptor: _common_pb2.PeripheralDescriptor
    config: PeripheralConfig
    def __init__(self, status: _Optional[_Union[_common_pb2.Status, _Mapping]] = ..., location: _Optional[str] = ..., interface: _Optional[_Union[_common_pb2.Interface, _Mapping]] = ..., descriptor: _Optional[_Union[_common_pb2.PeripheralDescriptor, _Mapping]] = ..., config: _Optional[_Union[PeripheralConfig, _Mapping]] = ...) -> None: ...

class PeripheralSetConfigRequest(_message.Message):
    __slots__ = ("handle", "config", "update_fields")
    HANDLE_FIELD_NUMBER: _ClassVar[int]
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    UPDATE_FIELDS_FIELD_NUMBER: _ClassVar[int]
    handle: _common_pb2.PeripheralHandle
    config: PeripheralConfig
    update_fields: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, handle: _Optional[_Union[_common_pb2.PeripheralHandle, _Mapping]] = ..., config: _Optional[_Union[PeripheralConfig, _Mapping]] = ..., update_fields: _Optional[_Iterable[str]] = ...) -> None: ...

class PeripheralSetConfigResponse(_message.Message):
    __slots__ = ("status", "config")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    status: _common_pb2.Status
    config: PeripheralConfig
    def __init__(self, status: _Optional[_Union[_common_pb2.Status, _Mapping]] = ..., config: _Optional[_Union[PeripheralConfig, _Mapping]] = ...) -> None: ...

class SetupInfo(_message.Message):
    __slots__ = ("name", "refs", "active")
    NAME_FIELD_NUMBER: _ClassVar[int]
    REFS_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_FIELD_NUMBER: _ClassVar[int]
    name: str
    refs: _containers.RepeatedScalarFieldContainer[str]
    active: bool
    def __init__(self, name: _Optional[str] = ..., refs: _Optional[_Iterable[str]] = ..., active: _Optional[bool] = ...) -> None: ...

class ActivateConfigRequest(_message.Message):
    __slots__ = ("peripheral", "config")
    PERIPHERAL_FIELD_NUMBER: _ClassVar[int]
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    peripheral: str
    config: str
    def __init__(self, peripheral: _Optional[str] = ..., config: _Optional[str] = ...) -> None: ...

class ActivateConfigResponse(_message.Message):
    __slots__ = ("status",)
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: _common_pb2.Status
    def __init__(self, status: _Optional[_Union[_common_pb2.Status, _Mapping]] = ...) -> None: ...

class ActivateSetupRequest(_message.Message):
    __slots__ = ("setup",)
    SETUP_FIELD_NUMBER: _ClassVar[int]
    setup: str
    def __init__(self, setup: _Optional[str] = ...) -> None: ...

class ActivateSetupResponse(_message.Message):
    __slots__ = ("status",)
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: _common_pb2.Status
    def __init__(self, status: _Optional[_Union[_common_pb2.Status, _Mapping]] = ...) -> None: ...
