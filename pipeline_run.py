#! /usr/bin/env python

import sys, os, glob, argparse, re
import ConfigParser
from ruffus import *

from utility import *
from stage_task import *
from resource.virus_count import *
from resource.star_ref import *
from resource.star_align import *
from resource.fusionfusion import *
from resource.exon_base_count import *
from resource.genomon_expression import *

##########
# store arguments

parser = argparse.ArgumentParser(prog = "genomon_pipeline")

parser.add_argument("--version", action = "version", version = "pdl1_pipeline-0.1.0")

parser.add_argument("input_fastq_list", metavar = "input_fastq_list.txt", default = None, type = str,
                    help = "input sample fastq list")

parser.add_argument("output_dir", metavar = "output_root_directory", default = None, type = str,
                    help = "output root directory")

parser.add_argument("--bam", help = "start from aligned bam files", action = "store_true", default = False)

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
exon_base_count = Exon_base_count(pipeline_conf.get("exon_base_count", "qsub_option"), abs_output_root + "/script", abs_output_root + "/log")
genomon_expression = Genomon_expression(pipeline_conf.get("expression", "qsub_option"), abs_output_root + "/script", abs_output_root + "/log")

##########


##########

##########
# prepare output directories

if not os.path.isdir(abs_output_root): os.makedirs(abs_output_root)
if not os.path.isdir(abs_output_root + '/script'): os.mkdir(abs_output_root + '/script')
if not os.path.isdir(abs_output_root + '/log'): os.mkdir(abs_output_root + '/log')
if not os.path.isdir(abs_output_root + '/fastq'): os.mkdir(abs_output_root + '/fastq')
if not os.path.isdir(abs_output_root + '/virus_count'): os.mkdir(abs_output_root + '/virus_count')
if not os.path.isdir(abs_output_root + '/virus_selected'): os.mkdir(abs_output_root + '/virus_selected')
if not os.path.isdir(abs_output_root + '/star_ref'): os.mkdir(abs_output_root + '/star_ref')
if not os.path.isdir(abs_output_root + '/star'): os.mkdir(abs_output_root + '/star')
if not os.path.isdir(abs_output_root + '/fusion'): os.mkdir(abs_output_root + '/fusion')
if not os.path.isdir(abs_output_root + '/expression'): os.mkdir(abs_output_root + '/expression')
if not os.path.isdir(abs_output_root + '/exon_base_count'): os.mkdir(abs_output_root + '/exon_base_count')

###########

linked_fastq_list = []
virus_check_seq_list = []
star_bam_list = []
fusion_fusion_bam_list = []
expression_bam_list = []
exon_count_bam_list = []
# if input is fastq
if not args.bam:
    
    # read input file
    sample_list_fastq = read_input_fastq(args.input_fastq_list)

    # link the input fastq files
    # generate list of linked_fastq file path
    for sample in sample_list_fastq:
        link_dir = abs_output_root + '/fastq/' + sample
        if not os.path.isdir(link_dir): os.mkdir(link_dir)
        if not os.path.exists(link_dir + '/1.fastq'): os.symlink(sample_list_fastq[sample][0], link_dir + '/1.fastq')
        if not os.path.exists(link_dir + '/2.fastq'): os.symlink(sample_list_fastq[sample][1], link_dir + '/2.fastq')
        linked_fastq_list.append([abs_output_root + '/fastq/' + sample + '/1.fastq',
                                  abs_output_root + '/fastq/' + sample + '/2.fastq'])

        if not os.path.exists(abs_output_root + '/virus_count/' + sample + '/' + sample + '.virus.selected.txt'):
            virus_check_seq_list.append([abs_output_root + '/fastq/' + sample + '/1.fastq',
                                         abs_output_root + '/fastq/' + sample + '/2.fastq'])

    # generate list of aligned bam file path
    for sample in sample_list_fastq:
        star_bam_list.append(abs_output_root + '/star/' + sample + '/' + sample + ".Aligned.sortedByCoord.out.bam")
        if not os.path.exists(abs_output_root + '/fusion/' + sample + '/fusion_fusion.result.txt'): 
            fusion_fusion_bam_list.append(abs_output_root + '/star/' + sample + '/' + sample + ".Aligned.sortedByCoord.out.bam")
        if not os.path.exists(abs_output_root + '/expression/' + sample + '/' + sample + ".sym2fkpm.txt"):
            expression_bam_list.append(abs_output_root + '/star/' + sample + '/' + sample + ".Aligned.sortedByCoord.out.bam")
        if not os.path.exists(abs_output_root + '/exon_base_count/' + sample + '/exon_base_count.result.txt'):
            exon_count_bam_list.append(abs_output_root + '/star/' + sample + '/' + sample + ".Aligned.sortedByCoord.out.bam")
    
else:
    # read input file
    sample_list_star_prefix = read_input_star_prefix(args.input_fastq_list)

    # generate list of aligned bam file path
    for sample in sample_list_star_prefix:
        link_dir = abs_output_root + '/star/' + sample
        if not os.path.isdir(link_dir): os.mkdir(link_dir)
        if not os.path.exists(link_dir + '/' + sample + ".Aligned.sortedByCoord.out.bam"): 
            os.symlink(sample_list_star_prefix[sample] + ".Aligned.sortedByCoord.out.bam", link_dir + '/' + sample + ".Aligned.sortedByCoord.out.bam")
        if not os.path.exists(link_dir + '/' + sample + ".Chimeric.out.sam"): 
            os.symlink(sample_list_star_prefix[sample] + ".Chimeric.out.sam", link_dir + '/' + sample + ".Chimeric.out.sam")
        if not os.path.exists(link_dir + '/' + sample + ".SJ.out.tab"): 
            os.symlink(sample_list_star_prefix[sample] + ".SJ.out.tab", link_dir + '/' + sample + ".SJ.out.tab")
        if not os.path.exists(link_dir + '/' + sample + ".Log.final.out"): 
            os.symlink(sample_list_star_prefix[sample] + ".Log.final.out", link_dir + '/' + sample + ".Log.final.out")
        if not os.path.exists(link_dir + '/' + sample + ".Aligned.sortedByCoord.out.bam.bai"): 
            os.symlink(sample_list_star_prefix[sample] + ".Aligned.sortedByCoord.out.bam.bai", link_dir + '/' + sample + ".Aligned.sortedByCoord.out.bam.bai")

        star_bam_list.append(abs_output_root + '/star/' + sample + '/' + sample + ".Aligned.sortedByCoord.out.bam")
        if not os.path.exists(abs_output_root + '/fusion/' + sample + '/fusion_fusion.result.txt'):
            fusion_fusion_bam_list.append(abs_output_root + '/star/' + sample + '/' + sample + ".Aligned.sortedByCoord.out.bam")
        if not os.path.exists(abs_output_root + '/expression/' + sample + '/' + sample + ".sym2fkpm.txt"):
            expression_bam_list.append(abs_output_root + '/star/' + sample + '/' + sample + ".Aligned.sortedByCoord.out.bam")
        if not os.path.exists(abs_output_root + '/exon_base_count/' + sample + '/exon_base_count.result.txt'):
            exon_count_bam_list.append(abs_output_root + '/star/' + sample + '/' + sample + ".Aligned.sortedByCoord.out.bam")


# count virus sequence
@active_if(not args.bam)
@transform(virus_check_seq_list, formatter(), "{subpath[0][2]}/virus_count/{subdir[0][0]}/{subdir[0][0]}.virus.selected.txt")
def task_virus_count(input_files, output_file):

    dir_name = os.path.dirname(output_file)
    sample_name = os.path.basename(dir_name)

    arguments = {"pythonhome": pipeline_conf.get("env", "PYTHONHOME"),
                 "pythonpath": pipeline_conf.get("env", "PYTHONPATH"),
                 "ld_library_path": pipeline_conf.get("env", "LD_LIBRARY_PATH"),
                 "genomon_virus_checker": pipeline_conf.get("software", "genomon_virus_checker"),
                 "virus_ref": pipeline_conf.get("virus_count", "virus_reference"),
                 "match_thres": pipeline_conf.get("virus_count", "match_thres"),
                 "select_thres": pipeline_conf.get("virus_count", "select_thres"),
                 "input_fastq_1": input_files[0],
                 "input_fastq_2": input_files[1],
                 "output_prefix": dir_name + '/' + sample_name}

    if not os.path.isdir(dir_name): os.mkdir(dir_name)
    virus_count.task_exec(arguments)


@active_if(not args.bam)
@follows(task_virus_count)
@merge(task_virus_count, abs_output_root + '/virus_count/virus.selected.merged.txt')
def virus_selected_merge(input_files, output_file):

    hout = open(output_file, 'w')
    print >> hout, '\n'.join(selected_virus_list(abs_output_root + "/virus_count"))
    hout.close()


@active_if(not args.bam)
@follows(virus_selected_merge)
@subdivide(virus_selected_merge, formatter(), "{subpath[0][1]}/virus_selected/*")
def virus_selected_split(input_file, output_files):

    for file in output_files:
        print file
        os.unlink(file)

    output_dir = os.path.dirname(os.path.dirname(input_file)) + '/virus_selected'
    with open(input_file, 'r') as hin:
        for line in hin:
            hout = open(output_dir + '/' + line.rstrip('\n'), 'w')
            # print >> hout, "touch"
            hout.close()

    print output_files


@active_if(not args.bam)
# @follows(virus_selected_split)
# @originate([abs_output_root + "/star_ref/" + x + "/SAindex" for x in selected_virus_list(abs_output_root + "/virus_count")])
@transform(virus_selected_split, formatter(), "{subpath[0][1]}/star_ref/{basename[0]}/SAindex")
# @transform(virus_selected_split, suffix(".txt"), "{subpath[0][2]}/star_ref/{basename[0]}/SAindex")
def make_star_ref(input_file, output_file):

    print input_file + '\t' + output_file
    star_ref_dir = os.path.dirname(output_file) 
    # selected_virus = os.path.basename(star_ref_dir)

    print star_ref_dir

    selected_virus = os.path.basename(input_file)

    if not os.path.isdir(star_ref_dir): os.mkdir(star_ref_dir)
    print_virus_seq(pipeline_conf.get("virus_count", "virus_reference"),
                    star_ref_dir + '/' + selected_virus + ".fa", selected_virus)

    arguments = {"star": pipeline_conf.get("software", "star"),
                 "human_ref": pipeline_conf.get("reference", "ref_fasta"),
                 "virus_ref": star_ref_dir + '/' + selected_virus + ".fa",
                 "output_dir": star_ref_dir,
                 "gtf_file": pipeline_conf.get("reference", "gtf_file")}
 
    star_ref.task_exec(arguments)


@active_if(not args.bam)
@follows(make_star_ref)
@transform(linked_fastq_list, formatter(), "{subpath[0][2]}/star/{subdir[0][0]}/{subdir[0][0]}.Aligned.sortedByCoord.out.bam")
# @originate(get_sequence_with_virus(abs_output_root, sample_list_fastq))
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
        print selected_virus
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



@follows( task_star_align )
@transform(fusion_fusion_bam_list, formatter(), "{subpath[0][2]}/fusion/{subdir[0][0]}/fusion_fusion.result.txt")
def task_fusionfusion(input_file, output_file):

    input_dir_name = os.path.dirname(input_file)
    sample_name = os.path.basename(input_dir_name)
    input_chimeric_sam = input_dir_name + '/' + sample_name + ".Chimeric.out.sam"
    output_dir_name = os.path.dirname(output_file) 

    if not os.path.isdir(output_dir_name): os.mkdir(output_dir_name)

    # check the selected virus
    selected_virus = "None" 
    if args.bam == False:
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


@follows( task_star_align )
@transform(exon_count_bam_list, formatter(), "{subpath[0][2]}/exon_base_count/{subdir[0][0]}/exon_base_count.result.txt")
def task_exon_base_cont(input_file, output_file):

    input_dir_name = os.path.dirname(input_file)
    output_dir_name = os.path.dirname(output_file)

    if not os.path.isdir(output_dir_name): os.mkdir(output_dir_name)


    arguments = {"input_bam": input_file, 
                "output": output_file,
                "region": pipeline_conf.get("exon_base_count", "region"),
                "exon_bed": pipeline_conf.get("exon_base_count", "exon_file"),
                "pythonhome": pipeline_conf.get("env", "PYTHONHOME"),
                "pythonpath": pipeline_conf.get("env", "PYTHONPATH"),
                "ld_library_path": pipeline_conf.get("env", "LD_LIBRARY_PATH"),
                "pdl1_pipeline_path" : os.path.abspath(os.path.dirname(__file__)),
                "samtools": pipeline_conf.get("software", "samtools"),
                "bedtools": pipeline_conf.get("software", "bedtools")}

    exon_base_count.task_exec(arguments)


@follows( task_star_align )
@transform(expression_bam_list, formatter(), "{subpath[0][2]}/expression/{subdir[0][0]}/{subdir[0][0]}.sym2fkpm.txt")
def task_genomon_expression(input_file, output_file):

    input_dir_name = os.path.dirname(input_file)
    output_dir_name = os.path.dirname(output_file)
    output_prefix = output_file.replace(".sym2fkpm.txt", "")

    if not os.path.isdir(output_dir_name): os.mkdir(output_dir_name)

    arguments = {"input_bam": input_file,
                "output_prefix": output_prefix,
                "ref_bed": pipeline_conf.get("expression", "gene_bed"),
                "genomon_expression": pipeline_conf.get("software", "genomon_expression"),
                "pythonhome": pipeline_conf.get("env", "PYTHONHOME"),
                "pythonpath": pipeline_conf.get("env", "PYTHONPATH"),
                "ld_library_path": pipeline_conf.get("env", "LD_LIBRARY_PATH"),
                "samtools": pipeline_conf.get("software", "samtools"),
                "bedtools_path": re.sub(r'\/bedtools$', '', pipeline_conf.get("software", "bedtools"))}

    genomon_expression.task_exec(arguments)


pipeline_run(multiprocess = 100)


