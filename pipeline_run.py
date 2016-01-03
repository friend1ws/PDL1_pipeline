#! /usr/bin/env python

import sys, os, argparse
from ruffus import *

from read_input import *

##########
# store arguments
parser = argparse.ArgumentParser(prog = "genomon_pipeline")

parser.add_argument("--version", action = "version", version = "pdl1_pipeline-0.1.0")

parser.add_argument("input_fastq_list", metavar = "input_fastq_list.txt", default = None, type = str,
                    help = "input sample fastq list")

parser.add_argument("output_dir", metavar = "output root directory", default = None, type = str,
                    help = "output root directory")

parser.add_argument("--mouse", help = "mouse rna-seq analysis", action = "store_true", default = False)

args = parser.parse_args()
##########


# prepare output directories
if not os.path.isdir(args.output_dir): os.makedirs(args.output_dir)
if not os.path.isdir(args.output_dir + '/script'): os.mkdir(args.output_dir + '/script')
if not os.path.isdir(args.output_dir + '/log'): os.mkdir(args.output_dir + '/log')
if not os.path.isdir(args.output_dir + '/fastq'): os.mkdir(args.output_dir + '/fastq')
if not os.path.isdir(args.output_dir + '/virus_count'): os.mkdir(args.output_dir + '/virus_count')
if not os.path.isdir(args.output_dir + '/star_ref'): os.mkdir(args.output_dir + '/star_ref')
if not os.path.isdir(args.output_dir + '/star'): os.mkdir(args.output_dir + '/star')
if not os.path.isdir(args.output_dir + '/fusion'): os.mkdir(args.output_dir + '/fusion')


sample_list_fastq = read_input(args.input_fastq_list)

# generate list of linked_fastq file path
linked_fastq_list = []
for sample in sample_list_fastq:
    linked_fastq_list.append([args.output_dir + '/fastq/' + sample + '/1_1.fastq',
                              args.output_dir + '/fastq/' + sample + '/1_2.fastq'])

# link the input fastq files
@originate(linked_fastq_list, sample_list_fastq)
def link_input_fastq(output_file, sample_list_fastq):
    sample = os.path.basename(os.path.dirname(output_file[0]))
    link_dir = args.output_dir + '/fastq/' + sample

    if not os.path.isdir(link_dir): os.mkdir(link_dir)
    if not os.path.exists(link_dir + '/1.fastq'): os.symlink(sample_list_fastq[sample][0][0], link_dir + '/1.fastq')
    if not os.path.exists(link_dir + '/2.fastq'): os.symlink(sample_list_fastq[sample][1][0], link_dir + '/2.fastq')

