#! /usr/bin/env python

import os, csv

def read_input(input_file):

    sample2fastq = {}
    sample_list = {}
    with open(input_file, 'r') as hin:
        csv_obj = csv.reader(hin)
        for cells in csv_obj:
             
            sample = cells[0] 
            fastq1 = cells[1]
            fastq2 = cells[2]

            if sample in sample_list: raise ValueError("Duplicated sample ID: " + sample)
            if not os.path.exists(fastq1): raise ValueError("File Not Exist:" + fastq1)
            if not os.path.exists(fastq2): raise ValueError("File Not Exist:" + fastq2)
        
            sample_list[sample] = 1
            sample2fastq[sample] = [fastq1, fastq2]

    return sample2fastq
