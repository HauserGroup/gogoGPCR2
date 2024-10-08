#!/bin/sh

# This script runs the QC process using PLINK on the merged file generated by 02_liftOver_files.sh

# How to Run:
# Run this shell script using:
# sh 02-step1-qc-filter.sh
# on the command line in a Jupyter instance

# Outputs:
# - /Data/WES_array_snps_qc_pass.snplist - Used as input for part D
# - /Data/WES_array_snps_qc_pass.log
# - /Data/WES_array_snps_qc_pass.id

#set output directory (also location of merged files)
data_file_dir="/Data/step1/"

run_plink_qc="plink2 --bfile ukb_allChrs.GRCh38\
 --autosome\
 --maf 0.01 --mac 20 --geno 0.1 --hwe 1e-15 \
 --mind 0.1 --write-snplist --write-samples --remove-nosex\
 --no-id-header --out  WES_qc_pass"

dx run swiss-army-knife -iin="${data_file_dir}/ukb_allChrs.GRCh38.bed" \
   -iin="${data_file_dir}/ukb_allChrs.GRCh38.bim" \
   -iin="${data_file_dir}/ukb_allChrs.GRCh38.fam"\
   -icmd="${run_plink_qc}" --tag="Step1" --instance-type "mem1_ssd1_v2_x16"\
   --destination="${project}:/Data/step1/" --brief --yes
