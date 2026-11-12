"""Peripheral clients on the shared mimickd channel.

    from mimick import peripherals
    from mimick.appliance.v1 import gpio_pb2

    level = peripherals.gpio().ReadPin(
        gpio_pb2.GpioReadPinRequest(handle=peripherals.handle("io0"), pin=3)).level

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
    peripheral_pb2_grpc,
    relay_pb2_grpc,
    spi_pb2_grpc,
    stepper_pb2_grpc,
    tty_pb2_grpc,
    uart_pb2_grpc,
)


def channel():
    return _env.channel()


def handle(peripheral_id: str) -> common_pb2.PeripheralHandle:
    """The handle of a peripheral, by the id `mimick peripheral list` shows."""
    return common_pb2.PeripheralHandle(id=peripheral_id)


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
