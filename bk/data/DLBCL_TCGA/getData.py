#! /usr/bin/env python

import os, glob


allfiles = glob.glob("/home/yshira/project/DLBCL_tcga_rna/output/star/TCGA-*")

for file in sorted(allfiles):
    sample_name = os.path.basename(file)
    bam_path = glob.glob(file + "/*.Aligned.sortedByCoord.out.bam")
    chimera_path = glob.glob(file + "/*.Chimeric.out.sam")
    junc_path = glob.glob(file + "/*.SJ.out.tab")

    print sample_name + '\t' + bam_path[0] + '\t' + chimera_path[0] + '\t' + junc_path[0]


