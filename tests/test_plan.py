import json
import pathlib
import unittest

from mimick import plan

VECTORS = json.loads((pathlib.Path(__file__).parent / "testdata" / "plan_vectors.json").read_text())


class SharedVectors(unittest.TestCase):
    """The Go CLI passes the same vectors, so both write the same bytes."""

    def test_valid(self):
        for v in VECTORS["valid"]:
            with self.subTest(v["name"]):
                canonical, _ = plan.canonicalize(v["plan"].encode())
                self.assertEqual(canonical.decode(), v["canonical"])
                self.assertEqual(plan.digest(canonical), v["digest"])

    def test_invalid(self):
        for v in VECTORS["invalid"]:
            with self.subTest(v["name"]):
                with self.assertRaises(plan.PlanError):
                    plan.canonicalize(v["plan"].encode())


class Numbers(unittest.TestCase):
    def test_ecmascript_form(self):
        cases = {
            0.0: "0", -0.0: "0", 1.0: "1", -1.5: "-1.5", 4.5: "4.5", 0.002: "0.002",
            0.000001: "0.000001", 1e-7: "1e-7", 1e21: "1e+21", 1e30: "1e+30",
            123456789012345680000.0: "123456789012345680000", 333333333.3333333: "333333333.3333333",
            5e-324: "5e-324", 1.7976931348623157e308: "1.7976931348623157e+308",
            9007199254740992.0: "9007199254740992", 1.5e-7: "1.5e-7", 1234.5678: "1234.5678",
        }
        for f, want in cases.items():
            with self.subTest(f):
                self.assertEqual(plan._number(f), want)


class Builder(unittest.TestCase):
    def test_tree_to_document(self):
        p = plan.plan(
            plan.node("flash", kind="phase", name="Flash"),
            plan.node("power", kind="group", children=[
                plan.node("vbat", kind="phase", observations=[
                    plan.measure("vbat", unit="V", lower=3.6, upper=4.3, marginal=(3.7, 4.2))]),
            ]),
        )
        doc = p.document()
        self.assertEqual([n["key"] for n in doc["nodes"]], ["flash", "power", "vbat"])
        self.assertEqual(doc["nodes"][2]["parent"], "power")
        self.assertEqual(doc["nodes"][2]["observations"][0]["marginal_lower"], 3.7)
        canonical = p.canonical()
        self.assertTrue(canonical.startswith(b'{"nodes":[{"key":"flash","kind":"phase","name":"Flash"}'))
        self.assertIsNotNone(p.find("vbat"))


if __name__ == "__main__":
    unittest.main()
