# Notebooks. Whole-Genome Sequencing (WGS) data

Notebooks should generally be run in order. Notebooks starting with `0*` should only be run once, and can be re-used for other analyses.

Notebooks order and use:
1. `01_QC_Samples_PCs.ipynb`: Obtain 20 genetic PCs (field 22009) for ancestry analysis.
2. `01_QC_Samples_Ancestry.ipynb`: Obtain ancestry file based on population centers obtained from: https://github.com/privefl/UKBB-PGS.
3. `01_QC_Samples.ipynb`: Generate list of samples to filter out based on quality measures, ancestry and relatedness. 
4. `02_Covariates.ipynb`: Generate standard covariates as per Mbatchou et al., 2021 for all 500k samples. Columns: FID, IID, sex, age, agesex, age^2, age^2sex, and 20 first PCs. 
5. `03a_phenotypes_BT.ipynb`: Generate PHESANT-friendly phenotype TSV files of binary traits. In this case, they are metabolic traits, but can be updated to specific traits. 
6. `03b_phenotypes_QT.ipynb`: Generate PHESANT-friendly phenotype TSV files of quantitative traits. In this case, they are metabolic traits, but can be updated to specific traits. 
7. `04_PHESANT.ipynb`: Fix phenotype files output for Regenie.
8. `1_QC_WGS`: Perform quality control on variants of specific set of genes. It also performs Variant Effect Predictor (VEP). Quality control is based on sequencing parameters (call rate, quality, etc.) and functional annotation from VEP. This script should be run only once per set of gene(s). 
