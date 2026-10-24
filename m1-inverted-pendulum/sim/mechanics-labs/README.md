# Mechanics Labs（M1 前置：力學 → 模擬 → 控制）

本目錄是 [docs/mechanics/](../../../docs/mechanics/README.md) 教材的可執行程式。每支程式都會用 `check()` 和解析解、守恆律或理論預測比對，印出 PASS/FAIL。

```bash
uv sync                      # 或 pip install -r requirements.txt
uv run python run_all.py     # 平行跑全部 Lab；-j 1 依序、--only labC 只跑 Part C、--save-output DIR 存 stdout
uv run python check_docs.py  # 文件「預期輸出」與實際輸出逐行比對；--update 回寫文件
uv run pytest -q             # pytest 介面（test_labs.py）
```

- `lab02`–`lab14_16`：對應 Malthe-Sørenssen《Elementary Mechanics Using Python》第 2–16 章
- `labB*`：Lagrangian 力學（Taylor《Classical Mechanics》Ch7、11、12、13）
- `labC*`：控制（Tedrake《Underactuated Robotics》）；`cartpole.py` 為共用模型，換成實體硬體時改 `PARAMS`
- `labutils.py`：共用 `check()`；有圖的 Lab（02、C2）加 `--plot` 會把圖存到 `out/`
- 相依版本鎖在 `uv.lock`，`requirements.txt` 由 `uv export` 產生；CI 見 `.github/workflows/mechanics-labs.yml`

最近一次驗證（2026-10-24）：96 項檢核全部 PASS（Python 3.13.15 / numpy 2.5.3 與 Python 3.12.14 / numpy 2.5.4；scipy 1.18.1、sympy 1.14.0、matplotlib 3.11.2）。圖檔輸出到 `out/`，已列入 `.gitignore`。
