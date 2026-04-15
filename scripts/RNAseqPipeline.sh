#!/bin/bash

SECONDS=0

#change working directory
cd ~/GitHub_Rong/RNAseq_pipline

#STEP1: Run fastqc
fastqc data/SRR390728_1.fastq data/SRR390728_2.fastq -o data/fastqc_output

#Run trimmomatic to trim reads with poor quality
java -jar ~/GitHub_Rong/RNAseq_pipline/tools/Trimmomatic-0.39/trimmomatic-0.39.jar PE -threads 4 data/SRR390728_1.fastq data/SRR390728_2.fastq data/SRR390728_1_trimmed.fastq data/SRR390728_1_unpaired.fastq data/SRR390728_2_trimmed.fastq data/SRR390728_2_unpaired.fastq ILLUMINACLIP:tools/Trimmomatic-0.39/adapters/TruSeq3-PE.fa:2:30:10 TRAILING:10 -phred33
echo "Trimmomatic finished running!"

fastqc data/SRR390728_1_trimmed.fastq data/SRR390728_2_trimmed.fastq -o data/fastqc_output
#STEP2: Run HISAT2
#makdir HISAT2
#get the genome indices
#wget https://genome-idx.s3.amazonaws.com/hisat/grch38_genome.tar.gz
#run alignment   
#add in --rna-strandness RF for stranded reads
hisat2 -q -x HISAT2/grch38/genome -1 data/SRR390728_1.fastq -2 data/SRR390728_2.fastq | samtools sort - -o HISAT2/SRR390728_trimmed.bam
echo "HISAT2 finished running!"
#STEP3: Run featureCounts - Quantification

#get gtf
#human: wget http://ftp.ensembl.org/pub/release-106/gtf/homo_sapiens/Homo_sapiens.GRCh38.106.gtf.gz
#mouse: wget ftp://ftp.ensembl.org/pub/release-110/gtf/mus_musculus/Mus_musculus.GRCm39.110.gtf.gz
featureCounts -p --countReadPairs -s 0 -a HISAT2/Homo_sapiens.GRCh38.106.gtf -o quants/SRR390728_featureCounts.txt HISAT2/SRR390728_trimmed.bam
echo "featureCounts finished running!"

duration=$SECONDS
echo "$(($duration / 60)) minutes and $(($duration % 60)) seconds elapsed."