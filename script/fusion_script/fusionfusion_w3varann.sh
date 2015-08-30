#! /bin/sh
#$ -S /bin/sh
#$ -cwd
#$ -e log/ -o log/

# python
export PYTHONHOME=/usr/local/package/python2.7/2.7.8
export PATH=${PYTHONHOME}/bin:${PATH}
export LD_LIBRARY_PATH=/home/w3varann/.local/lib:${PYTHONHOME}/lib:${LD_LIBRARY_PATH}
export PYTHONPATH=/home/w3varann/.local/lib/python2.7/site-packages
export PATH=/home/w3varann/.local/bin/fusionfusion:${PATH}


FILEPATH=$1
OUTPUTDIR=$2

echo "fusionfusion --star ${FILEPATH} --out ${OUTPUTDIR} --param param.yaml"
fusionfusion --star ${FILEPATH} --out ${OUTPUTDIR} --param param.yaml

