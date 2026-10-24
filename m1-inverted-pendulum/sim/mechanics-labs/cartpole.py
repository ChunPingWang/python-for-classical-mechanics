"""cartpole.py — 倒立擺（cart-pole）共用模型；Lab B1 用 sympy 從 Lagrangian 推導並驗證本檔方程式。

座標：x = 台車位置（向右為正），θ = 擺桿與「垂直向上」的夾角（θ=0 為倒立，θ=π 為自然下垂）。
擺桿：質量 m、質心距轉軸 l、繞質心轉動慣量 J；台車質量 M；水平推力 F 為輸入。
（若換成你自己的硬體，只要改 PARAMS。）

運動方程（manipulator form  M(q) q̈ = τ_g + C + B u）：
    (M+m) ẍ + m l cosθ θ̈ = F + m l sinθ θ̇² - b_x ẋ
    m l cosθ ẍ + (J + m l²) θ̈ = m g l sinθ - b_θ θ̇
"""
import numpy as np

PARAMS = dict(M=0.5, m=0.2, l=0.3, g=9.81, b_x=0.0, b_th=0.0)
PARAMS["J"] = PARAMS["m"] * (2 * PARAMS["l"]) ** 2 / 12      # 均勻細桿，總長 2l

def mass_matrix(th, p=PARAMS):
    return np.array([[p["M"] + p["m"], p["m"] * p["l"] * np.cos(th)],
                     [p["m"] * p["l"] * np.cos(th), p["J"] + p["m"] * p["l"] ** 2]])

def dynamics(t, s, F, p=PARAMS):
    """s = [x, θ, ẋ, θ̇]，回傳 ṡ。F 可以是常數或 callable F(t, s)。"""
    x, th, xd, thd = s
    u = F(t, s) if callable(F) else F
    s_, c_ = np.sin(th), np.cos(th)
    r1 = u + p["m"] * p["l"] * s_ * thd ** 2 - p["b_x"] * xd
    r2 = p["m"] * p["g"] * p["l"] * s_ - p["b_th"] * thd
    a11, a12, a22 = p["M"] + p["m"], p["m"] * p["l"] * c_, p["J"] + p["m"] * p["l"] ** 2
    det = a11 * a22 - a12 ** 2                       # 2×2 反矩陣寫開，比 np.linalg.solve 快很多
    xdd = (a22 * r1 - a12 * r2) / det
    thdd = (a11 * r2 - a12 * r1) / det
    return np.array([xd, thd, xdd, thdd])

def simulate(controller, s0, T, dt=1e-3, dt_ctrl=None, p=PARAMS):
    """固定步長 RK4 + 零階保持 (ZOH)：控制器每 dt_ctrl 秒算一次、期間輸出不變，貼近真實 MCU。
    controller(t, s) -> F。回傳 (t, S, U)。"""
    dt_ctrl = dt_ctrl or dt
    hold = max(1, int(round(dt_ctrl / dt)))
    n = int(round(T / dt))
    S = np.zeros((n + 1, 4)); U = np.zeros(n + 1); S[0] = s0
    u = 0.0
    for i in range(n):
        s = S[i]
        if i % hold == 0:
            u = controller(i * dt, s)
        k1 = dynamics(0, s, u, p); k2 = dynamics(0, s + dt / 2 * k1, u, p)
        k3 = dynamics(0, s + dt / 2 * k2, u, p); k4 = dynamics(0, s + dt * k3, u, p)
        S[i + 1] = s + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        U[i] = u
    U[-1] = u
    return np.arange(n + 1) * dt, S, U

def energy(s, p=PARAMS):
    x, th, xd, thd = s
    T = 0.5 * (p["M"] + p["m"]) * xd ** 2 + p["m"] * p["l"] * xd * thd * np.cos(th) \
        + 0.5 * (p["J"] + p["m"] * p["l"] ** 2) * thd ** 2
    V = p["m"] * p["g"] * p["l"] * np.cos(th)
    return T + V

def pole_energy(s, p=PARAMS):
    """只算擺桿相對轉軸的能量（swing-up 用），倒立靜止時 = m g l。"""
    th, thd = s[1], s[3]
    return 0.5 * (p["J"] + p["m"] * p["l"] ** 2) * thd ** 2 + p["m"] * p["g"] * p["l"] * np.cos(th)

def linearize_upright(p=PARAMS):
    """在 θ=0、全靜止處線性化：ṡ = A s + B F。"""
    Minv = np.linalg.inv(mass_matrix(0.0, p))
    dG = np.array([[0, 0], [0, p["m"] * p["g"] * p["l"]]])     # ∂(右手邊)/∂q
    D = np.diag([p["b_x"], p["b_th"]])
    A = np.zeros((4, 4)); A[0:2, 2:4] = np.eye(2)
    A[2:4, 0:2] = Minv @ dG
    A[2:4, 2:4] = -Minv @ D
    B = np.zeros((4, 1)); B[2:4, 0] = Minv @ np.array([1.0, 0.0])
    return A, B

def wrap(th):
    """角度包到 (-π, π]，θ=0 為倒立。"""
    return (th + np.pi) % (2 * np.pi) - np.pi
