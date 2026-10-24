"""Lab B2 — 雙擺：Lagrangian 的威力、正則模態與混沌（補充；對應 Taylor Ch7 / Ch11 Coupled Oscillators / Ch12 Nonlinear Mechanics and Chaos）
用牛頓法要處理兩根桿的內力；用 Lagrangian 只要寫出兩個質點的位置。
"""
import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp

from labutils import check

t = sp.symbols("t")
m1, m2, l1, l2, g = sp.symbols("m1 m2 l1 l2 g", positive=True)
q1, q2 = sp.Function("q1")(t), sp.Function("q2")(t)        # 兩根桿與「垂直向下」的夾角
x1, y1 = l1 * sp.sin(q1), -l1 * sp.cos(q1)
x2, y2 = x1 + l2 * sp.sin(q2), y1 - l2 * sp.cos(q2)
T = sp.Rational(1, 2) * m1 * (x1.diff(t)**2 + y1.diff(t)**2) + sp.Rational(1, 2) * m2 * (x2.diff(t)**2 + y2.diff(t)**2)
V = m1 * g * y1 + m2 * g * y2
L = T - V
eqs = [sp.diff(sp.diff(L, q.diff(t)), t) - sp.diff(L, q) for q in (q1, q2)]
qdd = [q1.diff(t, 2), q2.diff(t, 2)]
# 整理成 M(q) q̈ = r(q, q̇)，數值上每步解 2×2 線性方程（比 sympy 直接解 q̈ 快且式子短）
Mq = sp.Matrix([[sp.diff(e, a) for a in qdd] for e in eqs])
r = -sp.Matrix([e.subs({qdd[0]: 0, qdd[1]: 0}) for e in eqs])

W1, W2, Q1, Q2 = sp.symbols("W1 W2 Q1 Q2")
num = {m1: 1.0, m2: 1.0, l1: 1.0, l2: 1.0, g: 9.81}
def to_num(expr):
    return expr.subs({q1.diff(t): W1, q2.diff(t): W2}).subs({q1: Q1, q2: Q2}).subs(num)
f_M = sp.lambdify((Q1, Q2), to_num(Mq), "numpy")
f_r = sp.lambdify((Q1, Q2, W1, W2), to_num(r), "numpy")
energy = sp.lambdify((Q1, Q2, W1, W2), to_num(T + V), "numpy")
print("M(q) =", sp.simplify(Mq))

def rhs(t, s):
    a = np.linalg.solve(np.array(f_M(s[0], s[1]), float), np.array(f_r(*s), float).ravel())
    return [s[2], s[3], a[0], a[1]]

# ---------- 1) 小角度：正則模態頻率 ----------
# 線性化 M q̈ + K q = 0（m=l=1）：M = [[2,1],[1,1]]，K = g·diag(2,1) → ω² = g(2∓√2)
Mlin = np.array([[2.0, 1.0], [1.0, 1.0]]); K = 9.81 * np.diag([2.0, 1.0])
w2, modes = np.linalg.eig(np.linalg.solve(Mlin, K))
w = np.sqrt(np.sort(w2.real))
print("正則模態角頻率 ω =", np.round(w, 4), " 理論", np.round(np.sqrt(9.81 * np.array([2 - np.sqrt(2), 2 + np.sqrt(2)])), 4))
check("ω² = g(2∓√2)", np.allclose(w**2, 9.81 * np.array([2 - np.sqrt(2), 2 + np.sqrt(2)])))

# 以「慢模態」形狀小幅釋放 → 只出現單一頻率
v_slow = modes[:, np.argmin(w2.real)].real
v_slow = v_slow / v_slow[0] * 0.01
sol = solve_ivp(rhs, (0, 20), [*v_slow, 0, 0], rtol=1e-10, atol=1e-12, dense_output=True)
tt = np.linspace(0, 20, 4000)
q1t, q2t = sol.sol(tt)[:2]
ratio = v_slow[1] / v_slow[0]                       # 慢模態形狀：q2/q1 = √2
shape_err = np.max(np.abs(q2t - ratio * q1t)) / 0.01
print(f"慢模態 q2/q1 = {ratio:.4f}（理論 √2 = {np.sqrt(2):.4f}），20 s 內形狀偏差 {shape_err:.1e}（相對振幅）")
check("按模態形狀釋放 → 兩擺始終同步、形狀不變", np.isclose(ratio, np.sqrt(2)) and shape_err < 1e-2)
# 對照：只拉第一根擺 → 兩個模態都被激發，q2/q1 不再固定（拍頻）
sol_mix = solve_ivp(rhs, (0, 20), [0.01, 0, 0, 0], rtol=1e-10, atol=1e-12, dense_output=True)
q1m, q2m = sol_mix.sol(tt)[:2]
check("非模態初始條件 → 形狀不固定", np.max(np.abs(q2m - ratio * q1m)) / 0.01 > 0.5)

# ---------- 2) 大角度：混沌（對初始條件敏感）----------
def separation(theta0, delta=1e-9, T=20.0):
    s0 = np.array([theta0, theta0, 0, 0])
    a = solve_ivp(rhs, (0, T), s0, rtol=1e-11, atol=1e-12, dense_output=True)
    b = solve_ivp(rhs, (0, T), s0 + [delta, 0, 0, 0], rtol=1e-11, atol=1e-12, dense_output=True)
    ts = np.linspace(0, T, 400)
    d = np.linalg.norm(a.sol(ts)[:2] - b.sol(ts)[:2], axis=0)
    return ts, d, a

for th0 in [0.2, 2.0]:
    ts, d, a = separation(th0)
    # 粗估最大 Lyapunov 指數：log(距離) 對時間的斜率（取未飽和段）
    mask = (d > 0) & (d < 1e-2)
    lam = np.polyfit(ts[mask], np.log(d[mask]), 1)[0] if mask.sum() > 10 else np.nan
    E = energy(*a.y); dE = np.ptp(E) / abs(E[0])
    print(f"θ0={th0}: 20 s 後兩軌跡相距 {d[-1]:.1e} rad，估計 λ ≈ {lam:.2f} 1/s，能量誤差 {dE:.1e}")
    if th0 == 0.2:
        check("低能量：近似規則運動，1e-9 差異仍很小", d[-1] < 1e-6)
    else:
        check("高能量：混沌，1e-9 差異放大到 O(1)", d[-1] > 1e-2 and lam > 0.5)
    check(f"θ0={th0} 模擬能量守恆 (<1e-7)", dE < 1e-7)
