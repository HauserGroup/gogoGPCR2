#!/bin/sh
TRAIT="BT"
data_file_dir="/mnt/project/GLP2R"
PHENOTYPE="metabolic"
GENE="GLP2R"
TEST="recessive"
mkdir -p "${PHENOTYPE}.${TRAIT}.${TEST}.D470N"

run_regenie_step2="regenie \
  --step 2 \
  --bt \
  --test ${TEST} \
  --bgen ${data_file_dir}/metabolic.bgen \
  --sample ${data_file_dir}/metabolic.sample \
  --ref-first \
  --extract ${data_file_dir}/d470n.keep.txt \
  --phenoFile ${data_file_dir}/metabolic.BT.final.tsv \
  --covarFile ${data_file_dir}/covariates.tsv \
  --firth \
  --pred ${data_file_dir}/metabolic.BT.d470n.step1_pred.list \
  --bsize 200 \
  --out ${PHENOTYPE}.${TRAIT}.${TEST}.D470N \
  --verbose"

dx run swiss-army-knife \
   -icmd="${run_regenie_step2}" --tag="Step2" --instance-type "mem1_ssd1_v2_x16"\
   --destination="/GLP2R" \
   -iimage="ghcr.io/rgcgithub/regenie/regenie:v3.6.gz" --yes --priority "high"
