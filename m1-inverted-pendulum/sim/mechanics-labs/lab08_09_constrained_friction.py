"""Lab 08-09 — 受約束運動、摩擦與圓周運動（對應原書 Ch8 Constrained Motion、Ch9 Forces and Constrained Motion）
9.2 摩擦力模型（靜摩擦/動摩擦）、9.3 圓周運動、9.3.2 有空氣阻力的單擺。
單擺這裡是「約束 → 一個自由度 θ」的第一次出現，也是後面 Lagrangian 的伏筆。
"""
import numpy as np
from scipy.integrate import solve_ivp

from labutils import check

g = 9.81
# ---------- 9.2 木塊沿斜面上滑後是否滑回？ ----------
def block_on_incline(theta_deg, mu_s, mu_d, v0, dt=1e-4, T=5.0):
    th = np.radians(theta_deg)
    x, v, t = 0.0, v0, 0.0
    while t < T:
        if abs(v) < 1e-9:                          # 靜止：先問靜摩擦撐不撐得住
            if np.tan(th) <= mu_s:
                return "stuck", x
            a = -g * np.sin(th) + mu_d * g * np.cos(th)   # 開始下滑，摩擦向上
        else:
            a = -g * np.sin(th) - np.sign(v) * mu_d * g * np.cos(th)
        v_new = v + a * dt
        if v != 0 and np.sign(v_new) != np.sign(v):  # 速度過零：先停下來，讓下一步重新判斷靜摩擦
            v_new = 0.0
        v = v_new
        x += v * dt
        t += dt
    return "moving", x

state, x = block_on_incline(20, mu_s=0.5, mu_d=0.4, v0=3.0)
x_stop = 3.0**2 / (2 * g * (np.sin(np.radians(20)) + 0.4 * np.cos(np.radians(20))))
print(f"θ=20°, μs=0.5：{state}，停在 x={x:.3f} m（解析 {x_stop:.3f} m）")
check("tanθ < μs → 停住", state == "stuck" and abs(x - x_stop) < 1e-3)
state, x = block_on_incline(35, mu_s=0.5, mu_d=0.4, v0=3.0)
print(f"θ=35°, μs=0.5：{state}，5 s 後 x={x:.2f} m")
check("tanθ > μs → 滑回來（x 變負）", state == "moving" and x < 0)

# ---------- 9.3 圓周運動：彎道最大速率 ----------
mu, R = 0.8, 50.0
v_max = np.sqrt(mu * g * R)                        # μ m g = m v^2 / R
print(f"平面彎道 R=50 m, μ=0.8 → v_max = {v_max*3.6:.0f} km/h")
check("v_max = sqrt(μ g R)", np.isclose(v_max, 19.81, atol=0.01))

# ---------- 9.3.2 單擺 + 空氣阻力 ----------
L, mpend, D = 1.0, 0.1, 0.02
def pendulum(t, s):
    th, w = s
    v = L * w
    return [w, -(g / L) * np.sin(th) - (D / mpend) * abs(v) * v / L]

sol = solve_ivp(pendulum, (0, 30), [np.radians(60), 0], rtol=1e-9, atol=1e-11, dense_output=True)
E = lambda s: 0.5 * mpend * (L * s[1])**2 + mpend * g * L * (1 - np.cos(s[0]))
Ehist = np.array([E(sol.sol(t)) for t in np.linspace(0, 30, 600)])
check("有阻力時機械能單調遞減", np.all(np.diff(Ehist) <= 1e-12))

# 大角度單擺週期 ≠ 2π sqrt(L/g)：與橢圓積分解析值比較
from scipy.special import ellipk
def half_period_numeric(theta0):
    f = lambda t, s: [s[1], -(g / L) * np.sin(s[0])]
    ev = lambda t, s: s[1]; ev.direction = 1      # ω 由負變正：擺錘到達 -θ0（最左側）
    sol = solve_ivp(f, (0, 10), [theta0, 0], events=ev, rtol=1e-11, atol=1e-12)
    return sol.t_events[0][0]                    # +θ0 → -θ0 所需時間 = 半週期
for th0 in [10, 60, 150]:
    T_num = 2 * half_period_numeric(np.radians(th0))
    T_exact = 4 * np.sqrt(L / g) * ellipk(np.sin(np.radians(th0) / 2)**2)
    print(f"θ0={th0:3d}°  T_numeric={T_num:.5f}  T_elliptic={T_exact:.5f}  T_small={2*np.pi*np.sqrt(L/g):.5f}")
    check(f"θ0={th0}° 數值週期與橢圓積分一致", abs(T_num - T_exact) < 1e-6)
