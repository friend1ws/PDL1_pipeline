#! /bin/bash
#$ -S /bin/bash
#$ -cwd
#$ -e log/ -o log/

export PYTHONHOME=/usr/local/package/python2.7/2.7.8
export PATH=${PYTHONHOME}/bin:${PATH}
export LD_LIBRARY_PATH=/home/yshira/.local/lib:${PYTHONHOME}/lib:${LD_LIBRARY_PATH}
export PYTHONPATH=/home/yshira/.local/lib/python2.7/site-packages
export PATH=/home/yshira/.local/bin:${PATH}

INPUT=$1
OUTPUT=$2

REF=/home/yshira/GenomonVirusChecker/resource/viral.genomic.cancer.fasta


/home/w3varann/genomon_pipeline-2.0.2/tools/biobambam-0.0.191/bin//bamtofastq \
    collate=1 \
    exclude=QCFAIL,SECONDARY,SUPPLEMENTARY \
    filename=${INPUT} \
    F=${OUTPUT}.seq1.fastq \
    F2=${OUTPUT}.seq2.fastq \
    T=${OUTPUT}.temp \
    S=${OUTPUT}.single.fastq \
    O=${OUTPUT}.unmatch1 \
    O2=${OUTPUT}.unmatch2


genomon_virus_checker -q 35 ${OUTPUT}.seq1.fastq ${OUTPUT}.seq2.fastq ${OUTPUT} ${REF}

