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

FILEPATH=$1
OUTPUTDIR=$2

echo "fusionfusion --star ${FILEPATH} --out ${OUTPUTDIR} --param fusion_script/param.cfg"
fusionfusion --star ${FILEPATH} --out ${OUTPUTDIR} --param fusion_script/param.cfg

