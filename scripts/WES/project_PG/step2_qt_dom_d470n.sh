#!/bin/sh
TRAIT="QT"
data_file_dir="/mnt/project/GLP2R"
PHENOTYPE="metabolic"
GENE="GLP2R"
TEST="dominant"
mkdir -p "${PHENOTYPE}.${TRAIT}.${TEST}.D470N"

run_regenie_step2="regenie \
  --step 2 \
  --qt \
  --test ${TEST} \
  --bgen ${data_file_dir}/metabolic.bgen \
  --sample ${data_file_dir}/metabolic.sample \
  --ref-first \
  --extract ${data_file_dir}/d470n.keep.txt \
  --phenoFile ${data_file_dir}/metabolic.QT.final.tsv \
  --covarFile ${data_file_dir}/covariates.tsv \
  --pred ${data_file_dir}/metabolic.QT.d470n.step1_pred.list \
  --bsize 200 \
  --out ${PHENOTYPE}.${TRAIT}.${TEST}.D470N \
  --verbose"

dx run swiss-army-knife \
   -icmd="${run_regenie_step2}" --tag="Step2" --instance-type "mem1_ssd1_v2_x16"\
   --destination="/GLP2R" \
   -iimage="ghcr.io/rgcgithub/regenie/regenie:v3.6.gz" --yes --priority "high"
