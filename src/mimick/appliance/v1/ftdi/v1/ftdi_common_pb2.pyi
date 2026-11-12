from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class FtdiInterface(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    FTDI_INTERFACE_UNSPECIFIED: _ClassVar[FtdiInterface]
    FTDI_INTERFACE_A: _ClassVar[FtdiInterface]
    FTDI_INTERFACE_B: _ClassVar[FtdiInterface]
    FTDI_INTERFACE_C: _ClassVar[FtdiInterface]
    FTDI_INTERFACE_D: _ClassVar[FtdiInterface]

class FtdiChipType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    FTDI_CHIP_TYPE_UNSPECIFIED: _ClassVar[FtdiChipType]
    FTDI_CHIP_TYPE_FT232H: _ClassVar[FtdiChipType]
    FTDI_CHIP_TYPE_FT2232H: _ClassVar[FtdiChipType]
    FTDI_CHIP_TYPE_FT4232H: _ClassVar[FtdiChipType]
    FTDI_CHIP_TYPE_FT232R: _ClassVar[FtdiChipType]
    FTDI_CHIP_TYPE_FT2232C: _ClassVar[FtdiChipType]
    FTDI_CHIP_TYPE_FT4232HA: _ClassVar[FtdiChipType]
    FTDI_CHIP_TYPE_FT233HP: _ClassVar[FtdiChipType]

class MpsseMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    MPSSE_MODE_UNSPECIFIED: _ClassVar[MpsseMode]
    MPSSE_MODE_SPI0: _ClassVar[MpsseMode]
    MPSSE_MODE_SPI1: _ClassVar[MpsseMode]
    MPSSE_MODE_SPI2: _ClassVar[MpsseMode]
    MPSSE_MODE_SPI3: _ClassVar[MpsseMode]
    MPSSE_MODE_I2C: _ClassVar[MpsseMode]
    MPSSE_MODE_GPIO: _ClassVar[MpsseMode]
    MPSSE_MODE_BITBANG: _ClassVar[MpsseMode]

class CbusFunction(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CBUS_FUNCTION_UNSPECIFIED: _ClassVar[CbusFunction]
    CBUS_FUNCTION_TRISTATE: _ClassVar[CbusFunction]
    CBUS_FUNCTION_GPIO: _ClassVar[CbusFunction]
    CBUS_FUNCTION_TXLED: _ClassVar[CbusFunction]
    CBUS_FUNCTION_RXLED: _ClassVar[CbusFunction]
    CBUS_FUNCTION_TXRXLED: _ClassVar[CbusFunction]
    CBUS_FUNCTION_PWREN: _ClassVar[CbusFunction]
    CBUS_FUNCTION_SLEEP: _ClassVar[CbusFunction]
    CBUS_FUNCTION_CLK48: _ClassVar[CbusFunction]
    CBUS_FUNCTION_CLK24: _ClassVar[CbusFunction]
    CBUS_FUNCTION_CLK12: _ClassVar[CbusFunction]
    CBUS_FUNCTION_CLK6: _ClassVar[CbusFunction]
    CBUS_FUNCTION_IOMODE: _ClassVar[CbusFunction]
    CBUS_FUNCTION_BB_WR: _ClassVar[CbusFunction]
    CBUS_FUNCTION_BB_RD: _ClassVar[CbusFunction]
FTDI_INTERFACE_UNSPECIFIED: FtdiInterface
FTDI_INTERFACE_A: FtdiInterface
FTDI_INTERFACE_B: FtdiInterface
FTDI_INTERFACE_C: FtdiInterface
FTDI_INTERFACE_D: FtdiInterface
FTDI_CHIP_TYPE_UNSPECIFIED: FtdiChipType
FTDI_CHIP_TYPE_FT232H: FtdiChipType
FTDI_CHIP_TYPE_FT2232H: FtdiChipType
FTDI_CHIP_TYPE_FT4232H: FtdiChipType
FTDI_CHIP_TYPE_FT232R: FtdiChipType
FTDI_CHIP_TYPE_FT2232C: FtdiChipType
FTDI_CHIP_TYPE_FT4232HA: FtdiChipType
FTDI_CHIP_TYPE_FT233HP: FtdiChipType
MPSSE_MODE_UNSPECIFIED: MpsseMode
MPSSE_MODE_SPI0: MpsseMode
MPSSE_MODE_SPI1: MpsseMode
MPSSE_MODE_SPI2: MpsseMode
MPSSE_MODE_SPI3: MpsseMode
MPSSE_MODE_I2C: MpsseMode
MPSSE_MODE_GPIO: MpsseMode
MPSSE_MODE_BITBANG: MpsseMode
CBUS_FUNCTION_UNSPECIFIED: CbusFunction
CBUS_FUNCTION_TRISTATE: CbusFunction
CBUS_FUNCTION_GPIO: CbusFunction
CBUS_FUNCTION_TXLED: CbusFunction
CBUS_FUNCTION_RXLED: CbusFunction
CBUS_FUNCTION_TXRXLED: CbusFunction
CBUS_FUNCTION_PWREN: CbusFunction
CBUS_FUNCTION_SLEEP: CbusFunction
CBUS_FUNCTION_CLK48: CbusFunction
CBUS_FUNCTION_CLK24: CbusFunction
CBUS_FUNCTION_CLK12: CbusFunction
CBUS_FUNCTION_CLK6: CbusFunction
CBUS_FUNCTION_IOMODE: CbusFunction
CBUS_FUNCTION_BB_WR: CbusFunction
CBUS_FUNCTION_BB_RD: CbusFunction

class FtdiChipInfo(_message.Message):
    __slots__ = ("chip_type", "revision", "temperature_mc", "serial", "description", "max_freq_hz", "supports_tcx5")
    CHIP_TYPE_FIELD_NUMBER: _ClassVar[int]
    REVISION_FIELD_NUMBER: _ClassVar[int]
    TEMPERATURE_MC_FIELD_NUMBER: _ClassVar[int]
    SERIAL_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    MAX_FREQ_HZ_FIELD_NUMBER: _ClassVar[int]
    SUPPORTS_TCX5_FIELD_NUMBER: _ClassVar[int]
    chip_type: FtdiChipType
    revision: int
    temperature_mc: int
    serial: str
    description: str
    max_freq_hz: int
    supports_tcx5: bool
    def __init__(self, chip_type: _Optional[_Union[FtdiChipType, str]] = ..., revision: _Optional[int] = ..., temperature_mc: _Optional[int] = ..., serial: _Optional[str] = ..., description: _Optional[str] = ..., max_freq_hz: _Optional[int] = ..., supports_tcx5: _Optional[bool] = ...) -> None: ...

class CbusPinConfig(_message.Message):
    __slots__ = ("pin", "function", "gpio_out")
    PIN_FIELD_NUMBER: _ClassVar[int]
    FUNCTION_FIELD_NUMBER: _ClassVar[int]
    GPIO_OUT_FIELD_NUMBER: _ClassVar[int]
    pin: int
    function: CbusFunction
    gpio_out: bool
    def __init__(self, pin: _Optional[int] = ..., function: _Optional[_Union[CbusFunction, str]] = ..., gpio_out: _Optional[bool] = ...) -> None: ...

class FtdiConfig(_message.Message):
    __slots__ = ("mode", "freq_hz", "latency_timer_ms", "loopback", "flush_after_read")
    MODE_FIELD_NUMBER: _ClassVar[int]
    FREQ_HZ_FIELD_NUMBER: _ClassVar[int]
    LATENCY_TIMER_MS_FIELD_NUMBER: _ClassVar[int]
    LOOPBACK_FIELD_NUMBER: _ClassVar[int]
    FLUSH_AFTER_READ_FIELD_NUMBER: _ClassVar[int]
    mode: MpsseMode
    freq_hz: int
    latency_timer_ms: int
    loopback: bool
    flush_after_read: bool
    def __init__(self, mode: _Optional[_Union[MpsseMode, str]] = ..., freq_hz: _Optional[int] = ..., latency_timer_ms: _Optional[int] = ..., loopback: _Optional[bool] = ..., flush_after_read: _Optional[bool] = ...) -> None: ...
