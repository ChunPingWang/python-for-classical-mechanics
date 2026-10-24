"""Lab 03 — 單位與數值表示（對應原書 Ch3 Units and Measurement）
重點：電腦只存數字不存單位；浮點數不能用 == 比較；捨入誤差會累積。
"""
import numpy as np

def check(name, cond):
    print(f"[{'PASS' if cond else 'FAIL'}] {name}")
    assert cond, name

# 1) 單位換算：寫成常數表，所有計算一律先轉 SI
KM, HOUR, MILE = 1000.0, 3600.0, 1609.344
v_kmh = 144.0
v_si = v_kmh * KM / HOUR
print(f"144 km/h = {v_si} m/s")
check("144 km/h == 40 m/s", np.isclose(v_si, 40.0))

# 2) 浮點陷阱：0.1+0.2 != 0.3
check("0.1+0.2 != 0.3（直接比較會失敗）", (0.1 + 0.2) != 0.3)
check("改用 np.isclose 比較", np.isclose(0.1 + 0.2, 0.3))
print("machine epsilon (float64) =", np.finfo(float).eps)

# 3) 捨入誤差累積：把 0.1 加一千萬次
s = 0.0
for _ in range(10_000_000):
    s += 0.1
print(f"naive sum = {s!r}, math.fsum-like (np.sum pairwise) = {np.sum(np.full(10_000_000, 0.1))!r}")
check("逐項相加誤差 > 1e-6，pairwise 加總誤差小很多",
      abs(s - 1e6) > 1e-6 and abs(np.sum(np.full(10_000_000, 0.1)) - 1e6) < abs(s - 1e6))

# 4) 落地判斷：不要寫 y == 0，要找「變號」再內插
t = np.arange(0, 2, 0.013)
y = 10.0 - 0.5 * 9.81 * t**2
check("y 序列中沒有任何一點恰好為 0", not np.any(y == 0.0))
i = np.where(y < 0)[0][0]                        # 第一個負值
t_hit = t[i - 1] + (t[i] - t[i - 1]) * y[i - 1] / (y[i - 1] - y[i])
print(f"內插落地時間 {t_hit:.4f} s，解析解 {np.sqrt(2*10/9.81):.4f} s")
check("線性內插落地時間誤差 < 1e-3 s", abs(t_hit - np.sqrt(2 * 10 / 9.81)) < 1e-3)

# 延伸：pip install pint 可讓變數帶單位（ureg = pint.UnitRegistry(); 3*ureg.m/ureg.s）
