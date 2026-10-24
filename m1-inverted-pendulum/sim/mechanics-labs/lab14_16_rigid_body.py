"""Lab 14-16 — 轉動與剛體（對應原書 Ch14 Rotational Motion、Ch15 Rotation of Rigid Bodies、Ch16 Dynamics of Rigid Bodies）
15.3 數值計算轉動慣量、15.5.2 / 16.3.2 滾下斜面、16.2 力矩與物理擺。
物理擺 (physical pendulum) 就是倒立擺「擺桿」的模型，參數 I_pivot、m、l_c 會直接帶進 Lab B/C。
"""
import numpy as np
from scipy.integrate import solve_ivp

from labutils import check

g = 9.81
# ---------- 15.3 轉動慣量：Monte-Carlo 數值積分 vs 解析 ----------
rng = np.random.default_rng(1)
N = 400_000
M, R = 2.0, 0.3
pts = rng.uniform(-R, R, size=(N, 2))
inside = pts[np.hypot(pts[:, 0], pts[:, 1]) <= R]
I_disc = M * np.mean(np.sum(inside**2, axis=1))      # I = ∫ r^2 dm
print(f"圓盤 I_MC = {I_disc:.5f}, 解析 ½MR² = {0.5*M*R**2:.5f}")
check("Monte-Carlo 圓盤轉動慣量誤差 < 1%", abs(I_disc / (0.5 * M * R**2) - 1) < 0.01)

# 均勻細桿：繞質心 vs 繞端點（平行軸定理）
m_rod, l = 0.2, 0.5
s = np.linspace(-l/2, l/2, 100_001)
lam = m_rod / l
I_cm = np.trapezoid(lam * s**2, s)
I_end = np.trapezoid(lam * (s + l/2)**2, s)
check("I_cm = ml²/12", np.isclose(I_cm, m_rod * l**2 / 12, rtol=1e-8))
check("平行軸定理 I_end = I_cm + m(l/2)²", np.isclose(I_end, I_cm + m_rod * (l/2)**2, rtol=1e-8))

# ---------- 15.5.2 / 16.3.2 滾下斜面：誰先到？ ----------
th = np.radians(20)
shapes = {"實心球 2/5": 2/5, "實心圓柱 1/2": 1/2, "薄圓環 1": 1.0}
acc = {k: g * np.sin(th) / (1 + c) for k, c in shapes.items()}   # a = g sinθ/(1+I/mR²)
for k, a in acc.items():
    print(f"{k:12s} a = {a:.3f} m/s²")
check("實心球最快、圓環最慢（與質量和半徑無關）",
      acc["實心球 2/5"] > acc["實心圓柱 1/2"] > acc["薄圓環 1"])

# ---------- 16.2 物理擺（繞端點轉的細桿）：τ = I α ----------
I_p, lc = I_end, l / 2
def phys_pend(t, s):
    return [s[1], -m_rod * g * lc * np.sin(s[0]) / I_p]
w0 = np.sqrt(m_rod * g * lc / I_p)
sol = solve_ivp(phys_pend, (0, 5), [0.05, 0], rtol=1e-11, atol=1e-13, dense_output=True)
t = np.linspace(0, 5, 300)
err = np.max(np.abs(sol.sol(t)[0] - 0.05 * np.cos(w0 * t)))
# 殘差來自 sinθ≈θ 的非線性：週期略長，相位慢慢落後
print(f"物理擺小角度 ω0 = {w0:.4f} rad/s（等效擺長 {I_p/(m_rod*lc):.4f} m = 2l/3）, 誤差 {err:.1e}")
check("小角度物理擺 ≈ 簡諧（誤差 < 振幅 1%），等效擺長 2l/3", err < 5e-4 and np.isclose(I_p/(m_rod*lc), 2*l/3))

# 倒過來就是倒立擺：在 θ=π（朝上）附近線性化 → 特徵值一正一負（鞍點，不穩定）
A_up = np.array([[0, 1], [m_rod * g * lc / I_p, 0]])
eig = np.linalg.eigvals(A_up)
print("倒立平衡點特徵值:", np.round(eig, 3))
check("倒立點有正實部特徵值 → 不穩定，需要控制", np.max(eig.real) > 0)
