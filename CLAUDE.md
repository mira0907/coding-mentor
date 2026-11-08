# CLAUDE.md

這個 repo 是程式競賽練習紀錄，收錄卡關題目、解答與學習講義。公開於 https://github.com/mira0907/coding-mentor。

## 溝通

- 一律用繁體中文回覆。程式碼、指令、識別字維持原樣。
- 使用者是 Git 與 GitHub 新手。解釋 Git 操作時要說明每一步在做什麼，並提供 VS Code 按鈕的替代做法。

## 專案結構

- `problems/<題目名稱>/`：每題一個資料夾，含 `sol.cpp`、`tests/`（`1.in`／`1.out` 成對）與 `README.md`。
- `template/template.cpp`：新題目的模板，`LOCAL` 巨集下有 `dbg(x)`，輸出到 stderr。
- `include/bits/stdc++.h`：macOS 沒有這個標頭檔，編譯時必須加 `-I include`。
- `notes/`：學習講義。`docs/`：使用說明，C++ 環境見 `docs/cpp-environment.md`。
- `judge/`：本機評測系統，`judge/problems/<題號>/` 每題一個資料夾，格式見 `judge/README.md`。
- `solutions/`：使用者寫的講義題目解答，檔名用題號，例如 `solutions/3-1.cpp`。
- 新增題目後，要更新根目錄 `README.md` 的「題目清單」表格。新增講義或文件後，要更新「講義與文件」一節的連結。
- 寫給使用者學習的程式碼，註解要寫出每個變數的用途；一行宣告多個變數時，在上方每個變數各寫一行註解。

## 建立與測試題目

```bash
./scripts/new.sh cf-1900A            # 建立新題目，不要手動建資料夾
./scripts/run.sh problems/cf-1900A   # 編譯並比對 tests/ 內所有測資
```

- 語言是 C++17。編譯參數以 `scripts/run.sh` 為準：`-std=c++17 -O2 -Wall -Wextra -Wshadow -DLOCAL -fsanitize=address,undefined`，編譯器是 clang++。
- 自己單獨編譯時記得加 `-I include`（在 repo 根目錄執行；在別的資料夾就改成 include 的完整路徑）。
- 題目 `README.md` 依模板填寫：來源、標籤、日期、狀態、題目摘要、卡住的地方、正解思路、複雜度。重點是「卡住的地方」，要具體寫出錯在哪裡。

## 解答與講義的正確性

- 寫出的解答必須實際編譯並跑測資，不能只憑推理就宣稱正確。
- 講義或範例題的解答要用暴力解對拍：用 Python 寫暴力解與隨機測資產生器，至少比對數百組小測資。
- 要測最大規模的輸入，確認時間在限制內，並檢查是否需要 `long long`。
- 深度可能達 10⁵ 的 DFS 要改用顯式堆疊，避免遞迴爆堆疊。
- 執行 Python 腳本時用 `python3 -I`。對拍用的暫存檔放在 scratchpad，不要放進 repo。

## Judge 系統

- 評測：`./scripts/judge.sh <題號> <程式檔>`，或 `python3 judge/judge.py <題號> <程式檔>`。題號：講義範例 `1A`～`8B`、章末實作題 `1-1`～`8-3`。
- 自我檢查：`python3 judge/judge.py test all`，所有題目的參考解都必須 AC。改過 judge 或任何題目後都要跑。
- 測資由 `gen.py` 產生在 `judge/.cache/`，不進 git。`judge/.results.json` 是使用者的成績，不要刪除或 commit。
- 講義題目的參考解必須和講義的解答程式逐字相同，用 `python3 -I judge/tools/import_from_notes.py <題號>` 匯入，不要手改 `ref.cpp`、`statement.md` 與範例。講義的題目或解答改了，就重新匯入並重跑 `test`。

## 使用者丟新題目時：自動建立 judge 題目

使用者貼上題目（或說「幫這題做 judge」）時，照下面的步驟做完再回報，不需要另外詢問：

1. 題號：講義以外的題目用 `x-` 開頭加簡短英數名稱，例如 `x-cf1900A`、`x-apcs-202310-4`。建立 `judge/problems/<題號>/`。
2. `statement.md`：整理成繁體中文的題目敘述，保留所有限制與輸入輸出格式；`samples/1.in`、`samples/1.out` 放題目給的範例，有多組就編 2、3……。
3. `problem.json`：`id`、`title`、`level`（簡單／中等／困難）、`source`（出處或網址）、`time_limit`、`memory_mb`、`checker`（答案唯一時是 null）。
4. `ref.cpp`：自己寫參考解，註解寫出每個變數的用途。
5. `brute.py`：獨立、明顯正確的暴力解（可以指數時間），只跑小測資。
6. `gen.py`：介面 `python3 -I gen.py SEED SIZE`，SIZE 是 small／mid／max。small 要小到暴力解跑得動，並涵蓋邊界情況；max 用題目上限，依 seed 換鏈狀、星狀、全部相同、最大權重等刁鑽形狀；所有測資都要符合題目限制。
7. 答案不唯一（「輸出任一組」）時寫 `checker.py`：`python3 -I checker.py 輸入 參考答案 使用者輸出`，自己驗證使用者的答案是否合法，正確回傳 0。
8. 執行 `python3 judge/judge.py test <題號>`，必須 AC；再寫一份常見的錯誤解法（例如 int 溢位、少判邊界、複雜度太高）確認 judge 判得出錯，測完刪掉 `judge/.results.json` 裡這題的紀錄。
9. 使用者是來練習的：除非使用者要求，不要在對話中貼出參考解或講解解法，只回報題號、測資筆數與怎麼評測。

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
