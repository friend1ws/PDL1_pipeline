#! /usr/bin/env python

import sys, glob

selectedFile = sys.argv[1]
expDir = sys.argv[2]
fusionDir = sys.argv[3]

hIN = open(selectedFile, 'r')
for line in hIN:
    F = line.rstrip('\n').split('\t')

    if F[0] == "GBMLGG": continue

    targetExpDir = glob.glob(expDir + "/" + F[1] + "*")
    targetFusionDir = glob.glob(fusionDir + "/" + F[1] + "*")

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
        print F[1] + '\t' + F[0] + '\t' + F[2] + '\t' + str(expRatio) + '\t' + str(fusion)
        
        
