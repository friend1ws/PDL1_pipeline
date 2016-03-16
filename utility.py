#! /usr/bin/env python

import os, csv, glob

def read_input_fastq(input_file):

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


def read_input_star_prefix(input_file):

    sample2star_prefix = {}
    sample_list = {}

    with open(input_file, 'r') as hin:
        csv_obj = csv.reader(hin)
        for cells in csv_obj:

            sample = cells[0]
            star_prefix = cells[1]

            if sample in sample_list: raise ValueError("Duplicated sample ID: " + sample)

            if not os.path.exists(star_prefix + ".Aligned.sortedByCoord.out.bam"):
                raise ValueError("File Not Exist:" + star_prefix + ".Aligned.sortedByCoord.out.bam")
            if not os.path.exists(star_prefix + ".Chimeric.out.sam"):
                raise ValueError("File Not Exist:" + star_prefix + ".Chimeric.out.sam")
            if not os.path.exists(star_prefix + ".SJ.out.tab"):
                raise ValueError("File Not Exist:" + star_prefix + ".SJ.out.tab")
            if not os.path.exists(star_prefix + ".Log.final.out"):
                raise ValueError("File Not Exist:" + star_prefix + ".Log.final.out")
            if not os.path.exists(star_prefix + ".Aligned.sortedByCoord.out.bam.bai"):
                raise ValueError("File Not Exist:" + star_prefix + ".Aligned.sortedByCoord.out.bam.bai")

            sample_list[sample] = 1
            sample2star_prefix[sample] = star_prefix

    return sample2star_prefix


# function for listing up selected virus
def selected_virus_list(check_dir):
    virus_list = []
    allfiles = glob.glob(check_dir + "/*/*.virus.selected.txt")
    for file in allfiles:
        temp_virus = "None"
        with open(file, 'r') as hin:
            line = hin.readlines()
            temp_virus = line[0].rstrip('\n')


        if temp_virus != "None" and temp_virus not in virus_list: virus_list.append(temp_virus)

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


def generate_virus_fusionfusion_param(input_param_file, output_param_file, reference):

    hout = open(output_param_file, 'w')
    with open(input_param_file, 'r') as hin:
        for line in hin:
            line = line.rstrip('\n')
            if line.startswith("reference_genome"):
                print >> hout, "reference_genome = " + reference
            else:
                print >> hout, line

    hout.close()



def get_sequence_with_virus(input_dir, sample_list_fastq):

    # generate list of linked_fastq file path
    bam_list = []
    for sample in sample_list_fastq:
        # check the selected virus
        with open(input_dir + "/virus_count/" + sample + "/" + sample + ".virus.selected.txt") as hin:
            line = hin.readlines()
            selected_virus = line[0].rstrip('\n')
            if selected_virus != "None":
                bam_list.append(input_dir + "/star/" + sample + "/" + sample + ".Aligned.sortedByCoord.out.bam")

    print '\n'.join(bam_list)
    return bam_list


