"""Lab 05 — 一維受力模型（對應原書 Ch5 Forces in One Dimension）
力模型：重力、黏滯阻力（線性/二次）、彈簧力。範例：雨滴終端速度、懸掛彈簧木塊。
改用 scipy.integrate.solve_ivp（自適應步長 RK45）取代手寫迴圈。
"""
import numpy as np
from scipy.integrate import solve_ivp

from labutils import check

g = 9.81
# ---------- 雨滴：二次阻力 F = -D v|v| ----------
m = 4.2e-6                      # 直徑 2 mm 水滴質量 ≈ ρ_w·(4/3)π r^3
D = 0.5 * 1.2 * 0.5 * np.pi * (1e-3)**2   # ½·ρ_air·C_d·A，C_d≈0.5（球體近似）
vt = np.sqrt(m * g / D)         # 終端速度：mg = D vt^2

def raindrop(t, s):
    y, v = s                    # 向下為正
    return [v, g - (D / m) * v * abs(v)]

sol = solve_ivp(raindrop, (0, 10), [0, 0], dense_output=True, rtol=1e-9, atol=1e-12)
tt = np.linspace(0, 10, 200)
v_exact = vt * np.tanh(g * tt / vt)            # 解析解
err = np.max(np.abs(sol.sol(tt)[1] - v_exact))
print(f"終端速度 vt = {vt:.2f} m/s，數值 vs 解析最大誤差 {err:.1e}")
check("二次阻力數值解與 tanh 解析解一致", err < 1e-6)

# ---------- 懸掛木塊：彈簧 + 重力 ----------
k, mb, L0 = 20.0, 0.5, 0.3
x_eq = L0 + mb * g / k          # 平衡伸長
w = np.sqrt(k / mb)

def block(t, s):
    x, v = s                    # x：從懸掛點向下量的彈簧長度
    return [v, g - (k / mb) * (x - L0)]

x0 = L0                          # 從自然長度靜止釋放
sol = solve_ivp(block, (0, 5), [x0, 0], dense_output=True, rtol=1e-10, atol=1e-12)
x_exact = x_eq + (x0 - x_eq) * np.cos(w * tt / 2)   # tt/2 → 0..5 s
err = np.max(np.abs(sol.sol(tt / 2)[0] - x_exact))
print(f"週期 T = {2*np.pi/w:.3f} s，振盪中心 {x_eq:.4f} m，誤差 {err:.1e}")
check("彈簧木塊繞 x_eq 做簡諧運動", err < 1e-7)

# ---------- 電梯中的體重計（Newton 第三定律）----------
def scale_reading(m_person, a_elevator):        # a 向上為正
    return m_person * (g + a_elevator)          # N = m(g+a)
check("向上加速時體重計讀數變大", scale_reading(70, 2.0) > 70 * g)
check("自由落體時讀數為 0", np.isclose(scale_reading(70, -g), 0.0))
