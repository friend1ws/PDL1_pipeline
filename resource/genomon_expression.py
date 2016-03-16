#! /usr/bin/env python

from stage_task import *

class Genomon_expression(Stage_task):

    task_name = "genomon_expression"

    script_template = """
#!/bin/bash
#
# Set SGE
#
#$ -S /bin/bash         # set shell in UGE
#$ -cwd                 # execute at the submitted dir
pwd                     # print current working directory
hostname                # print hostname
date                    # print date
set -xv

# set python environment
export PYTHONHOME={pythonhome}
export PATH=$PYTHONHOME/bin:$PATH
export LD_LIBRARY_PATH={ld_library_path}
export PYTHONPATH={pythonpath}

TOTAL_READ=`{samtools} view {input_bam} | wc -l | cut -f 1 -d ' '`
SINGLE_READ=`{samtools} view -F 1 {input_bam} | wc -l | cut -f 1 -d ' '`

SINGLE_OR_PAIR=`echo "scale=3; $SINGLE_READ / $TOTAL_READ > 0.5" | bc`

echo $SINGLE_OR_PAIR

if [ $SINGLE_OR_PAIR = 0 ]
then
    {genomon_expression} {input_bam} {output_prefix} {ref_bed} {bedtools}
else
    {genomon_expression} --keep_improper_pair {input_bam} {output_prefix} {ref_bed} {bedtools}    
fi

"""

    def __init__(self, qsub_option, script_dir, log_dir):
        super(Genomon_expression, self).__init__(qsub_option, script_dir, log_dir)

