"""Plugs for the HWI v2 board: the hand-written one a runbook uses on a Station,
and a fake one for running the test with no Station.

HwiBoard drives the board through the Station's peripherals: a relay channel
switches its power, and a UART reaches its console. Which peripheral and
channel come from the runbook's inputs, as environment variables. The console
commands (`version`, `rail <name>`, `flash`, `boot`) belong to the board's
test firmware.
"""

from __future__ import annotations

import os
import re
import time

from openhtf import plugs

from mimick import peripherals
from mimick.appliance.v1 import relay_pb2, uart_pb2


class Board(plugs.BasePlug):
    """What the test needs of the board. Both plugs below provide it."""

    def power(self, on: bool) -> None:
        raise NotImplementedError

    def version(self) -> str:
        raise NotImplementedError

    def rail_volts(self, rail: str, load_ma: int = 0) -> float:
        raise NotImplementedError

    def flash(self) -> bool:
        raise NotImplementedError

    def boot(self) -> tuple[int, str]:
        """Boots the board. Returns the boot time in ms and the console log."""
        raise NotImplementedError


class HwiBoard(Board):
    """The HWI v2 on a Station."""

    def __init__(self):
        self._relay = peripherals.handle(os.environ.get("HWI_POWER_RELAY", "relay0"))
        self._channel = int(os.environ.get("HWI_POWER_CHANNEL", "1"))
        self._console = peripherals.handle(os.environ.get("HWI_CONSOLE", "uart0"))

    def _exec(self, command: str, expect: str = r"\n> ", timeout_ms: int = 5000) -> str:
        resp = peripherals.uart().Exec(uart_pb2.UartExecRequest(
            handle=self._console, command=command.encode(), append_terminator=True,
            expect_pattern=expect, timeout_ms=timeout_ms))
        if not resp.matched:
            raise TimeoutError(f"the console did not answer {command!r}")
        return resp.output.decode(errors="replace")

    def power(self, on: bool) -> None:
        peripherals.relay().WriteChannel(relay_pb2.RelayWriteChannelRequest(
            handle=self._relay, state=relay_pb2.ChannelState(number=self._channel, enabled=on)))

    def version(self) -> str:
        return self._exec("version").split()[0]

    def rail_volts(self, rail: str, load_ma: int = 0) -> float:
        out = self._exec(f"rail {rail} {load_ma}")
        match = re.search(r"([-0-9.]+)\s*V", out)
        if not match:
            raise ValueError(f"no reading for rail {rail!r} in {out!r}")
        return float(match.group(1))

    def flash(self) -> bool:
        return "flash ok" in self._exec("flash", expect=r"flash (ok|failed)", timeout_ms=60000)

    def boot(self) -> tuple[int, str]:
        start = time.monotonic()
        log = self._exec("boot", expect=r"login:", timeout_ms=30000)
        return int((time.monotonic() - start) * 1000), log


class FakeHwi(Board):
    """A scripted HWI v2: the first flash fails, the boot is slow."""

    flashes = 0

    def power(self, on: bool) -> None:
        self.logger.info("power %s", "on" if on else "off")

    def version(self) -> str:
        return "2.1.0"

    def rail_volts(self, rail: str, load_ma: int = 0) -> float:
        return {"vbat": 4.25, "3v3": 3.31 - load_ma / 10000}.get(rail, 0.0)

    def flash(self) -> bool:
        FakeHwi.flashes += 1
        return FakeHwi.flashes > 1

    def boot(self) -> tuple[int, str]:
        return 2300, "U-Boot 2024.01\nStarting kernel ...\nhwi login:"
