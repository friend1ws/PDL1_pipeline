#! /usr/bin/env python

from stage_task import *

class Star_ref(Stage_task):

    task_name = "star_ref"

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

cat {human_ref} {virus_ref} > {output_dir}/reference.fa

{star} --runThreadN 8 \
        --runMode genomeGenerate \
        --genomeDir {output_dir} \
        --outFileNamePrefix {output_dir} \
        --genomeFastaFiles {output_dir}/reference.fa \
        --sjdbGTFfile {gtf_file} \
        --sjdbOverhang 100
"""

    def __init__(self, qsub_option, script_dir, log_dir):
        super(Star_ref, self).__init__(qsub_option, script_dir, log_dir)

