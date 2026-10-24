"""Lab 02 — 現代 Python 科學計算起手式（對應原書 Ch2 Getting Started with Programming）
原書用 `from pylab import *` 與 Python 2 語法（print TF、整數除法）；這裡改用
numpy / matplotlib 物件導向 API、np.random.default_rng、向量化寫法。
"""
import numpy as np
from labutils import want_plot, out_path

from labutils import check

# 1) 中央差分求導數：f(x)=exp(-x^2)，與解析解比較（原書 Ex. 2.7.1）
x = np.linspace(-5, 5, 1001)
h = 1e-3
f = lambda x: np.exp(-x**2)
df_num = (f(x + h) - f(x - h)) / (2 * h)       # 向量化，不需 for-loop
df_exact = -2 * x * np.exp(-x**2)
err = np.max(np.abs(df_num - df_exact))
print(f"central difference max error = {err:.2e}")
check("中央差分誤差 < 1e-6（O(h^2)）", err < 1e-6)

# 2) 步長 h 與誤差：截斷誤差 vs 浮點捨入誤差的 U 形曲線
hs = np.logspace(-12, -1, 23)
errs = [abs((f(1 + hh) - f(1 - hh)) / (2 * hh) - (-2 * np.exp(-1))) for hh in hs]
h_best = hs[int(np.argmin(errs))]
print(f"最佳步長約 h = {h_best:.0e}")
check("最佳 h 落在 1e-7 ~ 1e-3 之間（不是越小越好）", 1e-7 <= h_best <= 1e-3)

# 3) 隨機漫步（原書 2.5–2.6），用新版亂數產生器並可重現
rng = np.random.default_rng(seed=42)
steps = rng.choice([-1, 1], size=(2000, 1000))      # 2000 條路徑 × 1000 步
paths = np.cumsum(steps, axis=1)
rms = np.sqrt(np.mean(paths[:, -1] ** 2))
print(f"RMS displacement after N=1000 steps = {rms:.1f} (理論 sqrt(N)={np.sqrt(1000):.1f})")
check("RMS 位移 ≈ sqrt(N)（誤差 < 5%）", abs(rms / np.sqrt(1000) - 1) < 0.05)

if want_plot():                                   # python lab02_python_basics.py --plot
    import matplotlib
    matplotlib.use("Agg")                         # 無視窗環境也能存檔
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(1, 2, figsize=(9, 3.5))
    ax[0].plot(x, f(x), label="f(x)")
    ax[0].plot(x, df_num, "--", label="f'(x) numeric")
    ax[0].legend(); ax[0].set_xlabel("x")
    ax[1].loglog(hs, errs, "o-"); ax[1].set_xlabel("h"); ax[1].set_ylabel("|error|")
    fig.tight_layout(); fig.savefig(out_path("lab02.png"), dpi=120)
    print("圖已存到", out_path("lab02.png"))
