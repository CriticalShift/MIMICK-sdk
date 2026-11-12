"""Report an OpenHTF test to MIMICK as it runs.

    import openhtf as htf
    from mimick import openhtf as mimick_htf

    test = htf.Test(connect, htf.Subtest("Clock", rtc_vs_bench), teardown)
    mimick_htf.execute(test)

The library sends the test's plan before the first phase, then each phase,
group, section, subtest, branch and checkpoint as it runs, from OpenHTF's live
test state. Outcomes pass through as OpenHTF settles them, at every level.
Measurements become observations with OpenHTF's verdicts, diagnoses become
coded messages, attachments become files, and the `openhtf` logger tree reaches
the step that logged. It needs openhtf 1.6.3: install the SDK's `openhtf`
extra.

Every branch and checkpoint needs a name, and names must be unique among
siblings, because a node's path of names is its key from run to run.
"""

from __future__ import annotations

from mimick.openhtf.plan import PlanError, walk
from mimick.openhtf.reporter import Reporter, execute

__all__ = ["PlanError", "Reporter", "execute", "walk"]
