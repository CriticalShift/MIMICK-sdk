from mimick.appliance.v1 import common_pb2 as _common_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class StepperDirection(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    STEPPER_DIRECTION_UNSPECIFIED: _ClassVar[StepperDirection]
    STEPPER_DIRECTION_RIGHT: _ClassVar[StepperDirection]
    STEPPER_DIRECTION_LEFT: _ClassVar[StepperDirection]

class StepperRefSearch(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    STEPPER_REF_SEARCH_UNSPECIFIED: _ClassVar[StepperRefSearch]
    STEPPER_REF_SEARCH_START: _ClassVar[StepperRefSearch]
    STEPPER_REF_SEARCH_STOP: _ClassVar[StepperRefSearch]
    STEPPER_REF_SEARCH_STATUS: _ClassVar[StepperRefSearch]
STEPPER_DIRECTION_UNSPECIFIED: StepperDirection
STEPPER_DIRECTION_RIGHT: StepperDirection
STEPPER_DIRECTION_LEFT: StepperDirection
STEPPER_REF_SEARCH_UNSPECIFIED: StepperRefSearch
STEPPER_REF_SEARCH_START: StepperRefSearch
STEPPER_REF_SEARCH_STOP: StepperRefSearch
STEPPER_REF_SEARCH_STATUS: StepperRefSearch

class StepperSetConfigRequest(_message.Message):
    __slots__ = ("handle", "max_velocity", "max_acceleration", "run_current", "standby_current", "microstep_resolution")
    HANDLE_FIELD_NUMBER: _ClassVar[int]
    MAX_VELOCITY_FIELD_NUMBER: _ClassVar[int]
    MAX_ACCELERATION_FIELD_NUMBER: _ClassVar[int]
    RUN_CURRENT_FIELD_NUMBER: _ClassVar[int]
    STANDBY_CURRENT_FIELD_NUMBER: _ClassVar[int]
    MICROSTEP_RESOLUTION_FIELD_NUMBER: _ClassVar[int]
    handle: _common_pb2.PeripheralHandle
    max_velocity: int
    max_acceleration: int
    run_current: int
    standby_current: int
    microstep_resolution: int
    def __init__(self, handle: _Optional[_Union[_common_pb2.PeripheralHandle, _Mapping]] = ..., max_velocity: _Optional[int] = ..., max_acceleration: _Optional[int] = ..., run_current: _Optional[int] = ..., standby_current: _Optional[int] = ..., microstep_resolution: _Optional[int] = ...) -> None: ...

class StepperSetConfigResponse(_message.Message):
    __slots__ = ("status",)
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: _common_pb2.Status
    def __init__(self, status: _Optional[_Union[_common_pb2.Status, _Mapping]] = ...) -> None: ...

class StepperGetConfigRequest(_message.Message):
    __slots__ = ("handle",)
    HANDLE_FIELD_NUMBER: _ClassVar[int]
    handle: _common_pb2.PeripheralHandle
    def __init__(self, handle: _Optional[_Union[_common_pb2.PeripheralHandle, _Mapping]] = ...) -> None: ...

class StepperGetConfigResponse(_message.Message):
    __slots__ = ("status", "max_velocity", "max_acceleration", "run_current", "standby_current", "microstep_resolution", "steps_per_rev")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    MAX_VELOCITY_FIELD_NUMBER: _ClassVar[int]
    MAX_ACCELERATION_FIELD_NUMBER: _ClassVar[int]
    RUN_CURRENT_FIELD_NUMBER: _ClassVar[int]
    STANDBY_CURRENT_FIELD_NUMBER: _ClassVar[int]
    MICROSTEP_RESOLUTION_FIELD_NUMBER: _ClassVar[int]
    STEPS_PER_REV_FIELD_NUMBER: _ClassVar[int]
    status: _common_pb2.Status
    max_velocity: int
    max_acceleration: int
    run_current: int
    standby_current: int
    microstep_resolution: int
    steps_per_rev: int
    def __init__(self, status: _Optional[_Union[_common_pb2.Status, _Mapping]] = ..., max_velocity: _Optional[int] = ..., max_acceleration: _Optional[int] = ..., run_current: _Optional[int] = ..., standby_current: _Optional[int] = ..., microstep_resolution: _Optional[int] = ..., steps_per_rev: _Optional[int] = ...) -> None: ...

class StepperRotateRequest(_message.Message):
    __slots__ = ("handle", "direction", "velocity")
    HANDLE_FIELD_NUMBER: _ClassVar[int]
    DIRECTION_FIELD_NUMBER: _ClassVar[int]
    VELOCITY_FIELD_NUMBER: _ClassVar[int]
    handle: _common_pb2.PeripheralHandle
    direction: StepperDirection
    velocity: int
    def __init__(self, handle: _Optional[_Union[_common_pb2.PeripheralHandle, _Mapping]] = ..., direction: _Optional[_Union[StepperDirection, str]] = ..., velocity: _Optional[int] = ...) -> None: ...

class StepperRotateResponse(_message.Message):
    __slots__ = ("status",)
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: _common_pb2.Status
    def __init__(self, status: _Optional[_Union[_common_pb2.Status, _Mapping]] = ...) -> None: ...

class StepperStopRequest(_message.Message):
    __slots__ = ("handle", "hard")
    HANDLE_FIELD_NUMBER: _ClassVar[int]
    HARD_FIELD_NUMBER: _ClassVar[int]
    handle: _common_pb2.PeripheralHandle
    hard: bool
    def __init__(self, handle: _Optional[_Union[_common_pb2.PeripheralHandle, _Mapping]] = ..., hard: _Optional[bool] = ...) -> None: ...

class StepperStopResponse(_message.Message):
    __slots__ = ("status",)
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: _common_pb2.Status
    def __init__(self, status: _Optional[_Union[_common_pb2.Status, _Mapping]] = ...) -> None: ...

class StepperMoveToRequest(_message.Message):
    __slots__ = ("handle", "position", "relative")
    HANDLE_FIELD_NUMBER: _ClassVar[int]
    POSITION_FIELD_NUMBER: _ClassVar[int]
    RELATIVE_FIELD_NUMBER: _ClassVar[int]
    handle: _common_pb2.PeripheralHandle
    position: int
    relative: bool
    def __init__(self, handle: _Optional[_Union[_common_pb2.PeripheralHandle, _Mapping]] = ..., position: _Optional[int] = ..., relative: _Optional[bool] = ...) -> None: ...

class StepperMoveToResponse(_message.Message):
    __slots__ = ("status", "target_position")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    TARGET_POSITION_FIELD_NUMBER: _ClassVar[int]
    status: _common_pb2.Status
    target_position: int
    def __init__(self, status: _Optional[_Union[_common_pb2.Status, _Mapping]] = ..., target_position: _Optional[int] = ...) -> None: ...

class StepperSetActualPositionRequest(_message.Message):
    __slots__ = ("handle", "position")
    HANDLE_FIELD_NUMBER: _ClassVar[int]
    POSITION_FIELD_NUMBER: _ClassVar[int]
    handle: _common_pb2.PeripheralHandle
    position: int
    def __init__(self, handle: _Optional[_Union[_common_pb2.PeripheralHandle, _Mapping]] = ..., position: _Optional[int] = ...) -> None: ...

class StepperSetActualPositionResponse(_message.Message):
    __slots__ = ("status",)
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: _common_pb2.Status
    def __init__(self, status: _Optional[_Union[_common_pb2.Status, _Mapping]] = ...) -> None: ...

class StepperReferenceSearchRequest(_message.Message):
    __slots__ = ("handle", "command")
    HANDLE_FIELD_NUMBER: _ClassVar[int]
    COMMAND_FIELD_NUMBER: _ClassVar[int]
    handle: _common_pb2.PeripheralHandle
    command: StepperRefSearch
    def __init__(self, handle: _Optional[_Union[_common_pb2.PeripheralHandle, _Mapping]] = ..., command: _Optional[_Union[StepperRefSearch, str]] = ...) -> None: ...

class StepperReferenceSearchResponse(_message.Message):
    __slots__ = ("status", "in_progress")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    IN_PROGRESS_FIELD_NUMBER: _ClassVar[int]
    status: _common_pb2.Status
    in_progress: bool
    def __init__(self, status: _Optional[_Union[_common_pb2.Status, _Mapping]] = ..., in_progress: _Optional[bool] = ...) -> None: ...

class StepperGetStateRequest(_message.Message):
    __slots__ = ("handle",)
    HANDLE_FIELD_NUMBER: _ClassVar[int]
    handle: _common_pb2.PeripheralHandle
    def __init__(self, handle: _Optional[_Union[_common_pb2.PeripheralHandle, _Mapping]] = ...) -> None: ...

class StepperGetStateResponse(_message.Message):
    __slots__ = ("status", "actual_position", "target_position", "actual_velocity", "moving", "target_reached", "stalled")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    ACTUAL_POSITION_FIELD_NUMBER: _ClassVar[int]
    TARGET_POSITION_FIELD_NUMBER: _ClassVar[int]
    ACTUAL_VELOCITY_FIELD_NUMBER: _ClassVar[int]
    MOVING_FIELD_NUMBER: _ClassVar[int]
    TARGET_REACHED_FIELD_NUMBER: _ClassVar[int]
    STALLED_FIELD_NUMBER: _ClassVar[int]
    status: _common_pb2.Status
    actual_position: int
    target_position: int
    actual_velocity: int
    moving: bool
    target_reached: bool
    stalled: bool
    def __init__(self, status: _Optional[_Union[_common_pb2.Status, _Mapping]] = ..., actual_position: _Optional[int] = ..., target_position: _Optional[int] = ..., actual_velocity: _Optional[int] = ..., moving: _Optional[bool] = ..., target_reached: _Optional[bool] = ..., stalled: _Optional[bool] = ...) -> None: ...

class StepperSendCommandRequest(_message.Message):
    __slots__ = ("handle", "opcode", "type", "motor_or_bank", "value")
    HANDLE_FIELD_NUMBER: _ClassVar[int]
    OPCODE_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    MOTOR_OR_BANK_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    handle: _common_pb2.PeripheralHandle
    opcode: int
    type: int
    motor_or_bank: int
    value: int
    def __init__(self, handle: _Optional[_Union[_common_pb2.PeripheralHandle, _Mapping]] = ..., opcode: _Optional[int] = ..., type: _Optional[int] = ..., motor_or_bank: _Optional[int] = ..., value: _Optional[int] = ...) -> None: ...

class StepperSendCommandResponse(_message.Message):
    __slots__ = ("status", "device_status", "value")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    DEVICE_STATUS_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    status: _common_pb2.Status
    device_status: int
    value: int
    def __init__(self, status: _Optional[_Union[_common_pb2.Status, _Mapping]] = ..., device_status: _Optional[int] = ..., value: _Optional[int] = ...) -> None: ...
