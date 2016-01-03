#! /bin/sh
#$ -S /bin/sh
#$ -cwd

JUNCTIONFILE=$1
OUTPUTDIR=$2
THRES=$3

python splicing_script/get_splicing_CD274.py ${JUNCTIONFILE} > ${OUTPUTDIR}/CD274.splicing.txt

python splicing_script/get_abnormal.py ${OUTPUTDIR}/CD274.splicing.txt ${THRES} > ${OUTPUTDIR}/CD274.splicing.abnormal.txt
