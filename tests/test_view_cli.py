from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

from genoray import SparseVar


def _run(argv: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, "-m", "genoray_cli", *argv],
        check=False,
        capture_output=True,
        text=True,
    )


def test_view_single_region_single_sample(tmp_path: Path, tiny_svar: Path):
    out = tmp_path / "view.svar"
    r = _run([
        "view", str(tiny_svar), str(out),
        "-r", "chr1:1-100",
        "-s", "A",
    ])
    assert r.returncode == 0, r.stderr
    sub = SparseVar(out)
    assert list(sub.available_samples) == ["A"]
    assert sub.n_variants >= 1  # A has at least one non-ref call in chr1:1-100


def test_view_bed_and_sample_file(tmp_path: Path, tiny_svar: Path):
    bed = tmp_path / "r.bed"
    bed.write_text("chr1\t0\t100\n")
    samples_f = tmp_path / "s.txt"
    samples_f.write_text("A\nB\n")
    out = tmp_path / "view.svar"
    r = _run([
        "view", str(tiny_svar), str(out),
        "-R", str(bed),
        "-S", str(samples_f),
    ])
    assert r.returncode == 0, r.stderr
    sub = SparseVar(out)
    assert sorted(sub.available_samples) == ["A", "B"]
