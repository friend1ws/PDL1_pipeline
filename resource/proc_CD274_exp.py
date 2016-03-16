#! /usr/bin/env python

import sys

inputFile = sys.argv[1]
hIN = open(inputFile, 'r')

exon2base = {}
for line in hIN:
    F = line.rstrip('\n').split('\t')

    if F[16] == "-1": continue

    key = F[16] + '\t' + str(int(F[14]) - int(F[13]))

    if key not in exon2base:
        exon2base[key] = 0

    exon2base[key] = exon2base[key] + int(F[18])

hIN.close()

for key in sorted(exon2base):
    print key + '\t' + str(exon2base[key])


