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


INPUT=$1
OUTPUT=$2

echo "samtools view -b -h ${INPUT} 9:5467839-5470567 > ${OUTPUT}.bam"
samtools view -b -h ${INPUT} 9:5467839-5470567 > ${OUTPUT}.bam
 
echo "fisher single -1 ${OUTPUT}.bam -o ${OUTPUT} -r /home/w3varann/database/GRCh37/GRCh37.fa -s /home/yshira/bin/samtools-1.2/samtools -p 0.05"
fisher single -1 ${OUTPUT}.bam -o ${OUTPUT} -r /home/w3varann/database/GRCh37/GRCh37.fa -s /home/yshira/bin/samtools-1.2/samtools -p 0.05


