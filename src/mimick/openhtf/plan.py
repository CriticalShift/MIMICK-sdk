"""The plan of an OpenHTF test: its phase tree, with a path key per node.

OpenHTF gives a phase only `id(phase)`, which changes every run, and groups,
branches and checkpoints no id at all. The key of a node here is the path of
names from the root, such as `Power/main/VBAT`, so it stays the same from run
to run.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import openhtf as htf
from openhtf.core import phase_branches
from openhtf.util import validators as htf_validators

from mimick import plan as mplan


class PlanError(ValueError):
    """The test cannot be keyed: a node that needs a name has none, or two
    siblings share one."""


@dataclass
class Walked:
    plan: mplan.Plan
    # Phase descriptor id() to its node key.
    phases: dict[int, str] = field(default_factory=dict)
    # A node's key to the keys of its ancestors, outermost first.
    ancestors: dict[str, list[str]] = field(default_factory=dict)
    # A node's key to its kind and name.
    nodes: dict[str, tuple[str, str]] = field(default_factory=dict)
    # Subtest, branch and checkpoint names to their keys.
    subtests: dict[str, str] = field(default_factory=dict)
    branches: dict[str, str] = field(default_factory=dict)
    checkpoints: dict[str, str] = field(default_factory=dict)


def walk(test: htf.Test) -> Walked:
    """The plan of a built test. Raises PlanError for a node it cannot key."""
    w = Walked(plan=mplan.Plan([]))
    _children(w, test.descriptor.phase_sequence.nodes, "", [], w.plan.nodes, "the test")
    return w


def _key(parent: str, name: str) -> str:
    return f"{parent}/{name}" if parent else name


def _children(w: Walked, nodes, parent: str, ancestors: list[str], out: list[mplan.Node], where: str) -> None:
    seen: dict[str, int] = {}
    for node in nodes:
        _node(w, node, parent, ancestors, out, where, seen)


def _add(w: Walked, out: list[mplan.Node], seen: dict[str, int], parent: str, ancestors: list[str],
         name: str, kind: str, unique: bool, where: str) -> mplan.Node:
    count = seen.get(name, 0) + 1
    seen[name] = count
    if count > 1 and unique:
        raise PlanError(f"two {kind} nodes in {where} are named {name!r}: give each a unique name")
    key = _key(parent, name if count == 1 else f"{name}#{count}")
    node = mplan.Node(key=key, kind=kind, name=name)
    out.append(node)
    w.ancestors[key] = list(ancestors)
    w.nodes[key] = (kind, name)
    return node


def _node(w: Walked, node, parent: str, ancestors: list[str], out: list[mplan.Node], where: str,
          seen: dict[str, int]) -> None:
    # Subclasses before PhaseSequence, in the order OpenHTF's executor checks.
    if isinstance(node, htf.Subtest):
        n = _add(w, out, seen, parent, ancestors, node.name, "subtest", True, where)
        w.subtests[node.name] = n.key
        _children(w, node.nodes, n.key, ancestors + [n.key], n.children, f"subtest {node.name!r}")
    elif isinstance(node, htf.BranchSequence):
        if not node.name:
            raise PlanError(f"a branch in {where} has no name: name every branch, as BranchSequence(..., name=...)")
        n = _add(w, out, seen, parent, ancestors, node.name, "branch", True, where)
        w.branches[node.name] = n.key
        _children(w, node.nodes, n.key, ancestors + [n.key], n.children, f"branch {node.name!r}")
    elif isinstance(node, htf.PhaseSequence):
        if node.name:
            n = _add(w, out, seen, parent, ancestors, node.name, "sequence", True, where)
            _children(w, node.nodes, n.key, ancestors + [n.key], n.children, f"sequence {node.name!r}")
        else:
            # An unnamed sequence only groups its nodes: they belong to its parent.
            for child in node.nodes:
                _node(w, child, parent, ancestors, out, where, seen)
    elif isinstance(node, htf.PhaseGroup):
        sections = [("setup", node.setup), ("main", node.main), ("teardown", node.teardown)]
        if node.name:
            n = _add(w, out, seen, parent, ancestors, node.name, "group", True, where)
            g_parent, g_ancestors, g_out = n.key, ancestors + [n.key], n.children
            g_where = f"group {node.name!r}"
        else:
            g_parent, g_ancestors, g_out, g_where = parent, ancestors, out, where
        g_seen: dict[str, int] = {} if node.name else seen
        for section, seq in sections:
            if seq is None:
                continue
            s = _add(w, g_out, g_seen, g_parent, g_ancestors, section, "section", False, g_where)
            _children(w, seq.nodes, s.key, g_ancestors + [s.key], s.children, f"{section} of {g_where}")
    elif isinstance(node, htf.PhaseDescriptor):
        n = _add(w, out, seen, parent, ancestors, node.name, "phase", False, where)
        w.phases[id(node)] = n.key
        n.observations = [_measure(m) for m in node.measurements]
    elif isinstance(node, phase_branches.Checkpoint):
        if not node.name:
            raise PlanError(f"a checkpoint in {where} has no name: name every checkpoint")
        n = _add(w, out, seen, parent, ancestors, node.name, "checkpoint", True, where)
        w.checkpoints[node.name] = n.key
    else:
        raise PlanError(f"{where} holds a {type(node).__name__}, which the plan does not know")


def _measure(m) -> mplan.Measure:
    unit = ""
    if m.units is not None:
        unit = m.units.suffix or m.units.name or ""
    lower = upper = mlower = mupper = None
    for v in m.validators:
        if isinstance(v, htf_validators.RangeValidatorBase):
            # The raw limits: the public properties cast an unset one through the
            # validator's type and can raise.
            lower, upper = getattr(v, "_minimum", None), getattr(v, "_maximum", None)
            mlower, mupper = getattr(v, "_marginal_minimum", None), getattr(v, "_marginal_maximum", None)
            break
    marginal = (mlower, mupper) if (mlower is not None or mupper is not None) else None
    return mplan.Measure(
        m.name, unit,
        float(lower) if lower is not None else None,
        float(upper) if upper is not None else None,
        tuple(float(x) if x is not None else None for x in marginal) if marginal else None,
    )
