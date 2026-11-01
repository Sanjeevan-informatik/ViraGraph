"""Position-wise variant graph for equal-length, pre-aligned haplotypes."""
from collections import Counter
from .core import Sequence, validate_alignment

def build_graph(records: list[Sequence]) -> dict:
    alphabet = validate_alignment(records)
    length = len(records[0].bases)
    nodes = []
    edges = set()
    paths = []
    for position in range(length):
        bases = sorted({seq.bases[position] for seq in records})
        for base in bases:
            nodes.append({"id": f"{position + 1}:{base}", "position": position + 1, "base": base})
    for record in records:
        steps = [f"{position + 1}:{base}" for position, base in enumerate(record.bases)]
        edges.update(zip(steps, steps[1:]))
        paths.append({"name": record.name, "nodes": steps})
    return {
        "schema_version": "0.1",
        "alphabet": alphabet,
        "nodes": nodes,
        "edges": [{"source": a, "target": b} for a, b in sorted(edges)],
        "paths": paths,
        "variant_positions": [
            i + 1 for i in range(length)
            if len({r.bases[i] for r in records if r.bases[i] != "N"}) > 1
        ],
        "haplotype_counts": dict(Counter(record.bases for record in records)),
        "warning": "Column graph for pre-aligned substitutions only; no phasing inference.",
    }
