from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TransportType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    TRANSPORT_TYPE_UNSPECIFIED: _ClassVar[TransportType]
    TRANSPORT_TYPE_USB: _ClassVar[TransportType]
    TRANSPORT_TYPE_PLATFORM: _ClassVar[TransportType]
    TRANSPORT_TYPE_NETWORK: _ClassVar[TransportType]
    TRANSPORT_TYPE_PCI: _ClassVar[TransportType]
    TRANSPORT_TYPE_UART: _ClassVar[TransportType]

class ProtocolType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PROTOCOL_TYPE_UNSPECIFIED: _ClassVar[ProtocolType]
    PROTOCOL_TYPE_SPI: _ClassVar[ProtocolType]
    PROTOCOL_TYPE_I2C: _ClassVar[ProtocolType]
    PROTOCOL_TYPE_GPIO: _ClassVar[ProtocolType]
    PROTOCOL_TYPE_UART: _ClassVar[ProtocolType]
    PROTOCOL_TYPE_CAN: _ClassVar[ProtocolType]
    PROTOCOL_TYPE_ETHERNET: _ClassVar[ProtocolType]
    PROTOCOL_TYPE_JTAG: _ClassVar[ProtocolType]
    PROTOCOL_TYPE_1WIRE: _ClassVar[ProtocolType]
    PROTOCOL_TYPE_TTY: _ClassVar[ProtocolType]
    PROTOCOL_TYPE_REST: _ClassVar[ProtocolType]
    PROTOCOL_TYPE_CHARDEV: _ClassVar[ProtocolType]
    PROTOCOL_TYPE_RELAY: _ClassVar[ProtocolType]
    PROTOCOL_TYPE_STEPPER: _ClassVar[ProtocolType]
    PROTOCOL_TYPE_WIFI: _ClassVar[ProtocolType]
    PROTOCOL_TYPE_SOFTWARE: _ClassVar[ProtocolType]

class ErrorCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ERROR_CODE_UNSPECIFIED: _ClassVar[ErrorCode]
    ERROR_CODE_PERIPHERAL_NOT_FOUND: _ClassVar[ErrorCode]
    ERROR_CODE_PERIPHERAL_BUSY: _ClassVar[ErrorCode]
    ERROR_CODE_INVALID_HANDLE: _ClassVar[ErrorCode]
    ERROR_CODE_OPEN_FAILED: _ClassVar[ErrorCode]
    ERROR_CODE_INVALID_CLOCK: _ClassVar[ErrorCode]
    ERROR_CODE_INVALID_MODE: _ClassVar[ErrorCode]
    ERROR_CODE_INVALID_PIN: _ClassVar[ErrorCode]
    ERROR_CODE_INVALID_SIZE: _ClassVar[ErrorCode]
    ERROR_CODE_INVALID_CONFIG: _ClassVar[ErrorCode]
    ERROR_CODE_INTERFACE_NOT_SUPPORTED: _ClassVar[ErrorCode]
    ERROR_CODE_WRITE_FAILED: _ClassVar[ErrorCode]
    ERROR_CODE_READ_FAILED: _ClassVar[ErrorCode]
    ERROR_CODE_TRANSFER_FAILED: _ClassVar[ErrorCode]
    ERROR_CODE_NACK_RECEIVED: _ClassVar[ErrorCode]
    ERROR_CODE_BUS_ERROR: _ClassVar[ErrorCode]
    ERROR_CODE_MONITOR_OVERFLOW: _ClassVar[ErrorCode]
    ERROR_CODE_STREAM_CANCELLED: _ClassVar[ErrorCode]
    ERROR_CODE_DIAL_FAILED: _ClassVar[ErrorCode]
    ERROR_CODE_SSH_AUTH_FAILED: _ClassVar[ErrorCode]
    ERROR_CODE_SSH_HANDSHAKE_FAILED: _ClassVar[ErrorCode]
    ERROR_CODE_WIFI_NOT_STA: _ClassVar[ErrorCode]
    ERROR_CODE_WIFI_ASSOC_FAILED: _ClassVar[ErrorCode]
    ERROR_CODE_WIFI_SCAN_BUSY: _ClassVar[ErrorCode]
    ERROR_CODE_WIFI_NOT_ASSOCIATED: _ClassVar[ErrorCode]
    ERROR_CODE_DHCP_NOT_CLIENT: _ClassVar[ErrorCode]
    ERROR_CODE_DHCP_TIMEOUT: _ClassVar[ErrorCode]
    ERROR_CODE_DHCP_RENEW_FAILED: _ClassVar[ErrorCode]
    ERROR_CODE_NOT_IMPLEMENTED: _ClassVar[ErrorCode]
    ERROR_CODE_INTERNAL: _ClassVar[ErrorCode]

class BitOrder(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    BIT_ORDER_UNSPECIFIED: _ClassVar[BitOrder]
    BIT_ORDER_MSB_FIRST: _ClassVar[BitOrder]
    BIT_ORDER_LSB_FIRST: _ClassVar[BitOrder]

class ClockRate(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CLOCK_RATE_UNSPECIFIED: _ClassVar[ClockRate]
    CLOCK_RATE_100KHZ: _ClassVar[ClockRate]
    CLOCK_RATE_400KHZ: _ClassVar[ClockRate]
    CLOCK_RATE_1MHZ: _ClassVar[ClockRate]
    CLOCK_RATE_2MHZ: _ClassVar[ClockRate]
    CLOCK_RATE_5MHZ: _ClassVar[ClockRate]
    CLOCK_RATE_6MHZ: _ClassVar[ClockRate]
    CLOCK_RATE_10MHZ: _ClassVar[ClockRate]
    CLOCK_RATE_12MHZ: _ClassVar[ClockRate]
    CLOCK_RATE_15MHZ: _ClassVar[ClockRate]
    CLOCK_RATE_30MHZ: _ClassVar[ClockRate]
    CLOCK_RATE_60MHZ: _ClassVar[ClockRate]
TRANSPORT_TYPE_UNSPECIFIED: TransportType
TRANSPORT_TYPE_USB: TransportType
TRANSPORT_TYPE_PLATFORM: TransportType
TRANSPORT_TYPE_NETWORK: TransportType
TRANSPORT_TYPE_PCI: TransportType
TRANSPORT_TYPE_UART: TransportType
PROTOCOL_TYPE_UNSPECIFIED: ProtocolType
PROTOCOL_TYPE_SPI: ProtocolType
PROTOCOL_TYPE_I2C: ProtocolType
PROTOCOL_TYPE_GPIO: ProtocolType
PROTOCOL_TYPE_UART: ProtocolType
PROTOCOL_TYPE_CAN: ProtocolType
PROTOCOL_TYPE_ETHERNET: ProtocolType
PROTOCOL_TYPE_JTAG: ProtocolType
PROTOCOL_TYPE_1WIRE: ProtocolType
PROTOCOL_TYPE_TTY: ProtocolType
PROTOCOL_TYPE_REST: ProtocolType
PROTOCOL_TYPE_CHARDEV: ProtocolType
PROTOCOL_TYPE_RELAY: ProtocolType
PROTOCOL_TYPE_STEPPER: ProtocolType
PROTOCOL_TYPE_WIFI: ProtocolType
PROTOCOL_TYPE_SOFTWARE: ProtocolType
ERROR_CODE_UNSPECIFIED: ErrorCode
ERROR_CODE_PERIPHERAL_NOT_FOUND: ErrorCode
ERROR_CODE_PERIPHERAL_BUSY: ErrorCode
ERROR_CODE_INVALID_HANDLE: ErrorCode
ERROR_CODE_OPEN_FAILED: ErrorCode
ERROR_CODE_INVALID_CLOCK: ErrorCode
ERROR_CODE_INVALID_MODE: ErrorCode
ERROR_CODE_INVALID_PIN: ErrorCode
ERROR_CODE_INVALID_SIZE: ErrorCode
ERROR_CODE_INVALID_CONFIG: ErrorCode
ERROR_CODE_INTERFACE_NOT_SUPPORTED: ErrorCode
ERROR_CODE_WRITE_FAILED: ErrorCode
ERROR_CODE_READ_FAILED: ErrorCode
ERROR_CODE_TRANSFER_FAILED: ErrorCode
ERROR_CODE_NACK_RECEIVED: ErrorCode
ERROR_CODE_BUS_ERROR: ErrorCode
ERROR_CODE_MONITOR_OVERFLOW: ErrorCode
ERROR_CODE_STREAM_CANCELLED: ErrorCode
ERROR_CODE_DIAL_FAILED: ErrorCode
ERROR_CODE_SSH_AUTH_FAILED: ErrorCode
ERROR_CODE_SSH_HANDSHAKE_FAILED: ErrorCode
ERROR_CODE_WIFI_NOT_STA: ErrorCode
ERROR_CODE_WIFI_ASSOC_FAILED: ErrorCode
ERROR_CODE_WIFI_SCAN_BUSY: ErrorCode
ERROR_CODE_WIFI_NOT_ASSOCIATED: ErrorCode
ERROR_CODE_DHCP_NOT_CLIENT: ErrorCode
ERROR_CODE_DHCP_TIMEOUT: ErrorCode
ERROR_CODE_DHCP_RENEW_FAILED: ErrorCode
ERROR_CODE_NOT_IMPLEMENTED: ErrorCode
ERROR_CODE_INTERNAL: ErrorCode
BIT_ORDER_UNSPECIFIED: BitOrder
BIT_ORDER_MSB_FIRST: BitOrder
BIT_ORDER_LSB_FIRST: BitOrder
CLOCK_RATE_UNSPECIFIED: ClockRate
CLOCK_RATE_100KHZ: ClockRate
CLOCK_RATE_400KHZ: ClockRate
CLOCK_RATE_1MHZ: ClockRate
CLOCK_RATE_2MHZ: ClockRate
CLOCK_RATE_5MHZ: ClockRate
CLOCK_RATE_6MHZ: ClockRate
CLOCK_RATE_10MHZ: ClockRate
CLOCK_RATE_12MHZ: ClockRate
CLOCK_RATE_15MHZ: ClockRate
CLOCK_RATE_30MHZ: ClockRate
CLOCK_RATE_60MHZ: ClockRate

class UsbAddress(_message.Message):
    __slots__ = ("vid", "pid", "serial", "usb_path")
    VID_FIELD_NUMBER: _ClassVar[int]
    PID_FIELD_NUMBER: _ClassVar[int]
    SERIAL_FIELD_NUMBER: _ClassVar[int]
    USB_PATH_FIELD_NUMBER: _ClassVar[int]
    vid: int
    pid: int
    serial: str
    usb_path: str
    def __init__(self, vid: _Optional[int] = ..., pid: _Optional[int] = ..., serial: _Optional[str] = ..., usb_path: _Optional[str] = ...) -> None: ...

class PlatformAddress(_message.Message):
    __slots__ = ("device_path", "device_name")
    DEVICE_PATH_FIELD_NUMBER: _ClassVar[int]
    DEVICE_NAME_FIELD_NUMBER: _ClassVar[int]
    device_path: str
    device_name: str
    def __init__(self, device_path: _Optional[str] = ..., device_name: _Optional[str] = ...) -> None: ...

class NetworkAddress(_message.Message):
    __slots__ = ("host", "port")
    HOST_FIELD_NUMBER: _ClassVar[int]
    PORT_FIELD_NUMBER: _ClassVar[int]
    host: str
    port: int
    def __init__(self, host: _Optional[str] = ..., port: _Optional[int] = ...) -> None: ...

class PeripheralDescriptor(_message.Message):
    __slots__ = ("transport", "usb", "platform", "network")
    TRANSPORT_FIELD_NUMBER: _ClassVar[int]
    USB_FIELD_NUMBER: _ClassVar[int]
    PLATFORM_FIELD_NUMBER: _ClassVar[int]
    NETWORK_FIELD_NUMBER: _ClassVar[int]
    transport: TransportType
    usb: UsbAddress
    platform: PlatformAddress
    network: NetworkAddress
    def __init__(self, transport: _Optional[_Union[TransportType, str]] = ..., usb: _Optional[_Union[UsbAddress, _Mapping]] = ..., platform: _Optional[_Union[PlatformAddress, _Mapping]] = ..., network: _Optional[_Union[NetworkAddress, _Mapping]] = ...) -> None: ...

class PeripheralHandle(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class Interface(_message.Message):
    __slots__ = ("type", "channel", "max_freq_hz", "features", "backed_by", "config")
    class ConfigEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    TYPE_FIELD_NUMBER: _ClassVar[int]
    CHANNEL_FIELD_NUMBER: _ClassVar[int]
    MAX_FREQ_HZ_FIELD_NUMBER: _ClassVar[int]
    FEATURES_FIELD_NUMBER: _ClassVar[int]
    BACKED_BY_FIELD_NUMBER: _ClassVar[int]
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    type: ProtocolType
    channel: int
    max_freq_hz: int
    features: _containers.RepeatedScalarFieldContainer[str]
    backed_by: InterfaceRef
    config: _containers.ScalarMap[str, str]
    def __init__(self, type: _Optional[_Union[ProtocolType, str]] = ..., channel: _Optional[int] = ..., max_freq_hz: _Optional[int] = ..., features: _Optional[_Iterable[str]] = ..., backed_by: _Optional[_Union[InterfaceRef, _Mapping]] = ..., config: _Optional[_Mapping[str, str]] = ...) -> None: ...

class InterfaceRef(_message.Message):
    __slots__ = ("type", "channel")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    CHANNEL_FIELD_NUMBER: _ClassVar[int]
    type: ProtocolType
    channel: int
    def __init__(self, type: _Optional[_Union[ProtocolType, str]] = ..., channel: _Optional[int] = ...) -> None: ...

class InterfaceManifest(_message.Message):
    __slots__ = ("interfaces",)
    INTERFACES_FIELD_NUMBER: _ClassVar[int]
    interfaces: _containers.RepeatedCompositeFieldContainer[Interface]
    def __init__(self, interfaces: _Optional[_Iterable[_Union[Interface, _Mapping]]] = ...) -> None: ...

class Status(_message.Message):
    __slots__ = ("code", "message")
    CODE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    code: ErrorCode
    message: str
    def __init__(self, code: _Optional[_Union[ErrorCode, str]] = ..., message: _Optional[str] = ...) -> None: ...

class Timestamp(_message.Message):
    __slots__ = ("seconds", "nanos")
    SECONDS_FIELD_NUMBER: _ClassVar[int]
    NANOS_FIELD_NUMBER: _ClassVar[int]
    seconds: int
    nanos: int
    def __init__(self, seconds: _Optional[int] = ..., nanos: _Optional[int] = ...) -> None: ...
