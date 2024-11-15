#!/bin/sh

phenotype=$1
trait=$2
pheno_file_dir="/mnt/project/Data/phenotypes"

run_phesant="mkdir -p /tmp/${phenotype}.phesant && cd /PHESANT && \
    Rscript WAS/phenomeScan.r --phenofile='${pheno_file_dir}/${phenotype}.${trait}.raw.tsv' --variablelistfile='../variable-info/outcome-info.tsv' --datacodingfile='../variable-info/data-coding-ordinal-info.txt' --resDir='/tmp/${phenotype}.phesant' --userId='xeid' --tab=TRUE --skipirnt=TRUE --save"

dx run swiss-army-knife -iin="/Data/dummy.file" \
   -icmd="${run_phesant}" --tag="PHESANT" --instance-type "mem1_ssd1_v2_x16"\
   --destination="/Data/phenotypes/${phenotype}.${trait}.phesant" \
   -iimage="jsture/phesant2" --yes;
