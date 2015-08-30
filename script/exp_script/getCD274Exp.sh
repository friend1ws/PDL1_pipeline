#! /bin/sh
#$ -S /bin/sh
#$ -cwd

export PATH=/home/yshira/bin/samtools-0.1.18:$PATH
export PATH=/home/yshira/bin/bedtools-2.17.0/bin:$PATH

INPUT=$1
OUTPUT=$2

echo "samtools view -F 3844 -b -h ${INPUT} 9:5450502-5470567 | intersectBed -abam - -b ../data/CD274.bed -wao -bed -split > ${OUTPUT}.CD274.bed"
samtools view -F 3844 -b -h ${INPUT} 9:5450502-5470567 | intersectBed -abam - -b ../data/CD274.bed -wao -bed -split > ${OUTPUT}.CD274.bed

echo "python proc_CD274_exp.py ${OUTPUT}.CD274.bed > ${OUTPUT}"
python proc_CD274_exp.py ${OUTPUT}.CD274.bed > ${OUTPUT}

# rm -rf ${OUTPUT}.bam
# rm -rf ${OUTPUT}.bam.bai
# rm -rf ${OUTPUT}.CD274.bed

