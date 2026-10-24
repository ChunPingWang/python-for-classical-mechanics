"""Lab C2 — 倒立擺 LQR 平衡控制（補充；對應 Tedrake《Underactuated Robotics》Acrobots, Cart-Poles, and Quadrotors 章與 LQR 章）
流程：Lagrangian 模型 (cartpole.py) → 倒立點線性化 (A,B) → 解 Riccati 得 K → u = -K s → 回到「非線性」模型驗證。
"""
import numpy as np
from scipy.linalg import solve_continuous_are
from scipy.signal import place_poles
import cartpole as cp

def check(name, cond):
    print(f"[{'PASS' if cond else 'FAIL'}] {name}")
    assert cond, name

A, B = cp.linearize_upright()

# ---------- LQR：最小化 ∫ (sᵀQs + uᵀRu) dt ----------
Q = np.diag([10.0, 100.0, 1.0, 1.0])     # 位置、角度、速度、角速度 的權重
R = np.array([[0.1]])
P = solve_continuous_are(A, B, Q, R)
K = np.linalg.solve(R, B.T @ P)           # K = R⁻¹ Bᵀ P
print("LQR K =", np.round(K, 3))
eig_cl = np.linalg.eigvals(A - B @ K)
print("閉迴路特徵值 =", np.round(eig_cl, 3))
check("A-BK 全部特徵值實部 < 0（線性系統漸近穩定）", np.all(eig_cl.real < 0))

# 驗證 Riccati 解：Lyapunov 函數 V = sᵀPs 沿閉迴路遞減
Acl = A - B @ K
check("P 正定 且 Aclᵀ P + P Acl = -(Q + KᵀRK)",
      np.all(np.linalg.eigvalsh(P) > 0) and np.allclose(Acl.T @ P + P @ Acl, -(Q + K.T @ R @ K), atol=1e-8))

# ---------- 回到非線性模型 ----------
def lqr_force(K, u_max=np.inf):
    def F(t, s):
        e = s.copy(); e[1] = cp.wrap(s[1])
        return float(np.clip(-(K @ e)[0], -u_max, u_max))
    return F

t, S, U = cp.simulate(lqr_force(K), [0.0, 0.2, 0.0, 0.0], T=6.0)
print(f"θ0=0.2 rad → 6 s 後 |s| = {np.linalg.norm(S[-1]):.1e}")
check("非線性模型：從 θ=0.2 rad 回到原點", np.linalg.norm(S[-1]) < 1e-3)

# ---------- 與極點配置 (pole placement) 比較：同樣穩定，但力的峰值不同 ----------
K_pp = place_poles(A, B, [-3, -4, -5, -6]).gain_matrix
for name, KK in [("LQR", K), ("pole placement", K_pp)]:
    t, S, U = cp.simulate(lqr_force(KK), [0.0, 0.2, 0.0, 0.0], T=6.0)
    print(f"{name:15s} 峰值推力 {np.max(np.abs(U)):6.2f} N，台車最大偏移 {np.max(np.abs(S[:, 0])):.3f} m")

# ---------- 吸引域 (region of attraction)：線性控制器在非線性系統上能救回多大的角度？ ----------
def recovers(th0, u_max):
    with np.errstate(all="ignore"):                  # 發散的案例會溢位，視為失敗即可
        t, S, U = cp.simulate(lqr_force(K, u_max), [0.0, th0, 0.0, 0.0], T=8.0, dt=2e-3)
    return bool(np.all(np.isfinite(S)) and abs(cp.wrap(S[-1, 1])) < 1e-2 and np.max(np.abs(S[:, 0])) < 5.0)

for u_max in [np.inf, 10.0]:
    ths = np.arange(0.1, 1.6, 0.1)
    th_max = 0.0
    for th in ths:                                    # 由小到大，遇到第一個失敗就停
        if not recovers(th, u_max):
            break
        th_max = th
    print(f"u_max = {u_max:>4} N：可救回的最大初始角 ≈ {np.degrees(th_max):.0f}°")
    if np.isinf(u_max):
        th_inf = th_max
    else:
        check("推力飽和會縮小吸引域", th_max < th_inf)
check("吸引域有限（> 30° 但不是全域）", np.radians(30) < th_inf < np.pi / 2 + 0.1)
