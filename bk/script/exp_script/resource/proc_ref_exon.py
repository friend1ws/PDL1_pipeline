#! /usr/bin/env python

import sys, gzip

inputFile = sys.argv[1]
hIN = gzip.open(inputFile, 'r')

for line in hIN:
    F = line.rstrip('\n').split('\t')

    chr = F[2]
    starts = F[9].split(',')
    ends = F[10].split(',')
    strand = F[3]
    exonNum = int(F[8])
    gene = F[1]
    symbol = F[12]

    chr = chr.replace('chr', '')

    for i in range(0, len(starts) - 1):
        key = chr + '\t' + starts[i] + '\t' + ends[i]
        if strand == "+":
            print key + '\t' + gene + "_" + str(i) + '\t' + symbol + '\t' + "+"
        else:
            print key + '\t' + gene + "_" + str(exonNum - i - 1) + '\t' + symbol + '\t' + "-"

hIN.close()


