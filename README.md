# PDL1_pipeline 
script for CD274 analysis 

# Genomon SV

## Introduction

PDL1_pipeline is pipeline program for analysing cancer transcriptome sequencing data and used in Kataoka et al., in submission.
Briefly, this program performs viral sequence detection, sequence alignment, gene fusion detection, gene expression analysis and so on.

## Dependency

### Python Packages
Python (>= 2.7), `genomon_virus_checker`, `fusionfusion`, `genomon_expression`

### Software
biobambam, star, samtools, bedtools

## Install
```
git clone https://github.com/friend1ws/PDL1_pipeline.git

```
## Preparation

First, mdify `pipeline.cfg` so that each path fit your environment.
Next, prepare input fastq or bam files

### fastq input format

Comma delimited file (sample_name, read1 sequence path, read2 sequence path).
Example:

sample1,/home/yshira/PDL1_project/sequence/sample1/sequence1.txt,/home/yshira/PDL1_project/sequence/sample1/sequence2.txt
sample2,/home/yshira/PDL1_project/sequence/sample2/sequence1.txt,/home/yshira/PDL1_project/sequence/sample2/sequence2.txt
sample3,/home/yshira/PDL1_project/sequence/sample3/sequence1.txt,/home/yshira/PDL1_project/sequence/sample3/sequence2.txt

See sample files for description of each parameters.


### bam input format

Comma delimited file (sample_name, star prefix).
There should be bam (.Aligned.sortedByCoord.out.bam), bam index (.Aligned.sortedByCoord.out.bam.bai), splicing file (.SJ.out.tab), chimera file (.Chimeric.out.sam), log file (.Log.final.out) after the specifed star prefix keys.

Example: 

sample1,/home/yshira/PDL1_project/star/sample1/sample1
sample2,/home/yshira/PDL1_project/star/sample2/sample2
sample3,/home/yshira/PDL1_project/star/sample3/sample3

Therefore, in the above example,
there should be /home/yshira/PDL1_project/star/sample1/sample1.Aligned.sortedByCoord.out.bam,
/home/yshira/PDL1_project/star/sample1/sample1.Aligned.sortedByCoord.out.bam.bai, and so on.

## Commands

1. Parsing breakpoint-containing and improperly aligned read pairs

```
GenomonSV parse sample.yaml param.yaml
```

2. Merging non-matched control panel breakpoint-containing read pairs
(for later filtering).

```
GenomonSV merge control.yaml mergedControl.bedpe.gz param.yaml                                        
```

3. Filtering and annotating candidate somatic structural variations

```
GenomonSV filt sample.yaml param.yaml
