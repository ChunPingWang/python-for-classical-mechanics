"""Lab C1 — 控制入門：力矩驅動單擺的 PID 與回授線性化（補充；對應 Tedrake《Underactuated Robotics》The Simple Pendulum 章）
這是「全驅動 (fully actuated)」系統：馬達直接作用在 θ 上。重點：
1) P → 會振盪；PD → 收斂；PID → 消除定常干擾造成的誤差
2) 回授線性化：把重力「抵銷」掉，閉迴路變成線性
3) 力矩飽和：小馬達撐不起來 → 需要利用能量（C3 swing-up）
"""
import numpy as np
from scipy.integrate import solve_ivp

from labutils import check

m, l, b, g = 0.5, 0.4, 0.02, 9.81
I = m * l**2
# θ 從「垂直向上」量起：I θ̈ = m g l sinθ - b θ̇ + u + d（d 為外部干擾力矩）
def make_rhs(controller, d=0.0, u_max=np.inf):
    def rhs(t, s):
        th, w, z = s                          # z = ∫θ dt（積分項狀態）
        u = np.clip(controller(th, w, z), -u_max, u_max)
        return [w, (m * g * l * np.sin(th) - b * w + u + d) / I, th]
    return rhs

def run(controller, th0=0.3, d=0.0, u_max=np.inf, T=6.0):
    sol = solve_ivp(make_rhs(controller, d, u_max), (0, T), [th0, 0, 0],
                    max_step=5e-3, rtol=1e-8, atol=1e-10)      # max_step 只是為了讓飽和切換不被跳過
    return sol.t, sol.y

# 以「期望閉迴路自然頻率 ωn、阻尼比 ζ」來設計 PD 增益（線性化後 I θ̈ = (mgl - Kp) θ - (b+Kd) θ̇）
wn, zeta = 8.0, 0.8
Kp = I * wn**2 + m * g * l               # 要先「贏過」重力造成的負剛性
Kd = 2 * zeta * wn * I - b
Ki = 0.5 * Kp
print(f"Kp={Kp:.3f}, Kd={Kd:.3f}, Ki={Ki:.3f}")

P   = lambda th, w, z: -Kp * th
PD  = lambda th, w, z: -Kp * th - Kd * w
PID = lambda th, w, z: -Kp * th - Kd * w - Ki * z

t, y = run(P)
check("只有 P：4 s 後仍大幅振盪（只靠機械摩擦慢慢衰減）", np.max(np.abs(y[0, t > 4])) > 0.1)
t, y = run(PD)
check("PD：3 s 內收斂到 |θ|<1e-3", np.max(np.abs(y[0, t > 3])) < 1e-3)

d = 0.15                                   # 定常干擾力矩（例如線材拉扯）
t, y = run(PD, d=d)
ss_pd = y[0, -1]
t, y = run(PID, d=d, T=10)
ss_pid = y[0, -1]
print(f"定常干擾下穩態誤差：PD {ss_pd:+.4f} rad，PID {ss_pid:+.2e} rad")
check("PD 有穩態誤差 ≈ d/(Kp-mgl)", np.isclose(ss_pd, d / (Kp - m * g * l), rtol=0.02))
check("PID 積分項把穩態誤差消掉", abs(ss_pid) < 1e-3)

# ---------- 回授線性化：u = -m g l sinθ + I·v，v 為線性控制律 ----------
FL = lambda th, w, z: -m * g * l * np.sin(th) + b * w + I * (-wn**2 * th - 2 * zeta * wn * w)
t, y = run(FL, th0=2.5)                    # 大角度也一樣好用（只要力矩夠大）
check("回授線性化：從 θ0=2.5 rad 也能直接拉回倒立", np.max(np.abs(y[0, t > 3])) < 1e-3)

# ---------- 力矩飽和：從下垂位置出發 ----------
u_need = m * g * l                         # 從水平撐住需要的最小靜力矩
for u_max in [3 * u_need, 0.5 * u_need]:
    t, y = run(FL, th0=np.pi - 0.01, u_max=u_max, T=8)
    up = np.max(np.abs(np.cos(y[0, t > 6]) - 1)) < 1e-3
    print(f"u_max = {u_max:.3f} N·m ({u_max/u_need:.1f}×mgl)：{'成功倒立' if up else '失敗，困在下方擺動'}")
    if u_max > u_need:
        check("力矩充足時 PD/FL 可以直接把擺舉起來", up)
    else:
        check("力矩不足（< mgl）時直接舉不起來 → 需要能量式 swing-up", not up)
