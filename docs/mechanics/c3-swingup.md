# Lab C3 — 能量式甩起 + LQR 接手（Tedrake Ch3）★

> Part C — 控制（補充）｜[教材目錄](README.md)｜[章節對照總表](README.md#1-章節對照總表)

**學習目標**：把「能量」當成控制目標；用 collocated partial feedback linearization（PFL）把「想要的台車加速度」換算成推力；實作混合控制（hybrid control）的切換邏輯。

**推導**（擺桿能量相對轉軸，$J_p=J+ml^2$）：

$$
E=\tfrac12J_p\dot\theta^2+mgl\cos\theta,\qquad E_d=mgl\ (\text{倒立靜止})
$$

把台車加速度 $a=\ddot x$ 當成虛擬輸入，由第二條運動方程得到 $\dot E=-ml\,\dot\theta\cos\theta\,a$。選擇

$$
a=k_E\,(E-E_d)\,\dot\theta\cos\theta-k_x x-k_v\dot x
$$

如果暫時忽略後兩項台車回中項，可以得到 $\tfrac{d}{dt}(E-E_d)=-k_E\,ml\,\dot\theta^2\cos^2\theta\,(E-E_d)\le0$，所以能量會單調逼近倒立能量。後兩項讓台車不會跑出軌道。擺桿進入 $|\theta|<0.35$ rad 時，切換到 Lab C2 的 LQR。

- **PFL**：已知想要的 $\ddot x=a$，用第二條方程解出 $\ddot\theta$，再代入第一條方程求出所需的推力 $F$。
- **對照組**：只用 LQR、從下垂出發會失敗，因為下垂狀態遠遠超出線性化的吸引域。

**程式碼**：[`labC3_swingup.py`](../../m1-inverted-pendulum/sim/mechanics-labs/labC3_swingup.py)　｜　執行：`python labC3_swingup.py`

**預期輸出**
```
切換到 LQR 的時間 ≈ 4.06 s；最終 θ = -3.4e-07 rad，x = +0.000 m
台車行程範圍 [-0.32, +0.22] m，最大推力 5.5 N
[PASS] 12 s 內成功甩起並穩定在倒立點
[PASS] 台車回到中央附近（|x| < 0.05 m）
[PASS] 推力未超過 F_max
[PASS] 台車行程 < ±1 m（實體軌道限制）
甩起階段 |E-E_d|：起始 1.174 J → 切換前 0.009 J
[PASS] 甩起階段能量誤差顯著縮小（< 起始 15%）
[PASS] 對照組：只用 LQR 從下垂出發會失敗（超出線性化的吸引域或撞出軌道）
```

> 增益 `kE=2, kx=2, kv=2.5, a_max=8` 是在本模型參數下掃描出的一組可行值：台車行程約 ±0.3 m，峰值推力約 5.5 N。`kE` 越大，甩得越快，但台車行程也越大；`kE=6` 時行程超過 1 m。換成實體硬體時，必須依照實際軌道長度和馬達能力重新掃描。

---

[← Lab C2](c2-cartpole-lqr.md)　｜　[目錄](README.md)　｜　[Lab C4 →](c4-digital-control.md)
