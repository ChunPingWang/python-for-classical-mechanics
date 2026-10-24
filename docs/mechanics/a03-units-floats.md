# Lab 03 — 單位、浮點數與數值表示（原書 Ch3）

> Part A — 對應原書的現代化實驗｜[教材目錄](README.md)｜[章節對照總表](README.md#1-章節對照總表)

**學習目標**：建立「先轉 SI、只在輸出時換單位」的習慣；永遠不用 `==` 比較浮點數；用事件內插取代「等於零」的判斷。

**核心觀念**：
- float64 的機器精度 $\varepsilon\approx2.2\times10^{-16}$。逐項累加 $N$ 次，誤差大約隨 $N\varepsilon$ 成長。`np.sum` 使用 pairwise 加總，誤差小很多。
- 原書 3.4 節提醒「不要檢查值是否恰好為 0」。本課示範正確做法：找出變號的位置，再做線性內插。Lab 06-07 會把這個做法升級成 `solve_ivp` 的 `events`。

**程式碼**：[`lab03_units_floats.py`](../../m1-inverted-pendulum/sim/mechanics-labs/lab03_units_floats.py)　｜　執行：`python lab03_units_floats.py`

**預期輸出**
```
144 km/h = 40.0 m/s
[PASS] 144 km/h == 40 m/s
[PASS] 0.1+0.2 != 0.3（直接比較會失敗）
[PASS] 改用 np.isclose 比較
machine epsilon (float64) = 2.220446049250313e-16
naive sum = 999999.9998389754, math.fsum-like (np.sum pairwise) = np.float64(1000000.0)
[PASS] 逐項相加誤差 > 1e-6，pairwise 加總誤差小很多
[PASS] y 序列中沒有任何一點恰好為 0
內插落地時間 1.4278 s，解析解 1.4278 s
[PASS] 線性內插落地時間誤差 < 1e-3 s
```

**延伸練習**：安裝 `pint`，用帶單位的變數重寫第 1 段。故意把 km/h 和 m/s 相加，看 `pint` 怎麼報錯。這正是原書提到 Mars Climate Orbiter 失事的教訓。

---

[← Lab 02](a02-python-basics.md)　｜　[目錄](README.md)　｜　[Lab 04 →](a04-motion-1d.md)
