# Changelog

* **v1 → v2**：新增機率機器人學、電源安全、RL 與模仿學習；《Modern Robotics》提前；控制論主教材改為 Åström & Murray；RHB 縮為指定章節；移除無法查證的書名；新增四階段實作主線。
* **v2 → v3**：M1 定為倒立擺；新增雙層架構（MCU 反射 / Jetson 大腦）論述與架構圖；新增 FreeRTOS 與 ROS 2 分工比較；新增 FreeRTOS task 設計、控制迴路圖、硬體清單；新增 micro-ROS 過渡與 CartPole Sim-to-Real 延伸；驗收改為 PID → LQR。
* **v3 → v4**：新增 M1 前置教材 `docs/mechanics/`：對應《Elementary Mechanics Using Python》2–16 章的現代化實驗，補充 Lagrangian 力學（Taylor）與控制（Tedrake：PID、LQR、能量式甩起、數位實作）；可執行程式放在 `m1-inverted-pendulum/sim/mechanics-labs/`，`run_all.py` 共 92 項自動檢核。
