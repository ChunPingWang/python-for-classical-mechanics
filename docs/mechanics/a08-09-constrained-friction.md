# Lab 08-09 — 受約束運動、摩擦與單擺（原書 Ch8、Ch9）

> Part A — 對應原書的現代化實驗｜[教材目錄](README.md)｜[章節對照總表](README.md#1-章節對照總表)

**學習目標**：處理「靜摩擦 ↔ 動摩擦」的切換邏輯；理解單擺是「約束把兩個座標降成一個自由度」的系統，這也是 Part B Lagrangian 的動機。

**核心觀念**：
- 斜面上的木塊停下後，只有 $\tan\theta>\mu_s$ 時才會再滑動。數值實作要在速度過零時強制停下，再重新判斷靜摩擦。
- 大角度單擺的週期是 $T=4\sqrt{L/g}\,K(\sin^2(\theta_0/2))$，其中 $K$ 是第一類完全橢圓積分。150° 時的週期比小角度公式長約 76%。
- 原書 9.2.3 有地震 stick-slip 振盪的範例。本課的摩擦切換邏輯可以直接延伸到那個例子。

**程式碼**：[`lab08_09_constrained_friction.py`](../../m1-inverted-pendulum/sim/mechanics-labs/lab08_09_constrained_friction.py)　｜　執行：`python lab08_09_constrained_friction.py`

**預期輸出**
```
θ=20°, μs=0.5：stuck，停在 x=0.639 m（解析 0.639 m）
[PASS] tanθ < μs → 停住
θ=35°, μs=0.5：moving，5 s 後 x=-25.69 m
[PASS] tanθ > μs → 滑回來（x 變負）
平面彎道 R=50 m, μ=0.8 → v_max = 71 km/h
[PASS] v_max = sqrt(μ g R)
[PASS] 有阻力時機械能單調遞減
θ0= 10°  T_numeric=2.00989  T_elliptic=2.00989  T_small=2.00607
[PASS] θ0=10° 數值週期與橢圓積分一致
θ0= 60°  T_numeric=2.15287  T_elliptic=2.15287  T_small=2.00607
[PASS] θ0=60° 數值週期與橢圓積分一致
θ0=150°  T_numeric=3.53510  T_elliptic=3.53510  T_small=2.00607
[PASS] θ0=150° 數值週期與橢圓積分一致
```

---

[← Lab 06-07](a06-07-motion-forces-2d.md)　｜　[目錄](README.md)　｜　[Lab 10-11 →](a10-11-work-energy.md)
