#!/bin/sh

# How to Run:
# Run this script using sh 2_regenie_step2.sh on the command line on your machine

regenie_file_dir="/mnt/project/WGS_Javier/Data/Input_regenie"
data_file_dir="/mnt/project/WGS_Javier/Data"
wgs_dir="/mnt/project/WGS_Javier/WGS_QC/Output"
dir="WGS_Javier/Data/Regenie/Step2"

# Binary treat
cp "${regenie_file_dir}/phenos.BT.LOCO/phenos.BT.step1_pred.list" .
#sed -i "s|/tmp/|${regenie_file_dir}/phenos.BT.LOCO/|g" phenos.BT.step1_pred.list
sed "s|/tmp/|${regenie_file_dir}/phenos.BT.LOCO/|g" "phenos.BT.step1_pred.list" > "new.list"
dx upload new.list --path WGS_Javier/Data/Input_regenie/phenos.BT.step1_pred_new.list

mkdir -p "/phenos.BT"

run_regenie_step2="regenie --step 2 --bt \
  --out phenos.BT.step2 \
  --bgen "${wgs_dir}/GIPR_test.bgen" \
  --sample "${wgs_dir}/GIPR_test.sample" \
  --ref-first \
  --phenoFile "${data_file_dir}/phenotypes/phenos.BT.final.tsv" \
  --covarFile "${regenie_file_dir}/covariates.tsv" \
  --pred ${regenie_file_dir}/phenos.BT.step1_pred_new.list \
  --bsize 200 \
  --set-list "${wgs_dir}/GIPR_test.setlist" \
  --anno-file "${wgs_dir}/GIPR_test.annotations" \
  --mask-def "${wgs_dir}/GIPR_test.masks" \
  --verbose
"

dx run swiss-army-knife \
   -icmd="${run_regenie_step2}" --tag="Step2_regenie_BT" --instance-type "mem1_ssd1_v2_x16"\
   --destination="/WGS_Javier/Data/Output_regenie/BT" \
   -iimage="ghcr.io/rgcgithub/regenie/regenie:v3.2.6.gz" --yes;

# Quantitative treat
cp "${regenie_file_dir}/phenos.QT.LOCO/phenos.QT.step1_pred.list" .
#sed -i "s|/tmp/|${regenie_file_dir}/phenos.QT.LOCO/|g" phenos.QT.step1_pred.list
sed "s|/tmp/|${regenie_file_dir}/phenos.QT.LOCO/|g" "phenos.QT.step1_pred.list" > "new_QT.list"
dx upload new_QT.list --path WGS_Javier/Data/Input_regenie/phenos.QT.step1_pred_new.list

mkdir -p "/phenos.QT"

run_regenie_step2="regenie --step 2 \
  --out phenos.QT.step2 \
  --bgen "${wgs_dir}/GIPR_test.bgen" \
  --sample "${wgs_dir}/GIPR_test.sample" \
  --ref-first \
  --phenoFile "${data_file_dir}/phenotypes/phenos.QT.final.tsv" \
  --covarFile "${regenie_file_dir}/covariates.tsv" \
  --pred "${regenie_file_dir}/phenos.QT.step1_pred_new.list" \
  --bsize 200 \
  --set-list "${wgs_dir}/GIPR_test.setlist" \
  --anno-file "${wgs_dir}/GIPR_test.annotations" \
  --mask-def "${wgs_dir}/GIPR_test.masks" \
  --verbose
"

dx run swiss-army-knife \
   -icmd="${run_regenie_step2}" --tag="Step2_regenie_QT" --instance-type "mem1_ssd1_v2_x16"\
   --destination="/WGS_Javier/Data/Output_regenie/QT" \
   -iimage="ghcr.io/rgcgithub/regenie/regenie:v3.2.6.gz" --yes;
