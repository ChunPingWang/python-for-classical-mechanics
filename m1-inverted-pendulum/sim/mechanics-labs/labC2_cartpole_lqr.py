"""Lab C2 — 倒立擺 LQR 平衡控制（補充；對應 Tedrake《Underactuated Robotics》Acrobots, Cart-Poles, and Quadrotors 章與 LQR 章）
流程：Lagrangian 模型 (cartpole.py) → 倒立點線性化 (A,B) → 解 Riccati 得 K → u = -K s → 回到「非線性」模型驗證。
"""
import numpy as np
from scipy.linalg import solve_continuous_are
from scipy.signal import place_poles
import cartpole as cp

from labutils import check, want_plot, out_path

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

# ---------- 吸引域的二維切片 (θ0, θ̇0)：把整個格點排成 (4, N) 陣列一次向量化模擬 ----------
def roa_grid(u_max, th_grid, thd_grid, T=8.0, dt=2e-3):
    """回傳布林矩陣 [i_θ, j_θ̇]：從 (x=0, θ0, ẋ=0, θ̇0) 出發能否回到倒立點。判準與 recovers() 相同。"""
    TH, THD = np.meshgrid(th_grid, thd_grid, indexing="ij")
    S = np.zeros((4, TH.size)); S[1], S[3] = TH.ravel(), THD.ravel()
    xmax = np.zeros(TH.size)
    with np.errstate(all="ignore"):
        for _ in range(int(round(T / dt))):
            e = S.copy(); e[1] = cp.wrap(S[1])
            u = np.clip(-(K @ e)[0], -u_max, u_max)
            k1 = cp.dynamics(0, S, u); k2 = cp.dynamics(0, S + dt / 2 * k1, u)
            k3 = cp.dynamics(0, S + dt / 2 * k2, u); k4 = cp.dynamics(0, S + dt * k3, u)
            S = S + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
            xmax = np.maximum(xmax, np.abs(S[0]))
        ok = np.isfinite(S).all(axis=0) & (np.abs(cp.wrap(S[1])) < 1e-2) & (xmax < 5.0)
    return ok.reshape(TH.shape)

th_grid = np.radians(np.arange(0, 91, 10))        # 0°..90°；(θ,θ̇)→(-θ,-θ̇) 對稱，負角不必再算
thd_grid = np.arange(-4, 4.1, 1.0)                # rad/s
roa = {u: roa_grid(u, th_grid, thd_grid) for u in [np.inf, 10.0]}
for u, R_ in roa.items():
    print(f"u_max={u:>4}：列 = θ0，欄 = θ̇0 由 {thd_grid[0]:+.0f} 到 {thd_grid[-1]:+.0f} rad/s，# = 可救回")
    for i, th in enumerate(th_grid):
        print(f"   {np.degrees(th):3.0f}°  " + "".join("#" if c else "." for c in R_[i]))
frac = {u: R_.mean() for u, R_ in roa.items()}
print(f"可救回比例：u_max=inf {frac[np.inf]:.0%}，u_max=10 N {frac[10.0]:.0%}")
check("二維切片：推力飽和讓吸引域面積縮小", frac[10.0] < frac[np.inf])
R_ = roa[np.inf][th_grid > 0]
check("吸引域是斜的：θ0>0 時往回倒（θ̇0<0）比繼續倒（θ̇0>0）更容易救回",
      R_[:, thd_grid < 0].sum() > R_[:, thd_grid > 0].sum())

if want_plot():                                    # python labC2_cartpole_lqr.py --plot
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    fig, ax = plt.subplots(1, 2, figsize=(9, 3.6), sharey=True)
    for a, (u, R_) in zip(ax, roa.items()):
        a.imshow(R_.T, origin="lower", aspect="auto", cmap="Greens",
                 extent=[np.degrees(th_grid[0]) - 5, np.degrees(th_grid[-1]) + 5, thd_grid[0] - .5, thd_grid[-1] + .5])
        a.set_title(f"u_max = {u}"); a.set_xlabel("θ0 (deg)")
    ax[0].set_ylabel("θ̇0 (rad/s)"); fig.tight_layout(); fig.savefig(out_path("labC2_roa.png"), dpi=120)
    print("圖已存到", out_path("labC2_roa.png"))
