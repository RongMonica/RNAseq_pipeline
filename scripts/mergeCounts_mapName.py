import pandas as pd
from pathlib import Path

# Parse GTF file to get gene_id -> gene_name mapping
def parse_gtf(gtf_file):
    gene_map = {}
    with open(gtf_file) as f:
        for line in f:
            if line.startswith('#') or line.strip() == '':
                continue
            fields = line.strip().split('\t')
            if fields[2] == 'gene':  # Only gene lines
                attributes = fields[8]
                gene_id = None
                gene_name = None
                for attr in attributes.split(';'):
                    attr = attr.strip()
                    if attr.startswith('gene_id'):
                        gene_id = attr.split('"')[1]
                    elif attr.startswith('gene_name'):
                        gene_name = attr.split('"')[1]
                if gene_id and gene_name:
                    gene_map[gene_id] = gene_name
    for gene_id, gene_name in list(gene_map.items())[:5]:
        print(gene_id, gene_name)
        
    return gene_map

# Process counts files and merge them into a single DataFrame
def merge_files(files):
    dfs = []
    for f in files: 
        df = pd.read_csv(f, sep="\t", comment="#")
        sample_name = f.name.split("_")[0]
        df = df[["EntrezID", df.columns[-1]]]
        df.columns = ["EntrezID", sample_name]
        dfs.append(df)

    merged = dfs[0]
    for df in dfs[1:]:
        merged = merged.merge(df, on="EntrezID", how="outer")

    merged = merged.fillna(0)
    return merged

# Get the mapping and add gene names to the merged DataFrame. Return the final .txt file with gene names
def map_gene_names(merged, gtf_dir, data_dir):
    gene_map = parse_gtf(gtf_dir / 'Mus_musculus.GRCm39.110.gtf')
    merged['EntrezID'] = merged['EntrezID'].map(gene_map)
    output_file = data_dir / 'merged_counts.txt'
    merged.to_csv(output_file, sep="\t", index=False)

if __name__ == "__main__":
    project_root = Path.cwd().parent
    data_dir = project_root / 'data'
    gtf_dir = project_root / 'HISAT2'
    files = list(data_dir.glob('GSM1480*.txt'))
    merged = merge_files(files)
    map_gene_names(merged, gtf_dir, data_dir)
