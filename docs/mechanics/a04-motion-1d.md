# Lab 04 — 一維運動：從資料到模型（原書 Ch4）

> Part A — 對應原書的現代化實驗｜[教材目錄](README.md)｜[章節對照總表](README.md#1-章節對照總表)

**學習目標**：體會「描述運動」（資料 → $v,a$）和「計算運動」（$a$ → $x(t)$）是兩個方向相反的問題；理解數值微分會放大雜訊。

**核心觀念**：
- 位置資料帶有 $\sigma$ 的雜訊時，差分得到的速度雜訊約 $\sigma/\Delta t$，加速度雜訊約 $\sigma/\Delta t^2$。所以 1 mm 的量測雜訊會變成每秒平方好幾公尺的加速度誤差。
- 實務上的對策是用物理模型做最小平方擬合（這裡用二次多項式）。真實感測器則會用濾波器（見 Lab C4）。
- Euler 和 Euler-Cromer 都是一階方法：$\Delta t$ 減半，誤差也減半。

**程式碼**：[`lab04_motion_1d.py`](../../m1-inverted-pendulum/sim/mechanics-labs/lab04_motion_1d.py)　｜　執行：`python lab04_motion_1d.py`

**預期輸出**
```
v 估計誤差 std = 0.065 m/s
a 估計誤差 std = 5.7 m/s^2   ← 二次微分把 1 mm 雜訊放大成數 m/s^2
[PASS] 二次微分後加速度雜訊遠大於速度雜訊
二次擬合得到 g = 9.814 m/s^2
[PASS] 擬合 g 誤差 < 1%
euler         err(dt=0.01)=4.9050e-02  err(dt=0.005)=2.4525e-02  ratio=2.00
[PASS] euler 為一階方法：dt 減半誤差約減半
euler_cromer  err(dt=0.01)=4.9050e-02  err(dt=0.005)=2.4525e-02  ratio=2.00
[PASS] euler_cromer 為一階方法：dt 減半誤差約減半
```

**延伸練習**：原書 4.1.1 用網球落下的資料示範。請用手機 phyphox 之類的 app 錄一段真實的加速度計資料，分別積分兩次和擬合，比較兩者的漂移。

---

[← Lab 03](a03-units-floats.md)　｜　[目錄](README.md)　｜　[Lab 05 →](a05-forces-1d.md)
