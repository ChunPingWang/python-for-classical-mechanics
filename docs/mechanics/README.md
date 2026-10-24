# 力學 × Python × 控制：對應《Elementary Mechanics Using Python》的現代化教材與實驗

> **版本** v1（2026-10-24）｜**定位**：Physical AI 自學手冊的「力學 → 模擬 → 控制」主線教材，終點是倒立擺（cart-pole）甩起與平衡。
> **驗證狀態**：本文所有程式碼都已實際執行，15 支實驗共 92 項自動檢核全部 PASS（測試環境：Python 3.13.15 / numpy 2.5.3 與 Python 3.12.14 / numpy 2.5.4，scipy 1.18.1、sympy 1.14.0、matplotlib 3.11.2，macOS Accelerate BLAS）。

---

## 0. 怎麼使用這份教材

### 0.1 設計原則

1. **章節對應原書**。Part A 的 Lab 02–16 依照 Malthe-Sørenssen《Elementary Mechanics Using Python》(Springer, 2015) 的 16 章順序排列。每一課標出對應的原書章節與範例。程式碼全部重寫，不複製原書內容。
2. **把舊寫法換成現代寫法**。原書使用 Python 2 語法（`print TF`、整數除法）和 `from pylab import *`。本教材改用以下寫法：
   - `numpy` 向量化
   - `matplotlib` 物件導向 API
   - `np.random.default_rng`
   - `scipy.integrate.solve_ivp`
   - `sympy` 符號推導
3. **每支程式都會自我驗證**。每個 Lab 都用 `check()` 把數值結果和解析解、守恆律或理論預測比對。PASS 代表模型、演算法和實作三者一致。這延續了原書 11.6 節「用能量守恆檢驗數值解」的精神，並把它推廣到每一課。
4. **補上原書沒有的兩塊**。
   - **Part B：Lagrangian 力學**。對應 Taylor《Classical Mechanics》Ch7、11、12、13。
   - **Part C：控制**。對應 Tedrake《Underactuated Robotics》Ch2、3、8，內容涵蓋 PID、LQR、能量式甩起，以及數位實作時要面對的現實問題。

### 0.2 環境與執行

程式在 [`m1-inverted-pendulum/sim/mechanics-labs/`](../../m1-inverted-pendulum/sim/mechanics-labs/)。

```bash
cd m1-inverted-pendulum/sim/mechanics-labs
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python run_all.py            # 一次跑完全部 Lab，彙整 PASS/FAIL
python labC3_swingup.py      # 或單獨執行任一課
```

- 需要 `numpy>=2.0`，因為 Lab 14–16 使用 `np.trapezoid`。在舊版 numpy 中，這個函式叫 `np.trapz`。
- 所有程式放在同一個資料夾，`labB*`、`labC*` 會 `import cartpole`。
- 每個 Lab 的「預期輸出」都是在上述環境實際跑出來的結果。不同平台在最後幾位小數可能略有差異，但 PASS/FAIL 不應改變。如果出現 FAIL，代表環境或程式有差異，值得追查。

### 0.3 檔案一覽

| 程式 | 文件 | 內容 | 檢核數 |
|---|---|---|---|
| [`lab02_python_basics.py`](../../m1-inverted-pendulum/sim/mechanics-labs/lab02_python_basics.py) | [a02-python-basics.md](a02-python-basics.md) | Ch2 向量化、數值微分、隨機漫步 | 3 |
| [`lab03_units_floats.py`](../../m1-inverted-pendulum/sim/mechanics-labs/lab03_units_floats.py) | [a03-units-floats.md](a03-units-floats.md) | Ch3 單位、浮點、事件內插 | 6 |
| [`lab04_motion_1d.py`](../../m1-inverted-pendulum/sim/mechanics-labs/lab04_motion_1d.py) | [a04-motion-1d.md](a04-motion-1d.md) | Ch4 資料↔運動、Euler | 4 |
| [`lab05_forces_1d.py`](../../m1-inverted-pendulum/sim/mechanics-labs/lab05_forces_1d.py) | [a05-forces-1d.md](a05-forces-1d.md) | Ch5 阻力、彈簧、電梯 | 4 |
| [`lab06_07_motion_forces_2d.py`](../../m1-inverted-pendulum/sim/mechanics-labs/lab06_07_motion_forces_2d.py) | [a06-07-motion-forces-2d.md](a06-07-motion-forces-2d.md) | Ch6-7 參考系、拋體、Kepler | 7 |
| [`lab08_09_constrained_friction.py`](../../m1-inverted-pendulum/sim/mechanics-labs/lab08_09_constrained_friction.py) | [a08-09-constrained-friction.md](a08-09-constrained-friction.md) | Ch8-9 摩擦、圓周、單擺 | 7 |
| [`lab10_11_work_energy.py`](../../m1-inverted-pendulum/sim/mechanics-labs/lab10_11_work_energy.py) | [a10-11-work-energy.md](a10-11-work-energy.md) | Ch10-11 功能、能量圖、積分器 | 9 |
| [`lab12_13_momentum_systems.py`](../../m1-inverted-pendulum/sim/mechanics-labs/lab12_13_momentum_systems.py) | [a12-13-momentum-systems.md](a12-13-momentum-systems.md) | Ch12-13 碰撞、火箭、質心 | 6 |
| [`lab14_16_rigid_body.py`](../../m1-inverted-pendulum/sim/mechanics-labs/lab14_16_rigid_body.py) | [a14-16-rigid-body.md](a14-16-rigid-body.md) | Ch14-16 轉動慣量、滾動、物理擺 | 6 |
| [`cartpole.py`](../../m1-inverted-pendulum/sim/mechanics-labs/cartpole.py) | [b0-lagrangian-intro.md](b0-lagrangian-intro.md) | 共用 cart-pole 模型（被 B、C 匯入） | — |
| [`labB1_lagrangian_cartpole.py`](../../m1-inverted-pendulum/sim/mechanics-labs/labB1_lagrangian_cartpole.py) | [b1-lagrangian-cartpole.md](b1-lagrangian-cartpole.md) | Lagrangian 推導 cart-pole、線性化 | 8 |
| [`labB2_double_pendulum.py`](../../m1-inverted-pendulum/sim/mechanics-labs/labB2_double_pendulum.py) | [b2-double-pendulum.md](b2-double-pendulum.md) | 雙擺模態與混沌 | 7 |
| [`labC1_pendulum_pid.py`](../../m1-inverted-pendulum/sim/mechanics-labs/labC1_pendulum_pid.py) | [c1-pendulum-pid.md](c1-pendulum-pid.md) | PID、回授線性化、飽和 | 7 |
| [`labC2_cartpole_lqr.py`](../../m1-inverted-pendulum/sim/mechanics-labs/labC2_cartpole_lqr.py) | [c2-cartpole-lqr.md](c2-cartpole-lqr.md) | LQR、吸引域 | 5 |
| [`labC3_swingup.py`](../../m1-inverted-pendulum/sim/mechanics-labs/labC3_swingup.py) | [c3-swingup.md](c3-swingup.md) | 能量式甩起 + LQR | 6 |
| [`labC4_digital_control.py`](../../m1-inverted-pendulum/sim/mechanics-labs/labC4_digital_control.py) | [c4-digital-control.md](c4-digital-control.md) | 取樣、量化、延遲、雜訊 | 7 |
| [`run_all.py`](../../m1-inverted-pendulum/sim/mechanics-labs/run_all.py) | — | 一鍵執行全部並彙整 | — |

---

## 1. 章節對照總表

| 原書章節 (Malthe-Sørenssen 2015) | 本教材 | Taylor《Classical Mechanics》 | Tedrake《Underactuated Robotics》 | 原書沒有、本教材補充的重點 |
|---|---|---|---|---|
| Ch2 Getting Started with Programming | [Lab 02](a02-python-basics.md) | — | — | 向量化、步長的 U 形誤差曲線、可重現亂數 |
| Ch3 Units and Measurement | [Lab 03](a03-units-floats.md) | — | — | 浮點比較、捨入累積、落地事件內插 |
| Ch4 Motion in One Dimension | [Lab 04](a04-motion-1d.md) | Ch1 | — | 數值微分放大雜訊 → 改用模型擬合 |
| Ch5 Forces in One Dimension | [Lab 05](a05-forces-1d.md) | Ch1–2 | — | `solve_ivp` 與解析解對照 |
| Ch6–7 Motion / Forces in 2D & 3D | [Lab 06-07](a06-07-motion-forces-2d.md) | Ch2、Ch8 | — | 事件偵測、有阻力最佳仰角、Kepler 守恆量 |
| Ch8–9 Constrained Motion / Friction | [Lab 08-09](a08-09-constrained-friction.md) | Ch4–5 | Ch2（單擺） | 靜/動摩擦切換、大角度單擺週期（橢圓積分） |
| Ch10–11 Work / Energy | [Lab 10-11](a10-11-work-energy.md) | Ch4 | — | **symplectic 積分器**、能量圖穩定性 |
| Ch12–13 Momentum / Multiparticle | [Lab 12-13](a12-13-momentum-systems.md) | Ch3 | — | 接觸力模型碰撞、Tsiolkovsky 驗證 |
| Ch14–16 Rotation / Rigid Bodies | [Lab 14-16](a14-16-rigid-body.md) | Ch10 | Ch3 | Monte-Carlo 轉動慣量、倒立點特徵值 |
| （無） | [**Lab B1**](b1-lagrangian-cartpole.md) cart-pole Lagrangian | **Ch7、Ch13** | Ch3 | sympy 推導、Noether、線性化、可控性 |
| （無） | [**Lab B2**](b2-double-pendulum.md) 雙擺 | **Ch11、Ch12** | — | 正則模態、混沌、Lyapunov 指數 |
| （無） | [**Lab C1**](c1-pendulum-pid.md) PID / 回授線性化 | — | **Ch2** | 力矩飽和 → 需要 swing-up |
| （無） | [**Lab C2**](c2-cartpole-lqr.md) LQR | — | **Ch3、Ch8** | Riccati、吸引域 |
| （無） | [**Lab C3**](c3-swingup.md) 能量式甩起 | Ch4（能量） | **Ch3** | PFL、混合控制切換 |
| （無） | [**Lab C4**](c4-digital-control.md) 數位實作 | — | Ch15、Ch19（延伸） | 取樣、量化、延遲、雜訊 |

> Taylor 章號依出版社目錄核對過。Tedrake 章號依 2026-10 的線上 HTML 版目錄核對；作者會持續更新 HTML 版，日後章號可能變動，請以章名為準。
> 書單中的 Christensen & Tjossem《Python for Classical Mechanics》(2024) 是**配合 Taylor 各章**的 Python 習作。上表的 Taylor 欄可以當成它的對照欄，但我沒有逐章核對它的實際章名。Pagonis《Classical Mechanics: A Computational Approach》2nd ed.（CRC 2025）也只能按主題對應，同樣沒有逐章核對。

### 建議學習路徑

```
Lab 02–05（工具 + 一維）──► Lab 06–09（向量、約束、單擺）──► Lab 10–11（能量 + 積分器）★
        │                                                              │
        └──── Lab 12–16（動量、剛體、物理擺）──────────────────────────┤
                                                                       ▼
                     Lab B1（Lagrangian cart-pole）★ ──► Lab B2（雙擺，選修）
                                                                       ▼
                     Lab C1（PID）──► Lab C2（LQR）★ ──► Lab C3（甩起）★ ──► Lab C4（數位實作）──► 實體倒立擺
```

標 ★ 的四課是通往倒立擺的最短路徑。時間不夠時，可以按 Lab 10-11 → B1 → C2 → C3 的順序先做。


---

## 2. 分章目錄


**Part A — 對應原書的現代化實驗**

- [Lab 02 — 現代 Python 科學計算起手式（原書 Ch2）](a02-python-basics.md)
- [Lab 03 — 單位、浮點數與數值表示（原書 Ch3）](a03-units-floats.md)
- [Lab 04 — 一維運動：從資料到模型（原書 Ch4）](a04-motion-1d.md)
- [Lab 05 — 一維力模型（原書 Ch5）](a05-forces-1d.md)
- [Lab 06-07 — 二維/三維運動與受力（原書 Ch6、Ch7）](a06-07-motion-forces-2d.md)
- [Lab 08-09 — 受約束運動、摩擦與單擺（原書 Ch8、Ch9）](a08-09-constrained-friction.md)
- [Lab 10-11 — 功、能量，以及積分器的選擇（原書 Ch10、Ch11）★](a10-11-work-energy.md)
- [Lab 12-13 — 動量、碰撞與多質點系統（原書 Ch12、Ch13）](a12-13-momentum-systems.md)
- [Lab 14-16 — 轉動與剛體（原書 Ch14、Ch15、Ch16）](a14-16-rigid-body.md)

**Part B — Lagrangian 力學（補充）**

- [Part B — Lagrangian 力學（補充）](b0-lagrangian-intro.md)
- [Lab B1 — 用 sympy 從 $L=T-V$ 推導 cart-pole（Taylor Ch7、Ch13）★](b1-lagrangian-cartpole.md)
- [Lab B2 — 雙擺：正則模態與混沌（Taylor Ch11、Ch12）](b2-double-pendulum.md)

**Part C — 控制（補充）**

- [Part C — 控制（補充）](c0-control-intro.md)
- [Lab C1 — 力矩驅動單擺：PID 與回授線性化（Tedrake Ch2）](c1-pendulum-pid.md)
- [Lab C2 — cart-pole LQR 平衡（Tedrake Ch3、Ch8）★](c2-cartpole-lqr.md)
- [Lab C3 — 能量式甩起 + LQR 接手（Tedrake Ch3）★](c3-swingup.md)
- [Lab C4 — 數位實作：取樣、量化、延遲、雜訊（銜接實體倒立擺）](c4-digital-control.md)

---

## 3. 附錄

### A. 書單與本教材的分工

| 書／資源 | 在這條主線中的角色 | 搭配哪些 Lab |
|---|---|---|
| Malthe-Sørenssen《Elementary Mechanics Using Python》(2015) | 牛頓力學與數值方法入門。物理內容不會過時，程式碼需要現代化（即 Part A） | Lab 02–16 |
| Taylor《Classical Mechanics》(2005) | Lagrangian、Hamiltonian、耦合振盪、混沌的理論主教材 | B1、B2；Lab 10-11（Ch4） |
| Christensen & Tjossem《Python for Classical Mechanics》(2024) | 配合 Taylor 各章的 Python 習作，可以補足 Taylor 本身沒有程式的缺口 | 與 Taylor 章節並行 |
| Pagonis《Classical Mechanics: A Computational Approach》2nd ed. (CRC 2025) | 想用一本書兼顧理論與 Python 時的替代選擇，範例程式在 GitHub | 可以取代 Taylor + Christensen |
| Tedrake《Underactuated Robotics》(MIT 6.832，線上免費、持續更新) | 從單擺、cart-pole 到 LQR、Lyapunov、軌跡最佳化、強化學習的控制主線 | C1–C4，以及之後的進階 |

### B. 從本教材到實體倒立擺的下一步

1. **系統辨識**（Tedrake Ch18）：量測擺桿的自由擺動週期和衰減，反推 $l_c$、$J$、$b_\theta$；用台車的階躍響應估計馬達常數和摩擦。辨識結果填入 `cartpole.PARAMS`，再把 Lab C2–C4 全部重跑一次。
2. **Sim-to-real 檢查清單**：取樣率、延遲、編碼器解析度、馬達飽和、軌道長度，對應 Lab C4 的各項掃描。
3. **進階路線**：Lyapunov 分析與吸引域估計（Ch9）→ 軌跡最佳化甩起（Ch10）→ 強化學習（Ch20）。用 RL 學出的甩起策略可以和 Lab C3 的能量法做 benchmark。

### C. 已知限制與待你驗證的地方

- **原書對應**：章節和範例名稱依 Springer 版目錄對照。程式全部是重新撰寫的，沒有和原書的範例程式碼或習題解答逐一比對數值。
- **參數都是示意值**：雨滴的 $C_d$、cart-pole 的質量與長度、控制增益等，都是為了讓物理現象清楚而選的，不是任何特定硬體的實測值。
- **臨界值依賴模型**：Lab C2 的吸引域角度、C3 的增益，以及 C4 的 45 Hz 與 35 ms，只要模型參數改變就會跟著變。
- **Christensen & Tjossem 與 Pagonis 的逐章內容**：我只依主題對應，沒有核對實際章名。
- **Tedrake 章號**：依 2026-10 的 HTML 版目錄。講義會持續更新，章號可能改變。

### 參考來源

- Malthe-Sørenssen, *Elementary Mechanics Using Python*, Springer 2015 — [Springer 書目頁](https://link.springer.com/978-3-319-38684-3)
- Taylor, *Classical Mechanics*, University Science Books — [出版社頁面（含目錄）](https://uscibooks.aip.org/?p=2549)
- Christensen & Tjossem, *Python for Classical Mechanics*, University Science Books 2024 — [NSF PAR 公開版本](https://par.nsf.gov//servlets/purl/10590262)
- Pagonis, *Classical Mechanics: A Computational Approach with Examples Using Mathematica and Python*, 2nd ed., CRC 2025 — [範例程式 GitHub](https://github.com/vpagonis/Classical_Mechanics_2nd_Edition)
- Tedrake, *Underactuated Robotics* (MIT 6.832) — [線上講義](https://underactuated.mit.edu/)、[配套程式](https://github.com/RussTedrake/underactuated)
