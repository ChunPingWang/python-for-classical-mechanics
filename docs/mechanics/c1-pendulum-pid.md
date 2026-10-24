# Lab C1 — 力矩驅動單擺：PID 與回授線性化（Tedrake Ch2）

> Part C — 控制（補充）｜[教材目錄](README.md)｜[章節對照總表](README.md#1-章節對照總表)

**學習目標**：從期望的自然頻率 $\omega_n$ 和阻尼比 $\zeta$ 推出 PD 增益；理解積分項消除穩態誤差的機制；理解回授線性化的能力和它的力矩代價。

**核心觀念**：
- 倒立點線性化後是 $I\ddot\theta=(mgl-K_p)\theta-(b+K_d)\dot\theta$，所以 $K_p$ 必須先大於 $mgl$，才能抵消重力造成的「負剛性」。
- 有定常干擾 $d$ 時，PD 的穩態誤差為 $d/(K_p-mgl)$。加入積分項後誤差歸零。
- 回授線性化 $u=-mgl\sin\theta+b\dot\theta+I v$ 可以讓閉迴路變成線性系統。但它要求的力矩大於 $mgl$；馬達力矩不足時就失效，這就是 Lab C3 swing-up 的動機。

**程式碼**：[`labC1_pendulum_pid.py`](../../m1-inverted-pendulum/sim/mechanics-labs/labC1_pendulum_pid.py)　｜　執行：`python labC1_pendulum_pid.py`

**預期輸出**
```
Kp=7.082, Kd=1.004, Ki=3.541
[PASS] 只有 P：4 s 後仍大幅振盪（只靠機械摩擦慢慢衰減）
[PASS] PD：3 s 內收斂到 |θ|<1e-3
定常干擾下穩態誤差：PD +0.0293 rad，PID -6.62e-06 rad
[PASS] PD 有穩態誤差 ≈ d/(Kp-mgl)
[PASS] PID 積分項把穩態誤差消掉
[PASS] 回授線性化：從 θ0=2.5 rad 也能直接拉回倒立
u_max = 5.886 N·m (3.0×mgl)：成功倒立
[PASS] 力矩充足時 PD/FL 可以直接把擺舉起來
u_max = 0.981 N·m (0.5×mgl)：失敗，困在下方擺動
[PASS] 力矩不足（< mgl）時直接舉不起來 → 需要能量式 swing-up
```

---

[← Part C](c0-control-intro.md)　｜　[目錄](README.md)　｜　[Lab C2 →](c2-cartpole-lqr.md)
