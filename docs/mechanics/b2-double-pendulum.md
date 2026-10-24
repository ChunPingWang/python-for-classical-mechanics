# Lab B2 — 雙擺：正則模態與混沌（Taylor Ch11、Ch12）

> Part B — Lagrangian 力學（補充）｜[教材目錄](README.md)｜[章節對照總表](README.md#1-章節對照總表)

**學習目標**：體會 Lagrangian 處理多連桿的效率；小角度時做模態分析，大角度時觀察混沌。

**核心觀念**：
- 小角度線性化 $M\ddot q+Kq=0$，正則模態頻率由 $\det(K-\omega^2M)=0$ 決定。$m=l=1$ 時 $\omega^2=g(2\mp\sqrt2)$。按照模態形狀（$q_2/q_1=\sqrt2$）釋放，兩擺會同步振盪，形狀保持不變。
- 大角度時，兩條初始差 $10^{-9}$ rad 的軌跡在 20 s 內分離到 $O(1)$。最大 Lyapunov 指數 $\lambda>0$ 是混沌的定量指標。能量誤差維持在 $10^{-10}$ 等級，證明這種分離是物理上的混沌，不是數值誤差。
- 這對控制的意義：長時間開迴路預測不可靠，必須靠回授。這也是 MPC 要不斷重新規劃的原因之一。

**程式碼**：[`labB2_double_pendulum.py`](../../m1-inverted-pendulum/sim/mechanics-labs/labB2_double_pendulum.py)　｜　執行：`python labB2_double_pendulum.py`

**預期輸出**
```
M(q) = Matrix([[l1**2*(m1 + m2), l1*l2*m2*cos(q1(t) - q2(t))], [l1*l2*m2*cos(q1(t) - q2(t)), l2**2*m2]])
正則模態角頻率 ω = [2.3972 5.7874]  理論 [2.3972 5.7874]
[PASS] ω² = g(2∓√2)
慢模態 q2/q1 = 1.4142（理論 √2 = 1.4142），20 s 內形狀偏差 7.4e-05（相對振幅）
[PASS] 按模態形狀釋放 → 兩擺始終同步、形狀不變
[PASS] 非模態初始條件 → 形狀不固定
θ0=0.2: 20 s 後兩軌跡相距 8.3e-10 rad，估計 λ ≈ 0.00 1/s，能量誤差 1.3e-12
[PASS] 低能量：近似規則運動，1e-9 差異仍很小
[PASS] θ0=0.2 模擬能量守恆 (<1e-7)
θ0=2.0: 20 s 後兩軌跡相距 1.4e+00 rad，估計 λ ≈ 1.21 1/s，能量誤差 6.5e-11
[PASS] 高能量：混沌，1e-9 差異放大到 O(1)
[PASS] θ0=2.0 模擬能量守恆 (<1e-7)
```

---

[← Lab B1](b1-lagrangian-cartpole.md)　｜　[目錄](README.md)　｜　[Part C →](c0-control-intro.md)
