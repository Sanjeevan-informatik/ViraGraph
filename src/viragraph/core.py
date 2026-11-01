"""Small, dependency-free, validated viral sequence analysis core."""
from collections import Counter
from dataclasses import dataclass
from math import log
from pathlib import Path

DNA = frozenset("ACGTN")
RNA = frozenset("ACGUN")
MAX_BASES = 2_000_000

@dataclass(frozen=True)
class Sequence:
    name: str
    bases: str

def parse_fasta(text: str, *, max_bases: int = MAX_BASES) -> list[Sequence]:
    if not text.strip():
        raise ValueError("Empty FASTA")
    records: list[Sequence] = []
    name: str | None = None
    chunks: list[str] = []
    total = 0
    def finish() -> None:
        if name is not None:
            seq = "".join(chunks).upper()
            if not seq:
                raise ValueError(f"Empty sequence: {name}")
            records.append(Sequence(name, seq))
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith(">"):
            finish()
            name = line[1:].split()[0]
            if not name:
                raise ValueError("Missing FASTA identifier")
            chunks = []
        else:
            if name is None:
                raise ValueError("FASTA sequence before header")
            total += len(line)
            if total > max_bases:
                raise ValueError("Total sequence size limit exceeded")
            chunks.append(line)
    finish()
    if len(set(r.name for r in records)) != len(records):
        raise ValueError("Duplicate FASTA identifiers")
    if not records:
        raise ValueError("No FASTA records")
    return records

def validate_alignment(records: list[Sequence]) -> str:
    if not records:
        raise ValueError("No records")
    lengths = {len(r.bases) for r in records}
    if len(lengths) != 1:
        raise ValueError("All haplotypes must be pre-aligned and equal length")
    observed = set("".join(r.bases for r in records))
    if "T" in observed and "U" in observed:
        raise ValueError("Cannot mix RNA U and DNA T in one alignment")
    alphabet = "RNA" if "U" in observed else "DNA"
    allowed = RNA if alphabet == "RNA" else DNA
    if observed - allowed:
        raise ValueError(f"Invalid nucleotide symbols: {sorted(observed - allowed)}")
    return alphabet

def haplotype_counts(records: list[Sequence]) -> dict[str, int]:
    validate_alignment(records)
    return dict(Counter(record.bases for record in records))

def shannon_diversity(records: list[Sequence]) -> float:
    counts = haplotype_counts(records)
    n = sum(counts.values())
    return -sum((v / n) * log(v / n) for v in counts.values())

def nucleotide_diversity(records: list[Sequence]) -> float:
    """Mean pairwise mismatch fraction, excluding columns with N for either sequence."""
    validate_alignment(records)
    if len(records) < 2:
        return 0.0
    pairs = []
    for i, a in enumerate(records):
        for b in records[i + 1:]:
            valid = [(x, y) for x, y in zip(a.bases, b.bases) if x != "N" and y != "N"]
            if valid:
                pairs.append(sum(x != y for x, y in valid) / len(valid))
    return sum(pairs) / len(pairs) if pairs else 0.0

def summary(records: list[Sequence]) -> dict:
    alphabet = validate_alignment(records)
    return {
        "alphabet": alphabet,
        "sample_count": len(records),
        "genome_length": len(records[0].bases),
        "distinct_haplotypes": len(haplotype_counts(records)),
        "shannon_diversity": shannon_diversity(records),
        "nucleotide_diversity": nucleotide_diversity(records),
    }

def read_fasta(path: str | Path) -> list[Sequence]:
    file = Path(path)
    if file.stat().st_size > MAX_BASES * 2:
        raise ValueError("File too large")
    return parse_fasta(file.read_text(encoding="utf-8"))
