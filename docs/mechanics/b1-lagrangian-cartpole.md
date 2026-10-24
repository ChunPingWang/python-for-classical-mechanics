# Lab B1 — 用 sympy 從 $L=T-V$ 推導 cart-pole（Taylor Ch7、Ch13）★

> Part B — Lagrangian 力學（補充）｜[教材目錄](README.md)｜[章節對照總表](README.md#1-章節對照總表)

**學習目標**：寫出通用的 `euler_lagrange()` 函式；推導 cart-pole 並驗證手寫模型；在倒立點線性化，得到 $(A,B)$ 並檢查可控性。

**核心觀念**：
- 狀態 $s=[x,\theta,\dot x,\dot\theta]$。在 $s=0$ 處線性化得到 $\dot s=As+BF$。
- **可控性**：$\mathrm{rank}[B,\,AB,\,A^2B,\,A^3B]=4$，代表只用一個推力就能同時穩住台車和擺桿。這正是 underactuated（輸入數少於自由度）卻仍然可控的關鍵。
- 用有限差分 Jacobian 交叉驗證解析的 $A,B$，可以抓出推導或實作中的錯誤。

**程式碼**：[`labB1_lagrangian_cartpole.py`](../../m1-inverted-pendulum/sim/mechanics-labs/labB1_lagrangian_cartpole.py)　｜　執行：`python labB1_lagrangian_cartpole.py`

**預期輸出**
```
單擺：θ̈ = -g*sin(theta(t))/l
[PASS] 單擺得到 θ̈ = -(g/l) sinθ
M(q) = Matrix([[M + m, l*m*cos(theta(t))], [l*m*cos(theta(t)), J + l**2*m]])
rhs  = Matrix([[F + l*m*sin(theta(t))*Derivative(theta(t), t)**2, g*l*m*sin(theta(t))]])
[PASS] sympy 推導結果 = cartpole.py 手寫模型（20 組隨機狀態）
被動擺動 10 s 能量相對誤差 3.0e-10
[PASS] 被動系統能量守恆
[PASS] 動量 p_x 守恆（x 為循環座標，Noether）
A 的特徵值: [-5.587  0.     0.     5.587]
[PASS] 倒立點開迴路不穩定（有正特徵值）
[PASS] 可控性矩陣滿秩（rank 4）→ 一個推力就能穩住兩個自由度
[PASS] 解析 A, B = 有限差分 Jacobian
單擺 Hamiltonian H = -g*l*m*cos(theta(t)) + p_theta**2/(2*l**2*m)
[PASS] H = p²/(2ml²) - mgl cosθ = 總能量
```

**延伸練習**：
1. 在 `Qs` 加入摩擦 $-b_x\dot x$ 和 $-b_\theta\dot\theta$，重新推導，並和 `cartpole.py` 的 `b_x`、`b_th` 參數比對。
2. 換成 **Furuta 旋轉倒立擺**（台車改成旋臂）。只要重寫 $T$ 和 $V$，其餘程式碼完全不用改。

---

[← Part B](b0-lagrangian-intro.md)　｜　[目錄](README.md)　｜　[Lab B2 →](b2-double-pendulum.md)
