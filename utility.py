#! /usr/bin/env python

import os, csv, glob

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


# function for listing up selected virus
def selected_virus_list(check_dir, thres):
    virus_list = []
    allfiles = glob.glob(check_dir + "/*/*.virus.base.txt")
    for file in allfiles:
        temp_base_count = 0
        temp_virus = None
        with open(file, 'r') as hin:
            for line in hin:
                F = line.rstrip('\n').split('\t')
                if int(F[1]) > temp_base_count and int(F[1]) > thres:
                    temp_base_count = int(F[1])
                    temp_virus = F[0]

        if temp_virus is not None and temp_virus not in virus_list: virus_list.append(temp_virus)

    return virus_list

# function for printing selected virus seq
def print_virus_seq(virus_fa, output_file, selected_virus):
# def print_virus_seq(human_fa, virus_fa, output_file, selected_virus):
    hout = open(output_file, 'w')

    """
    with open(human_fa, 'r') as hin:
        for line in hin:
            print >> hout, line.rstrip('\n')
    """
    print_on = False
    with open(virus_fa, 'r') as hin:
        for line in hin:
            if line.startswith('>'):
                print_on = True if line.startswith('>' + selected_virus) else False

            if print_on:
                print >> hout, line.rstrip('\n')

    hout.close()

