#! /usr/bin/env python

from stage_task import *

class Fusionfusion(Stage_task):

    task_name = "fusionfusion"

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

{fusionfusion} --star {star_chimeric_sam} --out {output_prefix} --param {param_file}
"""

    def __init__(self, qsub_option, script_dir, log_dir):
        super(Fusionfusion, self).__init__(qsub_option, script_dir, log_dir)
