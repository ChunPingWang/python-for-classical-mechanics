# Lab 02 — 現代 Python 科學計算起手式（原書 Ch2）

> Part A — 對應原書的現代化實驗｜[教材目錄](README.md)｜[章節對照總表](README.md#1-章節對照總表)

**學習目標**：寫出向量化運算；理解數值微分的誤差由兩部分組成（截斷誤差與捨入誤差）；寫出可重現的隨機模擬。

**核心觀念**：
- 中央差分 $f'(x)\approx\dfrac{f(x+h)-f(x-h)}{2h}$ 的截斷誤差是 $O(h^2)$。但 $h$ 太小時，分子會相減抵消（cancellation），捨入誤差以約 $\varepsilon/h$ 的速度變大。兩者加總後，誤差對 $h$ 呈 U 形。最佳的 $h$ 約在 $\varepsilon^{1/3}\approx 10^{-5}$ 附近。
- 隨機漫步走 $N$ 步之後，RMS 位移約為 $\sqrt N$。這是後面討論雜訊和擴散的基礎。

**與原書差異**：原書 2.4 節先教 for-loop 再教向量化，本課直接採用向量化。亂數改用 `default_rng(seed)`，確保每次結果相同。

**程式碼**：[`lab02_python_basics.py`](../../m1-inverted-pendulum/sim/mechanics-labs/lab02_python_basics.py)　｜　執行：`python lab02_python_basics.py`

**預期輸出**
```
central difference max error = 6.51e-07
[PASS] 中央差分誤差 < 1e-6（O(h^2)）
最佳步長約 h = 3e-06
[PASS] 最佳 h 落在 1e-7 ~ 1e-3 之間（不是越小越好）
RMS displacement after N=1000 steps = 31.3 (理論 sqrt(N)=31.6)
[PASS] RMS 位移 ≈ sqrt(N)（誤差 < 5%）
```

**延伸練習**
1. 把中央差分換成前向差分 $(f(x+h)-f(x))/h$，重畫 U 形曲線，比較最佳 $h$ 和最小誤差。
2. 讓隨機漫步只能在 $[-5,5]$ 內移動（原書 2.6 節），觀察 RMS 位移在長時間後如何飽和。

---

[← 概覽](README.md)　｜　[目錄](README.md)　｜　[Lab 03 →](a03-units-floats.md)
