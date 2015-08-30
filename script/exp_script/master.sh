#! /bin/sh
#$ -S /bin/sh
#$ -cwd

while read line;
do
    SAMPLE=`echo ${line} | cut -f 1 -d ' '`
    BAMPATH=`echo ${line} | cut -f 2 -d ' '`

    if [ ! -d ../result/${SAMPLE} ];
    then
        mkdir -p ../result/${SAMPLE}
    fi

    echo "sh getCD274Exp.sh ${BAMPATH} ../result/${SAMPLE}/CD274.exon.exp.txt "
    sh getCD274Exp.sh ${BAMPATH} ../result/${SAMPLE}/CD274.exon.exp.txt

done < ../data/sample2path.txt 
