# 講義題目 Judge

在自己電腦上評測講義的 40 題：16 題範例（題號 `1A` 到 `8B`）與 24 題章末實作題（題號 `1-1` 到 `8-3`）。交出程式後，judge 會用隱藏測資執行，並告訴你每一筆是否通過。

## 快速開始

```bash
./scripts/judge.sh list                 # 列出所有題目與你的最佳結果
./scripts/judge.sh new 3-1              # 建立 solutions/3-1.cpp（複製模板）並顯示題目
./scripts/judge.sh solutions/3-1.cpp    # 評測；檔名就是題號時不用另外寫題號
./scripts/judge.sh 3-1 my.cpp           # 檔名不是題號時，先寫題號
./scripts/judge.sh solutions/3-1.cpp --debug   # 用 sanitizer 編譯，抓越界與未定義行為
```

在 VS Code 裡：開著解答檔，按 `Cmd+Shift+P` → `Tasks: Run Task` → `Judge current file`。檔名就是題號時，跳出的題號欄直接按 Enter。

第一次評測某一題時，judge 會先產生測資，大約需要幾秒。之後就直接評測。

## 看懂結果

| 結果 | 意思 | 常見原因 |
| --- | --- | --- |
| AC | 通過 | |
| WA | 答案錯誤 | 溢位（該用 long long）、漏了邊界情況、輸出格式不對 |
| TLE | 超過時限 | 複雜度太高、無窮迴圈、忘了 `ios::sync_with_stdio(false)` |
| RE | 執行錯誤 | 陣列越界、遞迴太深、除以 0。加 `--debug` 重跑可以看到出錯的那一行 |
| MLE | 超過記憶體 | 開了太大的陣列 |
| CE | 編譯錯誤 | 語法錯誤，judge 會印出編譯器訊息 |

每題的測資依序是：題目範例、小測資（約 15 筆）、中測資、最大規模測資。小測資的答案都用暴力解驗證過。沒通過時，judge 會印出第一筆失敗的測資：小測資會直接顯示輸入、期望輸出和你的輸出，大測資則給出檔案位置。

**關於時限**：講義寫的是 1 秒，但這台 Mac 的 `cin` 比一般評測系統的 GCC 慢很多，讀 10⁶ 個整數就要約 0.5 秒。所以 judge 把時限放寬為「題目時限」與「參考解最慢時間的兩倍加 0.1 秒」兩者中較大的那個，畫面上會同時顯示兩個數字。

你的最佳結果存在 `judge/.results.json`，只在這台電腦上，不會上傳到 GitHub。

## 題目資料夾的格式

```
judge/problems/<題號>/
  problem.json   題名、難度、出處、時限（秒）、記憶體（MB）、checker、各規模測資筆數
  statement.md   題目敘述
  samples/       範例：1.in、1.out
  ref.cpp        參考解（講義題目就是講義裡的解答程式）
  gen.py         測資產生器：python3 -I gen.py SEED SIZE，SIZE 是 small、mid 或 max
  brute.py       暴力解，只在小測資上用來驗證參考解
  checker.py     （答案不唯一時才有）python3 -I checker.py 輸入 參考答案 你的輸出，正確時回傳 0
  subtasks.py    （有子題時才有）讀入一筆測資，印出它符合哪些子題的限制，例如「2 3 4」
```

有子題配分的題目，`problem.json` 加上 `"subtasks": [{"score": 13, "desc": "N ≤ 1000、K = 1"}, ...]`。評測時，符合某個子題限制的測資全部 AC，才拿到那個子題的分數，最後會印出總分。

產生的測資放在 `judge/.cache/`，不進 git，需要時會自動重新產生。

維護用的指令：

```bash
python3 judge/judge.py test all          # 用參考解自我檢查所有題目，應該全部 AC
python3 judge/judge.py build 3-1         # 強制重新產生某題的測資
python3 -I judge/tools/import_from_notes.py 3-1   # 講義改了之後，重新匯入題目敘述與參考解
```

## 加入新題目

把題目丟給 Claude，說「幫這題做 judge」。Claude 會照專案的 CLAUDE.md 建立題目資料夾，寫好參考解、暴力解和測資產生器，並驗證到全部通過。講義以外的題目，題號會用 `x-` 開頭，例如 `x-cf1900A`。
