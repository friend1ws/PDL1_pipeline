#! /bin/bash

# prepare
# HPV.HBV.sequence.fasta.txt
# target_virus_list.txt

rm -rf viral.1.1.genomic.fna.gz

wget ftp://ftp.ncbi.nlm.nih.gov/refseq/release/viral//viral.1.1.genomic.fna.gz

echo "python proc_virus_ref_target.py"
python proc_virus_ref_target.py

