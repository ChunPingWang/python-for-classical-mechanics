"""Lab 12-13 — 動量、碰撞、火箭方程、多質點系統（對應原書 Ch12 Momentum/Impulse/Collisions、Ch13 Multiparticle Systems）
12.3 衝量、12.5 碰撞（以彈簧接觸力模擬）、12.5.1 衝擊擺、12.7 火箭方程、13.3 爆炸後質心軌跡。
"""
import numpy as np
from scipy.integrate import solve_ivp

from labutils import check

g = 9.81
# ---------- 12.5/12.6 用「接觸彈簧」模擬一維碰撞 ----------
def collide(m1, m2, v1, v2, k=1e5, c=0.0, T=0.05):
    """兩顆半徑 0.01 m 的球；重疊時產生 k·δ（+阻尼 c·δ̇）的推力。c>0 代表非彈性。"""
    R = 0.01
    def rhs(t, s):
        x1, x2, u1, u2 = s
        delta = 2 * R - (x2 - x1)                   # 重疊量
        F = (k * delta + c * (u1 - u2)) if delta > 0 else 0.0
        F = max(F, 0.0)                             # 接觸力只能推不能拉
        return [u1, u2, -F / m1, F / m2]
    sol = solve_ivp(rhs, (0, T), [0.0, 0.03, v1, v2], max_step=1e-5, rtol=1e-9, atol=1e-12)
    return sol.y[2, -1], sol.y[3, -1]

m1, m2, v1, v2 = 1.0, 3.0, 2.0, 0.0
u1, u2 = collide(m1, m2, v1, v2)
u1_th = (m1 - m2) / (m1 + m2) * v1                  # 彈性碰撞解析解
u2_th = 2 * m1 / (m1 + m2) * v1
print(f"彈性：u1={u1:.4f} (理論 {u1_th:.4f}), u2={u2:.4f} (理論 {u2_th:.4f})")
check("動量守恆", np.isclose(m1*u1 + m2*u2, m1*v1 + m2*v2, rtol=1e-6))
check("彈性碰撞結果符合解析解", np.allclose([u1, u2], [u1_th, u2_th], atol=1e-3))
u1, u2 = collide(m1, m2, v1, v2, c=40.0)
e = (u2 - u1) / (v1 - v2)
print(f"加阻尼後恢復係數 e = {e:.3f}")
check("非彈性：動量仍守恆、動能減少",
      np.isclose(m1*u1 + m2*u2, m1*v1, rtol=1e-6) and 0.5*m1*u1**2 + 0.5*m2*u2**2 < 0.5*m1*v1**2)

# ---------- 12.5.1 衝擊擺：子彈速度 ----------
m_b, M, h = 0.01, 2.0, 0.05
V = np.sqrt(2 * g * h)                              # 擺上升 → 碰撞後速度（能量守恆）
v_bullet = (m_b + M) / m_b * V                      # 完全非彈性碰撞（動量守恆）
print(f"子彈速度 ≈ {v_bullet:.0f} m/s；碰撞中動能損失比例 {1 - m_b/(m_b+M):.1%}")
check("兩段分析：碰撞用動量、上擺用能量", 190 < v_bullet < 210)

# ---------- 12.7 火箭方程：數值 vs Tsiolkovsky ----------
u_ex, m0, mf, burn = 3000.0, 1000.0, 300.0, 60.0
mdot = (m0 - mf) / burn
def rocket(t, s):                                   # 太空中，無重力
    v, m = s
    return [u_ex * mdot / m, -mdot]
sol = solve_ivp(rocket, (0, burn), [0.0, m0], rtol=1e-10, atol=1e-10)
dv = sol.y[0, -1]
print(f"Δv 數值 {dv:.2f} m/s，Tsiolkovsky {u_ex*np.log(m0/mf):.2f} m/s")
check("Δv = u ln(m0/mf)", np.isclose(dv, u_ex * np.log(m0 / mf), rtol=1e-8))

# ---------- 13.3 爆炸：內力不改變質心運動 ----------
v0 = np.array([20.0, 20.0]); t_exp, T = 1.5, 3.0
p_exp = v0 * t_exp + 0.5 * np.array([0, -g]) * t_exp**2
v_exp = v0 + np.array([0, -g]) * t_exp
ms = np.array([1.0, 2.0, 1.5])
kicks = np.array([[5.0, 3.0], [-4.0, 1.0]])          # 前兩塊的內力衝量
kicks = np.vstack([kicks, -kicks.sum(axis=0)])       # 第三塊抵消，總衝量 = 0
vel = v_exp + kicks / ms[:, None]
dt = T - t_exp
pos = p_exp + vel * dt + 0.5 * np.array([0, -g]) * dt**2
cm = (ms[:, None] * pos).sum(0) / ms.sum()
cm_no_exp = v0 * T + 0.5 * np.array([0, -g]) * T**2
print("碎片質心", np.round(cm, 6), " 未爆炸拋物線", np.round(cm_no_exp, 6))
check("爆炸後質心仍沿原拋物線", np.allclose(cm, cm_no_exp))
