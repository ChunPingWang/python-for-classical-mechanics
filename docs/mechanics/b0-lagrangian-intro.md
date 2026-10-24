# Part B — Lagrangian 力學（補充）

> [教材目錄](README.md)｜[章節對照總表](README.md#1-章節對照總表)

## B.0 為什麼需要 Lagrangian

原書全程使用牛頓法：畫自由體圖，列出 $\sum\mathbf F=m\mathbf a$，再解約束力。這套方法對單一物體很直觀。但到了 cart-pole 這種**兩個互相耦合、有約束的物體**，就必須處理台車與擺桿之間的內力，容易出錯。

Lagrangian 法只需要四個步驟（Taylor Ch7）：

1. 選**廣義座標** $q$，數量等於自由度。cart-pole 取 $q=(x,\theta)$。
2. 寫出動能 $T(q,\dot q)$ 和位能 $V(q)$，令 $L=T-V$。
3. **Euler–Lagrange 方程**：$\dfrac{d}{dt}\dfrac{\partial L}{\partial\dot q_i}-\dfrac{\partial L}{\partial q_i}=Q_i$，其中 $Q_i$ 是非保守廣義力，例如推力 $F$ 只作用在 $x$ 上。
4. 整理成機器人學的標準 **manipulator form**：

$$M(q)\ddot q + C(q,\dot q)\dot q = \tau_g(q) + B u$$

約束力完全不會出現在方程中。這個形式也正是 Tedrake 講義和 MuJoCo、Drake 等模擬器內部使用的形式。

**cart-pole 的運動方程**（$\theta$ 從垂直向上量起；擺桿質量 $m$、質心距轉軸 $l$、繞質心轉動慣量 $J$）：

$$
\begin{aligned}
(M+m)\ddot x + ml\cos\theta\,\ddot\theta &= F + ml\sin\theta\,\dot\theta^2\\
ml\cos\theta\,\ddot x + (J+ml^2)\ddot\theta &= mgl\sin\theta
\end{aligned}
$$

這兩條方程由 Lab B1 用 sympy 自動推導，並和手寫的 `cartpole.py` 交叉比對。

Lagrangian 法還帶來兩個額外收穫：
- **Noether 定理**：$x$ 不出現在 $L$ 中（循環座標），所以無推力時 $p_x=\partial L/\partial\dot x$ 守恆。
- **Hamiltonian**：$H=\sum p_i\dot q_i-L$。它是 Taylor Ch13 的起點，也是 Lab 10-11 中 symplectic 積分器的理論根據。

## B.1 共用模型 `cartpole.py`

Part C 的所有控制實驗都使用這個模型。換成自己的硬體時，只需要修改 `PARAMS`，最好填入系統辨識得到的參數。

**程式碼**：[`cartpole.py`](../../m1-inverted-pendulum/sim/mechanics-labs/cartpole.py)　｜　模型模組，由 Lab B1、C2–C4 匯入（單獨執行不會有輸出）

---

[← Lab 14-16](a14-16-rigid-body.md)　｜　[目錄](README.md)　｜　[Lab B1 →](b1-lagrangian-cartpole.md)
