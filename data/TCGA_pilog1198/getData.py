#! /usr/bin/env python

import os, glob


allfiles = glob.glob("/home/ogawalab/workspace/h_tanaka/150730_TCGA_CD274/results/CD274_RNA_150731//out/20150805/star/TCGA-*")

for file in sorted(allfiles):
    sampleName = os.path.basename(file)
    print sampleName + '\t' + file + "/sequence1_Aligned.sortedByCoord.out.bam"


