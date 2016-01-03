#! /usr/bin/env python

from genomon_pipeline.stage_task import *

class Virus_count(Stage_task):

    task_name = "virus_count"

    script_template = """
#!/bin/bash
#
# Set SGE
#
#$ -S /bin/bash         # set shell in UGE
#$ -cwd                 # execute at the submitted dir
#$ -e {log}             # log file directory
#$ -o {log}             # log file directory
pwd                     # print current working directory
hostname                # print hostname
date                    # print date
set -xv

# set python environment
export PYTHONHOME={pythonhome}
export PATH=$PYTHONHOME/bin:$PATH
export LD_LIBRARY_PATH={ld_library_path}
export PYTHONPATH={pythonpath}

{genomon_virus_checker} -q {match_thres} {input_fastq_1} {input_fastq_2} {output} {virus_ref}
"""

    def __init__(self, qsub_option, script_dir):
        super(Virus_count, self).__init__(qsub_option, script_dir)

