#!/bin/sh

TRAIT="QT"
data_file_dir="/mnt/project/Burden"

#prompt="Enter PHENOTYPE for Step 2 (GENE burden files, PHENOTYPE .tsv file, and PHENOTYPE.${TRAIT}.LOCO files must exist):   "
#read -p "$prompt" PHENOTYPE
PHENOTYPE="metabolic"

cp "${data_file_dir}/${PHENOTYPE}.${TRAIT}.LOCO/${PHENOTYPE}.${TRAIT}.step1_pred.list" .

sed -i "s|/tmp/|${data_file_dir}/${PHENOTYPE}.${TRAIT}.LOCO/|g" "${PHENOTYPE}.${TRAIT}.step1_pred.list"


mkdir -p "/${PHENOTYPE}.${TRAIT}"


run_regenie_step2="
regenie \
  --step 2 \
  --interaction-snp "chr18:60372043:C:T" \
  --bgen "${data_file_dir}/${PHENOTYPE}.bgen" \
  --sample "${data_file_dir}/${PHENOTYPE}.sample" \
  --ref-first \
  --phenoFile "${data_file_dir}/${PHENOTYPE}.${TRAIT}.final.tsv" \
  --covarFile "${data_file_dir}/covariates.tsv" \
  --pred "${PHENOTYPE}.${TRAIT}.step1_pred.list" \
  #--pred "${data_file_dir}/${PHENOTYPE}.${TRAIT}.step1_pred.list" \
  --bsize 200 \
  --set-list "${data_file_dir}/${PHENOTYPE}.setlist" \
  --no-condtl \
  --force-condtl \
  --out ${PHENOTYPE}.${TRAIT}.step2_interaction2 \
  --verbose
"

#   --use-null-firth "${PHENOTYPE}.${TRAIT}.step1_firth.list"
#   --firth --approx \
#   --anno-file "${data_file_dir}/${PHENOTYPE}.annotations" \


#dx run swiss-army-knife -iin="/${PHENOTYPE}.${TRAIT}.LOCO/${PHENOTYPE}.${TRAIT}.step1_pred.list" \
#   -icmd="${run_regenie_step2}" \
#   --tag="Step2" --instance-type "mem1_hdd1_v2_x16" \
#   -iimage="jsture/phesant2" \
#   --destination="/Burden" --brief --yes;

dx run swiss-army-knife \
   -icmd="${run_regenie_step2}" --tag="Step2" --instance-type "mem1_ssd1_v2_x16"\
   --destination="/Burden" \
   -iimage="ghcr.io/rgcgithub/regenie/regenie:v3.2.6.gz" --yes;
