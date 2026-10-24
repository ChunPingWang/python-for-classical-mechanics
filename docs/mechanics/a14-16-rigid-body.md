# Lab 14-16 — 轉動與剛體（原書 Ch14、Ch15、Ch16）

> Part A — 對應原書的現代化實驗｜[教材目錄](README.md)｜[章節對照總表](README.md#1-章節對照總表)

**學習目標**：用數值積分（Monte-Carlo 與梯形法）計算轉動慣量；用 $\tau=I\alpha$ 分析物理擺；**看見倒立點的不穩定特徵值**，作為控制的動機。

**核心觀念**：
- 平行軸定理 $I_{end}=I_{cm}+m d^2$。細桿繞端點轉動的等效擺長是 $2l/3$。
- 物體滾下斜面時 $a=g\sin\theta/(1+I/mR^2)$，與質量、半徑無關，只和形狀因子有關。
- 物理擺在 $\theta=\pi$（倒立）附近線性化後，系統矩陣的特徵值為 $\pm\sqrt{mgl_c/I}$，其中正特徵值代表不穩定。cart-pole 擺桿的參數 $(m,l,J)$ 會原樣帶進 Part B、C。

**程式碼**：[`lab14_16_rigid_body.py`](../../m1-inverted-pendulum/sim/mechanics-labs/lab14_16_rigid_body.py)　｜　執行：`python lab14_16_rigid_body.py`

**預期輸出**
```
圓盤 I_MC = 0.08992, 解析 ½MR² = 0.09000
[PASS] Monte-Carlo 圓盤轉動慣量誤差 < 1%
[PASS] I_cm = ml²/12
[PASS] 平行軸定理 I_end = I_cm + m(l/2)²
實心球 2/5      a = 2.397 m/s²
實心圓柱 1/2     a = 2.237 m/s²
薄圓環 1        a = 1.678 m/s²
[PASS] 實心球最快、圓環最慢（與質量和半徑無關）
物理擺小角度 ω0 = 5.4249 rad/s（等效擺長 0.3333 m = 2l/3）, 誤差 2.1e-04
[PASS] 小角度物理擺 ≈ 簡諧（誤差 < 振幅 1%），等效擺長 2l/3
倒立平衡點特徵值: [ 5.425+0.j -5.425+0.j]
[PASS] 倒立點有正實部特徵值 → 不穩定，需要控制
```

---

[← Lab 12-13](a12-13-momentum-systems.md)　｜　[目錄](README.md)　｜　[Part B →](b0-lagrangian-intro.md)
