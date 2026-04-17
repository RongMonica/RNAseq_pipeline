# RNA-seq Pipeline

This repository contains my RNA-seq analysis workflow, from read preprocessing and quantification to differential expression analysis and downstream DEG interpretation.

In this project, I use:

- shell scripting for preprocessing and quantification
- Python for count-table merging and gene-name annotation
- Jupyter notebooks for differential expression analysis and exploratory downstream interpretation

## Workflow Overview

The pipeline is organized into four main steps:

1. `scripts/01_rnaseq_preprocess_quantify.sh`
   Runs read-level preprocessing and quantification steps such as `FastQC`, `Trimmomatic`, `HISAT2`, `samtools`, and `featureCounts`.

2. `scripts/02_merge_counts_map_name.py`
   Merges per-sample count files into one count matrix and inserts a `gene_name` column by parsing a GTF annotation file. The script supports count tables that use either Ensembl gene IDs or EntrezID, which is useful when working with raw count files downloaded from public databases.

3. `scripts/03_pyDEseq2_analysis.ipynb`
   Loads the merged count matrix, prepares sample metadata, runs `pyDESeq2`, and exports differential expression results.

4. `scripts/04_deg_visualization_enrichment.ipynb`
   Ongoing notebook for downstream DEG visualization and enrichment analysis after DESeq2 output has been generated.

## Repository Structure

```text
RNAseq_pipeline/
├── README.md
├── .gitignore
├── scripts/
│   ├── 01_rnaseq_preprocess_quantify.sh
│   ├── 02_merge_counts_map_name.py
│   ├── 03_pyDEseq2_analysis.ipynb
│   └── 04_deg_visualization_enrichment.ipynb
└── quants/
    ├── SRR390728_featureCounts.txt
    ├── SRR390728_featureCounts.txt.summary
    ├── GSE60450_merged_raw_counts.txt
    └── GSE60450_deseq2_results.csv
```

## Inputs and Outputs

### Typical Inputs

- raw FASTQ files in `data/`
- reference genome index and annotation files in `HISAT2/`
- sample count files used for merging

### Key Outputs

- `quants/SRR390728_featureCounts.txt`
  Raw gene-level quantification from `featureCounts`

- `quants/GSE60450_merged_raw_counts.txt`
  Merged count matrix with `GeneID` and `gene_name`

- `quants/GSE60450_deseq2_results.csv`
  Differential expression results exported from the `pyDESeq2` notebook

## Environment and Dependencies

I use a mix of command-line bioinformatics tools and Python packages in this repository.

### Command-line Tools

- `fastqc`
- `trimmomatic`
- `hisat2`
- `samtools`
- `featureCounts`

### Python Packages

- `pandas`
- `pathlib`
- `pydeseq2`
- Jupyter notebook environment

I use a local virtual environment such as `rnaseq_env/` for the Python and notebook-based analysis steps, and I exclude it from version control.

## How To Run

### 1. Preprocess and Quantify Reads

Run the shell script:

```bash
bash scripts/01_rnaseq_preprocess_quantify.sh
```

This step performs QC, trimming, alignment, and count quantification.

### 2. Merge Count Files and Add Gene Names

Run:

```bash
python3 scripts/02_merge_counts_map_name.py
```

This produces a merged counts table in `quants/`.

### 3. Run Differential Expression Analysis

Open and run:

```text
scripts/03_pyDEseq2_analysis.ipynb
```

This notebook:

- loads merged counts
- prepares metadata
- runs `pyDESeq2`
- saves DESeq2 results to `quants/GSE60450_deseq2_results.csv`

### 4. Continue With Downstream Interpretation

Use:

```text
scripts/04_deg_visualization_enrichment.ipynb
```

This notebook is still in progress. Suggested next analyses include:

- DEG filtering by `padj` and `log2FoldChange`
- volcano plots
- heatmaps
- KEGG pathway or GO enrichment

## Notes

- I store selected outputs in `quants/` for convenience and reproducibility.
- I exclude large raw data, alignment files, and environment folders through `.gitignore`.
- The preprocessing shell script currently uses hard-coded paths and may need to be adjusted for a different machine or project directory.

## Planned Future Improvements

- consider moving preprocessing into a workflow manager such as Snakemake or Nextflow for better reproducibility

## Status

This repository is my actively developed learning and analysis project for RNA-seq processing, count merging, DESeq2-based differential expression, and downstream DEG interpretation. The DEG visualization and enrichment stage is ongoing.
