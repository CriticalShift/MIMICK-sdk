import subprocess
import sys
import textwrap
import unittest

from mimick import testing

SCRIPT = textwrap.dedent("""
    from mimick import run
    r = run.start()
    r.__enter__()
    with r.step("flash") as s:
        for i in range(50):
            s.log("line", n=i)
    # No __exit__ and no flush: the process ends, and atexit sends what is queued.
""")


class FlushAtExit(unittest.TestCase):
    def test_queued_events_reach_the_collector_when_the_process_ends(self):
        with testing.FakeBench() as bench:
            subprocess.run([sys.executable, "-c", SCRIPT], env={**bench.environ, "PYTHONPATH": ":".join(sys.path)},
                           check=True, timeout=60)
            self.assertEqual(len(bench.collector.records), 52)


if __name__ == "__main__":
    unittest.main()
