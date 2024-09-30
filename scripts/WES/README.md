# Scripts. Whole-Exome Sequencing (WES) data

Scripts should generally be run in order. Scripts starting with `0*` should only be run once, and can be re-used for other analyses.

Notebooks order and use:
1. `00_merge_files.sh`: Merge all array genotype splitted into chromosomes into a single file using PLINK.
2. `03_plink_qc.sh`: Perform quality control on array genotypes using PLINK2 based on minor allele frequency and  count, missing genotype and Hardy-Weinberg equilibrium. It outputs `.bed`, `.bim`, and `.fam` files.
3. `04_run_phesant.sh`: Run Phesant on phenotype files. 
4. `1a_regenie_step1_BT.sh`: Perform Regenie Step 1 on binary traits. It requires `.bed`, `.bim`, and `.fam` files obtained from `01_plink_qc.sh`, covariate and phenotype files. It outputs .LOCO files require for Regenie Step 2. It takes several hours to run, and running-time increases with number of phenotypes. 
5. `1b_regenie_step1_QT.sh`: Perform Regenie Step 1 on quantitative traits. It requires `.bed`, `.bim`, and `.fam` files obtained from `01_plink_qc.sh`, covariate and phenotype files. It outputs .LOCO files require for Regenie Step 2. It takes several hours to run, and running-time increases with number of phenotypes.
6. `2_regenie_step2_interaction_BT.sh`: Perform Regenie Step 2 on binary traits. It requires .LOCO files obtained from Regenie Step 1, covariate and phenotype files and `.bgem`, `.sample`, `.annotations` and `.setlists` obtained from `Notebooks/WGS/1_QC_WGS.ipynb` and `.masks` file written according to specific interest. It outputs one .regenie file per phenotype, which can be visualized through forest plots.
7. `2_regenie_step2_interaction_QT.sh`: Perform Regenie Step 2 on quantitative traits. It requires .LOCO files obtained from Regenie Step 1, covariate and phenotype files and `.bgem`, `.sample`, `.annotations` and `.setlists` obtained from `Notebooks/WGS/1_QC_WGS.ipynb` and `.masks` file written according to specific interest. It outputs one .regenie file per phenotype, which can be visualized through forest plots.
