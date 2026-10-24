# Lab 05 — 一維力模型（原書 Ch5）

> Part A — 對應原書的現代化實驗｜[教材目錄](README.md)｜[章節對照總表](README.md#1-章節對照總表)

**學習目標**：用「力模型」建立牛頓第二定律的右手邊；用 `solve_ivp` 解題，再和解析解對照。

**核心觀念**：
- 二次阻力 $F=-Dv|v|$，其中 $D=\tfrac12\rho C_dA$。終端速度為 $v_t=\sqrt{mg/D}$，速度解析解為 $v(t)=v_t\tanh(gt/v_t)$。
- 彈簧加重力的系統，振盪中心會移到平衡點 $x_{eq}=L_0+mg/k$。重力只改變振盪中心，不改變頻率。
- 原書 5.9.1 的電梯範例：體重計讀數 $N=m(g+a)$。

**程式碼**：[`lab05_forces_1d.py`](../../m1-inverted-pendulum/sim/mechanics-labs/lab05_forces_1d.py)　｜　執行：`python lab05_forces_1d.py`

**預期輸出**
```
終端速度 vt = 6.61 m/s，數值 vs 解析最大誤差 1.9e-09
[PASS] 二次阻力數值解與 tanh 解析解一致
週期 T = 0.993 s，振盪中心 0.5453 m，誤差 2.4e-10
[PASS] 彈簧木塊繞 x_eq 做簡諧運動
[PASS] 向上加速時體重計讀數變大
[PASS] 自由落體時讀數為 0
```

> 雨滴參數取直徑 2 mm、$C_d\approx0.5$ 的球體近似，算出 $v_t\approx6.6$ m/s。這和量測到的 2 mm 雨滴終端速度屬同一數量級，但真實雨滴會變形，所以 $C_d$ 是假設值。

---

[← Lab 04](a04-motion-1d.md)　｜　[目錄](README.md)　｜　[Lab 06-07 →](a06-07-motion-forces-2d.md)
