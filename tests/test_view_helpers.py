from __future__ import annotations

import pytest
import polars as pl

from genoray_cli._view_helpers import parse_regions_arg, require_exactly_one


def test_parse_regions_arg_single():
    df = parse_regions_arg("chr1:10-20")
    assert df["chrom"].to_list() == ["chr1"]
    # 1-based inclusive -> 0-based half-open
    assert df["start"].to_list() == [9]
    assert df["end"].to_list() == [20]


def test_parse_regions_arg_comma_list():
    df = parse_regions_arg("chr1:10-20,chr2:30-40")
    assert df["chrom"].to_list() == ["chr1", "chr2"]
    assert df["start"].to_list() == [9, 29]
    assert df["end"].to_list() == [20, 40]


def test_parse_regions_arg_bad_format():
    with pytest.raises(ValueError, match="region"):
        parse_regions_arg("not_a_region")


def test_require_exactly_one_zero():
    with pytest.raises(ValueError, match="exactly one of"):
        require_exactly_one("regions", a=None, b=None)


def test_require_exactly_one_both():
    with pytest.raises(ValueError, match="exactly one of"):
        require_exactly_one("regions", a="x", b="y")


def test_require_exactly_one_ok():
    require_exactly_one("regions", a="x", b=None)  # no raise
    require_exactly_one("regions", a=None, b="y")  # no raise
