#!/usr/bin/env bash
set -euo pipefail

SECONDS=0

#set up directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="${PROJECT_DIR:-$(cd "$SCRIPT_DIR/.." && pwd)}"
SOURCE_DIR="${SOURCE_DIR:-$PROJECT_DIR/data}"
DEST_DIR="${DEST_DIR:-$PROJECT_DIR/quants}"
TOOL_DIR="${TOOL_DIR:-$PROJECT_DIR/tools}"
MODE="${MODE:-dry-run}"

fail() {
    echo "$*" >&2
    exit 1
}

[[ "$MODE" == "dry-run" || "$MODE" == "move" ]] || fail "MODE must be dry-run or move"
[[ -d "$SOURCE_DIR" ]] || fail "SOURCE_DIR does not exist"
mkdir -p "$DEST_DIR" "$SOURCE_DIR/fastqc_output"

#STEP1: Run fastqc
fastqc "$SOURCE_DIR/SRR390728_1.fastq" "$SOURCE_DIR/SRR390728_2.fastq" -o "$SOURCE_DIR/fastqc_output"

#Run trimmomatic to trim reads with poor quality
java -jar "$TOOL_DIR/Trimmomatic-0.39/trimmomatic-0.39.jar" PE \
    -threads 4 \
    "$SOURCE_DIR/SRR390728_1.fastq" "$SOURCE_DIR/SRR390728_2.fastq" \
    "$SOURCE_DIR/SRR390728_1_trimmed.fastq" "$SOURCE_DIR/SRR390728_1_unpaired.fastq" \
    "$SOURCE_DIR/SRR390728_2_trimmed.fastq" "$SOURCE_DIR/SRR390728_2_unpaired.fastq" \
    ILLUMINACLIP:"$TOOL_DIR/Trimmomatic-0.39/adapters/TruSeq3-PE.fa":2:30:10 \
    TRAILING:10 \
    -phred33
echo "Trimmomatic finished running!"

fastqc "$SOURCE_DIR/SRR390728_1_trimmed.fastq" \
    "$SOURCE_DIR/SRR390728_2_trimmed.fastq" \
    -o "$SOURCE_DIR/fastqc_output"
#STEP2: Run HISAT2
#makdir HISAT2
#get the genome indices
#wget https://genome-idx.s3.amazonaws.com/hisat/grch38_genome.tar.gz
#run alignment   
#add in --rna-strandness RF for stranded reads
hisat2 -q -x "$PROJECT_DIR/HISAT2/grch38/genome" \
    -1 "$SOURCE_DIR/SRR390728_1_trimmed.fastq" \
    -2 "$SOURCE_DIR/SRR390728_2_trimmed.fastq" \
    | samtools sort - -o "$PROJECT_DIR/HISAT2/SRR390728_trimmed.bam"
echo "HISAT2 finished running!"
#STEP3: Run featureCounts - Quantification

#get gtf
#human: wget http://ftp.ensembl.org/pub/release-106/gtf/homo_sapiens/Homo_sapiens.GRCh38.106.gtf.gz
#mouse: wget ftp://ftp.ensembl.org/pub/release-110/gtf/mus_musculus/Mus_musculus.GRCm39.110.gtf.gz
featureCounts -p --countReadPairs -s 0 \
    -a "$PROJECT_DIR/HISAT2/Homo_sapiens.GRCh38.106.gtf" \
    -o "$DEST_DIR/SRR390728_featureCounts.txt" \
    "$PROJECT_DIR/HISAT2/SRR390728_trimmed.bam"
echo "featureCounts finished running!"

duration=$SECONDS
echo "$(($duration / 60)) minutes and $(($duration % 60)) seconds elapsed."