#!/bin/sh

TRAIT="QT"
data_file_dir="/mnt/project/Burden"

prompt="Enter GENE and PHENOTYPE for Step 2 (GENE burden files, PHENOTYPE .tsv file, and PHENOTYPE.${TRAIT}.LOCO files must exist):   "
read -p "$prompt" GENE PHENOTYPE 

cp "${PHENOTYPE}.${TRAIT}.LOCO/${PHENOTYPE}.${TRAIT}.step1_pred.list" .

sed -i "s|/tmp/|${data_file_dir}/${PHENOTYPE}.${TRAIT}.LOCO/|" "${PHENOTYPE}.${TRAIT}.step1_pred.list" 

#48 /tmp/metabolic.QT.step1_1.loco


mkdir -p "${PHENOTYPE}.${TRAIT}.${GENE}"

./regenie \
  --step 2 \
  --interaction-snp	"chr18:60372043:C:T"\ 
  --bgen "${data_file_dir}/${GENE}.bgen" \
  --sample "${data_file_dir}/${GENE}.sample" \
  --ref-first \ 
  --phenoFile "${data_file_dir}/${PHENOTYPE}.${TRAIT}.final.tsv" \
  --covarFile "${data_file_dir}/covariates.tsv" \
  --firth --approx \
  #--use-null-firth "${PHENOTYPE}.${TRAIT}.step1_firth.list" \
  --pred "${PHENOTYPE}.${TRAIT}.step1_pred.list" \
  --bsize 200 \
  --anno-file "${data_file_dir}/${PHENOTYPE}.annotations" \
  --set-list "${data_file_dir}/${PHENOTYPE}.setlist" \
  --no-condtl \ 
  --force-condtl \
  --out "${PHENOTYPE}.${TRAIT}.${GENE}/${PHENOTYPE}.${TRAIT}.${GENE}.step2_interaction" \
  --verbose  
