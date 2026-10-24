"""labutils.py — 所有 Lab 共用的小工具：check()、輸出路徑、繪圖開關。
每支 Lab 仍可單獨執行（python labXX.py），只是把重複的三行 check() 收在這裡。
"""
import os
import sys
from pathlib import Path

LAB_DIR = Path(__file__).resolve().parent          # 不論從哪個目錄執行都指向本資料夾
OUT_DIR = LAB_DIR / "out"                          # 圖檔、暫存輸出；已列入 .gitignore


def check(name, cond):
    """印出 [PASS]/[FAIL] 並在失敗時 assert，讓 run_all.py 和 pytest 都能抓到。"""
    print(f"[{'PASS' if cond else 'FAIL'}] {name}")
    assert cond, name


def want_plot():
    """加 --plot 旗標或設 LAB_PLOT=1 才畫圖；預設只做數值檢核，CI 與 run_all 都更快。"""
    return "--plot" in sys.argv or os.environ.get("LAB_PLOT") == "1"


def out_path(filename):
    OUT_DIR.mkdir(exist_ok=True)
    return OUT_DIR / filename
