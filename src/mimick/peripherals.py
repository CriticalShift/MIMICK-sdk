"""Peripheral clients on the shared mimickd channel.

    from mimick import peripherals
    from mimick.appliance.v1 import gpio_pb2

    level = peripherals.gpio().ReadPin(
        gpio_pb2.GpioReadPinRequest(handle=peripherals.handle("io0.gpio0"), pin=3)).level

Each function returns the generated stub for one service, on the channel that
carries step correlation, so a call made inside a step is recorded under it.
A test may also build any stub in mimick.appliance.v1 on `channel()` itself.
"""

from __future__ import annotations

from mimick import env as _env
from mimick.appliance.v1 import (
    chardev_pb2_grpc,
    common_pb2,
    gpio_pb2_grpc,
    peripheral_pb2,
    peripheral_pb2_grpc,
    relay_pb2_grpc,
    spi_pb2_grpc,
    stepper_pb2_grpc,
    tty_pb2_grpc,
    uart_pb2_grpc,
)


def channel():
    return _env.channel()


_handles: dict[tuple[object, str], common_pb2.PeripheralHandle] = {}


def handle(location: str) -> common_pb2.PeripheralHandle:
    """An open handle on an interface, by the location `mimick peripheral list`
    shows, such as io0.gpio0. mimickd issues handles, so the first call for a
    location opens it, and later calls on the same channel reuse the handle.
    """
    key = (channel(), location)
    if key not in _handles:
        resp = peripheral().Open(peripheral_pb2.OpenRequest(location=location))
        _handles[key] = resp.handle
    return _handles[key]


def peripheral():
    return peripheral_pb2_grpc.PeripheralServiceStub(channel())


def gpio():
    return gpio_pb2_grpc.GpioServiceStub(channel())


def uart():
    return uart_pb2_grpc.UartServiceStub(channel())


def relay():
    return relay_pb2_grpc.RelayServiceStub(channel())


def spi():
    return spi_pb2_grpc.SpiServiceStub(channel())


def stepper():
    return stepper_pb2_grpc.StepperServiceStub(channel())


def tty():
    return tty_pb2_grpc.TtyServiceStub(channel())


def chardev():
    return chardev_pb2_grpc.ChardevServiceStub(channel())
