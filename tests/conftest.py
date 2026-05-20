"""Shared fixtures for genoray-cli tests."""
from __future__ import annotations

from pathlib import Path

import pytest


@pytest.fixture(scope="session")
def tiny_vcf(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """A tiny inline VCF with 3 samples × 4 variants on chr1."""
    p = tmp_path_factory.mktemp("vcf") / "tiny.vcf"
    p.write_text(
        "##fileformat=VCFv4.2\n"
        "##contig=<ID=chr1>\n"
        "##FORMAT=<ID=GT,Number=1,Type=String,Description=\"Genotype\">\n"
        "#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tA\tB\tC\n"
        "chr1\t10\t.\tA\tT\t.\t.\t.\tGT\t0/1\t0/0\t0/0\n"   # singleton in A
        "chr1\t20\t.\tC\tG\t.\t.\t.\tGT\t0/0\t0/1\t1/1\n"   # in B and C
        "chr1\t30\t.\tG\tA\t.\t.\t.\tGT\t0/0\t0/0\t1/0\n"   # singleton in C
        "chr1\t40\t.\tT\tC\t.\t.\t.\tGT\t1/0\t0/0\t0/0\n"   # singleton in A
    )
    return p


@pytest.fixture(scope="session")
def tiny_svar(tmp_path_factory: pytest.TempPathFactory, tiny_vcf: Path) -> Path:
    """A tiny SVAR built from `tiny_vcf` via `SparseVar.from_vcf`."""
    from genoray import VCF, SparseVar

    out = tmp_path_factory.mktemp("svar") / "tiny.svar"
    SparseVar.from_vcf(out, VCF(tiny_vcf), max_mem="64m", overwrite=True)
    return out
