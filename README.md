# MIMICK SDK

Drive a MIMICK Station's peripherals and report a test's structure and results
from Python, inside a runbook.

## Install

In the runbook image's Dockerfile, install a tagged release:

```dockerfile
RUN pip install "mimick-sdk @ git+https://github.com/CriticalShift/MIMICK-sdk@v0.10.7"
```

Use the release that matches your MIMICK Cloud.

## Report a run

```python
from mimick import run

plan = run.plan(
    run.node("flash", kind="phase", name="Flash"),
    run.node("power", kind="group", name="Power rails", children=[
        run.node("vbat", kind="phase", name="VBAT",
                 observations=[run.measure("vbat", unit="V", lower=3.6, upper=4.3, marginal=(3.7, 4.2))]),
    ]),
)

with run.start(plan) as r:
    for s in r.retry("flash", tries=3):
        with s:
            flash(r.dut.serial)
            s.attach("flash.log")
    with r.step("power"):
        with r.step("vbat") as s:
            s.observe("vbat", read_vbat())
```

- `run.start` reads the run and the DUT from the environment the runner sets,
  and declares the plan. The run page shows planned steps before they run.
- `r.step(key)` opens a step inside the open one. It passes unless its body
  sets another outcome (`s.fail()`, `s.skip()`, `s.error()`), an observation in
  it fails, or a child fails. An exception that escapes it records an error.
- `r.retry(key, tries=n)` yields attempts of a step until one passes.
- `s.observe(name, value)` records a value and judges it against the plan's
  limits, or the limits you pass.
- `s.log(message, level=..., code=...)` logs against the step. A code such as
  `FLASH_TIMEOUT` is a diagnosis that reports can search.
- `s.attach(path)` stores a file with the step.

Each record goes to the Station's collector, which delivers it to MIMICK even
across a lost connection. Outside a runbook, the SDK prints the records instead.

## Drive peripherals

```python
from mimick import peripherals
from mimick.appliance.v1 import gpio_pb2

level = peripherals.gpio().ReadPin(
    gpio_pb2.GpioReadPinRequest(handle=peripherals.handle("io0"), pin=3)).level
```

`mimick.appliance.v1` holds the generated client for every service the Station
serves. A call made inside a step is recorded under that step.

## Test without a Station

`mimick.testing.FakeBench` runs a fake collector and a fake Station daemon:

```python
from mimick import run, testing

with testing.FakeBench() as bench:
    with run.start(environ=bench.environ) as r:
        with r.step("flash") as s:
            s.observe("vbat", 4.1)
    print(bench.collector.records)
```

## Develop

The generated code under `src/mimick/appliance` and the plan test vectors under
`tests/testdata` come from MIMICK-Cloud: run `task --dir common sdk:sync` there.
Do not edit them here.

```bash
pip install -e .
python -m unittest discover -s tests
```
