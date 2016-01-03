#! /usr/bin/env python

import sys

inputFile = sys.argv[1]
hIN = open(inputFile, 'r')

exon2base = {}
for line in hIN:
    F = line.rstrip('\n').split('\t')

    if F[16] == "-1": continue

    if F[16] not in exon2base:
        exon2base[F[16]] = 0

    exon2base[F[16]] = exon2base[F[16]] + int(F[18])

hIN.close()

for key in sorted(exon2base):
    print key + '\t' + str(exon2base[key])

