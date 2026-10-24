"""Lab B1 — Lagrangian 力學：從 L = T - V 自動推導運動方程（補充；對應 Taylor Ch7 Lagrange's Equations）
步驟：選廣義座標 q → 寫 T、V → Euler-Lagrange: d/dt(∂L/∂q̇) - ∂L/∂q = Q（非保守廣義力）
1) 單擺暖身   2) 倒立擺 cart-pole 推導並與 cartpole.py 比對   3) 線性化 → A, B 與可控性
4) Legendre 轉換到 Hamiltonian（Taylor Ch13 預告）
"""
import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp
import cartpole as cp

from labutils import check

t = sp.symbols("t")

def euler_lagrange(L, qs, Qs=None):
    """回傳 [d/dt ∂L/∂q̇_i - ∂L/∂q_i - Q_i] 的 list（= 0 即運動方程）"""
    Qs = Qs or [0] * len(qs)
    return [sp.simplify(sp.diff(sp.diff(L, q.diff(t)), t) - sp.diff(L, q) - Q)
            for q, Q in zip(qs, Qs)]

# ---------- 1) 單擺：一個方程，不用畫自由體圖、不用算張力 ----------
m, l, g = sp.symbols("m l g", positive=True)
th = sp.Function("theta")(t)
T = sp.Rational(1, 2) * m * l**2 * th.diff(t)**2
V = -m * g * l * sp.cos(th)                      # θ 從下垂量起
eq, = euler_lagrange(T - V, [th])
thdd = sp.solve(eq, th.diff(t, 2))[0]
print("單擺：θ̈ =", thdd)
check("單擺得到 θ̈ = -(g/l) sinθ", sp.simplify(thdd + g / l * sp.sin(th)) == 0)

# ---------- 2) cart-pole：兩個自由度、一個輸入 ----------
M, J, F = sp.symbols("M J F")
x = sp.Function("x")(t); th = sp.Function("theta")(t)
xd, thd = x.diff(t), th.diff(t)
# 擺桿質心位置（θ 從垂直向上量起）
px, py = x + l * sp.sin(th), l * sp.cos(th)
T = sp.Rational(1, 2) * M * xd**2 \
    + sp.Rational(1, 2) * m * (px.diff(t)**2 + py.diff(t)**2) \
    + sp.Rational(1, 2) * J * thd**2
V = m * g * py
eqs = euler_lagrange(T - V, [x, th], Qs=[F, 0])   # 推力 F 只作用在 x 上：B = [1, 0]^T

# 整理成 M(q) q̈ = rhs
qdd = [x.diff(t, 2), th.diff(t, 2)]
Mq = sp.Matrix([[sp.diff(e, a) for a in qdd] for e in eqs])
rhs = -sp.Matrix([e.subs({qdd[0]: 0, qdd[1]: 0}) for e in eqs])
print("M(q) =", sp.simplify(Mq))
print("rhs  =", sp.simplify(rhs).T)

# 與手寫模型 cartpole.py 數值比對（隨機狀態 × 隨機輸入）
p = cp.PARAMS
X, TH, XD, THD = sp.symbols("X TH XD THD")
subs_state = {x.diff(t): XD, th.diff(t): THD}
f_M = sp.lambdify((TH, M, m, l, J), Mq.subs(th, TH))
f_r = sp.lambdify((TH, XD, THD, F, M, m, l, J, g), rhs.subs(subs_state).subs({th: TH, x: X}))
rng = np.random.default_rng(0)
ok = True
for _ in range(20):
    s = rng.uniform(-3, 3, 4); u = rng.uniform(-5, 5)
    qdd_sym = np.linalg.solve(np.array(f_M(s[1], p["M"], p["m"], p["l"], p["J"]), float),
                              np.array(f_r(s[1], s[2], s[3], u, p["M"], p["m"], p["l"], p["J"], p["g"]), float).ravel())
    ok &= np.allclose(qdd_sym, cp.dynamics(0, s, u)[2:], atol=1e-10)
check("sympy 推導結果 = cartpole.py 手寫模型（20 組隨機狀態）", ok)

# 無輸入、無摩擦 → 總能量守恆（模型正確性的另一道檢查）
sol = solve_ivp(cp.dynamics, (0, 10), [0, 2.5, 0, 0], args=(0.0,), rtol=1e-11, atol=1e-11)
E = np.array([cp.energy(sol.y[:, i]) for i in range(sol.y.shape[1])])
print(f"被動擺動 10 s 能量相對誤差 {np.ptp(E)/abs(E[0]):.1e}")
check("被動系統能量守恆", np.ptp(E) / abs(E[0]) < 1e-8)
check("動量 p_x 守恆（x 為循環座標，Noether）", np.ptp(
    (p["M"] + p["m"]) * sol.y[2] + p["m"] * p["l"] * np.cos(sol.y[1]) * sol.y[3]) < 1e-8)

# ---------- 3) 線性化：在倒立點求 A, B ----------
A, B = cp.linearize_upright()
eigA = np.linalg.eigvals(A)
print("A 的特徵值:", np.round(np.sort(eigA.real), 3))
check("倒立點開迴路不穩定（有正特徵值）", np.max(eigA.real) > 0)
ctrb = np.hstack([np.linalg.matrix_power(A, k) @ B for k in range(4)])
check("可控性矩陣滿秩（rank 4）→ 一個推力就能穩住兩個自由度", np.linalg.matrix_rank(ctrb) == 4)

# 用數值 Jacobian 交叉檢查 A, B（有限差分）
eps = 1e-6
A_fd = np.column_stack([(cp.dynamics(0, eps * e, 0.0) - cp.dynamics(0, -eps * e, 0.0)) / (2 * eps)
                        for e in np.eye(4)])
B_fd = ((cp.dynamics(0, np.zeros(4), eps) - cp.dynamics(0, np.zeros(4), -eps)) / (2 * eps))[:, None]
check("解析 A, B = 有限差分 Jacobian", np.allclose(A, A_fd, atol=1e-6) and np.allclose(B, B_fd, atol=1e-6))

# ---------- 4) Hamiltonian：p = ∂L/∂θ̇，H = p θ̇ - L ----------
th = sp.Function("theta")(t); pth = sp.symbols("p_theta")
L1 = sp.Rational(1, 2) * m * l**2 * th.diff(t)**2 + m * g * l * sp.cos(th)
w = sp.symbols("omega")
Lw = L1.subs(th.diff(t), w)
w_of_p = sp.solve(sp.Eq(pth, sp.diff(Lw, w)), w)[0]
H = sp.simplify((pth * w - Lw).subs(w, w_of_p))
print("單擺 Hamiltonian H =", H)
check("H = p²/(2ml²) - mgl cosθ = 總能量", sp.simplify(H - (pth**2 / (2 * m * l**2) - m * g * l * sp.cos(th))) == 0)
