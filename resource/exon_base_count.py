#! /usr/bin/env python

from stage_task import *

class Exon_base_count(Stage_task):

    task_name = "exon_base_count"

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
export LD_LIBRARY_PATH={ld_library_path}:$LD_LIBRARY_PATH
export PYTHONPATH={pythonpath}


{samtools} view -F 3844 -b -h {input_bam} {region} | {bedtools} intersect -abam - -b {exon_bed} -wao -bed -split > {output}.CD274.bed

python {pdl1_pipeline_path}/resource/proc_CD274_exp.py {output}.CD274.bed > {output}
 
rm -rf {output}.CD274.bed

"""

    def __init__(self, qsub_option, script_dir, log_dir):
        super(Exon_base_count, self).__init__(qsub_option, script_dir, log_dir)

