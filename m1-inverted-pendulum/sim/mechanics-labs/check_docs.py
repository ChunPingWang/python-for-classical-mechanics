"""比對教材文件與程式的實際輸出，避免文件過時。
用法：python check_docs.py            # 比對，不一致時 exit 1
      python check_docs.py --update   # 把文件的「預期輸出」改成實際輸出（先確認差異合理再提交）
      python check_docs.py --strict   # 要求逐字相同；預設容許數字只差末位（±1 個印出的最小單位或 10%），
                                      # 因為不同 BLAS / 作業系統會讓極限環振幅、雜訊 RMS 這類量的最後一位不同
檢查三件事：
  1. docs/mechanics/*.md 的「預期輸出」區塊 == 對應 Lab 的 stdout
  2. docs/mechanics/README.md 檔案一覽表的「檢核數」欄 == 各 Lab 實際 PASS 數
  3. 文件中「N 項自動檢核」的 N == 全部 PASS 數
"""
import difflib
import re
import sys
from pathlib import Path

from run_all import LAB_DIR, lab_files, run_many

ROOT = LAB_DIR.parents[2]
NUM_RE = re.compile(r"[-+]?\d+(?:\.\d+)?(?:e[-+]?\d+)?")
DOCS_DIR = ROOT / "docs" / "mechanics"
CODE_RE = re.compile(r"\*\*程式碼\*\*：\[`(lab[^`]+\.py)`\]")
BLOCK_RE = re.compile(r"(\*\*預期輸出\*\*\s*```\n)(.*?)(```)", re.S)
TABLE_RE = re.compile(r"^\| \[`(lab[^`]+\.py)`\].*\| (\d+) \|\s*$", re.M)
TOTAL_RE = re.compile(r"(\d+) 項(自動)?檢核")
TOTAL_FILES = [DOCS_DIR / "README.md", LAB_DIR / "README.md", ROOT / "CHANGELOG.md"]


def _ulp(tok):
    """數字字串印出的最小單位：0.124 → 0.001，5.4e-04 → 1e-05，12 → 1。"""
    m = re.fullmatch(r"[-+]?\d+(?:\.(\d+))?(?:e([-+]?\d+))?", tok)
    return 10.0 ** (int(m.group(2) or 0) - len(m.group(1) or ""))


def lines_close(a, b, rel=0.10):
    """文字部分（含 PASS/FAIL）必須相同；每個數字允許差 1 個印出單位或 10%。"""
    if NUM_RE.sub("#", a) != NUM_RE.sub("#", b):
        return False
    for ta, tb in zip(NUM_RE.findall(a), NUM_RE.findall(b)):
        x, y = float(ta), float(tb)
        if abs(x - y) > max(1.01 * _ulp(ta), rel * abs(x)):
            return False
    return True


def compare_all(update=False, strict=False, results=None):
    results = results or {r["name"]: r for r in run_many(lab_files())}
    problems = 0
    # 1) 預期輸出區塊
    for md in sorted(DOCS_DIR.glob("*.md")):
        txt = md.read_text(encoding="utf-8")
        code, blk = CODE_RE.search(txt), BLOCK_RE.search(txt)
        if not code or not blk:
            continue
        name = code.group(1)
        if name not in results:
            print(f"MISSING {md.name}: {name} 不存在"); problems += 1; continue
        exp = blk.group(2).rstrip("\n").splitlines()
        act = results[name]["stdout"].rstrip("\n").splitlines()
        if exp == act:
            print(f"MATCH   {md.name} <-> {name}")
            continue
        close = len(exp) == len(act) and all(lines_close(e, a) for e, a in zip(exp, act))
        if close and not strict:
            n = sum(e != a for e, a in zip(exp, act))
            print(f"MATCH≈  {md.name} <-> {name}（{n} 行僅末位數字不同，--strict 會視為差異）")
            continue
        print(f"DIFF    {md.name} <-> {name}")
        for line in difflib.unified_diff(exp, act, "doc", "actual", lineterm="", n=0):
            print("   ", line)
        if update:
            txt = txt[:blk.start(2)] + "\n".join(act) + "\n" + txt[blk.end(2):]
            md.write_text(txt, encoding="utf-8"); print(f"        -> 已更新 {md.name}")
        else:
            problems += 1
    # 2) README 表格的檢核數
    readme = DOCS_DIR / "README.md"; txt = readme.read_text(encoding="utf-8")
    for m in TABLE_RE.finditer(txt):
        name, n_doc = m.group(1), int(m.group(2))
        if name in results and results[name]["n_pass"] != n_doc:
            print(f"COUNT   README 表格 {name}: 文件 {n_doc}，實際 {results[name]['n_pass']}")
            if update:
                txt = txt.replace(m.group(0), m.group(0)[: m.start(2) - m.start(0)] + str(results[name]["n_pass"]) + " |")
            else:
                problems += 1
    if update:
        readme.write_text(txt, encoding="utf-8")
    # 3) 總檢核數
    total = sum(r["n_pass"] for r in results.values())
    for f in TOTAL_FILES:
        txt = f.read_text(encoding="utf-8")
        wrong = {int(n) for n, _ in TOTAL_RE.findall(txt)} - {total}
        if wrong:
            print(f"TOTAL   {f.relative_to(ROOT)}: 寫 {sorted(wrong)} 項，實際 {total} 項")
            if update:
                for n in wrong:
                    txt = txt.replace(f"{n} 項自動檢核", f"{total} 項自動檢核").replace(f"{n} 項檢核", f"{total} 項檢核")
                f.write_text(txt, encoding="utf-8")
            else:
                problems += 1
    print(f"\n{'全部一致' if problems == 0 else f'{problems} 處不一致'}；總檢核數 {total}")
    return problems


if __name__ == "__main__":
    sys.exit(1 if compare_all(update="--update" in sys.argv, strict="--strict" in sys.argv) else 0)
