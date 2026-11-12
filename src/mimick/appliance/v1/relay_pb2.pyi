from mimick.appliance.v1 import common_pb2 as _common_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ChannelInfo(_message.Message):
    __slots__ = ("number", "name")
    NUMBER_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    number: int
    name: str
    def __init__(self, number: _Optional[int] = ..., name: _Optional[str] = ...) -> None: ...

class ChannelState(_message.Message):
    __slots__ = ("number", "enabled")
    NUMBER_FIELD_NUMBER: _ClassVar[int]
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    number: int
    enabled: bool
    def __init__(self, number: _Optional[int] = ..., enabled: _Optional[bool] = ...) -> None: ...

class RelayListChannelsRequest(_message.Message):
    __slots__ = ("handle",)
    HANDLE_FIELD_NUMBER: _ClassVar[int]
    handle: _common_pb2.PeripheralHandle
    def __init__(self, handle: _Optional[_Union[_common_pb2.PeripheralHandle, _Mapping]] = ...) -> None: ...

class RelayListChannelsResponse(_message.Message):
    __slots__ = ("status", "channels")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    CHANNELS_FIELD_NUMBER: _ClassVar[int]
    status: _common_pb2.Status
    channels: _containers.RepeatedCompositeFieldContainer[ChannelInfo]
    def __init__(self, status: _Optional[_Union[_common_pb2.Status, _Mapping]] = ..., channels: _Optional[_Iterable[_Union[ChannelInfo, _Mapping]]] = ...) -> None: ...

class RelayGetConfigRequest(_message.Message):
    __slots__ = ("handle", "channel_numbers")
    HANDLE_FIELD_NUMBER: _ClassVar[int]
    CHANNEL_NUMBERS_FIELD_NUMBER: _ClassVar[int]
    handle: _common_pb2.PeripheralHandle
    channel_numbers: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, handle: _Optional[_Union[_common_pb2.PeripheralHandle, _Mapping]] = ..., channel_numbers: _Optional[_Iterable[int]] = ...) -> None: ...

class RelayGetConfigResponse(_message.Message):
    __slots__ = ("status", "channels")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    CHANNELS_FIELD_NUMBER: _ClassVar[int]
    status: _common_pb2.Status
    channels: _containers.RepeatedCompositeFieldContainer[ChannelInfo]
    def __init__(self, status: _Optional[_Union[_common_pb2.Status, _Mapping]] = ..., channels: _Optional[_Iterable[_Union[ChannelInfo, _Mapping]]] = ...) -> None: ...

class RelaySetConfigRequest(_message.Message):
    __slots__ = ("handle", "channels")
    HANDLE_FIELD_NUMBER: _ClassVar[int]
    CHANNELS_FIELD_NUMBER: _ClassVar[int]
    handle: _common_pb2.PeripheralHandle
    channels: _containers.RepeatedCompositeFieldContainer[ChannelInfo]
    def __init__(self, handle: _Optional[_Union[_common_pb2.PeripheralHandle, _Mapping]] = ..., channels: _Optional[_Iterable[_Union[ChannelInfo, _Mapping]]] = ...) -> None: ...

class RelaySetConfigResponse(_message.Message):
    __slots__ = ("status", "channels")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    CHANNELS_FIELD_NUMBER: _ClassVar[int]
    status: _common_pb2.Status
    channels: _containers.RepeatedCompositeFieldContainer[ChannelInfo]
    def __init__(self, status: _Optional[_Union[_common_pb2.Status, _Mapping]] = ..., channels: _Optional[_Iterable[_Union[ChannelInfo, _Mapping]]] = ...) -> None: ...

class RelayReadChannelRequest(_message.Message):
    __slots__ = ("handle", "channel_number")
    HANDLE_FIELD_NUMBER: _ClassVar[int]
    CHANNEL_NUMBER_FIELD_NUMBER: _ClassVar[int]
    handle: _common_pb2.PeripheralHandle
    channel_number: int
    def __init__(self, handle: _Optional[_Union[_common_pb2.PeripheralHandle, _Mapping]] = ..., channel_number: _Optional[int] = ...) -> None: ...

class RelayReadChannelResponse(_message.Message):
    __slots__ = ("status", "state", "sampled_at")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    SAMPLED_AT_FIELD_NUMBER: _ClassVar[int]
    status: _common_pb2.Status
    state: ChannelState
    sampled_at: _common_pb2.Timestamp
    def __init__(self, status: _Optional[_Union[_common_pb2.Status, _Mapping]] = ..., state: _Optional[_Union[ChannelState, _Mapping]] = ..., sampled_at: _Optional[_Union[_common_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class RelayReadChannelsRequest(_message.Message):
    __slots__ = ("handle",)
    HANDLE_FIELD_NUMBER: _ClassVar[int]
    handle: _common_pb2.PeripheralHandle
    def __init__(self, handle: _Optional[_Union[_common_pb2.PeripheralHandle, _Mapping]] = ...) -> None: ...

class RelayReadChannelsResponse(_message.Message):
    __slots__ = ("status", "states", "sampled_at")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    STATES_FIELD_NUMBER: _ClassVar[int]
    SAMPLED_AT_FIELD_NUMBER: _ClassVar[int]
    status: _common_pb2.Status
    states: _containers.RepeatedCompositeFieldContainer[ChannelState]
    sampled_at: _common_pb2.Timestamp
    def __init__(self, status: _Optional[_Union[_common_pb2.Status, _Mapping]] = ..., states: _Optional[_Iterable[_Union[ChannelState, _Mapping]]] = ..., sampled_at: _Optional[_Union[_common_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class RelayWriteChannelRequest(_message.Message):
    __slots__ = ("handle", "state")
    HANDLE_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    handle: _common_pb2.PeripheralHandle
    state: ChannelState
    def __init__(self, handle: _Optional[_Union[_common_pb2.PeripheralHandle, _Mapping]] = ..., state: _Optional[_Union[ChannelState, _Mapping]] = ...) -> None: ...

class RelayWriteChannelResponse(_message.Message):
    __slots__ = ("status", "state")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    status: _common_pb2.Status
    state: ChannelState
    def __init__(self, status: _Optional[_Union[_common_pb2.Status, _Mapping]] = ..., state: _Optional[_Union[ChannelState, _Mapping]] = ...) -> None: ...

class RelayWriteChannelsRequest(_message.Message):
    __slots__ = ("handle", "states")
    HANDLE_FIELD_NUMBER: _ClassVar[int]
    STATES_FIELD_NUMBER: _ClassVar[int]
    handle: _common_pb2.PeripheralHandle
    states: _containers.RepeatedCompositeFieldContainer[ChannelState]
    def __init__(self, handle: _Optional[_Union[_common_pb2.PeripheralHandle, _Mapping]] = ..., states: _Optional[_Iterable[_Union[ChannelState, _Mapping]]] = ...) -> None: ...

class RelayWriteChannelsResponse(_message.Message):
    __slots__ = ("status", "states")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    STATES_FIELD_NUMBER: _ClassVar[int]
    status: _common_pb2.Status
    states: _containers.RepeatedCompositeFieldContainer[ChannelState]
    def __init__(self, status: _Optional[_Union[_common_pb2.Status, _Mapping]] = ..., states: _Optional[_Iterable[_Union[ChannelState, _Mapping]]] = ...) -> None: ...

class RelayWatchStreamRequest(_message.Message):
    __slots__ = ("handle",)
    HANDLE_FIELD_NUMBER: _ClassVar[int]
    handle: _common_pb2.PeripheralHandle
    def __init__(self, handle: _Optional[_Union[_common_pb2.PeripheralHandle, _Mapping]] = ...) -> None: ...

class RelayWatchStreamResponse(_message.Message):
    __slots__ = ("status", "states", "occurred_at")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    STATES_FIELD_NUMBER: _ClassVar[int]
    OCCURRED_AT_FIELD_NUMBER: _ClassVar[int]
    status: _common_pb2.Status
    states: _containers.RepeatedCompositeFieldContainer[ChannelState]
    occurred_at: _common_pb2.Timestamp
    def __init__(self, status: _Optional[_Union[_common_pb2.Status, _Mapping]] = ..., states: _Optional[_Iterable[_Union[ChannelState, _Mapping]]] = ..., occurred_at: _Optional[_Union[_common_pb2.Timestamp, _Mapping]] = ...) -> None: ...
