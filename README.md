# 程式競賽練習：卡關題目紀錄

收錄練習時不會的題目，記錄卡住的地方與正解思路。

## 目錄結構

```
problems/<題目名稱>/
  README.md     題目連結、卡住的點、正解思路
  sol.cpp       解答
  tests/        測資：1.in / 1.out、2.in / 2.out ...
template/       新題目使用的 C++ 模板
include/bits/   macOS 用的 <bits/stdc++.h> 替代
scripts/        new.sh（建立新題）、run.sh（編譯並跑測資）
notes/          學習講義
docs/           使用說明
```

## 講義與文件

- [競賽圖論講義](notes/graph-theory.md)：八章觀念、十六題範例程式題、章末觀念檢測，以及每章簡單、中等、困難各一題的實作題與詳解
- [GitHub 使用指南](docs/github-guide.md)：commit、push、pull 與常見狀況

## 使用方式

```bash
./scripts/new.sh cf-1900A           # 建立新題目
./scripts/run.sh problems/cf-1900A  # 編譯並比對 tests/ 內所有測資
```

VS Code：開啟 `sol.cpp` 後按 `Cmd+Shift+B` 即可編譯並跑測資；
「New problem」任務可從 `Cmd+Shift+P → Tasks: Run Task` 執行。

編譯參數：`-std=c++17 -O2 -Wall -Wextra -Wshadow -DLOCAL -fsanitize=address,undefined`
（`LOCAL` 巨集下 `dbg(x)` 會輸出到 stderr，送出時不受影響。）

## 題目清單

| 題目 | 來源 | 標籤 | 狀態 |
|------|------|------|------|
