"""Run plans: the tree of nodes a run may execute, and its canonical form.

A plan travels as RFC 8785 canonical JSON, and its digest is the hex SHA-256 of
those bytes. The Go CLI writes the same bytes for the same plan, and both are
tested against the shared vectors in tests/testdata/plan_vectors.json, which
come from MIMICK-Cloud's common/pkg/runplan.
"""

from __future__ import annotations

import hashlib
import json
import math
from decimal import Decimal
from dataclasses import dataclass, field
from typing import Any


@dataclass
class Measure:
    """An observation a node declares, with its unit and limits."""

    name: str
    unit: str = ""
    lower: float | None = None
    upper: float | None = None
    # (lower, upper) inside which a passing value is not marginal.
    marginal: tuple[float | None, float | None] | None = None

    def document(self) -> dict[str, Any]:
        doc: dict[str, Any] = {"name": self.name}
        if self.unit:
            doc["unit"] = self.unit
        if self.lower is not None:
            doc["lower"] = self.lower
        if self.upper is not None:
            doc["upper"] = self.upper
        if self.marginal:
            lo, hi = self.marginal
            if lo is not None:
                doc["marginal_lower"] = lo
            if hi is not None:
                doc["marginal_upper"] = hi
        return doc


@dataclass
class Node:
    key: str
    kind: str = ""
    name: str = ""
    children: list[Node] = field(default_factory=list)
    observations: list[Measure] = field(default_factory=list)


def node(key: str, kind: str = "", name: str = "", children=(), observations=()) -> Node:
    return Node(key, kind, name, list(children), list(observations))


def measure(name: str, unit: str = "", lower=None, upper=None, marginal=None) -> Measure:
    return Measure(name, unit, lower, upper, marginal)


@dataclass
class Plan:
    nodes: list[Node]

    def flat(self) -> list[tuple[Node, str]]:
        """Every node with its parent's key, parents first."""
        out: list[tuple[Node, str]] = []

        def walk(n: Node, parent: str) -> None:
            out.append((n, parent))
            for c in n.children:
                walk(c, n.key)

        for n in self.nodes:
            walk(n, "")
        return out

    def find(self, key: str) -> Node | None:
        return next((n for n, _ in self.flat() if n.key == key), None)

    def document(self) -> dict[str, Any]:
        nodes = []
        for n, parent in self.flat():
            doc: dict[str, Any] = {"key": n.key}
            if parent:
                doc["parent"] = parent
            if n.kind:
                doc["kind"] = n.kind
            if n.name:
                doc["name"] = n.name
            if n.observations:
                doc["observations"] = [o.document() for o in n.observations]
            nodes.append(doc)
        return {"nodes": nodes}

    def canonical(self) -> bytes:
        canonical, _ = canonicalize(json.dumps(self.document()).encode())
        return canonical


def plan(*nodes: Node) -> Plan:
    return Plan(list(nodes))


def digest(canonical: bytes) -> str:
    return hashlib.sha256(canonical).hexdigest()


class PlanError(ValueError):
    pass


def canonicalize(raw: bytes) -> tuple[bytes, dict[str, Any]]:
    """Checks a plan document and returns its canonical bytes and the document.

    The rules match MIMICK-Cloud's runplan.Canonicalize: an object with a
    non-empty "nodes" array, unique keys, known parents with no cycle, unique
    observation names per node, no repeated member name, and members the SDK
    does not know kept as they are.
    """
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as e:
        raise PlanError("the plan is not valid UTF-8") from e

    def no_repeats(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        out: dict[str, Any] = {}
        for k, v in pairs:
            if k in out:
                raise PlanError(f"member {k!r} appears twice")
            out[k] = v
        return out

    def no_constants(name: str) -> Any:
        raise PlanError(f"{name} is not a JSON number")

    try:
        doc = json.loads(
            text, object_pairs_hook=no_repeats, parse_float=float, parse_int=float, parse_constant=no_constants
        )
    except json.JSONDecodeError as e:
        raise PlanError(f"the plan is not valid JSON: {e}") from e
    if not isinstance(doc, dict):
        raise PlanError("the plan must be a JSON object")
    _check(doc)
    return _write(doc).encode("utf-8"), doc


def _check(doc: dict[str, Any]) -> None:
    nodes = doc.get("nodes")
    if not isinstance(nodes, list) or not nodes:
        raise PlanError('the plan has no "nodes"')
    parents: dict[str, str] = {}
    for n in nodes:
        if not isinstance(n, dict):
            raise PlanError("a plan node is not an object")
        key = n.get("key", "")
        if not isinstance(key, str) or not key:
            raise PlanError("a plan node has no key")
        if key in parents:
            raise PlanError(f"the plan has two nodes with key {key!r}")
        parent = n.get("parent", "")
        if not isinstance(parent, str):
            raise PlanError(f"node {key!r} has a parent that is not a string")
        parents[key] = parent
        for f in ("kind", "name"):
            if f in n and not isinstance(n[f], str):
                raise PlanError(f"node {key!r} has a {f} that is not a string")
        seen: set[str] = set()
        for o in n.get("observations") or []:
            if not isinstance(o, dict) or not isinstance(o.get("name"), str) or not o["name"]:
                raise PlanError(f"node {key!r} declares an observation with no name")
            if o["name"] in seen:
                raise PlanError(f"node {key!r} declares observation {o['name']!r} twice")
            seen.add(o["name"])
            for lim in ("lower", "upper", "marginal_lower", "marginal_upper"):
                if lim in o and not isinstance(o[lim], float):
                    raise PlanError(f"node {key!r} has a {lim} that is not a number")
    for key, parent in parents.items():
        steps = 0
        while parent:
            if parent not in parents:
                raise PlanError(f"node {key!r} has parent {parent!r}, which is not in the plan")
            if parent == key or steps > len(parents):
                raise PlanError(f"node {key!r} is its own ancestor")
            parent = parents[parent]
            steps += 1


def _write(v: Any) -> str:
    if v is None:
        return "null"
    if v is True:
        return "true"
    if v is False:
        return "false"
    if isinstance(v, float):
        return _number(v)
    if isinstance(v, str):
        return _string(v)
    if isinstance(v, list):
        return "[" + ",".join(_write(e) for e in v) + "]"
    if isinstance(v, dict):
        keys = sorted(v, key=lambda k: k.encode("utf-16-be"))
        return "{" + ",".join(_string(k) + ":" + _write(v[k]) for k in keys) + "}"
    raise PlanError(f"cannot write {type(v).__name__} in a plan")


def _number(f: float) -> str:
    """A number as ECMAScript's Number.prototype.toString writes it (RFC 8785 3.2.2.3)."""
    if math.isnan(f) or math.isinf(f):
        raise PlanError("a plan number must be finite")
    if f == 0:
        return "0"
    sign = "-" if f < 0 else ""
    # repr gives the shortest digits that round-trip, as ECMAScript requires.
    t = Decimal(repr(abs(f))).as_tuple()
    digits = "".join(str(d) for d in t.digits).rstrip("0") or "0"
    k = len(digits)
    # The value is 0.d1..dk times 10^n.
    n = len(t.digits) + t.exponent
    if k <= n <= 21:
        return sign + digits + "0" * (n - k)
    if 0 < n <= 21:
        return sign + digits[:n] + "." + digits[n:]
    if -6 < n <= 0:
        return sign + "0." + "0" * -n + digits
    e = n - 1
    mantissa = digits[0] + ("." + digits[1:] if k > 1 else "")
    return f"{sign}{mantissa}e{'+' if e > 0 else '-'}{abs(e)}"


def _string(s: str) -> str:
    """A string with only the escapes RFC 8785 3.2.2.2 requires."""
    out = ['"']
    for ch in s:
        o = ord(ch)
        if ch == '"':
            out.append('\\"')
        elif ch == "\\":
            out.append("\\\\")
        elif ch == "\b":
            out.append("\\b")
        elif ch == "\f":
            out.append("\\f")
        elif ch == "\n":
            out.append("\\n")
        elif ch == "\r":
            out.append("\\r")
        elif ch == "\t":
            out.append("\\t")
        elif o < 0x20:
            out.append(f"\\u{o:04x}")
        else:
            out.append(ch)
    out.append('"')
    return "".join(out)
