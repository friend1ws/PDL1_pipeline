#! /usr/bin/env python

import os, glob


allfiles = glob.glob("/home/ogawalab/workspace/h_tanaka/prj_8788/results/phs000532_RNA-Seq_Sample/out/20150902/star/SAMN00*")

for file in sorted(allfiles):
    sample_name = os.path.basename(file)
    bam_path = file + "/sequence1_Aligned.sortedByCoord.out.bam"
    chimera_path = file + "/sequence1_Chimeric.out.sam"

    print sample_name + '\t' + bam_path + '\t' + chimera_path


