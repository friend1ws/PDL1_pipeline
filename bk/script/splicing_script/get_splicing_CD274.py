#! /usr/bin/env python

import sys

input_file = sys.argv[1]

hIN = open(input_file, 'r')

for line in hIN:
    F = line.rstrip('\n').split('\t')

    # remove splicing outside CD274
    if F[0] != "9": continue
    if int(F[1]) > 5470567: continue
    if int(F[2]) < 5450503: continue

    print '\t'.join(F)

