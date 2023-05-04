#!/bin/sh

TRAIT="QT"
data_file_dir="/mnt/project/Data"

prompt="Enter GENE and PHENOTYPE for Step 2 (GENE burden files, PHENOTYPE .tsv file, and PHENOTYPE.${TRAIT}.LOCO/FIRTH files must exist):   "
read -p "$prompt" GENE PHENOTYPE 

cp "${data_file_dir}/step1/${PHENOTYPE}.${TRAIT}.LOCO/${PHENOTYPE}.${TRAIT}.step1_firth.list" .
cp "${data_file_dir}/step1/${PHENOTYPE}.${TRAIT}.LOCO/${PHENOTYPE}.${TRAIT}.step1_pred.list" .

sed -i "s|/home/dnanexus/out/out/|${data_file_dir}/step1/${PHENOTYPE}.${TRAIT}.LOCO/|" "${PHENOTYPE}.${TRAIT}.step1_pred.list" 
sed -i "s|/home/dnanexus/out/out/|${data_file_dir}/step1/${PHENOTYPE}.${TRAIT}.LOCO/|" "${PHENOTYPE}.${TRAIT}.step1_firth.list"

mkdir -p "${PHENOTYPE}.${TRAIT}.${GENE}"

./regenie \
  --step 2 \
  --interaction-snp	"chr18:60372043:C:T"\ 
  --bgen "${data_file_dir}/burden/${GENE}.bgen" \
  --sample "${data_file_dir}/burden/${GENE}.sample" \
  --phenoFile "${data_file_dir}/phenotypes/${PHENOTYPE}.${TRAIT}.final.tsv" \
  --covarFile "${data_file_dir}/phenotypes/covariates.tsv" \
  --firth --approx \
  --use-null-firth "${PHENOTYPE}.${TRAIT}.step1_firth.list" \
  --bsize 200 \
  --no-condtl \ 
  --force-condtl \
  --out "${PHENOTYPE}.${TRAIT}.${GENE}/${PHENOTYPE}.${TRAIT}.${GENE}.step2_interaction" \
  --verbose # what is it? 
