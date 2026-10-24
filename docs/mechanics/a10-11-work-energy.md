# Lab 10-11 — 功、能量，以及積分器的選擇（原書 Ch10、Ch11）★

> Part A — 對應原書的現代化實驗｜[教材目錄](README.md)｜[章節對照總表](README.md#1-章節對照總表)

**學習目標**：用能量守恆檢驗數值解（原書 11.6）；理解為什麼長時間模擬機械系統要用 **symplectic 積分器**；用能量圖判斷平衡點穩定性。

**核心觀念**：
- 功能定理 $W_{net}=\Delta K$。Simpson 法對三次以下的多項式是精確的。
- 能量圖上，$U'(x)=0$ 的點是平衡點：$U''>0$ 為穩定，$U''<0$ 為不穩定。倒立擺的倒立點就是 $U''<0$ 的點。
- 四種積分器的比較如下：

| 方法 | 階數 | symplectic | 長時間能量行為 |
|---|---|---|---|
| Euler | 1 | ✗ | 單調爆增（本例 100 s 內相對誤差達 1100%） |
| Euler-Cromer（先更新 v） | 1 | ✓ | 誤差有界、不漂移 |
| Velocity Verlet | 2 | ✓ | 有界，誤差更小 |
| RK4 | 4 | ✗ | 短時間極準，但非常長時間仍會慢慢漂移 |

Euler 和 Euler-Cromer 的程式碼只差一行順序。這一行決定了模擬能不能長時間跑。物理引擎（MuJoCo、Isaac 等）的半隱式積分就是同一個想法。

**程式碼**：[`lab10_11_work_energy.py`](../../m1-inverted-pendulum/sim/mechanics-labs/lab10_11_work_energy.py)　｜　執行：`python lab10_11_work_energy.py`

**預期輸出**
```
trapezoid W = 1.002500 J (exact 1.000000)
simpson   W = 1.000000 J (exact 1.000000)
[PASS] Simpson 對三次多項式精確
[PASS] W_net = ΔK
平衡點 x ≈ [-1.001e+00 -1.000e-03  1.000e+00]
[PASS] 雙井位能平衡點為 -1, 0, +1
[PASS] x=0 為不穩定（U''<0），x=±1 為穩定（U''>0）
euler            max relative energy error over 100 s = 1.10e+01
euler_cromer     max relative energy error over 100 s = 1.50e-02
velocity_verlet  max relative energy error over 100 s = 2.26e-04
rk4              max relative energy error over 100 s = 9.57e-08
[PASS] Euler 能量爆增 (>50%)
[PASS] Euler-Cromer 只差一行順序，能量誤差 < 5%
euler_cromer 跑 1000 s 的最大誤差 = 1.50e-02（與 100 s 幾乎相同 → 有界、不漂移）
[PASS] Euler-Cromer 誤差不隨時間累積
[PASS] Verlet 二階 symplectic 誤差更小
[PASS] RK4 精度高但非 symplectic（短時間極準）
```

**延伸練習**：把 `T` 延長到 10⁴ s，比較 RK4 和 Verlet 的能量誤差曲線。RK4 的誤差會緩慢成長，Verlet 的誤差會保持有界振盪。

---

[← Lab 08-09](a08-09-constrained-friction.md)　｜　[目錄](README.md)　｜　[Lab 12-13 →](a12-13-momentum-systems.md)
