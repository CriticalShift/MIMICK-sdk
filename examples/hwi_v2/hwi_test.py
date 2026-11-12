"""An OpenHTF test of the HWI v2 board, reported to MIMICK.

Run it on a Station as a runbook (see Dockerfile and runbook.sh), or off the
bench with the fake board:

    python hwi_test.py --fake
"""

from __future__ import annotations

import sys

import openhtf as htf
from openhtf.util import units

from mimick import openhtf as mimick_htf

from hwi_plug import Board, FakeHwi, HwiBoard


class Diag(htf.DiagResultEnum):
    SLOW_BOOT = "slow_boot"
    NO_LOGIN = "no_login"


def rail_in_tolerance(points) -> bool:
    """Every (load, volts) point of the 3V3 load line within 3.2 to 3.4 V."""
    return all(3.2 <= volts <= 3.4 for *_, volts in points)


@htf.PhaseDiagnoser(Diag)
def boot_diagnoser(phase_record):
    if phase_record.measurements["boot_ms"].measured_value.value > 2000:
        return htf.Diagnosis(Diag.SLOW_BOOT, "Boot took over two seconds")
    return None


def build(board: type[Board]) -> htf.Test:
    @htf.plug(board=board)
    def power_on(test, board):
        board.power(True)

    @htf.plug(board=board)
    def power_off(test, board):
        board.power(False)

    @htf.measures(htf.Measurement("fw_version").equals("2.1.0"))
    @htf.plug(board=board)
    def identify(test, board):
        test.measurements.fw_version = board.version()

    @htf.measures(htf.Measurement("vbat").in_range(3.6, 4.3, marginal_minimum=3.7, marginal_maximum=4.2)
                  .with_units(units.VOLT))
    @htf.plug(board=board)
    def vbat(test, board):
        test.measurements.vbat = board.rail_volts("vbat")

    @htf.measures(htf.Measurement("rail_3v3").with_dimensions(units.MILLIAMPERE)
                  .with_validator(rail_in_tolerance).with_units(units.VOLT))
    @htf.plug(board=board)
    def load_line(test, board):
        for load in (0, 100, 500):
            test.measurements.rail_3v3[load] = board.rail_volts("3v3", load)

    @htf.PhaseOptions(repeat_limit=3)
    @htf.plug(board=board)
    def flash(test, board):
        if not board.flash():
            test.logger.warning("flash failed, retrying")
            return htf.PhaseResult.REPEAT
        return htf.PhaseResult.CONTINUE

    @htf.diagnose(boot_diagnoser)
    @htf.measures(htf.Measurement("boot_ms").in_range(maximum=10000).with_units(units.MILLISECOND))
    @htf.plug(board=board)
    def boot(test, board):
        ms, log = board.boot()
        test.measurements.boot_ms = ms
        test.attach("console.log", log.encode(), mimetype="text/plain")

    def slow_boot_detail(test):
        test.logger.info("collecting boot timing detail after a slow boot")

    def recover_login(test):
        test.logger.info("recovering the login prompt")

    return htf.Test(
        htf.PhaseGroup(
            setup=[power_on],
            main=[
                identify,
                htf.Subtest("Rails", vbat, load_line),
                flash,
                htf.PhaseFailureCheckpoint.all_previous("Rails and flash ok"),
                boot,
                htf.BranchSequence(htf.DiagnosisCondition.on_all(Diag.SLOW_BOOT), slow_boot_detail,
                                   name="Slow boot"),
                htf.BranchSequence(htf.DiagnosisCondition.on_all(Diag.NO_LOGIN), recover_login,
                                   name="No login"),
            ],
            teardown=[power_off],
            name="HWI v2",
        ),
        test_name="hwi-v2",
    )


if __name__ == "__main__":
    test = build(FakeHwi if "--fake" in sys.argv else HwiBoard)
    sys.exit(0 if mimick_htf.execute(test) else 1)
