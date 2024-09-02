#!/bin/sh

# How to Run:
# Run this script using sh 1_regenie_step1.sh on the command line on your machine

#output directory - this should also be where the files in 02-step1-qc-filter.sh end up
data_file_dir="/mnt/project/Data"
regenie_file_dir="/mnt/project/Data/Regenie/Step1"
dir="/Data/Regenie/Step1"

# Binary treat
run_regenie_step1="regenie --step 1 --bt \
 --out phenos.BT.step1 \
 --bed ukb_allChrs \
 --phenoFile ${data_file_dir}/phenotypes/phenos.BT.final.tsv --covarFile ${data_file_dir}/Input_regenie/covariates.tsv \
 --extract ${regenie_file_dir}/WGS_qc_pass.snplist --keep ${regenie_file_dir}/WGS_qc_pass.id \
 --bsize 1000 \
 --write-null-firth \
 --lowmem --lowmem-prefix tmp_preds \
 --verbose --threads 16 \
 --covarExcludeList BMI_STD_PRS 
"

dx run swiss-army-knife -iin="${dir}/ukb_allChrs.bed" \
   -iin="${dir}/ukb_allChrs.bim" \
   -iin="${dir}/ukb_allChrs.fam" \
   -icmd="${run_regenie_step1}" \
   --tag="Step1_regenie_BT" --instance-type "mem1_ssd1_v2_x16" --destination="${dir}/phenos.BT.LOCO" --brief --yes \
   -iimage="ghcr.io/rgcgithub/regenie/regenie:v3.2.5.3.gz" --yes

# Quantiative treat
run_regenie_step1="regenie --step 1 \
 --out phenos.QT.step1 \
 --bed ukb_allChrs \
 --phenoFile ${data_file_dir}/phenotypes/phenos.QT.final.tsv --covarFile ${data_file_dir}/Input_regenie/covariates.tsv \
 --extract ${regenie_file_dir}/WGS_qc_pass.snplist --keep ${regenie_file_dir}/WGS_qc_pass.id \
 --bsize 1000 \
 --lowmem --lowmem-prefix tmp_preds \
 --verbose --threads 16 \
 --covarExcludeList BMI_STD_PRS \
 --apply-rint
"

dx run swiss-army-knife -iin="${dir}/ukb_allChrs.bed" \
   -iin="${dir}/ukb_allChrs.bim" \
   -iin="${dir}/ukb_allChrs.fam" \
   -icmd="${run_regenie_step1}" \
   --tag="Step1_regenie_QT" --instance-type "mem1_ssd1_v2_x16" --destination="${dir}/phenos.QT.LOCO" --brief --yes \
   -iimage="ghcr.io/rgcgithub/regenie/regenie:v3.2.5.3.gz" --yes