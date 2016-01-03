#! /usr/bin/env python

import sys

input_file = sys.argv[1]
thres = int(sys.argv[2])

hIN = open(input_file, 'r')

for line in hIN:
    F = line.rstrip('\n').split('\t')
    
    # remove cannonical
    if F[5] == "1": continue
        
    # filter those with little number supporting reads
    if int(F[6]) < thres: continue

    print '\t'.join(F)

