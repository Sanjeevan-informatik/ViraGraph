# ViraGraph

An **independent, research-oriented prototype** for DNA/RNA virus sequence analysis, within-sample diversity, haplotypes and sequence-variation graph exploration. Not affiliated with the VirusREvolution consortium.

## Working foundation
- Python 3.11+ library: FASTA validation/parsing, SNP-based variation graph construction, haplotype frequencies, Shannon diversity and nucleotide diversity.
- FastAPI endpoints with input validation and safe request-size limits.
- CLI for FASTA metrics and variants; JSON graph export.
- Synthetic example viral data and pytest tests.
- Extension architecture for Rust/C++, R, TypeScript, GFA, VCF, sequencing pipelines and databases.

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev,api]"
pytest
viragraph summary examples/viral_sequences.fasta
viragraph graph examples/viral_sequences.fasta --output graph.json
uvicorn viragraph.api:app --reload
```

On Windows use `.venv\Scripts\activate`.

## Scope and scientific cautions

Graph construction currently aligns **equal-length, pre-aligned** DNA/RNA sequences and represents substitutions, not insertions, deletions or true long-range genome graph inference. Inferred sequences are treated as observed haplotypes without error correction, read phasing or abundance correction. The toy sample is synthetic. Never interpret demonstration metrics as validated biological conclusions.

## Planned data domains
Genomics: FASTQ, FASTA, BAM/CRAM, VCF/BCF, GFF3/GenBank, BED, GFA.
Populations: variant frequencies, haplotypes, entropy, nucleotide diversity, recombination, reassortment.
Multi-omics: RNA counts, proteomics mzML, metabolomics, methylation, structural PDB/mmCIF.
Metadata: taxonomy, host-range assays, sample provenance, environment and geographical coordinates.
Databases: NCBI Virus/SRA/ENA, IMG/VR, UniProt, PRIDE and MGnify using explicit provenance-aware importers.

See [architecture](docs/ARCHITECTURE.md) and [roadmap](docs/ROADMAP.md).
