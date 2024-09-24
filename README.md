# gogoGPCR2
[![Rye](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/rye/main/artwork/badge.json)](https://rye-up.com)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Orcid: Jakob](https://img.shields.io/badge/Jakob-bar?style=flat&logo=orcid&labelColor=white&color=grey)](https://orcid.org/0000-0002-2841-7284)

**Note that much of the code is custom to the project and may not be directly applicable to other projects. Please contact the authors for assistance and collaboration on using this code**

gogoGPCR2 is a framework for performing burden testing on UK Biobank Research Analysis Platform (RAP). It can be used as inspiration for burden testing on Whole-Exome Sequencing (WES) and Whole Genome Sequencing (WGS) data in the UKB using [regenie](https://rgcgithub.github.io/regenie/). Despite the name, gogoGPCR2 can be used for analyses of any (set of) gene(s)

This repo contains a series of notebooks, for pre-processing and quality controlling phenotype and genetic data, a Dockerfile for pre-processing phenotypes with [PHESANT](https://github.com/MRCIEU/PHESANT), and a series of scripts, for performing burden testing, with regenie. For information on running individual notebooks and scripts, see `notebooks/[WES/WGS]/README.md` and `scripts/[WES/WGS]/README.md`, respectively.

## Usage

Notebooks and scripts should be run in numerical order. Notebooks and scripts starting with "0*" should only be run once and the output files can be re-used for further analyses.

## Citation
Kizilkaya, H.S., Sørensen, K.V., Madsen, J.S. et al. Characterization of genetic variants of GIPR reveals a contribution of β-arrestin to metabolic phenotypes. Nat Metab 6, 1268–1281 (2024). https://doi.org/10.1038/s42255-024-01061-4
