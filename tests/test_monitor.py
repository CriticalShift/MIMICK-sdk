import time
import unittest

from mimick import run, testing


def observes(records):
    return [r.attrs for r in records if r.event_name == "mimick.task.observe"]


class Monitors(unittest.TestCase):
    def setUp(self):
        self.bench = testing.FakeBench().__enter__()
        self.addCleanup(self.bench.__exit__, None, None, None)

    def start(self):
        return run.start(environ=self.bench.environ)

    def test_in_process_samples_and_a_series(self):
        values = iter([3.9, 4.0, 4.5] + [4.0] * 1000)
        with self.start() as r:
            with r.step("boot") as s:
                with s.monitor("vbat", every=0.02, unit="V", lower=3.6, upper=4.3, source=lambda: next(values)) as m:
                    time.sleep(0.15)
        self.assertGreaterEqual(m.series.count, 5)
        self.assertEqual(m.series.verdict, "fail")
        self.assertEqual(m.series.max, 4.5)
        recs = observes(self.bench.collector.records)
        samples = [a for a in recs if a.get("mimick.observation.sample") == "true"]
        self.assertEqual(len(samples), m.series.count)
        self.assertTrue(all("mimick.event.count" not in a for a in samples), "a sample was numbered")
        self.assertTrue(all(a["mimick.task.id"] == s.id for a in samples))
        series = [a for a in recs if "mimick.observation.series.rows" in a]
        self.assertEqual(len(series), 1)
        self.assertEqual(series[0]["mimick.observation.series.rows"], str(m.series.count))
        self.assertEqual(series[0]["mimick.observation.verdict"], "fail")
        self.assertIn("mimick.observation.series.from", series[0])
        stop = [a for a in self.bench.collector.records if a.event_name == "mimick.task.stop"][0]
        self.assertEqual(stop.attrs["mimick.task.result"], "fail")

    def test_closing_the_step_stops_its_monitors(self):
        with self.start() as r:
            with r.step("soak") as s:
                m = s.monitor("temp_c", every=0.02, source=lambda: 25.0)
                time.sleep(0.05)
        self.assertIsNotNone(m.series)
        self.assertEqual(m.series.verdict, "unset")
        count = m.series.count
        time.sleep(0.06)
        samples = [a for a in observes(self.bench.collector.records) if a.get("mimick.observation.sample")]
        self.assertEqual(len(samples), count, "a monitor sampled after its step closed")

    def test_a_controller_monitor_uses_the_station(self):
        self.bench.monitor_verdict = "marginal"
        with self.start() as r:
            with r.step("boot") as s:
                with s.monitor("vbat", every=0.1, unit="V", upper=4.3, software=("meter.software0", r"([0-9.]+) V")) as m:
                    pass
        req = self.bench.monitors["monitor-1"]
        self.assertEqual((req.name, req.node_run_id, req.every_ms, req.upper), ("vbat", s.id, 100, 4.3))
        self.assertEqual((req.software_read.location, req.software_read.pattern), ("meter.software0", "([0-9.]+) V"))
        self.assertEqual(self.bench.stopped, ["monitor-1"])
        self.assertEqual((m.series.count, m.series.min, m.series.max), (3, 1.0, 3.0))
        series = [a for a in observes(self.bench.collector.records) if "mimick.observation.series.rows" in a][0]
        self.assertEqual(series["mimick.observation.verdict"], "marginal")
        stop = [a for a in self.bench.collector.records if a.event_name == "mimick.task.stop"][0]
        self.assertEqual((stop.attrs["mimick.task.result"], stop.attrs["mimick.task.marginal"]), ("pass", "true"))

    def test_a_monitor_needs_one_source(self):
        with self.start() as r:
            with r.step("x") as s:
                with self.assertRaises(ValueError):
                    s.monitor("v", source=lambda: 1.0, gpio=("io0", 1))
                with self.assertRaises(ValueError):
                    s.monitor("v")


if __name__ == "__main__":
    unittest.main()
