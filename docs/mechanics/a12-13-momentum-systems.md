# Lab 12-13 — 動量、碰撞與多質點系統（原書 Ch12、Ch13）

> Part A — 對應原書的現代化實驗｜[教材目錄](README.md)｜[章節對照總表](README.md#1-章節對照總表)

**學習目標**：用「接觸彈簧＋阻尼」模擬碰撞（原書 12.6），並驗證動量守恆；用火箭方程練習變質量系統；確認內力不會改變質心運動。

**核心觀念**：
- 碰撞期間的接觸力是內力，所以總動量守恆。阻尼決定恢復係數 $e$ 和動能損失。這就是物理引擎 penalty-based contact 的原型。
- 衝擊擺分兩段分析：碰撞階段用動量守恆（動能不守恆，本例損失 99.5%），上擺階段用能量守恆。
- Tsiolkovsky 火箭方程：$\Delta v=u\ln(m_0/m_f)$。
- 爆炸前後，質心都沿同一條拋物線前進。

**程式碼**：[`lab12_13_momentum_systems.py`](../../m1-inverted-pendulum/sim/mechanics-labs/lab12_13_momentum_systems.py)　｜　執行：`python lab12_13_momentum_systems.py`

**預期輸出**
```
彈性：u1=-1.0000 (理論 -1.0000), u2=1.0000 (理論 1.0000)
[PASS] 動量守恆
[PASS] 彈性碰撞結果符合解析解
加阻尼後恢復係數 e = 0.803
[PASS] 非彈性：動量仍守恆、動能減少
子彈速度 ≈ 199 m/s；碰撞中動能損失比例 99.5%
[PASS] 兩段分析：碰撞用動量、上擺用能量
Δv 數值 3611.92 m/s，Tsiolkovsky 3611.92 m/s
[PASS] Δv = u ln(m0/mf)
碎片質心 [60.    15.855]  未爆炸拋物線 [60.    15.855]
[PASS] 爆炸後質心仍沿原拋物線
```

---

[← Lab 10-11](a10-11-work-energy.md)　｜　[目錄](README.md)　｜　[Lab 14-16 →](a14-16-rigid-body.md)
