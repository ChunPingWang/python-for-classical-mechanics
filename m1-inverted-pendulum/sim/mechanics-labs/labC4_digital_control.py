"""Lab C4 — 從模擬走向硬體：取樣、量化、雜訊、延遲、飽和（補充；銜接自學手冊的實體倒立擺里程碑）
真實 MCU 控制迴路和 Lab C2 的「連續時間理想 LQR」差在哪裡？
  1) 控制器以固定頻率執行（ZOH）       → 用離散 LQR（c2d + DARE）設計
  2) 只量得到 x、θ（編碼器量化）        → 速度要自己差分 + 低通濾波
  3) 運算/通訊延遲一個取樣週期
  4) 馬達推力有上限
"""
import numpy as np
from scipy.signal import cont2discrete
from scipy.linalg import solve_discrete_are, solve_continuous_are
import cartpole as cp

def check(name, cond):
    print(f"[{'PASS' if cond else 'FAIL'}] {name}")
    assert cond, name

A, B = cp.linearize_upright()
Q, R = np.diag([10.0, 100.0, 1.0, 1.0]), np.array([[0.1]])

def dlqr(Ts):
    Ad, Bd, *_ = cont2discrete((A, B, np.eye(4), np.zeros((4, 1))), Ts, method="zoh")
    P = solve_discrete_are(Ad, Bd, Q * Ts, R * Ts)            # 權重乘 Ts：與連續版成本同尺度
    return np.linalg.solve(R * Ts + Bd.T @ P @ Bd, Bd.T @ P @ Ad), Ad, Bd

K_c = np.linalg.solve(R, B.T @ solve_continuous_are(A, B, Q, R))

class DigitalController:
    """模擬一顆 MCU：只讀編碼器、自己估速度、輸出延遲一拍、推力飽和。"""
    def __init__(self, K, Ts, enc_cpr=4096, x_res=1e-4, noise=0.0, delay=1, F_max=10.0, f_cut=None, seed=0):
        self.K, self.Ts, self.delay, self.F_max = K, Ts, delay, F_max
        self.th_res = 2 * np.pi / enc_cpr
        self.x_res, self.noise = x_res, noise
        self.rng = np.random.default_rng(seed)
        fc = f_cut or 0.25 / Ts                                   # 一階低通截止頻率（預設 Nyquist/2）
        self.alpha = 1 - np.exp(-2 * np.pi * fc * Ts)
        self.prev = None; self.v_est = np.zeros(2); self.u_queue = [0.0] * delay
    def measure(self, s):
        x = np.round((s[0] + self.noise * self.rng.normal()) / self.x_res) * self.x_res
        th = np.round((cp.wrap(s[1]) + self.noise * self.rng.normal()) / self.th_res) * self.th_res
        return np.array([x, th])
    def __call__(self, t, s):
        y = self.measure(s)
        if self.prev is not None:
            raw = (y - self.prev) / self.Ts
            raw[1] = cp.wrap(y[1] - self.prev[1]) / self.Ts
            self.v_est += self.alpha * (raw - self.v_est)          # 差分 + 低通
        self.prev = y
        e = np.array([y[0], y[1], *self.v_est])
        u = float(np.clip(-(self.K @ e)[0], -self.F_max, self.F_max))
        self.u_queue.append(u)
        return self.u_queue.pop(0)                                 # 延遲 delay 拍才送到馬達

def trial(Ts, use_dlqr=True, **kw):
    K = dlqr(Ts)[0] if use_dlqr else K_c
    ctrl = DigitalController(K, Ts, **kw)
    with np.errstate(all="ignore"):
        t, S, U = cp.simulate(ctrl, [0.0, 0.15, 0.0, 0.0], T=8.0, dt=5e-4, dt_ctrl=Ts)
    ok = bool(np.all(np.isfinite(S)) and np.max(np.abs(cp.wrap(S[t > 6, 1]))) < 0.02
              and np.max(np.abs(S[:, 0])) < 1.0)
    rms = float(np.sqrt(np.mean(cp.wrap(S[t > 6, 1])**2))) if ok else np.nan
    return ok, rms

# ---------- 1) 取樣頻率掃描：離散 LQR vs 直接沿用連續 K ----------
print(" f_ctrl | 離散LQR | 連續K直接用")
res = {}
for f in [500, 200, 100, 50, 45, 40]:
    Ts = 1.0 / f
    res[f] = (trial(Ts, True)[0], trial(Ts, False)[0])
    print(f" {f:4d} Hz |  {'OK ' if res[f][0] else 'FAIL'}   |   {'OK ' if res[f][1] else 'FAIL'}")
check("200 Hz 以上兩種設計都能穩住", res[500] == (True, True) and res[200] == (True, True))
check("取樣變慢時，離散化設計的容忍度 ≥ 直接沿用連續增益",
      all(res[f][0] >= res[f][1] for f in res))
check("45 Hz：離散 LQR 仍穩、直接沿用連續 K 已失敗", res[45] == (True, False))
check("40 Hz + 1 拍延遲 → 兩者都失敗：取樣率是硬體規格，不是細節", res[40] == (False, False))
check("同樣 40 Hz 但沒有延遲 → 離散 LQR 可以穩住（延遲吃掉了相位裕度）", trial(1 / 40, True, delay=0)[0])

# ---------- 2) 延遲掃描（200 Hz）----------
max_ok = 0
for d in range(1, 16):
    if trial(1 / 200, True, delay=d)[0]:
        max_ok = d
    else:
        break
print(f"200 Hz 下可容忍的延遲 ≈ {max_ok} 拍 = {max_ok*5} ms（再多就失穩）")
check("延遲預算有限：數十 ms 等級", 1 <= max_ok < 15)

# ---------- 3) 量測雜訊 → 角度殘餘抖動 ----------
for noise in [0.0, 2e-3]:
    ok, rms = trial(1 / 200, True, noise=noise)
    print(f"量測雜訊 σ={noise:.0e}：{'穩定' if ok else '失敗'}，穩態 θ RMS = {rms:.1e} rad")
    if noise == 0.0:
        rms0 = rms
    else:
        check("加入雜訊仍穩定，但穩態抖動變大", ok and rms > rms0)
