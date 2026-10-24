"""平行執行所有實驗並彙整 PASS/FAIL。
用法：python run_all.py [-j N] [--only 關鍵字] [--save-output DIR]
不論從哪個目錄執行都可以：每支 Lab 都以本資料夾為工作目錄、用同一個直譯器執行。
"""
import argparse
import os
import subprocess
import sys
import time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

LAB_DIR = Path(__file__).resolve().parent


def lab_files(only=None):
    """Part A 依章節排序，再接 Part B、Part C（labutils.py、cartpole.py 不在內）。"""
    labs = (sorted(LAB_DIR.glob("lab0*.py")) + sorted(LAB_DIR.glob("lab1*.py"))
            + sorted(LAB_DIR.glob("labB*.py")) + sorted(LAB_DIR.glob("labC*.py")))
    return [p for p in labs if not only or only in p.name]


def run_lab(path):
    """執行單支 Lab，回傳 dict（stdout、PASS 數、是否成功、耗時）。"""
    t0 = time.time()
    env = dict(os.environ, MPLBACKEND="Agg", PYTHONIOENCODING="utf-8")
    r = subprocess.run([sys.executable, "-X", "utf8", Path(path).name],
                       cwd=LAB_DIR, capture_output=True, text=True, encoding="utf-8", env=env)
    return dict(name=Path(path).name, rc=r.returncode, stdout=r.stdout, stderr=r.stderr,
                n_pass=r.stdout.count("[PASS]"),
                ok=r.returncode == 0 and "[FAIL]" not in r.stdout,
                secs=time.time() - t0)


def run_many(paths, jobs=None):
    jobs = jobs or min(4, os.cpu_count() or 1)
    if jobs <= 1:
        return [run_lab(p) for p in paths]
    with ProcessPoolExecutor(max_workers=jobs) as ex:
        return list(ex.map(run_lab, paths))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("-j", "--jobs", type=int, default=None, help="平行數（預設 min(4, CPU 數)；1 = 依序執行）")
    ap.add_argument("--only", help="只跑檔名含此關鍵字的 Lab，例如 --only labC")
    ap.add_argument("--save-output", metavar="DIR", help="把每支 Lab 的 stdout 存成 DIR/<lab>.txt")
    args = ap.parse_args(argv)

    t0 = time.time()
    results = run_many(lab_files(args.only), args.jobs)
    if args.save_output:
        out = Path(args.save_output); out.mkdir(parents=True, exist_ok=True)
        for r in results:
            (out / (Path(r["name"]).stem + ".txt")).write_text(r["stdout"], encoding="utf-8")
    for r in results:
        print(f"{'OK  ' if r['ok'] else 'FAIL'} {r['name']:38s} {r['n_pass']:2d} checks  {r['secs']:5.1f}s")
        if not r["ok"]:
            print(r["stdout"][-1500:], r["stderr"][-1500:])
    n_ok = sum(r["ok"] for r in results)
    print(f"\n{n_ok}/{len(results)} labs passed, {sum(r['n_pass'] for r in results)} checks total "
          f"(wall {time.time() - t0:.1f}s)")
    return 0 if n_ok == len(results) else 1


if __name__ == "__main__":
    sys.exit(main())
