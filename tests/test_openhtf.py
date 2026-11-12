import pathlib
import sys
import unittest

try:
    import openhtf as htf
except ImportError:  # the openhtf extra is not installed
    htf = None

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent / "examples" / "hwi_v2"))

if htf is not None:
    from mimick import openhtf as mimick_htf, testing
    from hwi_plug import FakeHwi
    import hwi_test

PHASE_OUTCOMES = {"PASS": "pass", "FAIL": "fail", "SKIP": "skip", "ERROR": "error"}


@unittest.skipIf(htf is None, "the openhtf extra is not installed")
class HwiExample(unittest.TestCase):
    """Runs the HWI v2 example against the fake board and compares what MIMICK
    receives with OpenHTF's own record."""

    @classmethod
    def setUpClass(cls):
        FakeHwi.flashes = 0
        cls.bench = testing.FakeBench(dut={"id": "dut-42"}).__enter__()
        test = hwi_test.build(FakeHwi)
        records = []
        test.add_output_callbacks(records.append)
        cls.passed = mimick_htf.execute(test, environ=cls.bench.environ)
        cls.record = records[0]
        cls.records = list(cls.bench.collector.records)

    @classmethod
    def tearDownClass(cls):
        cls.bench.__exit__(None, None, None)

    def named(self, event):
        return [r.attrs for r in self.records if r.event_name == event]

    def stops_of(self, key):
        starts = {a["mimick.task.id"] for a in self.named("mimick.task.start") if a["mimick.task.node"] == key}
        return [a for a in self.named("mimick.task.stop") if a.get("mimick.task.id") in starts]

    def test_plan_keys_every_node_by_its_path(self):
        import json

        plan = json.loads(self.records[0].body)
        keys = [n["key"] for n in plan["nodes"]]
        self.assertEqual(keys, [
            "HWI v2", "HWI v2/setup", "HWI v2/setup/power_on", "HWI v2/main", "HWI v2/main/identify",
            "HWI v2/main/Rails", "HWI v2/main/Rails/vbat", "HWI v2/main/Rails/load_line", "HWI v2/main/flash",
            "HWI v2/main/Rails and flash ok", "HWI v2/main/boot", "HWI v2/main/Slow boot",
            "HWI v2/main/Slow boot/slow_boot_detail", "HWI v2/main/No login", "HWI v2/main/No login/recover_login",
            "HWI v2/teardown", "HWI v2/teardown/power_off",
        ])
        vbat = next(n for n in plan["nodes"] if n["key"] == "HWI v2/main/Rails/vbat")
        self.assertEqual(vbat["observations"][0],
                         {"name": "vbat", "unit": "V", "lower": 3.6, "upper": 4.3,
                          "marginal_lower": 3.7, "marginal_upper": 4.2})

    def test_phase_outcomes_match_openhtf(self):
        reported = []
        for a in self.named("mimick.task.stop"):
            name = a.get("mimick.task.name")
            if name and any(p.name == name for p in self.record.phases):
                reported.append((name, a["mimick.task.result"]))
        expected = [(p.name, PHASE_OUTCOMES[p.outcome.name]) for p in self.record.phases]
        self.assertEqual(reported, expected)

    def test_a_repeated_phase_reports_each_attempt(self):
        stops = self.stops_of("HWI v2/main/flash")
        self.assertEqual([s["mimick.task.result"] for s in stops], ["skip", "pass"])
        starts = [a for a in self.named("mimick.task.start") if a["mimick.task.node"] == "HWI v2/main/flash"]
        self.assertEqual([s["mimick.task.attempt"] for s in starts], ["1", "2"])

    def test_containers_nest_and_pass_outcomes_through(self):
        starts = {a["mimick.task.node"]: a for a in self.named("mimick.task.start")}
        self.assertEqual(starts["HWI v2/main/Rails/vbat"]["mimick.task.parent"],
                         starts["HWI v2/main/Rails"]["mimick.task.id"])
        self.assertEqual(starts["HWI v2/main"]["mimick.task.parent"], starts["HWI v2"]["mimick.task.id"])
        subtest = next(s for s in self.record.subtests if s.name == "Rails")
        self.assertEqual(self.stops_of("HWI v2/main/Rails")[0]["mimick.task.result"],
                         {"PASS": "pass", "FAIL": "fail", "STOP": "aborted"}[subtest.outcome.name])
        self.assertEqual(self.stops_of("HWI v2/main")[0]["mimick.task.result"], "none")

    def test_branches_taken_and_not(self):
        self.assertIn("HWI v2/main/Slow boot/slow_boot_detail", {a["mimick.task.node"] for a in self.named("mimick.task.start")})
        self.assertNotIn("HWI v2/main/No login", {a["mimick.task.node"] for a in self.named("mimick.task.start")})

    def test_checkpoint_continues(self):
        self.assertEqual(self.stops_of("HWI v2/main/Rails and flash ok")[0]["mimick.task.result"], "pass")

    def test_dimensioned_measurement(self):
        rail = [a for a in self.named("mimick.task.observe") if a["mimick.observation.name"] == "rail_3v3"]
        self.assertEqual(len(rail), 3)
        coords = [{k: v for k, v in a.items() if k.startswith("mimick.observation.coords.")} for a in rail]
        self.assertTrue(all(len(c) == 1 for c in coords), coords)
        self.assertEqual(sorted(v for c in coords for v in c.values()), ["0", "100", "500"])
        self.assertTrue(all(a["mimick.observation.verdict"] == "pass" for a in rail), rail)

    def test_diagnosis_attachment_and_logs(self):
        coded = [a for a in self.records if a.attrs.get("mimick.code") == "SLOW_BOOT"]
        self.assertEqual(len(coded), 1)
        boot = next(a for a in self.named("mimick.task.start") if a["mimick.task.node"] == "HWI v2/main/boot")
        self.assertEqual(coded[0].attrs["mimick.task.id"], boot["mimick.task.id"])
        stored = next(f for f in self.bench.files.values() if f.name == "console.log")
        self.assertIn(b"hwi login:", stored.data)
        flash_ids = {a["mimick.task.id"] for a in self.named("mimick.task.start")
                     if a["mimick.task.node"] == "HWI v2/main/flash"}
        logs = [r for r in self.records if r.body == "flash failed, retrying"]
        self.assertEqual(len(logs), 1)
        self.assertIn(logs[0].attrs["mimick.task.id"], flash_ids)

    def test_the_run_ends_as_openhtf_decided(self):
        run_stop = [a for a in self.named("mimick.task.stop") if "mimick.task.id" not in a][-1]
        expected = {"PASS": "pass", "FAIL": "fail", "ERROR": "error", "TIMEOUT": "error",
                    "ABORTED": "aborted"}[self.record.outcome.name]
        self.assertEqual(run_stop["mimick.task.result"], expected)
        self.assertEqual(self.record.dut_id, "dut-42")


@unittest.skipIf(htf is None, "the openhtf extra is not installed")
class OpenHTFMonitors(unittest.TestCase):
    def test_monitor_samples_reach_mimick_and_openhtf_judges_the_phase(self):
        from openhtf.util import units

        readings = iter([10.0, 11.0, 12.0] * 1000)

        @htf.monitors("current_ma", lambda: next(readings), units=units.MILLIAMPERE, poll_interval_ms=20)
        def soak(test):
            import time

            time.sleep(0.15)

        with testing.FakeBench() as bench:
            test = htf.Test(soak)
            records = []
            test.add_output_callbacks(records.append)
            mimick_htf.execute(test, environ=bench.environ)
            phase = records[0].phases[0]
            samples = [r.attrs for r in bench.collector.records if r.event_name == "mimick.task.observe"
                       and r.attrs["mimick.observation.name"] == "current_ma"]
            self.assertGreaterEqual(len(samples), 3)
            self.assertEqual(len(samples), len(phase.measurements["current_ma"].measured_value.value))
            self.assertTrue(all(len([k for k in a if k.startswith("mimick.observation.coords.")]) == 1
                                for a in samples))
            stop = [r.attrs for r in bench.collector.records if r.event_name == "mimick.task.stop"
                    and r.attrs.get("mimick.task.name") == "soak"][0]
            self.assertEqual(stop["mimick.task.result"], PHASE_OUTCOMES[phase.outcome.name])


@unittest.skipIf(htf is None, "the openhtf extra is not installed")
class PlanCheck(unittest.TestCase):
    def test_an_unnamed_branch_is_refused(self):
        class D(htf.DiagResultEnum):
            X = "x"

        def phase(test):
            pass

        test = htf.Test(htf.BranchSequence(htf.DiagnosisCondition.on_all(D.X), phase))
        with self.assertRaisesRegex(mimick_htf.PlanError, "branch .* has no name"):
            mimick_htf.walk(test)

    def test_duplicate_checkpoints_are_refused(self):
        def phase(test):
            pass

        test = htf.Test(phase, htf.PhaseFailureCheckpoint.all_previous("ok"), phase,
                        htf.PhaseFailureCheckpoint.all_previous("ok"))
        with self.assertRaisesRegex(mimick_htf.PlanError, "named 'ok'"):
            mimick_htf.walk(test)


if __name__ == "__main__":
    unittest.main()
