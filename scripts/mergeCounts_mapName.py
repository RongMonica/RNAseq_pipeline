import pandas as pd

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
    return gene_map

# Get the mapping
gene_map = parse_gtf('HISAT2/Homo_sapiens.GRCh38.106.gtf')

# Process counts files and merge them into a single file
files = ['sample1_counts.txt', 'sample2_counts.txt', 'sample3_counts.txt']

dfs = []
for f in files: 
    df = pd.read_csv(f, sep="\t", comment="#")
    sample_name = f.split("_")[0]
    df = df[["Geneid", df.columns[-1]]]
    df.columns = ["Geneid", sample_name]
    dfs.append(df)

merged = dfs[0]
for df in dfs[1:]:
    merged = merged.merge(df, on="Geneid", how="outer")

merged = merged.fillna(0)

# Add gene names
merged['GeneName'] = merged['Geneid'].map(gene_map)

merged.to_csv("merged_counts.txt", sep="\t", index=False)