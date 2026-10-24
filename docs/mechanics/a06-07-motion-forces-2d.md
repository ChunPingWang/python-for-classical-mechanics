# Lab 06-07 — 二維/三維運動與受力（原書 Ch6、Ch7）

> Part A — 對應原書的現代化實驗｜[教材目錄](README.md)｜[章節對照總表](README.md#1-章節對照總表)

**學習目標**：把狀態寫成向量 $\mathbf s=[\mathbf r,\mathbf v]$；用 `events` 偵測落地；驗證中心力問題的守恆量。

**核心觀念**：
- Galilean 速度合成：$\mathbf v_{船/地}=\mathbf v_{船/水}+\mathbf v_{水/地}$（原書 6.4.1）。
- 有二次阻力時，最佳發射角小於 45°。
- 中心力 $\mathbf F=-GMm\,\hat{\mathbf r}/r^2$ 下，角動量 $L$ 與能量 $E$ 守恆，週期遵守 Kepler 第三定律 $T^2\propto a^3$。
- 用天文單位 (AU、年) 時 $GM_\odot=4\pi^2$，這是「無因次化」的實例（呼應原書 3.4 節）。

**程式碼**：[`lab06_07_motion_forces_2d.py`](../../m1-inverted-pendulum/sim/mechanics-labs/lab06_07_motion_forces_2d.py)　｜　執行：`python lab06_07_motion_forces_2d.py`

**預期輸出**
```
渡河 30 s，被沖往下游 45 m
[PASS] 下游漂移 = 水速 × 渡河時間
k=0.0   射程 R =  91.74 m
[PASS] 無阻力射程 = v0^2 sin2θ / g
k=0.01  射程 R =  55.78 m
[PASS] 有阻力射程較短
有阻力最佳發射角 ≈ 41°
[PASS] 有阻力最佳角度小於 45°
a = 1.786 AU, T = 2.386 yr, 一個週期後回到起點誤差 6.7e-10
[PASS] 一個 Kepler 週期後回到原點
[PASS] 角動量守恆（中心力）
[PASS] 能量守恆
```

**延伸練習**：把彗星的 `rtol` 放寬到 `1e-4`，跑 50 個週期，觀察能量和近日點進動（數值造成的假進動）。再改用 Lab 10-11 的 Verlet 積分器比較。

---

[← Lab 05](a05-forces-1d.md)　｜　[目錄](README.md)　｜　[Lab 08-09 →](a08-09-constrained-friction.md)
