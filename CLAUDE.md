# CLAUDE.md

這個 repo 是程式競賽練習紀錄，收錄卡關題目、解答與學習講義。公開於 https://github.com/mira0907/coding-mentor。

## 溝通

- 一律用繁體中文回覆。程式碼、指令、識別字維持原樣。
- 使用者是 Git 與 GitHub 新手。解釋 Git 操作時要說明每一步在做什麼，並提供 VS Code 按鈕的替代做法。

## 專案結構

- `problems/<題目名稱>/`：每題一個資料夾，含 `sol.cpp`、`tests/`（`1.in`／`1.out` 成對）與 `README.md`。
- `template/template.cpp`：新題目的模板，`LOCAL` 巨集下有 `dbg(x)`，輸出到 stderr。
- `include/bits/stdc++.h`：macOS 沒有這個標頭檔，編譯時必須加 `-I include`。
- `notes/`：學習講義。`docs/`：使用說明。
- 新增題目後，要更新根目錄 `README.md` 的「題目清單」表格。新增講義或文件後，要更新「講義與文件」一節的連結。

## 建立與測試題目

```bash
./scripts/new.sh cf-1900A            # 建立新題目，不要手動建資料夾
./scripts/run.sh problems/cf-1900A   # 編譯並比對 tests/ 內所有測資
```

- 語言是 C++17。編譯參數以 `scripts/run.sh` 為準：`-std=c++17 -O2 -Wall -Wextra -Wshadow -DLOCAL -fsanitize=address,undefined`，編譯器是 clang++。
- 自己單獨編譯時記得加 `-I/Users/zhuangminruo/cp-practice/include`。
- 題目 `README.md` 依模板填寫：來源、標籤、日期、狀態、題目摘要、卡住的地方、正解思路、複雜度。重點是「卡住的地方」，要具體寫出錯在哪裡。

## 解答與講義的正確性

- 寫出的解答必須實際編譯並跑測資，不能只憑推理就宣稱正確。
- 講義或範例題的解答要用暴力解對拍：用 Python 寫暴力解與隨機測資產生器，至少比對數百組小測資。
- 要測最大規模的輸入，確認時間在限制內，並檢查是否需要 `long long`。
- 深度可能達 10⁵ 的 DFS 要改用顯式堆疊，避免遞迴爆堆疊。
- 執行 Python 腳本時用 `python3 -I`。對拍用的暫存檔放在 scratchpad，不要放進 repo。

## Git 規則

- 只有使用者要求時才 commit 或 push。
- 每次修改完 repo 裡的檔案，都要在回覆結尾主動詢問使用者要不要 commit 並 push，不要等使用者自己提起。
- commit 訊息用繁體中文，一個 commit 只做一件事，寫清楚做了什麼，例如「新增 cf-1900A 解答與卡關紀錄」。
- commit 前先看 `git status` 與 `git diff`，確認沒有夾帶不相關的檔案。
- 不要 commit 編譯產物（`sol` 執行檔、`.dSYM`、`*.o`、`a.out`），這些已列在 `.gitignore`。
- 不要使用 `git push --force`，不要改寫已經 push 的歷史。
- 本機沒有安裝 `gh` 與 `brew`。推送靠 macOS 鑰匙圈裡的憑證，終端機無法互動輸入帳密，推送失敗時請使用者改用 VS Code 的「同步變更」。

## 公開 repo 的隱私

- repo 是公開的。不要放入真實姓名、密碼、權杖、金鑰或個人 email。
- 從 Claude Docs 匯出的講義，作者欄會帶出真實姓名，放進 repo 前要拿掉，只保留日期。
- `notes/graph-theory.md` 是從 Claude Docs 匯出的版本。講義在 Claude Docs 上修改後，要重新匯出並再次移除姓名，GitHub 上的版本才會更新。
