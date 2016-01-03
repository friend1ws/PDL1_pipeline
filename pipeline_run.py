#! /usr/bin/env python

import sys, os, argparse
import ConfigParser
from ruffus import *

from read_input import *
from stage_task import *
from resource.virus_count import *

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

pipeline_conf = ConfigParser.SafeConfigParser()
pipeline_conf.read("pipeline.cfg")

abs_output_root = os.path.abspath(args.output_dir)
##########


##########
# set task classes

virus_count = Virus_count(pipeline_conf.get("virus_count", "qsub_option"), abs_output_root + "/script", abs_output_root + "/log")
# star_align = Star_align(task_conf.get("star_align", "qsub_option"), run_conf.project_root + '/script')###
##########


##########
# read input file

sample_list_fastq = read_input(args.input_fastq_list)

##########


##########
# prepare output directories

if not os.path.isdir(abs_output_root): os.makedirs(abs_output_root)
if not os.path.isdir(abs_output_root + '/script'): os.mkdir(abs_output_root + '/script')
if not os.path.isdir(abs_output_root + '/log'): os.mkdir(abs_output_root + '/log')
if not os.path.isdir(abs_output_root + '/fastq'): os.mkdir(abs_output_root + '/fastq')
if not os.path.isdir(abs_output_root + '/virus_count'): os.mkdir(abs_output_root + '/virus_count')
if not os.path.isdir(abs_output_root + '/star_ref'): os.mkdir(abs_output_root + '/star_ref')
if not os.path.isdir(abs_output_root + '/star'): os.mkdir(abs_output_root + '/star')
if not os.path.isdir(abs_output_root + '/fusion'): os.mkdir(abs_output_root + '/fusion')

###########



# generate list of linked_fastq file path
linked_fastq_list = []
for sample in sample_list_fastq:
    linked_fastq_list.append([abs_output_root + '/fastq/' + sample + '/1.fastq',
                              abs_output_root + '/fastq/' + sample + '/2.fastq'])


# link the input fastq files
@originate(linked_fastq_list, sample_list_fastq)
def link_input_fastq(output_file, sample_list_fastq):
    sample = os.path.basename(os.path.dirname(output_file[0]))
    link_dir = abs_output_root + '/fastq/' + sample
    print link_dir

    if not os.path.isdir(link_dir): os.mkdir(link_dir)
    if not os.path.exists(link_dir + '/1.fastq'): os.symlink(sample_list_fastq[sample][0], link_dir + '/1.fastq')
    if not os.path.exists(link_dir + '/2.fastq'): os.symlink(sample_list_fastq[sample][1], link_dir + '/2.fastq')


# count virus sequence
@transform(link_input_fastq, formatter(), "{subpath[0][2]}/virus_count/{subdir[0][0]}/{subdir[0][0]}.virus.base.txt")
def task_Virus_count(input_files, output_file):

    dir_name = os.path.dirname(output_file)
    sample_name = os.path.basename(dir_name)

    arguments = {"pythonhome": pipeline_conf.get("common", "PYTHONHOME"),
                 "pythonpath": pipeline_conf.get("common", "PYTHONPATH"),
                 "ld_library_path": pipeline_conf.get("common", "LD_LIBRARY_PATH"),
                 "genomon_virus_checker": pipeline_conf.get("virus_count", "genomon_virus_checker"),
                 "virus_ref": pipeline_conf.get("virus_count", "virus_reference"),
                 "match_thres": pipeline_conf.get("virus_count", "match_thres"),
                 "input_fastq_1": input_files[0],
                 "input_fastq_2": input_files[1],
                 "output_prefix": dir_name + '/' + sample_name,
                 "log": abs_output_root + "/log"}

    if not os.path.isdir(dir_name): os.mkdir(dir_name)
    virus_count.task_exec(arguments)

pipeline_run(multiprocess = 100)


