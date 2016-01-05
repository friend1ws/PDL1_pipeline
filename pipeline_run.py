#! /usr/bin/env python

import sys, os, glob, argparse
import ConfigParser
from ruffus import *

from utility import *
from stage_task import *
from resource.virus_count import *
from resource.star_ref import *
from resource.star_align import *
from resource.fusionfusion import *

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
star_ref = Star_ref(pipeline_conf.get("star_ref", "qsub_option"), abs_output_root + "/script", abs_output_root + "/log")
star_align = Star_align(pipeline_conf.get("star_align", "qsub_option"), abs_output_root + "/script", abs_output_root + "/log")
fusionfusion = Fusionfusion(pipeline_conf.get("fusionfusion", "qsub_option"), abs_output_root + "/script", abs_output_root + "/log")

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
@transform(link_input_fastq, formatter(), "{subpath[0][2]}/virus_count/{subdir[0][0]}/{subdir[0][0]}.virus.selected.txt")
def task_virus_count(input_files, output_file):

    dir_name = os.path.dirname(output_file)
    sample_name = os.path.basename(dir_name)

    arguments = {"pythonhome": pipeline_conf.get("env", "PYTHONHOME"),
                 "pythonpath": pipeline_conf.get("env", "PYTHONPATH"),
                 "ld_library_path": pipeline_conf.get("env", "LD_LIBRARY_PATH"),
                 "genomon_virus_checker": pipeline_conf.get("virus_count", "genomon_virus_checker"),
                 "virus_ref": pipeline_conf.get("virus_count", "virus_reference"),
                 "match_thres": pipeline_conf.get("virus_count", "match_thres"),
                 "select_thres": pipeline_conf.get("virus_count", "select_thres"),
                 "input_fastq_1": input_files[0],
                 "input_fastq_2": input_files[1],
                 "output_prefix": dir_name + '/' + sample_name}

    if not os.path.isdir(dir_name): os.mkdir(dir_name)
    virus_count.task_exec(arguments)


@follows(task_virus_count)
@originate([abs_output_root + "/star_ref/" + x + "/SAindex" for x in selected_virus_list(abs_output_root + "/virus_count")])
def make_star_ref(output_file):

    star_ref_dir = os.path.dirname(output_file) 
    selected_virus = os.path.basename(star_ref_dir)

    if not os.path.isdir(star_ref_dir): os.mkdir(star_ref_dir)
    print_virus_seq(pipeline_conf.get("virus_count", "virus_reference"),
                    star_ref_dir + '/' + selected_virus + ".fa", selected_virus)

    arguments = {"star": pipeline_conf.get("software", "star"),
                 "human_ref": pipeline_conf.get("reference", "ref_fasta"),
                 "virus_ref": star_ref_dir + '/' + selected_virus + ".fa",
                 "output_dir": star_ref_dir,
                 "gtf_file": pipeline_conf.get("reference", "gtf_file")}
 
    star_ref.task_exec(arguments)


@follows(make_star_ref)
@transform(link_input_fastq, formatter(), "{subpath[0][2]}/star/{subdir[0][0]}/{subdir[0][0]}.Aligned.sortedByCoord.out.bam")
def task_star_align(input_files, output_file):

    dir_name = os.path.dirname(output_file)
    sample_name = os.path.basename(dir_name)

    # check the selected virus
    selected_virus = ""
    with open(abs_output_root + "/virus_count/" + sample_name + "/" + sample_name + ".virus.selected.txt") as hin:
        line = hin.readlines()
        selected_virus = line[0].rstrip('\n')

    star_genome = pipeline_conf.get("reference", "star_ref")
    if selected_virus != "None":
        star_genome = abs_output_root + "/star_ref/" + selected_virus

    arguments = {"star": pipeline_conf.get("software", "star"),
                 "star_genome": star_genome,
                 "additional_params": pipeline_conf.get("star_align", "star_params"),
                 "samtools": pipeline_conf.get("software", "samtools"),
                 "samtools_sort_params": pipeline_conf.get("star_align", "samtools_sort_params"),
                 "fastq1": input_files[0],
                 "fastq2": input_files[1],
                 "out_prefix": dir_name + '/' + sample_name + '.'}

    if not os.path.isdir(dir_name): os.mkdir(dir_name)
    star_align.task_exec(arguments)


@transform(task_star_align, formatter(), "{subpath[0][2]}/fusion/{subdir[0][0]}/fusion_fusion.result.txt")
def task_fusionfusion(input_file, output_file):

    input_dir_name = os.path.dirname(input_file)
    sample_name = os.path.basename(input_dir_name)
    input_chimeric_sam = input_dir_name + '/' + sample_name + ".Chimeric.out.sam"
    output_dir_name = os.path.dirname(output_file) 

    if not os.path.isdir(output_dir_name): os.mkdir(output_dir_name)

    # check the selected virus
    selected_virus = ""
    with open(abs_output_root + "/virus_count/" + sample_name + "/" + sample_name + ".virus.selected.txt") as hin:
        line = hin.readlines()
        selected_virus = line[0].rstrip('\n')

    reference = abs_output_root + "/star_ref/" + selected_virus + "/reference.fa" if selected_virus != "None" \
                    else pipeline_conf.get("reference", "ref_fasta")

    generate_virus_fusionfusion_param(pipeline_conf.get("fusionfusion", "param_file"),
                                      output_dir_name + "/param.cfg",
                                      reference)                                        

    arguments = {"fusionfusion": pipeline_conf.get("software", "fusionfusion"),
                 "star_chimeric_sam": input_chimeric_sam,
                 "output_prefix": output_dir_name,
                 "param_file": output_dir_name + "/param.cfg",
                 "pythonhome": pipeline_conf.get("env", "PYTHONHOME"),
                 "pythonpath": pipeline_conf.get("env", "PYTHONPATH"),   
                 "ld_library_path": pipeline_conf.get("env", "LD_LIBRARY_PATH")}

    fusionfusion.task_exec(arguments)

pipeline_run(multiprocess = 100)


