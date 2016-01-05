#! /usr/bin/env python

from stage_task import *

class Virus_count(Stage_task):

    task_name = "virus_count"

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

{genomon_virus_checker} -q {match_thres} {input_fastq_1} {input_fastq_2} {output_prefix} {virus_ref}


if [ -s {output_prefix}.virus.base.txt ]
then
    VIRUS=`sort -k 2 -n -r {output_prefix}.virus.base.txt | head -n 1 | cut -f 1 -d '	'`
    BASE=`sort -k 2 -n -r {output_prefix}.virus.base.txt | head -n 1 | cut -f 2 -d '	'`
    if [ $BASE -ge {select_thres} ]
    then
        echo "$VIRUS" > {output_prefix}.virus.selected.txt 
    else
        echo "None" > {output_prefix}.virus.selected.txt 
    fi
else
    echo "None" > {output_prefix}.virus.selected.txt 
fi
"""

    def __init__(self, qsub_option, script_dir, log_dir):
        super(Virus_count, self).__init__(qsub_option, script_dir, log_dir)

