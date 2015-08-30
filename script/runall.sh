#! /usr/bin/env bash

INPUT=$1
OUTPUTDIR=$2

while read line
do
    SAMPLE=`echo ${line} | cut -f 1 -d ' '`
    BAMPATH=`echo ${line} | cut -f 2 -d ' '`
    CHIMERAPATH=`echo ${line} | cut -f 3 -d ' '`

    if [ ! -d ${OUTPUTDIR}/fusion/${SAMPLE} ]
    then
        mkdir -p ${OUTPUTDIR}/fusion/${SAMPLE}  
    fi

    if [ ! -d ${OUTPUTDIR}/exp/${SAMPLE} ]
    then
        mkdir -p ${OUTPUTDIR}/exp/${SAMPLE}
    fi

    # echo "qsub -l s_vmem=6G,mem_req=6G fusion_script/fusionfusion.sh ${CHIMERAPATH} ${OUTPUTDIR}/fusion/${SAMPLE}"
    # qsub -l s_vmem=6G,mem_req=6G fusion_script/fusionfusion.sh ${CHIMERAPATH} ${OUTPUTDIR}/fusion/${SAMPLE} 

    # echo "qsub -l s_vmem=2G,mem_req=2G exp_script/getCD274Exp.sh ${BAMPATH} ${OUTPUTDIR}/exp/${SAMPLE}/CD274.exon.exp.txt"
    # qsub -l s_vmem=2G,mem_req=2G exp_script/getCD274Exp.sh ${BAMPATH} ${OUTPUTDIR}/exp/${SAMPLE}/CD274.exon.exp.txt 

    # echo "exp_script/getCD274Exp.sh ${BAMPATH} ${OUTPUTDIR}/exp/${SAMPLE}/CD274.exon.exp.txt"
    # sh exp_script/getCD274Exp.sh ${BAMPATH} ${OUTPUTDIR}/exp/${SAMPLE}/CD274.exon.exp.txt

done < ${INPUT}

echo "python summarize_script/summary_phs.py ${INPUT} ${OUTPUTDIR}/exp ${OUTPUTDIR}/fusion > ${OUTPUTDIR}/summary.txt"
python summarize_script/summary_phs.py ${INPUT} ${OUTPUTDIR}/exp ${OUTPUTDIR}/fusion > ${OUTPUTDIR}/summary.txt

