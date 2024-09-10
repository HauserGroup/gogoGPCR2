#!/bin/sh

# This script merges all chromosome genotype calls into one file

# Requirements: 
# Please refer to readme.md for more information about the requirements

# How to Run:
# Run this script using: sh 00_merge_files.sh on the command line

# Inputs
# - empty dummy.file

# Outputs
# - ukb_allChrs.bed 
# - ukb_allChrs.bim 
# - ukb_allChrs.fam 

run_merge="cp /mnt/project/Bulk/Genotype\ Results/Genotype\ calls/ukb22418_c[1-9]* . ;\
        ls *.bed | sed -e 's/.bed//g'> files_to_merge.txt; \
        plink --merge-list files_to_merge.txt --make-bed\
        --autosome-xy --out ukb_allChrs;\
        rm files_to_merge.txt;\
        rm ukb22418_c*_b*_v2.*;"

dx run swiss-army-knife \
   -icmd="${run_merge}" --tag="Step1_merge" --instance-type "mem1_ssd1_v2_x16"\
   --destination="/WGS_Javier/Data/Input_regenie/" --brief --yes 