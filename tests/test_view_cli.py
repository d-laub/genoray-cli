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
