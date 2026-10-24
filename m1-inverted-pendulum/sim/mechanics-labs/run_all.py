"""依序執行所有實驗並彙整 PASS/FAIL。用法：python run_all.py"""
import subprocess, sys, glob, time

labs = sorted(glob.glob("lab0*.py") + glob.glob("lab1*.py")) + sorted(glob.glob("labB*.py")) + sorted(glob.glob("labC*.py"))
summary = []
for f in labs:
    t0 = time.time()
    r = subprocess.run([sys.executable, f], capture_output=True, text=True)
    n_pass = r.stdout.count("[PASS]")
    ok = r.returncode == 0 and "[FAIL]" not in r.stdout
    summary.append((f, ok, n_pass, time.time() - t0))
    print(f"{'OK  ' if ok else 'FAIL'} {f:38s} {n_pass:2d} checks  {time.time()-t0:5.1f}s")
    if not ok:
        print(r.stdout[-1500:], r.stderr[-1500:])
print(f"\n{sum(s[1] for s in summary)}/{len(summary)} labs passed, {sum(s[2] for s in summary)} checks total")
sys.exit(0 if all(s[1] for s in summary) else 1)
