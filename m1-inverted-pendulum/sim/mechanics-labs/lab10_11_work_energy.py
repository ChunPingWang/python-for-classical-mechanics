"""Lab 10-11 — 功、能量，以及「用能量守恆檢驗數值解」（對應原書 Ch10 Work、Ch11 Energy，特別是 11.6）
10.1 數值積分求功（梯形 / Simpson）、10.2 功能定理、11.3 能量圖、11.6 積分器能量漂移比較。
這一課直接連到控制：swing-up 控制器就是在「操控能量」(Lab C3)。
"""
import numpy as np
from scipy.integrate import trapezoid, simpson, solve_ivp

def check(name, cond):
    print(f"[{'PASS' if cond else 'FAIL'}] {name}")
    assert cond, name

# ---------- 10.1 數值積分求功：W = ∫ F(x) dx ----------
k, x1 = 100.0, 0.2
x = np.linspace(0, x1, 21)
F = k * x**3 / x1**2                 # 非線性「硬化彈簧」
W_exact = k * x1**2 / 4
for name, W in [("trapezoid", trapezoid(F, x=x)), ("simpson", simpson(F, x=x))]:
    print(f"{name:9s} W = {W:.6f} J (exact {W_exact:.6f})")
check("Simpson 對三次多項式精確", np.isclose(simpson(F, x=x), W_exact, rtol=1e-12))

# ---------- 10.2 功能定理：沿路徑做的功 = 動能變化 ----------
g, m = 9.81, 2.0
def slide(t, s):                     # 斜面下滑 + 動摩擦
    th, mu = np.radians(30), 0.2
    return [s[1], g * np.sin(th) - mu * g * np.cos(th)]
sol = solve_ivp(slide, (0, 2), [0, 0], rtol=1e-10, atol=1e-12)
d, v = sol.y[0, -1], sol.y[1, -1]
W_net = m * g * np.sin(np.radians(30)) * d - 0.2 * m * g * np.cos(np.radians(30)) * d
check("W_net = ΔK", np.isclose(W_net, 0.5 * m * v**2, rtol=1e-8))

# ---------- 11.3 能量圖：U(x) 的極值 = 平衡點 ----------
xs = np.linspace(-2, 2, 4000)        # 偶數點：網格不會剛好落在 x=0
U = xs**4 - 2 * xs**2                # 雙井位能
dU = 4 * xs**3 - 4 * xs              # F = -dU/dx
eq = xs[np.where(np.diff(np.sign(dU)))[0]]
print("平衡點 x ≈", np.round(eq, 3))
check("雙井位能平衡點為 -1, 0, +1", np.allclose(eq, [-1, 0, 1], atol=2e-3))
d2U = 12 * xs**2 - 4
check("x=0 為不穩定（U''<0），x=±1 為穩定（U''>0）",
      d2U[np.argmin(abs(xs))] < 0 and d2U[np.argmin(abs(xs - 1))] > 0)

# ---------- 11.6 能量守恆作為數值解的檢驗：單擺 50 個週期 ----------
L = 1.0
acc = lambda th: -(g / L) * np.sin(th)
Efun = lambda th, w: 0.5 * L**2 * w**2 + g * L * (1 - np.cos(th))

def integrate(method, dt=0.01, T=100.0):
    """回傳整段模擬中「最大」相對能量誤差（symplectic 方法的誤差會振盪，看終點會誤判）"""
    th, w = 1.0, 0.0
    E0, worst = Efun(th, w), 0.0
    for _ in range(int(T / dt)):
        if method == "euler":
            th, w = th + w * dt, w + acc(th) * dt
        elif method == "euler_cromer":           # 半隱式 / symplectic Euler
            w = w + acc(th) * dt
            th = th + w * dt
        elif method == "velocity_verlet":        # 二階 symplectic
            w_half = w + 0.5 * dt * acc(th)
            th = th + dt * w_half
            w = w_half + 0.5 * dt * acc(th)
        elif method == "rk4":
            f = lambda s: np.array([s[1], acc(s[0])])
            s = np.array([th, w])
            k1 = f(s); k2 = f(s + dt/2*k1); k3 = f(s + dt/2*k2); k4 = f(s + dt*k3)
            th, w = s + dt / 6 * (k1 + 2*k2 + 2*k3 + k4)
        worst = max(worst, abs(Efun(th, w) / E0 - 1))
    return worst

drift = {m: integrate(m) for m in ["euler", "euler_cromer", "velocity_verlet", "rk4"]}
for m, e in drift.items():
    print(f"{m:16s} max relative energy error over 100 s = {e:.2e}")
check("Euler 能量爆增 (>50%)", drift["euler"] > 0.5)
check("Euler-Cromer 只差一行順序，能量誤差 < 5%", drift["euler_cromer"] < 0.05)
long_run = integrate("euler_cromer", T=1000.0)
print(f"euler_cromer 跑 1000 s 的最大誤差 = {long_run:.2e}（與 100 s 幾乎相同 → 有界、不漂移）")
check("Euler-Cromer 誤差不隨時間累積", long_run < 1.2 * drift["euler_cromer"])
check("Verlet 二階 symplectic 誤差更小", drift["velocity_verlet"] < drift["euler_cromer"])
check("RK4 精度高但非 symplectic（短時間極準）", drift["rk4"] < 1e-6)
