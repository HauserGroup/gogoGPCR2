trait=$1

run_phesant="mkdir -p /tmp/phenos.phesant && cd /PHESANT && \
    Rscript WAS/phenomeScan.r --phenofile='/mnt/project/Data/phenotypes/phenos.${trait}.raw.tsv' --variablelistfile='../variable-info/outcome-info.tsv' --datacodingfile='../variable-info/data-coding-ordinal-info.txt' --resDir='/tmp/phenos.phesant' --userId='xeid' --tab=TRUE --skipirnt=TRUE --save"

dx run swiss-army-knife \
   -icmd="${run_phesant}" --tag="test" --instance-type "mem1_ssd1_v2_x16"\
   --destination="/Data/phenotypes/phenos.${trait}.phesant" \
   -iimage="jsture/phesant2" --yes;