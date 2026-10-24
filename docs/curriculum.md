# 核心模組與推薦書籍

> [!TIP]
> 《Modern Robotics》、《Feedback Systems》(Åström & Murray)、《Reinforcement Learning: An Introduction》三本書作者網站均提供免費 PDF，可先讀電子版再決定是否購買實體書。

### 1. 系統全貌：機電整合導論 (Mechatronics)
* **書名**：《Introduction to Mechatronics and Measurement Systems》— David G. Alciatore
* **技術定位**：初學者的系統全域地圖，對應 §一 架構圖中的每一個方塊。
* **核心技術內容**：感測器原理與 ADC/DAC；運算放大器於感測介面；MCU 周邊通訊協定（PWM, I2C, SPI, UART）；驅動執行器與雜訊抑制。
* **連結**：[Amazon 檢索](https://www.amazon.com/s?k=Introduction+to+Mechatronics+and+Measurement+Systems+Alciatore)

### 2. 演算法語言：現代線性代數 (Linear Algebra) — 數理主教材
* **書名**：《Introduction to Linear Algebra》/《Linear Algebra and Learning from Data》— Gilbert Strang
* **技術定位**：數理層主線。LQR 的 Riccati 方程、Kalman filter 的協方差更新、SO(3) 的旋轉矩陣全部建立在此。
* **核心技術內容**：四大基本子空間；正交投影、特徵值與譜定理；SVD 與 PCA；深度神經網路的矩陣推導。
* **連結**：[Amazon 檢索](https://www.amazon.com/s?k=Gilbert+Strang+Linear+Algebra) / MIT OCW 18.06

### 3. 數理補充：數學物理方法與機率統計 — 指定章節
* **書名 A**：《Mathematical Methods for Physics and Engineering》(3rd Ed.) — Riley, Hobson, Bence (RHB)
* **技術定位**：僅讀指定章節（章節編號依第三版目錄，取得書後請核對）：向量微積分、常微分方程（倒立擺的運動方程）、變分法（拉格朗日力學前置）、數值方法。
* **連結**：[Amazon (ISBN 978-0521679718)](https://www.amazon.com/dp/0521679710)
* **書名 B**：任一本工程機率統計教材
* **技術定位**：條件機率與貝氏定理、多變量高斯、期望值與變異數、馬可夫鏈。Kalman filter（§6）與 RL（§12）的前置。

### 4. 共同語言：現代機器人運動學與動力學 (Modern Robotics)
* **書名**：《Modern Robotics: Mechanics, Planning, and Control》— Kevin M. Lynch, Frank C. Park
* **技術定位**：SO(3)/SE(3)、FK/IK 是控制、感測融合、模擬器共用的語言，在動手前建立。倒立擺的拉格朗日推導是此書動力學章節的最小練習題。
* **核心技術內容**：李群與李代數；旋量理論取代 DH 參數；Newton-Euler 與拉格朗日動力學；軌跡規劃。
* **連結**：作者網站免費 PDF 與 Coursera 專項課程 / [Amazon 檢索](https://www.amazon.com/s?k=Modern+Robotics+Kevin+M+Lynch)

### 5. 小腦反射：回授控制 (Feedback Control)
* **書名 A（正式教材）**：《Feedback Systems: An Introduction for Scientists and Engineers》— Karl J. Åström, Richard M. Murray（作者網站免費 PDF）
* **核心技術內容**：狀態空間與線性化；Lyapunov 穩定性與極點配置；Bode / Nyquist 與相位裕度；PID 設計、anti-windup、致動器飽和；**LQR**。
* **書名 B（軟體人入門）**：《Feedback Control for Computer Systems》— Philipp K. Janert
* **技術定位**：以佇列、快取等軟體案例建立回授直覺，適合先讀；不涵蓋慣性、共振等物理系統特性，不能取代 A。
* **實作對應**：M1。倒立擺用 PID 可以站，但 LQR 才是標準解；驗收訂為「先 PID 站穩，再改 LQR 並比較響應」。

### 6. 感知與狀態估計：機率機器人學 (Probabilistic Robotics)
* **書名**：《Probabilistic Robotics》— Sebastian Thrun, Wolfram Burgard, Dieter Fox
* **核心技術內容**：貝氏濾波框架（Kalman / EKF / 粒子濾波）；動作模型與感測模型；定位與 SLAM；MDP / POMDP 基礎。
* **實作對應**：M1 的 IMU + 編碼器融合（互補濾波 → Kalman）；M2 的 SLAM。
* **連結**：[Amazon 檢索](https://www.amazon.com/s?k=Probabilistic+Robotics+Thrun)

### 7. 神經感知電路：電子元件與訊號處理 (Electronics)
* **書名**：《Electronic Devices》— Thomas L. Floyd
* **核心技術內容**：Op-Amp 訊號放大、主動濾波、比較器；MOSFET / BJT 功率開關偏壓；示波器量測、邏輯分析、EMI 抑制。
* **實作對應**：M1 的編碼器訊號整形、馬達電流量測與雜訊排除。
* **連結**：[Amazon 檢索](https://www.amazon.com/s?k=Electronic+Devices+Thomas+L+Floyd)

### 8. 肌肉致動：電機與驅動系統 (Actuators & Motor Drives)
* **書名**：《Electric Motors and Drives: Fundamentals, Types and Applications》— Austin Hughes, Bill Drury
* **核心技術內容**：DC / 步進 / BLDC 特性；轉矩-轉速曲線與反電動勢；H 橋、PWM 調速、FOC。
* **實作對應**：M1 選用帶編碼器 DC 馬達（簡單）或 BLDC + SimpleFOC（進階）。
* **連結**：[Amazon 檢索](https://www.amazon.com/s?k=Electric+Motors+and+Drives+Hughes)

### 9. 電源與安全 (Power & Safety)
* **技術定位**：實體機器最容易出事的環節，無單一教科書。
* **必備知識點**：LiPo 的 C-rate、截止電壓、平衡充電、儲存電壓、鼓包處置；BMS 與過流 / 過放 / 短路保護；**硬體級 E-Stop**；邏輯電與動力電分軌、共地隔離雜訊；XT60 / XT30 與線徑電流對應。
* **實作對應**：M1 的安全 task 是軟體層防線，硬體 E-Stop 是最後防線，兩者都要有。
* **資源**：驅動器與電池廠商的 Application Notes。

### 10. 實體骨架：CAD、3D 列印與機構 (Body & Mechanisms)
* **CAD 工具**：Fusion 360（個人版免費）或 Onshape。第一個練習件：倒立擺的擺桿與馬達座。
* **書名 A**：《Functional Design for 3D Printing》— Clifford Smyth：FDM 各向異性、熱熔螺母與軸承座公差、支架剛性。
* **書名 B**：《Making Things Move》— Dustyn Roberts：齒輪比與減速扭矩、四連桿與凸輪、摩擦與慣性矩評估。
* **連結**：[Amazon 檢索 A](https://www.amazon.com/s?k=Functional+Design+for+3D+Printing) / [Amazon 檢索 B](https://www.amazon.com/s?k=Making+Things+Move+Dustyn+Roberts)

### 11. 邊緣計算大腦：Jetson、ROS 2 與 micro-ROS (Edge Computing)
* **核心主控**：NVIDIA Jetson Orin Nano 系列（含 Super 開發套件；以採購時官方現行產品為準）
* **推薦資源**：ROS 2 官方 Tutorials（docs.ros.org）；Articulated Robotics（YouTube，從零組 ROS 2 差速車）；micro-ROS 官方文件（micro.ros.org）；NVIDIA DLI Jetson 課程。
* **核心技術內容**：
  * **ROS 2**：Nodes / Topics / Services / Actions、tf2 座標樹、Nav2。
  * **micro-ROS**：讓 FreeRTOS 上的 MCU 成為 ROS 2 節點，透過 Agent（UART / USB / UDP）發布姿態、電流等 topic，接收 setpoint。這是反射層與大腦層之間的標準橋樑。
  * **TensorRT**：邊緣 GPU 即時執行 YOLO、語意分割、姿態估計。
  * **感測融合**：LiDAR / RGB-D / IMU 進行 SLAM（理論見 §6）。
* **連結**：[NVIDIA Jetson 開發者入門](https://developer.nvidia.com/embedded/learn/getting-started-jetson)

### 12. 學習型策略：強化學習與模仿學習 (RL & Imitation Learning)
* **書名**：《Reinforcement Learning: An Introduction》(2nd Ed.) — Sutton, Barto（作者網站免費 PDF）
* **核心技術內容**：MDP、Bellman 方程、價值函數與策略；TD 學習、Q-learning、策略梯度；深度 RL（PPO、SAC）需另讀論文與 Isaac Lab 範例。
* **模仿學習與 VLA**：Hugging Face **LeRobot**（SO-101 手臂、遙操作收集、ACT / Diffusion Policy 訓練部署）為 M3 主軸；論文順序 ACT → Diffusion Policy → RT-2 → OpenVLA → π0。前置需 Transformer 與擴散模型基礎（Goodfellow《Deep Learning》或 fast.ai）。
* **與 M1 的連結**：倒立擺也是 RL 的經典環境（CartPole）。M1 完成 LQR 後，可在 MuJoCo 訓練 PPO 策略並嘗試部署到實體，作為最小的 Sim-to-Real 練習。

### 13. 虛實融合：模擬器與 Sim-to-Real (Simulation)
* **工具**：MuJoCo（輕量、入門）；NVIDIA Isaac Sim + **Isaac Lab**（平行化 RL 訓練，M4 使用）；Genesis 等新興引擎可留意。
* **核心技術內容**：Domain Randomization（質量、摩擦、延遲）；系統辨識校正模擬參數；位置控制 vs. 力矩控制對遷移的影響。
