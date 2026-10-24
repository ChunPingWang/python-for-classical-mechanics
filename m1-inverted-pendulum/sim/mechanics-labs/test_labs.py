"""pytest 入口：pytest -q（每支 Lab 一個測項，另加一項文件一致性檢查）。"""
import pytest

from run_all import lab_files, run_lab


@pytest.mark.parametrize("lab", lab_files(), ids=lambda p: p.name)
def test_lab(lab):
    r = run_lab(lab)
    assert r["ok"], r["stdout"][-2000:] + r["stderr"][-2000:]


def test_docs_match_actual_output():
    from check_docs import compare_all
    assert compare_all() == 0
