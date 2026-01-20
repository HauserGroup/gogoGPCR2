from functools import partial
from typing import List

import hail as hl
import pandas as pd

import warnings


def import_mt(
    genes: List[str],
    mapping: pd.DataFrame,
    vcf_dir: str,
    vcf_version: str,
    field_id: int = 23157,
) -> hl.matrixtable.MatrixTable:
    """Maps a (list of) genes to their corresponding VCF file and region before import as Hail MatrixTable

    .. deprecated::
        This function is hard deprecated and will be removed in a future version.
        hl.import_gvcfs() is no longer available in recent Hail versions.
        See WGS 01_QC notebook implementation for alternatives.

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
    warnings.warn(
        "import_mt() is hard deprecated. hl.import_gvcfs() is no longer available. "
        "See WGS 01_QC notebook implementation for alternatives.",
        DeprecationWarning,
        stacklevel=2,
    )

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
    blocks = mapping.loc[gene, "VCF_block"].split(",")  # type: ignore
    chromosome = mapping.loc[gene, "GRCh38_region"]
    start = mapping.loc[gene, "GRCh38_start"]
    end = mapping.loc[gene, "GRCh38_end"]

    return chromosome, blocks, start, end


def lookup_regions(gene: str, mapping: pd.DataFrame):
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

    .. deprecated::
        This function is soft deprecated and will be removed in a future version.
        ML-corrected is already bi-allelic.


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
    warnings.warn(
        "smart_split_multi_mt() is soft deprecated. ML-corrected is already bi-allelic",
        DeprecationWarning,
        stacklevel=2,
    )

    mt = mt.key_rows_by("locus", "alleles")

    # Only split relevant alleles as suggested by Hail docs

    bi = mt.filter_rows(hl.len(mt.alleles) == 2)
    bi = bi.annotate_rows(a_index=1, was_split=False)
    multi = mt.filter_rows(hl.len(mt.alleles) > 2)
    split = hl.split_multi_hts(multi, left_aligned=left_aligned)
    mt = split.union_rows(bi)

    return mt


def make_single_gene_setlist(
    mt: hl.matrixtable.MatrixTable, set_list_file: str = "/tmp/GIPR.setlist"
):
    """Create a SETLIST file for VEP annotation from a Hail MatrixTable

    .. warning::
        This function only supports single-gene MatrixTables. For multi-gene MTs,
        filter to one gene first or call this function separately for each gene.

    Parameters
    ----------
    mt : hl.matrixtable.MatrixTable
        Hail MatrixTable containing variants from a SINGLE gene
    set_list_file : str
        Output path for the setlist file

    Returns
    -------
    None
        Writes a SETLIST file to specified path

    Raises
    ------
    ValueError
        If the MatrixTable contains variants from multiple genes or chromosomes
    """
    # Validate single gene/chromosome
    gene_symbols = mt.aggregate_rows(
        hl.agg.collect_as_set(mt.vep.transcript_consequences.gene_symbol)
    )
    chromosomes = mt.aggregate_rows(hl.agg.collect_as_set(mt.locus.contig))

    if len(gene_symbols) > 1:
        raise ValueError(
            f"MatrixTable contains {len(gene_symbols)} genes: {gene_symbols}. "
            "make_setlist() only supports single-gene MTs. Filter to one gene first."
        )

    if len(chromosomes) > 1:
        raise ValueError(
            f"MatrixTable spans {len(chromosomes)} chromosomes: {chromosomes}. "
            "make_setlist() requires all variants on the same chromosome."
        )

    # SETLIST file
    position = mt.aggregate_rows(hl.agg.min(mt.locus.position))
    names = mt.varid.collect()
    names_str = ",".join(names)

    line = f"{list(gene_symbols)[0]}\t{list(chromosomes)[0]}\t{position}\t{names_str}"

    with open(set_list_file, "w") as f:
        f.write(line)
