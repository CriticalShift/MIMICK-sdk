from mimick.appliance.v1 import common_pb2 as _common_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class UartParity(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UART_PARITY_UNSPECIFIED: _ClassVar[UartParity]
    UART_PARITY_NONE: _ClassVar[UartParity]
    UART_PARITY_EVEN: _ClassVar[UartParity]
    UART_PARITY_ODD: _ClassVar[UartParity]

class UartStopBits(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UART_STOP_BITS_UNSPECIFIED: _ClassVar[UartStopBits]
    UART_STOP_BITS_ONE: _ClassVar[UartStopBits]
    UART_STOP_BITS_ONE_POINT_FIVE: _ClassVar[UartStopBits]
    UART_STOP_BITS_TWO: _ClassVar[UartStopBits]

class UartFlowControl(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UART_FLOW_CONTROL_UNSPECIFIED: _ClassVar[UartFlowControl]
    UART_FLOW_CONTROL_NONE: _ClassVar[UartFlowControl]
    UART_FLOW_CONTROL_HARDWARE: _ClassVar[UartFlowControl]
    UART_FLOW_CONTROL_SOFTWARE: _ClassVar[UartFlowControl]
UART_PARITY_UNSPECIFIED: UartParity
UART_PARITY_NONE: UartParity
UART_PARITY_EVEN: UartParity
UART_PARITY_ODD: UartParity
UART_STOP_BITS_UNSPECIFIED: UartStopBits
UART_STOP_BITS_ONE: UartStopBits
UART_STOP_BITS_ONE_POINT_FIVE: UartStopBits
UART_STOP_BITS_TWO: UartStopBits
UART_FLOW_CONTROL_UNSPECIFIED: UartFlowControl
UART_FLOW_CONTROL_NONE: UartFlowControl
UART_FLOW_CONTROL_HARDWARE: UartFlowControl
UART_FLOW_CONTROL_SOFTWARE: UartFlowControl

class UartConfig(_message.Message):
    __slots__ = ("baud_rate", "data_bits", "parity", "stop_bits", "flow_control")
    BAUD_RATE_FIELD_NUMBER: _ClassVar[int]
    DATA_BITS_FIELD_NUMBER: _ClassVar[int]
    PARITY_FIELD_NUMBER: _ClassVar[int]
    STOP_BITS_FIELD_NUMBER: _ClassVar[int]
    FLOW_CONTROL_FIELD_NUMBER: _ClassVar[int]
    baud_rate: int
    data_bits: int
    parity: UartParity
    stop_bits: UartStopBits
    flow_control: UartFlowControl
    def __init__(self, baud_rate: _Optional[int] = ..., data_bits: _Optional[int] = ..., parity: _Optional[_Union[UartParity, str]] = ..., stop_bits: _Optional[_Union[UartStopBits, str]] = ..., flow_control: _Optional[_Union[UartFlowControl, str]] = ...) -> None: ...

class UartGetConfigRequest(_message.Message):
    __slots__ = ("handle",)
    HANDLE_FIELD_NUMBER: _ClassVar[int]
    handle: _common_pb2.PeripheralHandle
    def __init__(self, handle: _Optional[_Union[_common_pb2.PeripheralHandle, _Mapping]] = ...) -> None: ...

class UartGetConfigResponse(_message.Message):
    __slots__ = ("status", "config")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    status: _common_pb2.Status
    config: UartConfig
    def __init__(self, status: _Optional[_Union[_common_pb2.Status, _Mapping]] = ..., config: _Optional[_Union[UartConfig, _Mapping]] = ...) -> None: ...

class UartSetConfigRequest(_message.Message):
    __slots__ = ("handle", "config", "update_fields")
    HANDLE_FIELD_NUMBER: _ClassVar[int]
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    UPDATE_FIELDS_FIELD_NUMBER: _ClassVar[int]
    handle: _common_pb2.PeripheralHandle
    config: UartConfig
    update_fields: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, handle: _Optional[_Union[_common_pb2.PeripheralHandle, _Mapping]] = ..., config: _Optional[_Union[UartConfig, _Mapping]] = ..., update_fields: _Optional[_Iterable[str]] = ...) -> None: ...

class UartSetConfigResponse(_message.Message):
    __slots__ = ("status", "config")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    status: _common_pb2.Status
    config: UartConfig
    def __init__(self, status: _Optional[_Union[_common_pb2.Status, _Mapping]] = ..., config: _Optional[_Union[UartConfig, _Mapping]] = ...) -> None: ...

class UartSendRequest(_message.Message):
    __slots__ = ("handle", "data")
    HANDLE_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    handle: _common_pb2.PeripheralHandle
    data: bytes
    def __init__(self, handle: _Optional[_Union[_common_pb2.PeripheralHandle, _Mapping]] = ..., data: _Optional[bytes] = ...) -> None: ...

class UartSendResponse(_message.Message):
    __slots__ = ("status", "bytes_written")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    BYTES_WRITTEN_FIELD_NUMBER: _ClassVar[int]
    status: _common_pb2.Status
    bytes_written: int
    def __init__(self, status: _Optional[_Union[_common_pb2.Status, _Mapping]] = ..., bytes_written: _Optional[int] = ...) -> None: ...

class UartRecvRequest(_message.Message):
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

class UartRecvResponse(_message.Message):
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

class UartExecRequest(_message.Message):
    __slots__ = ("handle", "command", "append_terminator", "expect_pattern", "timeout_ms")
    HANDLE_FIELD_NUMBER: _ClassVar[int]
    COMMAND_FIELD_NUMBER: _ClassVar[int]
    APPEND_TERMINATOR_FIELD_NUMBER: _ClassVar[int]
    EXPECT_PATTERN_FIELD_NUMBER: _ClassVar[int]
    TIMEOUT_MS_FIELD_NUMBER: _ClassVar[int]
    handle: _common_pb2.PeripheralHandle
    command: bytes
    append_terminator: bool
    expect_pattern: str
    timeout_ms: int
    def __init__(self, handle: _Optional[_Union[_common_pb2.PeripheralHandle, _Mapping]] = ..., command: _Optional[bytes] = ..., append_terminator: _Optional[bool] = ..., expect_pattern: _Optional[str] = ..., timeout_ms: _Optional[int] = ...) -> None: ...

class UartExecResponse(_message.Message):
    __slots__ = ("status", "output", "matched", "completed_at")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_FIELD_NUMBER: _ClassVar[int]
    MATCHED_FIELD_NUMBER: _ClassVar[int]
    COMPLETED_AT_FIELD_NUMBER: _ClassVar[int]
    status: _common_pb2.Status
    output: bytes
    matched: bool
    completed_at: _common_pb2.Timestamp
    def __init__(self, status: _Optional[_Union[_common_pb2.Status, _Mapping]] = ..., output: _Optional[bytes] = ..., matched: _Optional[bool] = ..., completed_at: _Optional[_Union[_common_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class UartReadStreamRequest(_message.Message):
    __slots__ = ("handle", "frame_size")
    HANDLE_FIELD_NUMBER: _ClassVar[int]
    FRAME_SIZE_FIELD_NUMBER: _ClassVar[int]
    handle: _common_pb2.PeripheralHandle
    frame_size: int
    def __init__(self, handle: _Optional[_Union[_common_pb2.PeripheralHandle, _Mapping]] = ..., frame_size: _Optional[int] = ...) -> None: ...

class UartReadFrame(_message.Message):
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

class UartModemLines(_message.Message):
    __slots__ = ("dtr", "rts", "cts", "dsr", "ri", "dcd")
    DTR_FIELD_NUMBER: _ClassVar[int]
    RTS_FIELD_NUMBER: _ClassVar[int]
    CTS_FIELD_NUMBER: _ClassVar[int]
    DSR_FIELD_NUMBER: _ClassVar[int]
    RI_FIELD_NUMBER: _ClassVar[int]
    DCD_FIELD_NUMBER: _ClassVar[int]
    dtr: bool
    rts: bool
    cts: bool
    dsr: bool
    ri: bool
    dcd: bool
    def __init__(self, dtr: _Optional[bool] = ..., rts: _Optional[bool] = ..., cts: _Optional[bool] = ..., dsr: _Optional[bool] = ..., ri: _Optional[bool] = ..., dcd: _Optional[bool] = ...) -> None: ...

class UartLineStep(_message.Message):
    __slots__ = ("dtr", "rts", "hold_ms")
    DTR_FIELD_NUMBER: _ClassVar[int]
    RTS_FIELD_NUMBER: _ClassVar[int]
    HOLD_MS_FIELD_NUMBER: _ClassVar[int]
    dtr: bool
    rts: bool
    hold_ms: int
    def __init__(self, dtr: _Optional[bool] = ..., rts: _Optional[bool] = ..., hold_ms: _Optional[int] = ...) -> None: ...

class UartSetModemLinesRequest(_message.Message):
    __slots__ = ("handle", "lines", "steps")
    HANDLE_FIELD_NUMBER: _ClassVar[int]
    LINES_FIELD_NUMBER: _ClassVar[int]
    STEPS_FIELD_NUMBER: _ClassVar[int]
    handle: _common_pb2.PeripheralHandle
    lines: UartModemLines
    steps: _containers.RepeatedCompositeFieldContainer[UartLineStep]
    def __init__(self, handle: _Optional[_Union[_common_pb2.PeripheralHandle, _Mapping]] = ..., lines: _Optional[_Union[UartModemLines, _Mapping]] = ..., steps: _Optional[_Iterable[_Union[UartLineStep, _Mapping]]] = ...) -> None: ...

class UartSetModemLinesResponse(_message.Message):
    __slots__ = ("status", "lines")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    LINES_FIELD_NUMBER: _ClassVar[int]
    status: _common_pb2.Status
    lines: UartModemLines
    def __init__(self, status: _Optional[_Union[_common_pb2.Status, _Mapping]] = ..., lines: _Optional[_Union[UartModemLines, _Mapping]] = ...) -> None: ...

class UartGetModemLinesRequest(_message.Message):
    __slots__ = ("handle",)
    HANDLE_FIELD_NUMBER: _ClassVar[int]
    handle: _common_pb2.PeripheralHandle
    def __init__(self, handle: _Optional[_Union[_common_pb2.PeripheralHandle, _Mapping]] = ...) -> None: ...

class UartGetModemLinesResponse(_message.Message):
    __slots__ = ("status", "lines")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    LINES_FIELD_NUMBER: _ClassVar[int]
    status: _common_pb2.Status
    lines: UartModemLines
    def __init__(self, status: _Optional[_Union[_common_pb2.Status, _Mapping]] = ..., lines: _Optional[_Union[UartModemLines, _Mapping]] = ...) -> None: ...

class UartSendBreakRequest(_message.Message):
    __slots__ = ("handle", "duration_ms")
    HANDLE_FIELD_NUMBER: _ClassVar[int]
    DURATION_MS_FIELD_NUMBER: _ClassVar[int]
    handle: _common_pb2.PeripheralHandle
    duration_ms: int
    def __init__(self, handle: _Optional[_Union[_common_pb2.PeripheralHandle, _Mapping]] = ..., duration_ms: _Optional[int] = ...) -> None: ...

class UartSendBreakResponse(_message.Message):
    __slots__ = ("status",)
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: _common_pb2.Status
    def __init__(self, status: _Optional[_Union[_common_pb2.Status, _Mapping]] = ...) -> None: ...

class UartStreamOpen(_message.Message):
    __slots__ = ("handle", "config", "lines")
    HANDLE_FIELD_NUMBER: _ClassVar[int]
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    LINES_FIELD_NUMBER: _ClassVar[int]
    handle: _common_pb2.PeripheralHandle
    config: UartConfig
    lines: UartModemLines
    def __init__(self, handle: _Optional[_Union[_common_pb2.PeripheralHandle, _Mapping]] = ..., config: _Optional[_Union[UartConfig, _Mapping]] = ..., lines: _Optional[_Union[UartModemLines, _Mapping]] = ...) -> None: ...

class UartStreamClientMessage(_message.Message):
    __slots__ = ("open", "data", "set_config", "set_lines", "break_ms", "purge_rx")
    OPEN_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    SET_CONFIG_FIELD_NUMBER: _ClassVar[int]
    SET_LINES_FIELD_NUMBER: _ClassVar[int]
    BREAK_MS_FIELD_NUMBER: _ClassVar[int]
    PURGE_RX_FIELD_NUMBER: _ClassVar[int]
    open: UartStreamOpen
    data: bytes
    set_config: UartConfig
    set_lines: UartSetModemLinesRequest
    break_ms: int
    purge_rx: bool
    def __init__(self, open: _Optional[_Union[UartStreamOpen, _Mapping]] = ..., data: _Optional[bytes] = ..., set_config: _Optional[_Union[UartConfig, _Mapping]] = ..., set_lines: _Optional[_Union[UartSetModemLinesRequest, _Mapping]] = ..., break_ms: _Optional[int] = ..., purge_rx: _Optional[bool] = ...) -> None: ...

class UartStreamServerMessage(_message.Message):
    __slots__ = ("data", "config", "modem", "error")
    DATA_FIELD_NUMBER: _ClassVar[int]
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    MODEM_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    data: bytes
    config: UartConfig
    modem: UartModemLines
    error: _common_pb2.Status
    def __init__(self, data: _Optional[bytes] = ..., config: _Optional[_Union[UartConfig, _Mapping]] = ..., modem: _Optional[_Union[UartModemLines, _Mapping]] = ..., error: _Optional[_Union[_common_pb2.Status, _Mapping]] = ...) -> None: ...
