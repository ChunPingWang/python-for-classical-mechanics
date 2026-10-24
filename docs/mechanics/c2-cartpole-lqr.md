# Lab C2 — cart-pole LQR 平衡（Tedrake Ch3、Ch8）★

> Part C — 控制（補充）｜[教材目錄](README.md)｜[章節對照總表](README.md#1-章節對照總表)

**學習目標**：解 Riccati 方程得到最佳增益；**回到非線性模型**驗證控制器；量化吸引域（region of attraction）。

**核心觀念**：
- LQR 最小化 $J=\int_0^\infty(s^\top Qs+u^\top Ru)\,dt$。解代數 Riccati 方程 $A^\top P+PA-PBR^{-1}B^\top P+Q=0$，得到 $K=R^{-1}B^\top P$。
- $V(s)=s^\top Ps$ 是閉迴路的 Lyapunov 函數。程式會驗證 $A_{cl}^\top P+PA_{cl}=-(Q+K^\top RK)$。
- 調整 $Q$ 和 $R$ 就是在角度誤差、台車位移和推力大小之間取捨。LQR 和極點配置都能穩定系統，但峰值推力和台車行程不同。
- **線性控制器只在局部有效**。本例在推力不受限時，最大可救回約 57°；推力限制在 10 N 時縮小到約 40°。更大的角度要交給 Lab C3 的甩起控制。

**程式碼**：[`labC2_cartpole_lqr.py`](../../m1-inverted-pendulum/sim/mechanics-labs/labC2_cartpole_lqr.py)　｜　執行：`python labC2_cartpole_lqr.py`

**預期輸出**
```
LQR K = [[-10.    -59.61  -10.841 -10.342]]
閉迴路特徵值 = [-12.297+0.95j -12.297-0.95j  -1.352+1.05j  -1.352-1.05j]
[PASS] A-BK 全部特徵值實部 < 0（線性系統漸近穩定）
[PASS] P 正定 且 Aclᵀ P + P Acl = -(Q + KᵀRK)
θ0=0.2 rad → 6 s 後 |s| = 1.6e-04
[PASS] 非線性模型：從 θ=0.2 rad 回到原點
LQR             峰值推力  11.92 N，台車最大偏移 0.170 m
pole placement  峰值推力   7.26 N，台車最大偏移 0.193 m
u_max =  inf N：可救回的最大初始角 ≈ 57°
u_max = 10.0 N：可救回的最大初始角 ≈ 40°
[PASS] 推力飽和會縮小吸引域
[PASS] 吸引域有限（> 30° 但不是全域）
```

**延伸練習**：把 $Q$ 的角度權重從 100 改成 10 和 1000，畫出 $\theta(t)$、$x(t)$、$F(t)$，建立調參的直覺。

---

[← Lab C1](c1-pendulum-pid.md)　｜　[目錄](README.md)　｜　[Lab C3 →](c3-swingup.md)
