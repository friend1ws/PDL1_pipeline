#! /usr/bin/env python

import sys, glob

sampleList = sys.argv[1]
expDir = sys.argv[2]
fusionDir = sys.argv[3]

hIN = open(sampleList, 'r')
for line in hIN:
    F = line.rstrip('\n').split('\t')
    sample = F[0]

    targetExpDir = glob.glob(expDir + "/" + sample + "*")
    targetFusionDir = glob.glob(fusionDir + "/" + sample + "*")

    expRatio = "---"
    if len(targetExpDir) > 0:

        hIN2 = open(targetExpDir[0] + "/CD274.exon.exp.txt", "r")
        tmp1 = 10.0
        tmp2 = 10.0
        for line in hIN2:
            F2 = line.rstrip('\n').split('\t')
            if F2[0] == "CD274_3": tmp1 = float(F2[1])
            if F2[0] == "CD274_UTR": tmp2 = float(F2[1])
        
        expRatio = tmp1 / tmp2

    fusion = "---" 
    if len(targetFusionDir) > 0:
    
        hIN2 = open(targetFusionDir[0] + "/star.fusion.result.txt", "r")
        for line in hIN2:
            F2 = line.rstrip('\n').split('\t')
            if F2[8] == "CD274" or F2[9] == "CD274":
                fusion = True

        if fusion == "---": fusion = False

    if expRatio != "---" and fusion != "---":
        print sample + '\t' + str(expRatio) + '\t' + str(fusion)
        
        
