# M1 倒立擺

## 驗收 checklist

- [ ] 手動擾動後一秒內回到平衡且不振盪
- [ ] PID 雙迴路站穩，能說明 Kp / Ki / Kd 影響
- [ ] 由拉格朗日方程推導狀態方程並實作 LQR
- [ ] 比較 PID 與 LQR 的超調、恢復時間、控制量峰值
- [ ] micro-ROS topic 可在 PC 端 rqt_plot 即時繪圖
- [ ] 安全 task 能在傾倒或通訊逾時斷電
- [ ] MuJoCo 建模並訓練 PPO，嘗試部署（延伸）

## 建議目錄

```
firmware/  — FreeRTOS 專案
microros/  — micro-ROS Agent 設定與 msg 定義
cad/       — 擺桿、馬達座 STEP / STL
sim/       — MuJoCo 模型與 PPO 訓練腳本
  mechanics-labs/ — 力學、Lagrangian、PID/LQR/甩起的 Python 實驗（教材見 docs/mechanics/）
```
