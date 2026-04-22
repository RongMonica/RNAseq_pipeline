# RNA-seq Pipeline

This repository contains my RNA-seq analysis workflow, from raw-read preprocessing and quantification to differential expression analysis, visualization, and downstream functional interpretation.

The project combines:

- shell scripting for read preprocessing, alignment, and quantification
- Python for count-table merging and gene-name annotation
- Jupyter notebooks for DESeq2 analysis, DEG visualization, and functional enrichment

## Workflow Overview

The pipeline is organized into five main steps:

1. `scripts/01_rnaseq_preprocess_quantify.sh`
   Runs read-level preprocessing and quantification with tools such as `FastQC`, `Trimmomatic`, `HISAT2`, `samtools`, and `featureCounts`.

2. `scripts/02_merge_counts_map_name.py`
   Merges per-sample count files into one count matrix and inserts a `gene_name` column by parsing a GTF annotation file. The script supports count tables that use either Ensembl gene IDs or Entrez IDs.

3. `scripts/03_pyDEseq2_analysis.ipynb`
   Loads the merged count matrix and sample metadata, runs `pyDESeq2`, and exports differential expression results.

4. `scripts/04_deg_visualization.ipynb`
   Performs downstream DEG visualization, including PCA, volcano plot, MA plot, and a heatmap of top significant genes.

5. `scripts/05_functional_enrichment.ipynb`
   Performs functional enrichment analysis using significant DEGs and ranked gene lists, including:
   - GO Biological Process enrichment for upregulated and downregulated genes
   - KEGG pathway enrichment for upregulated and downregulated genes
   - GSEA on preranked differential expression results
   - summary bubble plot of enriched GSEA pathways
   - top `n` enrichment curves for the most significant upregulated and downregulated GSEA terms

## Repository Structure

```text
RNAseq_pipeline/
├── README.md
├── data/
├── HISAT2/
├── plots/
├── quants/
│   ├── GSE60450_deseq2_results.csv
│   ├── GSE60450_merged_raw_counts.txt
│   ├── GSE60450_metadata.csv
│   ├── GSE60450_significant_genes.csv
│   ├── GSE60450_vst_matrix.csv
│   ├── GSE60450_GO/
│   ├── GSE60450_KEGG/
│   └── GSE60450_GSEA/
├── scripts/
│   ├── 01_rnaseq_preprocess_quantify.sh
│   ├── 02_merge_counts_map_name.py
│   ├── 03_pyDEseq2_analysis.ipynb
│   ├── 04_deg_visualization.ipynb
│   └── 05_functional_enrichment.ipynb
├── tools/
└── rnaseq_env/
```

## Inputs and Outputs

### Typical Inputs

- raw FASTQ files in `data/`
- reference genome index and annotation files in `HISAT2/`
- per-sample count files used for merging
- sample metadata for differential expression analysis

### Key Outputs

- `quants/SRR390728_featureCounts.txt`
  Raw gene-level quantification from `featureCounts`

- `quants/GSE60450_merged_raw_counts.txt`
  Merged count matrix with `GeneID` and `gene_name`

- `quants/GSE60450_metadata.csv`
  Sample metadata used for DESeq2 analysis

- `quants/GSE60450_deseq2_results.csv`
  Differential expression results exported from the `pyDESeq2` notebook

- `quants/GSE60450_significant_genes.csv`
  Filtered set of significant DEGs used in downstream interpretation

- `quants/GSE60450_vst_matrix.csv`
  Variance-stabilized expression matrix used for exploratory visualization

### Functional Enrichment Outputs

#### GO Enrichment

- `quants/GSE60450_GO/GSE60450_GO_enrichment_up_results.csv`
- `quants/GSE60450_GO/GSE60450_GO_enrichment_down_results.csv`
- `quants/GSE60450_GO/GSE60450_GO_up_barplot.png`
- `quants/GSE60450_GO/GSE60450_GO_down_barplot.png`

These files summarize GO Biological Process enrichment results for upregulated and downregulated DEGs.

#### KEGG Enrichment

- `quants/GSE60450_KEGG/GSE60450_KEGG_enrichment_up_results.csv`
- `quants/GSE60450_KEGG/GSE60450_KEGG_enrichment_down_results.csv`
- `quants/GSE60450_KEGG/GSE60450_KEGG_up_barplot.png`
- `quants/GSE60450_KEGG/GSE60450_KEGG_down_barplot.png`

These files summarize KEGG pathway enrichment results for upregulated and downregulated DEGs.

#### GSEA Outputs

- `quants/GSE60450_GSEA/prerank_data.rnk`
- `quants/GSE60450_GSEA/gene_sets.gmt`
- `quants/GSE60450_GSEA/GSE60450_GSEA_enrichment_results.csv`
- `quants/GSE60450_GSEA/GSE60450_GSEA_summary_dotplot.png`
- `quants/GSE60450_GSEA/GSE60450_GSEA_up_Ribosome_curve.png`
- `quants/GSE60450_GSEA/GSE60450_GSEA_down_Focal_adhesion_curve.png`

These files include the preranked input used for GSEA, the tested gene-set collection, a table of enrichment results, a summary bubble plot, and example enrichment curves for the top positively and negatively enriched pathways.

## Requirements and Setup

To run this pipeline end to end, you need a combination of repository files, locally stored reference resources, command-line bioinformatics tools, and a Python notebook environment.

### What Is Included in This Repository

This GitHub repository contains the analysis scripts, notebooks, selected result files, and example output tables used in the workflow.

### Local Resources Required but Not Tracked in GitHub

The following resources are expected locally but are not committed to this repository:

- raw FASTQ files stored in a local `data/` directory
- HISAT2 genome index files and annotation references stored in a local `HISAT2/` directory
- optional local helper programs or utility files stored in `tools/`
- a local Python virtual environment such as `rnaseq_env/`

These folders are machine-specific or too large to keep under version control, so they should be created or linked locally before running the full pipeline.

## Environment and Dependencies

This repository uses a mix of command-line bioinformatics tools and Python packages.

### Command-line Tools

- `fastqc`
- `trimmomatic`
- `hisat2`
- `samtools`
- `featureCounts`

### Python Packages

- `pandas`
- `numpy`
- `matplotlib`
- `seaborn`
- `scikit-learn`
- `pydeseq2`
- `gseapy`
- Jupyter notebook environment

I use a local virtual environment such as `rnaseq_env/` for the Python and notebook-based analysis steps, and I exclude it from version control.

## How To Run

### 1. Preprocess and Quantify Reads

Run:

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

- loads merged counts and metadata
- runs `pyDESeq2`
- exports DESeq2 results to `quants/GSE60450_deseq2_results.csv`
- saves additional downstream-ready files such as significant-gene and VST matrices

### 4. Generate DEG Visualizations

Open and run:

```text
scripts/04_deg_visualization.ipynb
```

This notebook generates downstream visualizations for differential expression results, including:

- PCA plot
- volcano plot
- MA plot
- heatmap of top significant DEGs

Plots are saved to `plots/`.

### 5. Run Functional Enrichment Analysis

Open and run:

```text
scripts/05_functional_enrichment.ipynb
```

This notebook:

- filters significant genes using `padj < 0.05`
- separates upregulated and downregulated genes using `log2FoldChange > 1` and `< -1`
- performs GO enrichment with `GO_Biological_Process_2021`
- performs KEGG enrichment with `KEGG_2019_Mouse`
- runs GSEA from a preranked gene list
- generates enrichment summary plots and top-pathway enrichment curves

All functional enrichment outputs are written under `quants/GSE60450_GO/`, `quants/GSE60450_KEGG/`, and `quants/GSE60450_GSEA/`.

## Notes

- I store selected intermediate and final outputs in `quants/` for convenience and reproducibility.
- I exclude large raw data, alignment files, and local environment folders through `.gitignore`.
- The preprocessing shell script uses project-specific paths and may need to be adjusted for another machine or dataset.
- The enrichment notebook is currently configured for mouse pathway libraries in `gseapy`.

## Project Status

This repository is an actively developed RNA-seq analysis project covering:

- preprocessing and alignment
- gene-level quantification
- count-matrix assembly and annotation
- DESeq2-based differential expression analysis
- DEG visualization
- completed functional enrichment analysis, including GO, KEGG, MA plotting, and GSEA with both summary and pathway-level plots

The downstream enrichment section is now complete and documented in this README.
