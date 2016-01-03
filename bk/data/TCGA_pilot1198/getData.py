#! /usr/bin/env python

import os, glob


allfiles = glob.glob("/home/ogawalab/workspace/h_tanaka/150730_TCGA_CD274/results/CD274_RNA_150731//out/20150805/star/TCGA-*")

for file in sorted(allfiles):
    sample_name = os.path.basename(file)
    bam_path = file + "/sequence1_Aligned.sortedByCoord.out.bam"
    chimera_path = file + "/sequence1_Chimeric.out.sam"

    print sample_name + '\t' + bam_path + '\t' + chimera_path


