#!/bin/bash
#$ -S /bin/bash         # set shell in UGE
#$ -cwd                 # execute at the submitted dir
#$ -e log/             # log file directory
#$ -o log/             # log file directory

pwd                     # print current working directory
hostname                # print hostname
date                    # print date
set -xv
export PERL5LIB=/home/w3varann/.local/lib/perl/lib:/home/w3varann/.local/lib/perl/lib/perl5:/home/w3varann/.local/lib/perl/lib/perl5/x86_64-linux-thread-multi

chimeric_sam=$1
chimeric_junction=$2
out_prefix=$3

star_fusion=/home/w3varann/tools/STAR-Fusion-master/STAR-Fusion
gtf_file=/home/w3varann/database/GTF/Homo_sapiens.GRCh37.74.gtf

${star_fusion} \
    --chimeric_out_sam ${chimeric_sam} \
    --chimeric_junction ${chimeric_junction} \
    --ref_GTF ${gtf_file} \
    --out_prefix ${out_prefix} 

