from mimick.appliance.v1 import common_pb2 as _common_pb2
from mimick.appliance.v1 import tty_pb2 as _tty_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SshSessionHandle(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class SshPrivateKey(_message.Message):
    __slots__ = ("pem", "passphrase")
    PEM_FIELD_NUMBER: _ClassVar[int]
    PASSPHRASE_FIELD_NUMBER: _ClassVar[int]
    pem: bytes
    passphrase: str
    def __init__(self, pem: _Optional[bytes] = ..., passphrase: _Optional[str] = ...) -> None: ...

class OpenSshSessionRequest(_message.Message):
    __slots__ = ("host", "port", "username", "password", "private_key", "requested_size", "via")
    HOST_FIELD_NUMBER: _ClassVar[int]
    PORT_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    PRIVATE_KEY_FIELD_NUMBER: _ClassVar[int]
    REQUESTED_SIZE_FIELD_NUMBER: _ClassVar[int]
    VIA_FIELD_NUMBER: _ClassVar[int]
    host: str
    port: int
    username: str
    password: str
    private_key: SshPrivateKey
    requested_size: _tty_pb2.TerminalSize
    via: _common_pb2.PeripheralHandle
    def __init__(self, host: _Optional[str] = ..., port: _Optional[int] = ..., username: _Optional[str] = ..., password: _Optional[str] = ..., private_key: _Optional[_Union[SshPrivateKey, _Mapping]] = ..., requested_size: _Optional[_Union[_tty_pb2.TerminalSize, _Mapping]] = ..., via: _Optional[_Union[_common_pb2.PeripheralHandle, _Mapping]] = ...) -> None: ...

class OpenSshSessionResponse(_message.Message):
    __slots__ = ("status", "handle", "host_key_fingerprint", "server_version")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    HANDLE_FIELD_NUMBER: _ClassVar[int]
    HOST_KEY_FINGERPRINT_FIELD_NUMBER: _ClassVar[int]
    SERVER_VERSION_FIELD_NUMBER: _ClassVar[int]
    status: _common_pb2.Status
    handle: SshSessionHandle
    host_key_fingerprint: str
    server_version: str
    def __init__(self, status: _Optional[_Union[_common_pb2.Status, _Mapping]] = ..., handle: _Optional[_Union[SshSessionHandle, _Mapping]] = ..., host_key_fingerprint: _Optional[str] = ..., server_version: _Optional[str] = ...) -> None: ...

class WatchSshSessionRequest(_message.Message):
    __slots__ = ("handle", "requested_size")
    HANDLE_FIELD_NUMBER: _ClassVar[int]
    REQUESTED_SIZE_FIELD_NUMBER: _ClassVar[int]
    handle: SshSessionHandle
    requested_size: _tty_pb2.TerminalSize
    def __init__(self, handle: _Optional[_Union[SshSessionHandle, _Mapping]] = ..., requested_size: _Optional[_Union[_tty_pb2.TerminalSize, _Mapping]] = ...) -> None: ...

class SshServerMessage(_message.Message):
    __slots__ = ("opened", "history", "output", "resize", "closed", "error")
    OPENED_FIELD_NUMBER: _ClassVar[int]
    HISTORY_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_FIELD_NUMBER: _ClassVar[int]
    RESIZE_FIELD_NUMBER: _ClassVar[int]
    CLOSED_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    opened: SshOpened
    history: SshHistory
    output: SshOutput
    resize: SshNegotiatedResize
    closed: SshClosed
    error: SshError
    def __init__(self, opened: _Optional[_Union[SshOpened, _Mapping]] = ..., history: _Optional[_Union[SshHistory, _Mapping]] = ..., output: _Optional[_Union[SshOutput, _Mapping]] = ..., resize: _Optional[_Union[SshNegotiatedResize, _Mapping]] = ..., closed: _Optional[_Union[SshClosed, _Mapping]] = ..., error: _Optional[_Union[SshError, _Mapping]] = ...) -> None: ...

class SshOpened(_message.Message):
    __slots__ = ("handle", "negotiated_size", "target", "username", "host_key_fingerprint")
    HANDLE_FIELD_NUMBER: _ClassVar[int]
    NEGOTIATED_SIZE_FIELD_NUMBER: _ClassVar[int]
    TARGET_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    HOST_KEY_FINGERPRINT_FIELD_NUMBER: _ClassVar[int]
    handle: SshSessionHandle
    negotiated_size: _tty_pb2.TerminalSize
    target: str
    username: str
    host_key_fingerprint: str
    def __init__(self, handle: _Optional[_Union[SshSessionHandle, _Mapping]] = ..., negotiated_size: _Optional[_Union[_tty_pb2.TerminalSize, _Mapping]] = ..., target: _Optional[str] = ..., username: _Optional[str] = ..., host_key_fingerprint: _Optional[str] = ...) -> None: ...

class SshHistory(_message.Message):
    __slots__ = ("size", "data", "captured_at")
    SIZE_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    CAPTURED_AT_FIELD_NUMBER: _ClassVar[int]
    size: _tty_pb2.TerminalSize
    data: bytes
    captured_at: _common_pb2.Timestamp
    def __init__(self, size: _Optional[_Union[_tty_pb2.TerminalSize, _Mapping]] = ..., data: _Optional[bytes] = ..., captured_at: _Optional[_Union[_common_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class SshOutput(_message.Message):
    __slots__ = ("data",)
    DATA_FIELD_NUMBER: _ClassVar[int]
    data: bytes
    def __init__(self, data: _Optional[bytes] = ...) -> None: ...

class SshNegotiatedResize(_message.Message):
    __slots__ = ("size",)
    SIZE_FIELD_NUMBER: _ClassVar[int]
    size: _tty_pb2.TerminalSize
    def __init__(self, size: _Optional[_Union[_tty_pb2.TerminalSize, _Mapping]] = ...) -> None: ...

class SshClosed(_message.Message):
    __slots__ = ("exit_status", "exit_signal")
    EXIT_STATUS_FIELD_NUMBER: _ClassVar[int]
    EXIT_SIGNAL_FIELD_NUMBER: _ClassVar[int]
    exit_status: int
    exit_signal: str
    def __init__(self, exit_status: _Optional[int] = ..., exit_signal: _Optional[str] = ...) -> None: ...

class SshError(_message.Message):
    __slots__ = ("code", "message")
    CODE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    code: str
    message: str
    def __init__(self, code: _Optional[str] = ..., message: _Optional[str] = ...) -> None: ...

class SendSshInputRequest(_message.Message):
    __slots__ = ("handle", "data")
    HANDLE_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    handle: SshSessionHandle
    data: bytes
    def __init__(self, handle: _Optional[_Union[SshSessionHandle, _Mapping]] = ..., data: _Optional[bytes] = ...) -> None: ...

class SendSshInputResponse(_message.Message):
    __slots__ = ("status",)
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: _common_pb2.Status
    def __init__(self, status: _Optional[_Union[_common_pb2.Status, _Mapping]] = ...) -> None: ...

class ResizeSshSessionRequest(_message.Message):
    __slots__ = ("handle", "size")
    HANDLE_FIELD_NUMBER: _ClassVar[int]
    SIZE_FIELD_NUMBER: _ClassVar[int]
    handle: SshSessionHandle
    size: _tty_pb2.TerminalSize
    def __init__(self, handle: _Optional[_Union[SshSessionHandle, _Mapping]] = ..., size: _Optional[_Union[_tty_pb2.TerminalSize, _Mapping]] = ...) -> None: ...

class ResizeSshSessionResponse(_message.Message):
    __slots__ = ("status", "negotiated_size")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    NEGOTIATED_SIZE_FIELD_NUMBER: _ClassVar[int]
    status: _common_pb2.Status
    negotiated_size: _tty_pb2.TerminalSize
    def __init__(self, status: _Optional[_Union[_common_pb2.Status, _Mapping]] = ..., negotiated_size: _Optional[_Union[_tty_pb2.TerminalSize, _Mapping]] = ...) -> None: ...

class CloseSshSessionRequest(_message.Message):
    __slots__ = ("handle",)
    HANDLE_FIELD_NUMBER: _ClassVar[int]
    handle: SshSessionHandle
    def __init__(self, handle: _Optional[_Union[SshSessionHandle, _Mapping]] = ...) -> None: ...

class CloseSshSessionResponse(_message.Message):
    __slots__ = ("status",)
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: _common_pb2.Status
    def __init__(self, status: _Optional[_Union[_common_pb2.Status, _Mapping]] = ...) -> None: ...
