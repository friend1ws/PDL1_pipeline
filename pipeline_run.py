#! /usr/bin/env python

import sys, os, argparse, ruffus

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
if not os.path.isdir(run_conf.project_root): os.makedirs(run_conf.project_root)
if not os.path.isdir(run_conf.project_root + '/script'): os.mkdir(run_conf.project_root + '/script')
if not os.path.isdir(run_conf.project_root + '/log'): os.mkdir(run_conf.project_root + '/log')
if not os.path.isdir(run_conf.project_root + '/fastq'): os.mkdir(run_conf.project_root + '/fastq')
if not os.path.isdir(run_conf.project_root + '/virus_count'): os.mkdir(run_conf.project_root + '/virus_count')
if not os.path.isdir(run_conf.project_root + '/star_ref'): os.mkdir(run_conf.project_root + '/star_ref')
if not os.path.isdir(run_conf.project_root + '/star'): os.mkdir(run_conf.project_root + '/star')
if not os.path.isdir(run_conf.project_root + '/fusion'): os.mkdir(run_conf.project_root + '/fusion')


