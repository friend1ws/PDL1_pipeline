#! /usr/bin/env python

import os, glob


allfiles = glob.glob("/home/ogawalab/workspace/h_tanaka/prj_8788/results/phs000689_RNA-Seq/out/20150820/star/SRR*")

for file in sorted(allfiles):
    sample_name = os.path.basename(file)
    bam_path = file + "/sequence1_Aligned.sortedByCoord.out.bam"
    chimera_path = file + "/sequence1_Chimeric.out.sam"

    print sample_name + '\t' + bam_path + '\t' + chimera_path


