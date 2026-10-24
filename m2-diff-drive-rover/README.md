# M2 無人車

## 驗收 checklist

- [ ] 未知室內環境完成建圖
- [ ] 自主導航到指定點
- [ ] 能讀懂 tf2 座標樹與 Nav2 costmap
- [ ] MCU 端輪速控制沿用 M1 的雙層架構

## 建議目錄

```
firmware/ — 輪速控制 FreeRTOS 專案
ros2_ws/  — ROS 2 workspace（SLAM、Nav2 設定）
cad/
```
