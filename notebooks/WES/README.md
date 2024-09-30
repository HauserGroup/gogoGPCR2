# Notebooks. Whole-Exome Sequencing (WES) data

Notebooks should generally be run in order. Notebooks starting with `0*` should only be run once, and can be re-used for other analyses.

Notebooks order and use:
1. `02_Covariates.ipynb`: Generate standard covariates as per Mbatchou et al., 2021 for all 500k samples. Columns: FID, IID, sex, age, agesex, age^2, age^2sex, and 20 first PCs. 
2. `03a_metabolic_phenotypes_BT.ipynb` or `03a_metabolic_phenotypes_BT.py`: Generate PHESANT-friendly phenotype TSV files of binary traits. In this case, they are metabolic traits, but can be updated to specific traits. 
3. `03b_phenotypes_QT.ipynb` or `03b_phenotypes_QT.py`: Generate PHESANT-friendly phenotype TSV files of quantitative traits. In this case, they are metabolic traits, but can be updated to specific traits. 
4. `04_fix_phesant_output.py`, `04a_fix_phesant_QT.py`, and `04b_fix_phesant_BT.py`: Fix phenotype files output for Regenie.
5. `QC.ipynb`: Perform quality control on variants of specific set of genes. It also performs Variant Effect Predictor (VEP). Quality control is based on sequencing parameters (call rate, quality, depth, etc.) and functional annotation from VEP. This script should be run only once per set of gene(s). 
