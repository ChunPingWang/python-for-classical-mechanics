"""Lab C3 — 能量式甩起 (energy-shaping swing-up) + LQR 接手（補充；對應 Tedrake Cart-Pole 章的 swing-up 與 partial feedback linearization）
把 Lab 10-11 的「能量」直接當成控制目標：
  擺桿能量 E = ½ J_p θ̇² + m g l cosθ，倒立靜止時 E_d = m g l
  以台車加速度 a 為「虛擬輸入」：Ė = -m l θ̇ cosθ · a
  取 a = k_E (E - E_d) θ̇ cosθ  ⇒  d/dt (E-E_d) = -k_E m l θ̇² cos²θ (E-E_d) ≤ 0   → 能量單調逼近 E_d
再用 collocated partial feedback linearization 把 a 換算成真正的推力 F。
"""
import numpy as np
from scipy.linalg import solve_continuous_are
import cartpole as cp

def check(name, cond):
    print(f"[{'PASS' if cond else 'FAIL'}] {name}")
    assert cond, name

p = cp.PARAMS
m, l, g, M = p["m"], p["l"], p["g"], p["M"]
Jp = p["J"] + m * l**2
E_d = m * g * l

A, B = cp.linearize_upright()
K = np.linalg.solve([[0.1]], B.T @ solve_continuous_are(A, B, np.diag([10, 100, 1, 1.0]), [[0.1]]))

def force_for_cart_accel(s, a):
    """collocated PFL：已知想要的 ẍ = a，由兩條運動方程反解推力 F（假設無摩擦）"""
    th, thd = s[1], s[3]
    thdd = (m * g * l * np.sin(th) - m * l * np.cos(th) * a) / Jp
    return (M + m) * a + m * l * np.cos(th) * thdd - m * l * np.sin(th) * thd**2

class SwingUpLQR:
    def __init__(self, kE=2.0, kx=2.0, kv=2.5, a_max=8.0, F_max=20.0, switch=0.35):
        self.kE, self.kx, self.kv, self.a_max, self.F_max, self.switch = kE, kx, kv, a_max, F_max, switch
        self.mode_log = []
    def __call__(self, t, s):
        e = s.copy(); e[1] = cp.wrap(s[1])
        if abs(e[1]) < self.switch and abs(e[3]) < 4.0:          # 進入吸引域 → LQR 接手
            self.mode_log.append(1)
            return float(np.clip(-(K @ e)[0], -self.F_max, self.F_max))
        self.mode_log.append(0)
        E_err = cp.pole_energy(s) - E_d
        a = self.kE * E_err * s[3] * np.cos(s[1]) - self.kx * s[0] - self.kv * s[2]   # 能量泵 + 台車拉回中央
        a = np.clip(a, -self.a_max, self.a_max)
        return float(np.clip(force_for_cart_accel(s, a), -self.F_max, self.F_max))

# 從「幾乎」自然下垂出發（完全靜止下垂時 θ̇=0，能量泵沒有槓桿 → 給一點初始偏擺）
ctrl = SwingUpLQR()
t, S, U = cp.simulate(ctrl, [0.0, np.pi - 0.1, 0.0, 0.0], T=12.0, dt=1e-3)
th_w = cp.wrap(S[:, 1])
modes = np.array(ctrl.mode_log)
t_switch = t[np.argmax(modes == 1)] if modes.any() else np.nan
print(f"切換到 LQR 的時間 ≈ {t_switch:.2f} s；最終 θ = {th_w[-1]:+.1e} rad，x = {S[-1,0]:+.3f} m")
print(f"台車行程範圍 [{S[:,0].min():+.2f}, {S[:,0].max():+.2f}] m，最大推力 {np.max(np.abs(U)):.1f} N")
check("12 s 內成功甩起並穩定在倒立點", np.all(np.abs(th_w[t > 10]) < 0.01))
check("台車回到中央附近（|x| < 0.05 m）", abs(S[-1, 0]) < 0.05)
check("推力未超過 F_max", np.max(np.abs(U)) <= ctrl.F_max + 1e-9)
check("台車行程 < ±1 m（實體軌道限制）", np.max(np.abs(S[:, 0])) < 1.0)

# 能量泵階段：擺桿能量誤差應該整體趨近 0
pump = t < t_switch
E_err = np.array([cp.pole_energy(s) - E_d for s in S[pump]])
print(f"甩起階段 |E-E_d|：起始 {abs(E_err[0]):.3f} J → 切換前 {abs(E_err[-1]):.3f} J")
check("甩起階段能量誤差顯著縮小（< 起始 15%）", abs(E_err[-1]) < 0.15 * abs(E_err[0]))

# 只用 LQR、不做 swing-up：從下垂出發會失敗（對照組）
lqr_only = lambda t, s: float(np.clip(-(K @ np.array([s[0], cp.wrap(s[1]), s[2], s[3]]))[0], -20, 20))
with np.errstate(all="ignore"):
    t2, S2, _ = cp.simulate(lqr_only, [0.0, np.pi - 0.1, 0.0, 0.0], T=12.0, dt=1e-3)
fail = (not np.all(np.isfinite(S2))) or np.any(np.abs(cp.wrap(S2[t2 > 10, 1])) > 0.1) or np.max(np.abs(S2[:, 0])) > 1.0
check("對照組：只用 LQR 從下垂出發會失敗（超出線性化的吸引域或撞出軌道）", fail)
