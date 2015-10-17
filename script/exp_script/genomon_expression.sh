#! /bin/sh
#$ -S /bin/sh
#$ -cwd
#$ -e log/ -o log/

# python
export PYTHONHOME=/usr/local/package/python2.7/2.7.8
export PATH=${PYTHONHOME}/bin:${PATH}
export LD_LIBRARY_PATH=/home/yshira/.local/lib:${PYTHONHOME}/lib:${LD_LIBRARY_PATH}
export PYTHONPATH=/home/yshira/.local/lib/python2.7/site-packages
export PATH=/home/yshira/.local/bin:${PATH}

BEDTOOLS=/home/yshira/bin/bedtools-2.17.0/bin
export PATH=${BEDTOOLS}:${PATH}

BAMPATH=$1
OUTDIR=$2
REFBED=$3

echo "genomon_expression ${BAMPATH} ${OUTDIR} ${REFBED} ${BEDTOOLS}"
genomon_expression ${BAMPATH} ${OUTDIR} ${REFBED} ${BEDTOOLS}

