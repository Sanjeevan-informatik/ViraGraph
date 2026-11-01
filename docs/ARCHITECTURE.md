# Architecture

## Implemented
- `src/viragraph/core.py`: strict FASTA reader, alphabet checks, haplotype counts, entropy, pairwise nucleotide diversity.
- `src/viragraph/graph.py`: positional DAG for aligned viral genomes with explicit sample paths.
- `src/viragraph/cli.py`: portable CLI and JSON exports.
- `src/viragraph/api.py`: optional validated FastAPI API; no execution of arbitrary user code.
- `tests/`: deterministic tests using synthetic inputs.

## Design principles
Preserve original raw reads and metadata with accession, assay, sample and processing provenance. Separate individual particles, samples and inferred viral populations. Use stable IDs and explicit missing-value semantics. Reject unaligned sequences rather than pretending they are phased. Maintain sequence orientation and coordinate conventions in all importers.

## Future programming languages
Python: orchestration, API, genomics, statistics.
Rust: memory-safe high-performance graph/index computation through a PyO3 extension.
C++: optional adapters to established sequence graph libraries.
R: statistics and Bioconductor ecosystem.
TypeScript/React/D3: web frontend, graph visualization and accessibility.
SQL/PostgreSQL: normalized metadata and analysis provenance.
Bash/Snakemake/Nextflow: reproducible sequencing workflows.
Docker: reproducible deployment.

## Proposed data model
Virus(taxon_id, genome_type, host_taxa); Sample(sample_id, collection_date, environment, protocol); Sequence(sequence_id, sample_id, accession, sha256); Variant(sample_id, position, ref, alt, depth, allele_frequency); Haplotype(sample_id, sequence, count, uncertainty); Graph(graph_id, provenance, nodes, edges, paths); HostRange(virus_id, host_id, assay, value, units); OmicsAssay(sample_id, assay_type, data_uri, reference_build, method); AnalysisRun(version, parameters, input_hashes, output_hashes).

## Security
No remote fetchers or automatic uploads in the MVP. Never trust user-supplied paths in server routes. Constrain payload sizes; no SQL string interpolation or shell execution. For production add authentication, quotas, per-user isolation, malware scanning on uploads, security headers, and retention controls. Host and location information may be sensitive and requires appropriate governance.
