"""Lab 06-07 — 二維/三維運動與受力（對應原書 Ch6 Motion in 2D/3D、Ch7 Forces in 2D/3D）
6.4 參考座標系（河中小船）、7.3–7.4 拋體 + 阻力、7.6 中心力（彗星軌道）。
狀態向量寫成 numpy 陣列，r 與 v 都是向量，程式碼和向量方程式一一對應。
"""
import numpy as np
from scipy.integrate import solve_ivp

from labutils import check

g = np.array([0.0, -9.81])

# ---------- 6.4 參考座標系：小船橫渡河流 ----------
v_boat_water = np.array([0.0, 2.0])     # 船頭朝對岸
v_water_ground = np.array([1.5, 0.0])   # 河水往下游流
v_boat_ground = v_boat_water + v_water_ground   # Galilean 速度合成
width = 60.0
t_cross = width / v_boat_ground[1]
drift = v_boat_ground[0] * t_cross
print(f"渡河 {t_cross:.0f} s，被沖往下游 {drift:.0f} m")
check("下游漂移 = 水速 × 渡河時間", np.isclose(drift, 45.0))

# ---------- 7.3–7.4 拋體：無阻力 vs 二次阻力 ----------
def projectile(k):
    def rhs(t, s):
        r, v = s[:2], s[2:]
        a = g - k * np.linalg.norm(v) * v          # F_drag = -D|v|v，k = D/m
        return np.concatenate([v, a])
    return rhs

def hit_ground(t, s):                                # 事件：y 由正變負時停止
    return s[1]
hit_ground.terminal, hit_ground.direction = True, -1

v0, ang = 30.0, np.radians(45)
s0 = [0, 0, v0 * np.cos(ang), v0 * np.sin(ang)]
for k in [0.0, 0.01]:
    sol = solve_ivp(projectile(k), (0, 20), s0, events=hit_ground, rtol=1e-9, atol=1e-9)
    R = sol.y_events[0][0][0]
    print(f"k={k:<5} 射程 R = {R:6.2f} m")
    if k == 0:
        check("無阻力射程 = v0^2 sin2θ / g", np.isclose(R, v0**2 / 9.81, rtol=1e-6))
    else:
        check("有阻力射程較短", R < v0**2 / 9.81)

# 有阻力時最佳發射角 < 45°
angles = np.radians(np.arange(25, 50, 1.0))
ranges = []
for a in angles:
    sol = solve_ivp(projectile(0.01), (0, 20), [0, 0, v0*np.cos(a), v0*np.sin(a)],
                    events=hit_ground, rtol=1e-8, atol=1e-8)
    ranges.append(sol.y_events[0][0][0])
best = np.degrees(angles[int(np.argmax(ranges))])
print(f"有阻力最佳發射角 ≈ {best:.0f}°")
check("有阻力最佳角度小於 45°", best < 45)

# ---------- 7.6 中心力：彗星軌道（天文單位 AU、年、GM_sun = 4π^2）----------
GM = 4 * np.pi**2
def kepler(t, s):
    r, v = s[:2], s[2:]
    return np.concatenate([v, -GM * r / np.linalg.norm(r)**3])

r0, v0c = np.array([1.0, 0.0]), np.array([0.0, 1.2 * 2 * np.pi])   # 比圓軌道快 20% → 橢圓
a_semimajor = 1 / (2 / 1.0 - np.dot(v0c, v0c) / GM)                  # vis-viva
T_kepler = a_semimajor**1.5                                           # Kepler 第三定律（年）
sol = solve_ivp(kepler, (0, 3 * T_kepler), [*r0, *v0c], rtol=1e-11, atol=1e-11, dense_output=True)
rT = sol.sol(T_kepler)[:2]
E = lambda s: 0.5 * (s[2]**2 + s[3]**2) - GM / np.hypot(s[0], s[1])
L = lambda s: s[0] * s[3] - s[1] * s[2]
print(f"a = {a_semimajor:.3f} AU, T = {T_kepler:.3f} yr, 一個週期後回到起點誤差 {np.linalg.norm(rT - r0):.1e}")
check("一個 Kepler 週期後回到原點", np.linalg.norm(rT - r0) < 1e-6)
check("角動量守恆（中心力）", abs(L(sol.y[:, -1]) - L(sol.y[:, 0])) < 1e-8)
check("能量守恆", abs(E(sol.y[:, -1]) - E(sol.y[:, 0])) < 1e-7)
