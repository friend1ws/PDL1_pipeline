#! /usr/bin/env bash

while read line
do
    SAMPLE=`echo ${line} | cut -f 1 -d ' '`
    FILEPATH=`echo ${line} | cut -f 2 -d ' '`

    if [ ! -d ../result/${SAMPLE} ]
    then
        mkdir -p ../result/${SAMPLE}
    fi

    echo "qsub -l s_vmem=6G,mem_req=6G fusionfusion.sh ${FILEPATH} ../result/${SAMPLE}"
    qsub -l s_vmem=6G,mem_req=6G fusionfusion.sh ${FILEPATH} ../result/${SAMPLE}

done < ../data/sample2path.txt
