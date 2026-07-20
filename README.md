# 中區每週營運報告

依 **FY → 季 → 週** 分類的每週營運報告（HTML）。

## 目錄結構

```
FY26/
  Q4/
    FY26Q4W1_中區營運報告.html
    FY26Q4W2_中區營運報告.html
    FY26Q4W3_中區營運報告.html
```

## 線上瀏覽（GitHub Pages）

首頁：<https://moriochang.github.io/report/>

（需先於 GitHub 倉庫 **Settings → Pages** 將來源設定為 `main` 分支 `/ (root)`。）

## 每週新增報告 SOP

1. 把新的 HTML 放到對應的 `FY??/Q?/` 資料夾（檔名維持 `FY??Q?W?_中區營運報告.html`）
2. 重新產生首頁索引：
   ```bash
   python3 build_index.py
   ```
3. 提交並推送：
   ```bash
   git add -A && git commit -m "add FY26Q4W4" && git push
   ```
