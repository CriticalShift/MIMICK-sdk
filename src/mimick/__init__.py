"""MIMICK SDK: drive a Station's peripherals and report a test's structure and
results from inside a runbook.

    from mimick import run

    plan = run.plan(
        run.node("flash", kind="phase", name="Flash"),
        run.node("power", kind="group", name="Power rails", children=[
            run.node("vbat", kind="phase", name="VBAT",
                     observations=[run.measure("vbat", unit="V", lower=3.6, upper=4.3)]),
        ]),
    )

    with run.start(plan) as r:
        with r.step("flash") as s:
            s.attach("flash.log")
        with r.step("power"):
            with r.step("vbat") as s:
                s.observe("vbat", 4.21)
"""

__version__ = "0.10.7"
