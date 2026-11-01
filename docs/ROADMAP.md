# Scientific roadmap

## P0: dependable foundation (this PR)
- [x] FASTA parsing / alphabet validation
- [x] Position-wise graph for equally aligned sequences
- [x] Sample haplotype counts, Shannon and nucleotide diversity
- [x] CLI, API, tests, synthetic examples
- [ ] Continuous integration with dependency vulnerability checks

## P1: real sequencing formats
- [ ] FASTQ quality assessment and read error profiles
- [ ] BAM/CRAM via pysam; VCF via cyvcf2/pysam
- [ ] Paired reads, strand bias, quality filters, coverage, UMI support
- [ ] GFA 1.0 import/export, coordinate and path validation
- [ ] Genome annotation via GFF3/GenBank; lineage provenance

## P2: genuine quasispecies methods
- [ ] Haplotype assembly and phasing; validation on synthetic truth sets
- [ ] Indels/structural variation; ambiguous bases and circular/segmented genomes
- [ ] Sequencing-error models and detection limits
- [ ] Bootstrap uncertainty, biological replicates, diversity indices
- [ ] Comparison with established tools, simulated mixtures and long reads

## P3: multi-omics and experimental integration
- [ ] Environmental sampling and phage host-range assays with provenance
- [ ] Expression matrices, proteins, metabolomics and interactions
- [ ] NCBI/ENA/IMG-VR/MGnify/UniProt adapters with rate limits and attribution
- [ ] PostgreSQL schema and Parquet/DuckDB analytics
- [ ] Workflow engines and reproducible HPC/SLURM jobs

## P4: interactive interface
- [ ] React+TypeScript+Vite dashboard
- [ ] D3/cytoscape graph navigation with bounded layout
- [ ] Privacy, authentication, access controls and audit events
- [ ] Validated report exports and visual comparisons

Metrics and association tests must control for sequencing depth, genome length, sample size, host sampling and phylogenetic relatedness. Never interpret graph complexity alone as host-range causality.
