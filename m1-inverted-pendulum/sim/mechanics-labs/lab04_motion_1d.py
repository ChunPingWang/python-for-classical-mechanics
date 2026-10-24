"""Lab 04 — 一維運動：從資料求速度、從加速度求運動（對應原書 Ch4 Motion in One Dimension）
4.1 描述運動：位置資料 → 數值微分得 v、a（雜訊會被放大）
4.2 計算運動：已知 a(x,v,t) → Euler / Euler-Cromer 積分
"""
import numpy as np

def check(name, cond):
    print(f"[{'PASS' if cond else 'FAIL'}] {name}")
    assert cond, name

g = 9.81
# ---------- 4.1 從「量測」位置資料反推速度 ----------
dt = 0.01
t = np.arange(0, 1.0, dt)
y_true = 1.5 - 0.5 * g * t**2
rng = np.random.default_rng(0)
y_meas = y_true + rng.normal(0, 1e-3, t.size)      # 1 mm 量測雜訊

v_num = np.gradient(y_meas, dt)                    # 中央差分
a_num = np.gradient(v_num, dt)
print(f"v 估計誤差 std = {np.std(v_num + g*t):.3f} m/s")
print(f"a 估計誤差 std = {np.std(a_num + g):.1f} m/s^2   ← 二次微分把 1 mm 雜訊放大成數 m/s^2")
check("二次微分後加速度雜訊遠大於速度雜訊", np.std(a_num + g) > 10 * np.std(v_num + g * t))

# 對策：用最小平方法擬合二次多項式（物理模型擬合優於直接微分）
c = np.polyfit(t, y_meas, 2)
g_fit = -2 * c[0]
print(f"二次擬合得到 g = {g_fit:.3f} m/s^2")
check("擬合 g 誤差 < 1%", abs(g_fit / g - 1) < 0.01)

# ---------- 4.2 已知加速度，數值積分求運動 ----------
# 等加速度下兩者誤差相同；差異要到振盪系統才看得出來（見 Lab 10-11 的能量漂移）
def simulate(method, dt, T=1.0):
    n = int(round(T / dt))
    y, v = 1.5, 0.0
    for _ in range(n):
        a = -g
        if method == "euler":            # 用舊的 v 更新位置
            y, v = y + v * dt, v + a * dt
        elif method == "euler_cromer":   # 先更新 v，再用新的 v 更新位置
            v = v + a * dt
            y = y + v * dt
    return y

y_exact = 1.5 - 0.5 * g * 1.0**2
for m in ["euler", "euler_cromer"]:
    e1 = abs(simulate(m, 0.01) - y_exact)
    e2 = abs(simulate(m, 0.005) - y_exact)
    print(f"{m:13s} err(dt=0.01)={e1:.4e}  err(dt=0.005)={e2:.4e}  ratio={e1/e2:.2f}")
    check(f"{m} 為一階方法：dt 減半誤差約減半", 1.8 < e1 / e2 < 2.2)
