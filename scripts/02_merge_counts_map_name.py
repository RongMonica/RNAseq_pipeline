from pathlib import Path

import pandas as pd


def get_attribute_value(attributes, key):
    for attr in attributes.split(";"):
        attr = attr.strip()
        if attr.startswith(f'{key} "'):
            return attr.split('"')[1]
    return None


def parse_geneid_gtf(gtf_file):
    """Build a mapping from Ensembl GeneID to gene_name from a GTF file."""
    gene_map = {}

    with open(gtf_file) as handle:
        for line in handle:
            if line.startswith("#") or not line.strip():
                continue

            fields = line.rstrip("\n").split("\t")
            if len(fields) < 9 or fields[2] != "gene":
                continue

            gene_id = None
            gene_name = None
            for attr in fields[8].split(";"):
                attr = attr.strip()
                if attr.startswith("gene_id"):
                    gene_id = attr.split('"')[1].split(".", 1)[0]
                elif attr.startswith("gene_name"):
                    gene_name = attr.split('"')[1]

            if gene_id and gene_name:
                gene_map[gene_id] = gene_name

    return gene_map


def parse_entrez_gtf(gtf_file):
    """Build a mapping from EntrezID to gene name from a RefSeq-style GTF file."""
    gene_map = {}

    with open(gtf_file) as handle:
        for line in handle:
            if line.startswith("#") or not line.strip():
                continue

            fields = line.rstrip("\n").split("\t")
            if len(fields) < 9 or fields[2] != "gene":
                continue

            attributes = fields[8]
            gene_name = get_attribute_value(attributes, "gene")
            entrez_id = None

            for attr in attributes.split(";"):
                attr = attr.strip()
                if attr.startswith('db_xref "GeneID:'):
                    entrez_id = attr.split("GeneID:", 1)[1].split('"')[0]
                    break

            if entrez_id and gene_name:
                gene_map[entrez_id] = gene_name

    return gene_map


def get_id_column(id_type):
    if id_type == "EntrezID":
        return "EntrezID"
    if id_type == "GeneID":
        return "GeneID"
    raise ValueError(f"Unsupported id type: {id_type}")


def read_count_file(count_file, id_column):
    df = pd.read_csv(count_file, sep="\t", comment="#")

    if id_column not in df.columns:
        raise ValueError(f"{id_column} not found in {count_file}")

    sample_name = count_file.name.split("_")[0]
    sample_df = df[[id_column, df.columns[-1]]].copy()
    sample_df.columns = ["GeneID", sample_name]

    if id_column == "GeneID":
        sample_df["GeneID"] = sample_df["GeneID"].astype(str).str.split(".", n=1).str[0]
    else:
        sample_df["GeneID"] = sample_df["GeneID"].astype(str).str.strip()

    return sample_df


def merge_files(files, id_type):
    id_column = get_id_column(id_type)
    merged = None

    for count_file in files:
        sample_df = read_count_file(count_file, id_column)
        if merged is None:
            merged = sample_df
        else:
            merged = merged.merge(sample_df, on="GeneID", how="outer")

    if merged is None:
        raise ValueError("No count files were found to merge.")

    return merged.fillna(0)


def map_gene_names(merged, id_type, gtf_file=None, entrez_gtf_file=None):
    merged = merged.copy()

    if id_type == "GeneID":
        if gtf_file is None or not gtf_file.exists():
            raise FileNotFoundError(f"GTF file not found: {gtf_file}")
        gene_map = parse_geneid_gtf(gtf_file)
    elif id_type == "EntrezID":
        if entrez_gtf_file is None or not entrez_gtf_file.exists():
            raise FileNotFoundError(f"Entrez GTF file not found: {entrez_gtf_file}")
        gene_map = parse_entrez_gtf(entrez_gtf_file)
    else:
        raise ValueError(f"Unsupported id type: {id_type}")

    merged.insert(1, "gene_name", merged["GeneID"].map(gene_map))
    return merged


def main():
    project_root = Path.cwd()
    data_dir = project_root / "data"
    pattern = "GSM1480*.txt"
    map_by = "EntrezID"  # Change to "GeneID" when your count files use GeneID.
    gtf_file = project_root / "HISAT2" / "Mus_musculus.GRCm39.110.gtf"
    entrez_gtf_file = project_root / "HISAT2" / "GCF_000001635.27_GRCm39_genomic.gtf"
    output_file = data_dir / "merged_counts.txt"

    files = sorted(data_dir.glob(pattern))

    merged = merge_files(files, map_by)
    merged = map_gene_names(
        merged,
        id_type=map_by,
        gtf_file=gtf_file,
        entrez_gtf_file=entrez_gtf_file,
    )

    merged.to_csv(output_file, sep="\t", index=False)
    print(f"Saved merged counts to {output_file}")


if __name__ == "__main__":
    main()
