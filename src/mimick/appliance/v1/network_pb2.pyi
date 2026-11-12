import datetime

from mimick.appliance.v1 import common_pb2 as _common_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DhcpLeaseAction(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DHCP_LEASE_ACTION_UNSPECIFIED: _ClassVar[DhcpLeaseAction]
    DHCP_LEASE_ACTION_REBIND: _ClassVar[DhcpLeaseAction]
    DHCP_LEASE_ACTION_RENEW: _ClassVar[DhcpLeaseAction]

class WifiRateFamily(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    WIFI_RATE_FAMILY_UNSPECIFIED: _ClassVar[WifiRateFamily]
    WIFI_RATE_FAMILY_LEGACY: _ClassVar[WifiRateFamily]
    WIFI_RATE_FAMILY_HT: _ClassVar[WifiRateFamily]
    WIFI_RATE_FAMILY_VHT: _ClassVar[WifiRateFamily]
    WIFI_RATE_FAMILY_HE: _ClassVar[WifiRateFamily]

class WifiPowerSave(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    WIFI_POWER_SAVE_UNSPECIFIED: _ClassVar[WifiPowerSave]
    WIFI_POWER_SAVE_ON: _ClassVar[WifiPowerSave]
    WIFI_POWER_SAVE_OFF: _ClassVar[WifiPowerSave]
DHCP_LEASE_ACTION_UNSPECIFIED: DhcpLeaseAction
DHCP_LEASE_ACTION_REBIND: DhcpLeaseAction
DHCP_LEASE_ACTION_RENEW: DhcpLeaseAction
WIFI_RATE_FAMILY_UNSPECIFIED: WifiRateFamily
WIFI_RATE_FAMILY_LEGACY: WifiRateFamily
WIFI_RATE_FAMILY_HT: WifiRateFamily
WIFI_RATE_FAMILY_VHT: WifiRateFamily
WIFI_RATE_FAMILY_HE: WifiRateFamily
WIFI_POWER_SAVE_UNSPECIFIED: WifiPowerSave
WIFI_POWER_SAVE_ON: WifiPowerSave
WIFI_POWER_SAVE_OFF: WifiPowerSave

class GetNetworkStatusRequest(_message.Message):
    __slots__ = ("handle",)
    HANDLE_FIELD_NUMBER: _ClassVar[int]
    handle: _common_pb2.PeripheralHandle
    def __init__(self, handle: _Optional[_Union[_common_pb2.PeripheralHandle, _Mapping]] = ...) -> None: ...

class GetNetworkStatusResponse(_message.Message):
    __slots__ = ("status", "network")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    NETWORK_FIELD_NUMBER: _ClassVar[int]
    status: _common_pb2.Status
    network: NetworkInterfaceStatus
    def __init__(self, status: _Optional[_Union[_common_pb2.Status, _Mapping]] = ..., network: _Optional[_Union[NetworkInterfaceStatus, _Mapping]] = ...) -> None: ...

class NetworkInterfaceStatus(_message.Message):
    __slots__ = ("interface_name", "mac_address", "link_up", "mode", "ip_address", "subnet", "nat_masq_enabled", "leases", "gateway", "dns_servers", "route_table", "is_bridge", "bridge_members", "network_namespace")
    INTERFACE_NAME_FIELD_NUMBER: _ClassVar[int]
    MAC_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    LINK_UP_FIELD_NUMBER: _ClassVar[int]
    MODE_FIELD_NUMBER: _ClassVar[int]
    IP_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    SUBNET_FIELD_NUMBER: _ClassVar[int]
    NAT_MASQ_ENABLED_FIELD_NUMBER: _ClassVar[int]
    LEASES_FIELD_NUMBER: _ClassVar[int]
    GATEWAY_FIELD_NUMBER: _ClassVar[int]
    DNS_SERVERS_FIELD_NUMBER: _ClassVar[int]
    ROUTE_TABLE_FIELD_NUMBER: _ClassVar[int]
    IS_BRIDGE_FIELD_NUMBER: _ClassVar[int]
    BRIDGE_MEMBERS_FIELD_NUMBER: _ClassVar[int]
    NETWORK_NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    interface_name: str
    mac_address: str
    link_up: bool
    mode: str
    ip_address: str
    subnet: str
    nat_masq_enabled: bool
    leases: _containers.RepeatedCompositeFieldContainer[DhcpLease]
    gateway: str
    dns_servers: _containers.RepeatedScalarFieldContainer[str]
    route_table: int
    is_bridge: bool
    bridge_members: _containers.RepeatedScalarFieldContainer[str]
    network_namespace: str
    def __init__(self, interface_name: _Optional[str] = ..., mac_address: _Optional[str] = ..., link_up: _Optional[bool] = ..., mode: _Optional[str] = ..., ip_address: _Optional[str] = ..., subnet: _Optional[str] = ..., nat_masq_enabled: _Optional[bool] = ..., leases: _Optional[_Iterable[_Union[DhcpLease, _Mapping]]] = ..., gateway: _Optional[str] = ..., dns_servers: _Optional[_Iterable[str]] = ..., route_table: _Optional[int] = ..., is_bridge: _Optional[bool] = ..., bridge_members: _Optional[_Iterable[str]] = ..., network_namespace: _Optional[str] = ...) -> None: ...

class DhcpLease(_message.Message):
    __slots__ = ("mac_address", "ip_address", "hostname", "expires_at")
    MAC_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    IP_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    HOSTNAME_FIELD_NUMBER: _ClassVar[int]
    EXPIRES_AT_FIELD_NUMBER: _ClassVar[int]
    mac_address: str
    ip_address: str
    hostname: str
    expires_at: _timestamp_pb2.Timestamp
    def __init__(self, mac_address: _Optional[str] = ..., ip_address: _Optional[str] = ..., hostname: _Optional[str] = ..., expires_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class RenewDhcpLeaseRequest(_message.Message):
    __slots__ = ("handle", "action", "timeout_ms")
    HANDLE_FIELD_NUMBER: _ClassVar[int]
    ACTION_FIELD_NUMBER: _ClassVar[int]
    TIMEOUT_MS_FIELD_NUMBER: _ClassVar[int]
    handle: _common_pb2.PeripheralHandle
    action: DhcpLeaseAction
    timeout_ms: int
    def __init__(self, handle: _Optional[_Union[_common_pb2.PeripheralHandle, _Mapping]] = ..., action: _Optional[_Union[DhcpLeaseAction, str]] = ..., timeout_ms: _Optional[int] = ...) -> None: ...

class RenewDhcpLeaseResponse(_message.Message):
    __slots__ = ("status", "network", "previous_ip_address")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    NETWORK_FIELD_NUMBER: _ClassVar[int]
    PREVIOUS_IP_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    status: _common_pb2.Status
    network: NetworkInterfaceStatus
    previous_ip_address: str
    def __init__(self, status: _Optional[_Union[_common_pb2.Status, _Mapping]] = ..., network: _Optional[_Union[NetworkInterfaceStatus, _Mapping]] = ..., previous_ip_address: _Optional[str] = ...) -> None: ...

class WifiScanRequest(_message.Message):
    __slots__ = ("handle", "timeout_ms")
    HANDLE_FIELD_NUMBER: _ClassVar[int]
    TIMEOUT_MS_FIELD_NUMBER: _ClassVar[int]
    handle: _common_pb2.PeripheralHandle
    timeout_ms: int
    def __init__(self, handle: _Optional[_Union[_common_pb2.PeripheralHandle, _Mapping]] = ..., timeout_ms: _Optional[int] = ...) -> None: ...

class WifiScanResponse(_message.Message):
    __slots__ = ("status", "results")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    RESULTS_FIELD_NUMBER: _ClassVar[int]
    status: _common_pb2.Status
    results: _containers.RepeatedCompositeFieldContainer[WifiScanResult]
    def __init__(self, status: _Optional[_Union[_common_pb2.Status, _Mapping]] = ..., results: _Optional[_Iterable[_Union[WifiScanResult, _Mapping]]] = ...) -> None: ...

class WifiScanResult(_message.Message):
    __slots__ = ("bssid", "ssid", "frequency_mhz", "channel", "signal_dbm", "security", "key_mgmt", "pairwise_ciphers")
    BSSID_FIELD_NUMBER: _ClassVar[int]
    SSID_FIELD_NUMBER: _ClassVar[int]
    FREQUENCY_MHZ_FIELD_NUMBER: _ClassVar[int]
    CHANNEL_FIELD_NUMBER: _ClassVar[int]
    SIGNAL_DBM_FIELD_NUMBER: _ClassVar[int]
    SECURITY_FIELD_NUMBER: _ClassVar[int]
    KEY_MGMT_FIELD_NUMBER: _ClassVar[int]
    PAIRWISE_CIPHERS_FIELD_NUMBER: _ClassVar[int]
    bssid: str
    ssid: str
    frequency_mhz: int
    channel: int
    signal_dbm: float
    security: str
    key_mgmt: _containers.RepeatedScalarFieldContainer[str]
    pairwise_ciphers: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, bssid: _Optional[str] = ..., ssid: _Optional[str] = ..., frequency_mhz: _Optional[int] = ..., channel: _Optional[int] = ..., signal_dbm: _Optional[float] = ..., security: _Optional[str] = ..., key_mgmt: _Optional[_Iterable[str]] = ..., pairwise_ciphers: _Optional[_Iterable[str]] = ...) -> None: ...

class WifiConnectRequest(_message.Message):
    __slots__ = ("handle", "ssid", "psk", "timeout_ms")
    HANDLE_FIELD_NUMBER: _ClassVar[int]
    SSID_FIELD_NUMBER: _ClassVar[int]
    PSK_FIELD_NUMBER: _ClassVar[int]
    TIMEOUT_MS_FIELD_NUMBER: _ClassVar[int]
    handle: _common_pb2.PeripheralHandle
    ssid: str
    psk: str
    timeout_ms: int
    def __init__(self, handle: _Optional[_Union[_common_pb2.PeripheralHandle, _Mapping]] = ..., ssid: _Optional[str] = ..., psk: _Optional[str] = ..., timeout_ms: _Optional[int] = ...) -> None: ...

class WifiConnectResponse(_message.Message):
    __slots__ = ("status", "network", "bssid", "signal_dbm")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    NETWORK_FIELD_NUMBER: _ClassVar[int]
    BSSID_FIELD_NUMBER: _ClassVar[int]
    SIGNAL_DBM_FIELD_NUMBER: _ClassVar[int]
    status: _common_pb2.Status
    network: NetworkInterfaceStatus
    bssid: str
    signal_dbm: float
    def __init__(self, status: _Optional[_Union[_common_pb2.Status, _Mapping]] = ..., network: _Optional[_Union[NetworkInterfaceStatus, _Mapping]] = ..., bssid: _Optional[str] = ..., signal_dbm: _Optional[float] = ...) -> None: ...

class WifiDisconnectRequest(_message.Message):
    __slots__ = ("handle",)
    HANDLE_FIELD_NUMBER: _ClassVar[int]
    handle: _common_pb2.PeripheralHandle
    def __init__(self, handle: _Optional[_Union[_common_pb2.PeripheralHandle, _Mapping]] = ...) -> None: ...

class WifiDisconnectResponse(_message.Message):
    __slots__ = ("status", "was_connected")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    WAS_CONNECTED_FIELD_NUMBER: _ClassVar[int]
    status: _common_pb2.Status
    was_connected: bool
    def __init__(self, status: _Optional[_Union[_common_pb2.Status, _Mapping]] = ..., was_connected: _Optional[bool] = ...) -> None: ...

class GetWifiLinkStatsRequest(_message.Message):
    __slots__ = ("handle",)
    HANDLE_FIELD_NUMBER: _ClassVar[int]
    handle: _common_pb2.PeripheralHandle
    def __init__(self, handle: _Optional[_Union[_common_pb2.PeripheralHandle, _Mapping]] = ...) -> None: ...

class GetWifiLinkStatsResponse(_message.Message):
    __slots__ = ("status", "connected", "stats")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    CONNECTED_FIELD_NUMBER: _ClassVar[int]
    STATS_FIELD_NUMBER: _ClassVar[int]
    status: _common_pb2.Status
    connected: bool
    stats: WifiLinkStats
    def __init__(self, status: _Optional[_Union[_common_pb2.Status, _Mapping]] = ..., connected: _Optional[bool] = ..., stats: _Optional[_Union[WifiLinkStats, _Mapping]] = ...) -> None: ...

class WifiRate(_message.Message):
    __slots__ = ("mbps", "family", "mcs_index", "nss", "bandwidth_mhz", "guard_interval_ns")
    MBPS_FIELD_NUMBER: _ClassVar[int]
    FAMILY_FIELD_NUMBER: _ClassVar[int]
    MCS_INDEX_FIELD_NUMBER: _ClassVar[int]
    NSS_FIELD_NUMBER: _ClassVar[int]
    BANDWIDTH_MHZ_FIELD_NUMBER: _ClassVar[int]
    GUARD_INTERVAL_NS_FIELD_NUMBER: _ClassVar[int]
    mbps: float
    family: WifiRateFamily
    mcs_index: int
    nss: int
    bandwidth_mhz: int
    guard_interval_ns: int
    def __init__(self, mbps: _Optional[float] = ..., family: _Optional[_Union[WifiRateFamily, str]] = ..., mcs_index: _Optional[int] = ..., nss: _Optional[int] = ..., bandwidth_mhz: _Optional[int] = ..., guard_interval_ns: _Optional[int] = ...) -> None: ...

class WifiLinkStats(_message.Message):
    __slots__ = ("ssid", "bssid", "frequency_mhz", "signal_dbm", "signal_dbm_per_chain", "tx_rate", "rx_rate", "tx_retries", "tx_failed", "rx_drop_misc", "tx_bytes", "rx_bytes", "tx_packets", "rx_packets", "connected_time_seconds", "power_save")
    SSID_FIELD_NUMBER: _ClassVar[int]
    BSSID_FIELD_NUMBER: _ClassVar[int]
    FREQUENCY_MHZ_FIELD_NUMBER: _ClassVar[int]
    SIGNAL_DBM_FIELD_NUMBER: _ClassVar[int]
    SIGNAL_DBM_PER_CHAIN_FIELD_NUMBER: _ClassVar[int]
    TX_RATE_FIELD_NUMBER: _ClassVar[int]
    RX_RATE_FIELD_NUMBER: _ClassVar[int]
    TX_RETRIES_FIELD_NUMBER: _ClassVar[int]
    TX_FAILED_FIELD_NUMBER: _ClassVar[int]
    RX_DROP_MISC_FIELD_NUMBER: _ClassVar[int]
    TX_BYTES_FIELD_NUMBER: _ClassVar[int]
    RX_BYTES_FIELD_NUMBER: _ClassVar[int]
    TX_PACKETS_FIELD_NUMBER: _ClassVar[int]
    RX_PACKETS_FIELD_NUMBER: _ClassVar[int]
    CONNECTED_TIME_SECONDS_FIELD_NUMBER: _ClassVar[int]
    POWER_SAVE_FIELD_NUMBER: _ClassVar[int]
    ssid: str
    bssid: str
    frequency_mhz: int
    signal_dbm: float
    signal_dbm_per_chain: _containers.RepeatedScalarFieldContainer[float]
    tx_rate: WifiRate
    rx_rate: WifiRate
    tx_retries: int
    tx_failed: int
    rx_drop_misc: int
    tx_bytes: int
    rx_bytes: int
    tx_packets: int
    rx_packets: int
    connected_time_seconds: int
    power_save: WifiPowerSave
    def __init__(self, ssid: _Optional[str] = ..., bssid: _Optional[str] = ..., frequency_mhz: _Optional[int] = ..., signal_dbm: _Optional[float] = ..., signal_dbm_per_chain: _Optional[_Iterable[float]] = ..., tx_rate: _Optional[_Union[WifiRate, _Mapping]] = ..., rx_rate: _Optional[_Union[WifiRate, _Mapping]] = ..., tx_retries: _Optional[int] = ..., tx_failed: _Optional[int] = ..., rx_drop_misc: _Optional[int] = ..., tx_bytes: _Optional[int] = ..., rx_bytes: _Optional[int] = ..., tx_packets: _Optional[int] = ..., rx_packets: _Optional[int] = ..., connected_time_seconds: _Optional[int] = ..., power_save: _Optional[_Union[WifiPowerSave, str]] = ...) -> None: ...
