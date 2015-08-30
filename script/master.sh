#! /usr/bin/env bash

INPUT=$1
OUTPUTDIR=$2

while read line
do
    SAMPLE=`echo ${line} | cut -f 1 -d ' '`
    BAMPATH=`echo ${line} | cut -f 2 -d ' '`

    if [ ! -d ${OUTPUTDIR}/fusion/${SAMPLE} ]
    then
        mkdir -p ${OUTPUTDIR}/fusion/${SAMPLE}  
    fi

    if [ ! -d ${OUTPUTDIR}/exp/${SAMPLE} ]
    then
        mkdir -p ${OUTPUTDIR}/exp/${SAMPLE}
    fi


    echo "qsub -l s_vmem=6G,mem_req=6G fusionfusion.sh ${BAMPATH} ${OUTPUTDIR}/fusion/${SAMPLE}"
    qsub -l s_vmem=6G,mem_req=6G fusionfusion.sh ${BAMPATH} ${OUTPUTDIR}/fusion/${SAMPLE} 

done < ${INPUT}

