import math
import pytest
from viragraph.core import parse_fasta, summary, nucleotide_diversity
from viragraph.graph import build_graph

DATA = ">one\nACGT\n>two\nACGA\n>three\nACGT\n"

def test_summary():
    result = summary(parse_fasta(DATA))
    assert result["alphabet"] == "DNA"
    assert result["genome_length"] == 4
    assert result["distinct_haplotypes"] == 2
    assert math.isclose(result["nucleotide_diversity"], 1 / 6)

def test_graph_paths():
    graph = build_graph(parse_fasta(DATA))
    assert graph["variant_positions"] == [4]
    assert len(graph["paths"]) == 3
    assert {"4:A", "4:T"} <= {node["id"] for node in graph["nodes"]}

def test_rna():
    assert summary(parse_fasta(">rna\nACGU\n"))["alphabet"] == "RNA"

def test_invalid_sequence():
    with pytest.raises(ValueError):
        summary(parse_fasta(">bad\nACGX\n"))

def test_mixed_alphabet():
    with pytest.raises(ValueError):
        summary(parse_fasta(">a\nACGT\n>b\nACGU\n"))

def test_unaligned():
    with pytest.raises(ValueError):
        build_graph(parse_fasta(">a\nACG\n>b\nACGT\n"))

def test_duplicate_ids():
    with pytest.raises(ValueError):
        parse_fasta(">x\nAC\n>x\nAG\n")
