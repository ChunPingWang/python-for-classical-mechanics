# Mechanics Labs（M1 前置：力學 → 模擬 → 控制）

本目錄是 [docs/mechanics/](../../../docs/mechanics/README.md) 教材的可執行程式。每支程式都會用 `check()` 和解析解、守恆律或理論預測比對，印出 PASS/FAIL。

```bash
pip install -r requirements.txt
python run_all.py
```

- `lab02`–`lab14_16`：對應 Malthe-Sørenssen《Elementary Mechanics Using Python》第 2–16 章
- `labB*`：Lagrangian 力學（Taylor《Classical Mechanics》Ch7、11、12、13）
- `labC*`：控制（Tedrake《Underactuated Robotics》）；`cartpole.py` 為共用模型，換成實體硬體時改 `PARAMS`

最近一次驗證：92 項檢核全部 PASS（Python 3.13.17、numpy 2.5.3、scipy 1.18.1、sympy 1.14.0、matplotlib 3.11.2）。
