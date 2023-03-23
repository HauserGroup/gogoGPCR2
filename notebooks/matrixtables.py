import hail as hl
import pandas as pd
from functools import partial

from pathlib import Path
from typing import Optional, Union, List


def import_mt(
    genes: List[str],
    mapping: pd.DataFrame,
    vcf_dir: str,
    vcf_version: str,
    field_id: int = 23157,
) -> hl.matrixtable.MatrixTable:
    """Maps a (list of) genes to their corresponding VCF file and region before import as Hail MatrixTable
    Parameters
    ----------
    genes : List[str]
        List of HGNC genes
    mapping : pd.DataFrame
        DataFrame with columns: "HGNC", "GRCh38_end", "GRCh38_start", "GRCh38_region", "VCF_block". See data folder
    vcf_dir : str
        Location of UKB VCF files
    vcf_version : str
        Used to construct file names, currently v1
    Returns
    -------
    hl.matrixtable.MatrixTable
        MT of all samples with all variants located within specified genes
    """
    get_vcfs = partial(
        lookup_vcfs,
        mapping=mapping,
        vcfdir=vcf_dir,
        version=vcf_version,
        field_id=field_id,
    )
    get_regions = partial(lookup_regions, mapping=mapping)

    # evil double list-comprehension
    vcf_files = [vcf for gene in genes for vcf in get_vcfs(gene=gene)]
    regions = [region for gene in genes for region in get_regions(gene=gene)]

    mts = hl.import_gvcfs(
        vcf_files,
        partitions=regions,
        reference_genome="GRCh38",
        array_elements_required=False,
    )

    # union multiple matrixtables before returning them

    if len(mts) == 1:
        return mts[0]
    else:
        return hl.MatrixTable.union_rows(*mts)


def get_position(gene: str, mapping: pd.DataFrame):
    blocks = mapping.loc[gene, "VCF_block"].split(",")
    chromosome = mapping.loc[gene, "GRCh38_region"]
    start = mapping.loc[gene, "GRCh38_start"]
    end = mapping.loc[gene, "GRCh38_end"]

    return chromosome, blocks, start, end


def lookup_regions(gene: str, mapping: pd.DataFrame) -> hl.expr.LocusExpression:
    chromosome, _, start, end = get_position(gene, mapping)

    region = [
        hl.parse_locus_interval(f"[chr{chromosome}:{start}-chr{chromosome}:{end}]")
    ]

    return region


def lookup_vcfs(
    mapping: pd.DataFrame, vcfdir: str, gene: str, version: str, field_id: int = 23157
) -> List[str]:

    chromosome, blocks, _, _ = get_position(gene, mapping)

    vcf_files = [
        f"file://{vcfdir}/ukb{field_id}_c{chromosome}_b{block}_{version}.vcf.gz"
        for block in blocks
    ]

    return vcf_files


def smart_split_multi_mt(
    mt: hl.matrixtable.MatrixTable, left_aligned=False
) -> hl.matrixtable.MatrixTable:
    """Split multiple alleles into bi-allelic in a clever way
    Parameters
    ----------
    mt : hl.matrixtable.MatrixTable
        MT with non-bi-allelic sites
    left_aligned : bool, optional
        Assume that alleles are left-aligned for faster splitting, by default False
    Returns
    -------
    hl.matrixtable.MatrixTable
        MT with only bi-allelic sites
    """

    mt = mt.key_rows_by("locus", "alleles")

    # Only split relevant alleles as suggested by Hail docs

    bi = mt.filter_rows(hl.len(mt.alleles) == 2)
    bi = bi.annotate_rows(a_index=1, was_split=False)
    multi = mt.filter_rows(hl.len(mt.alleles) > 2)
    split = hl.split_multi_hts(multi, left_aligned=left_aligned)
    mt = split.union_rows(bi)

    return mt

def interval_qc_mt(
    mt: hl.matrixtable.MatrixTable,
    bed_file: Union[str, Path],
) -> hl.matrixtable.MatrixTable:
    """Filter to only Target region used by the WES capture experiment
    Parameters
    ----------
    mt : hl.matrixtable.MatrixTable
        MatrixTable
    intervals : str
        .BED file of targeted capture regions which meet quality standards
    Returns
    -------
    hl.matrixtable.MatrixTable
        MatrixTable filtered to only target regions
    """

    interval_table = hl.import_bed(
        bed_file,
        reference_genome="GRCh38",
    )

    mt = mt.filter_rows(hl.is_defined(interval_table[mt.locus]))

    return mt