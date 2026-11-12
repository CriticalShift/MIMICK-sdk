import os
import tempfile
import threading
import unittest

from mimick import peripherals, run, testing
from mimick.appliance.v1 import gpio_pb2

PLAN = run.plan(
    run.node("flash", kind="phase", name="Flash"),
    run.node("power", kind="group", name="Power rails", children=[
        run.node("vbat", kind="phase", name="VBAT", observations=[
            run.measure("vbat", unit="V", lower=3.6, upper=4.3, marginal=(3.7, 4.2))]),
    ]),
)


def attrs_of(records, name):
    return [r.attrs for r in records if r.event_name == name]


class RunModel(unittest.TestCase):
    def setUp(self):
        self.bench = testing.FakeBench(dut={"serial": "SN-1"}).__enter__()
        self.addCleanup(self.bench.__exit__, None, None, None)

    def start(self, p=PLAN):
        return run.start(p, environ=self.bench.environ)

    def records(self):
        return self.bench.collector.records

    def test_plan_nesting_and_verdicts(self):
        with self.start() as r:
            self.assertEqual(r.dut.serial, "SN-1")
            with r.step("flash"):
                pass
            with r.step("power") as power:
                with r.step("vbat") as s:
                    self.assertEqual(s.observe("vbat", 4.25), "marginal")
                    self.assertEqual(s.observe("peak_c", 61, unit="C", upper=60), "fail")
        recs = self.records()
        self.assertEqual(recs[0].event_name, "mimick.task.plan")
        starts = attrs_of(recs, "mimick.task.start")
        self.assertEqual([s["mimick.task.node"] for s in starts], ["flash", "power", "vbat"])
        self.assertEqual(starts[2]["mimick.task.parent"], power.id)
        self.assertEqual(starts[0]["mimick.task.kind"], "phase")
        self.assertEqual(starts[0]["mimick.task.name"], "Flash")
        obs = attrs_of(recs, "mimick.task.observe")
        self.assertEqual(obs[0]["mimick.observation.unit"], "V")
        self.assertNotIn("mimick.observation.upper", obs[0])
        self.assertEqual(obs[1]["mimick.observation.upper"], "60")
        stops = {a["mimick.task.name"]: a for a in attrs_of(recs, "mimick.task.stop") if "mimick.task.name" in a}
        self.assertEqual(stops["VBAT"]["mimick.task.result"], "fail")
        self.assertEqual(stops["Power rails"]["mimick.task.result"], "fail")
        self.assertEqual(stops["Flash"]["mimick.task.result"], "pass")
        run_stop = [a for a in attrs_of(recs, "mimick.task.stop") if "mimick.task.name" not in a][-1]
        self.assertEqual(run_stop["mimick.task.result"], "fail")
        for rec in recs:
            self.assertEqual(rec.attrs["mimick.run.id"], "run-1")
            self.assertEqual(rec.attrs["mimick.session.id"], "session-1")
        counts = [int(rec.attrs["mimick.event.count"]) for rec in recs]
        self.assertEqual(counts, list(range(1, len(recs) + 1)))

    def test_marginal_pass_reaches_the_parent(self):
        with self.start() as r:
            with r.step("power"):
                with r.step("vbat") as s:
                    s.observe("vbat", 4.25)
        stops = {a["mimick.task.name"]: a for a in attrs_of(self.records(), "mimick.task.stop") if "mimick.task.name" in a}
        self.assertEqual(stops["Power rails"]["mimick.task.marginal"], "true")
        self.assertEqual(stops["Power rails"]["mimick.task.result"], "pass")

    def test_retries_count_attempts_and_swallow_earlier_failures(self):
        tries = []
        with self.start() as r:
            for s in r.retry("flash", tries=3):
                with s:
                    tries.append(s.attempt)
                    if len(tries) < 2:
                        raise RuntimeError("uuu exit 1")
        self.assertEqual(tries, [1, 2])
        stops = [a for a in attrs_of(self.records(), "mimick.task.stop") if a.get("mimick.task.name") == "Flash"]
        self.assertEqual([s["mimick.task.result"] for s in stops], ["error", "pass"])
        self.assertEqual(stops[0]["mimick.task.error_source"], "test")

    def test_a_retry_replaces_the_failed_attempt(self):
        with self.start() as r:
            with r.step("power"):
                for s in r.retry("vbat", tries=2):
                    with s:
                        if s.attempt == 1:
                            s.fail("noise")
        stops = attrs_of(self.records(), "mimick.task.stop")
        self.assertEqual(stops[-2]["mimick.task.name"], "Power rails")
        self.assertEqual(stops[-2]["mimick.task.result"], "pass")
        self.assertEqual(stops[-1]["mimick.task.result"], "pass")

    def test_loop_coordinates_are_not_retries(self):
        with self.start() as r:
            for slot in ("a", "b"):
                with r.step("vbat", iteration={"slot": slot}):
                    pass
        starts = attrs_of(self.records(), "mimick.task.start")
        self.assertEqual([s["mimick.task.attempt"] for s in starts], ["1", "1"])
        self.assertEqual(starts[1]["mimick.task.iteration.slot"], "b")

    def test_explicit_outcomes_codes_and_source(self):
        with self.start() as r:
            with r.step("flash") as s:
                s.fail("CRC mismatch", source="dut", codes=("CRC_BAD",))
        recs = self.records()
        coded = [r.attrs for r in recs if r.attrs.get("mimick.code") == "CRC_BAD"]
        self.assertEqual(len(coded), 1)
        stop = attrs_of(recs, "mimick.task.stop")[0]
        self.assertEqual(stop["mimick.task.error_source"], "dut")
        self.assertEqual(stop["mimick.task.reason"], "CRC mismatch")
        with self.assertRaises(ValueError):
            run.Step.fail(r.step("x"), source="gremlins")

    def test_an_unhandled_exception_closes_open_steps_as_error(self):
        with self.assertRaises(KeyError):
            with self.start() as r:
                with r.step("power"):
                    with r.step("vbat"):
                        raise KeyError("pin")
        stops = attrs_of(self.records(), "mimick.task.stop")
        self.assertEqual([s.get("mimick.task.name", "<run>") for s in stops], ["VBAT", "Power rails", "<run>"])
        self.assertTrue(all(s["mimick.task.result"] == "error" for s in stops))
        self.assertEqual(stops[0]["mimick.task.error_source"], "test")

    def test_peripheral_calls_land_under_the_step(self):
        with self.start() as r:
            with r.step("vbat") as s:
                peripherals.gpio().ReadPin(gpio_pb2.GpioReadPinRequest(handle=peripherals.handle("io0"), pin=3))
            peripherals.gpio().ReadPin(gpio_pb2.GpioReadPinRequest(pin=3))
        self.assertEqual([c.task_id for c in self.bench.gpio_calls], [s.id, ""])

    def test_attach_uploads_with_the_run_token(self):
        with tempfile.NamedTemporaryFile("wb", suffix=".log", delete=False) as f:
            f.write(b"flash output")
        self.addCleanup(os.unlink, f.name)
        with self.start() as r:
            with r.step("flash") as s:
                file_id = s.attach(f.name, name="uuu.log")
        stored = self.bench.files[file_id]
        self.assertEqual((stored.name, stored.data, stored.task_id), ("uuu.log", b"flash output", s.id))
        attach = attrs_of(self.records(), "mimick.task.attach")[0]
        self.assertEqual(attach["mimick.file.id"], file_id)
        self.assertEqual(attach["mimick.task.id"], s.id)
        self.assertEqual(attach["mimick.file.media_type"], "text/plain; charset=utf-8")

    def test_counts_never_repeat_across_threads(self):
        with self.start(None) as r:
            with r.step("soak") as s:
                threads = [threading.Thread(target=lambda i=i: [s.log("tick", n=i) for _ in range(25)])
                           for i in range(8)]
                for t in threads:
                    t.start()
                for t in threads:
                    t.join()
        counts = sorted(int(rec.attrs["mimick.event.count"]) for rec in self.records())
        self.assertEqual(counts, list(range(1, len(counts) + 1)))


if __name__ == "__main__":
    unittest.main()
