# C++ 開發環境

這台 Mac 已經可以編譯、測試、評測和逐行除錯 C++。這份文件說明裝了什麼、還需要你做的一次性設定，以及日常怎麼用。

## 已經裝好的工具

| 工具 | 版本 | 用途 |
| --- | --- | --- |
| clang++（Apple） | 21.0 | 編譯器，支援 C++17 |
| lldb | 系統內建 | 除錯器 |
| Python 3 | 系統內建 | judge 與測資產生器 |
| VS Code | 1.144 | 編輯器 |
| C/C++ 擴充套件 | 1.34 | 自動完成、跳到定義、即時標出錯誤 |
| CodeLLDB 擴充套件 | 1.12 | 在 VS Code 裡設中斷點、逐行執行 |

macOS 的編譯器沒有 `bits/stdc++.h`，專案裡的 `include/bits/stdc++.h` 補上了它。所有腳本與 VS Code 設定都已經指向那裡。

## 一次性設定（請做一次）

原本的 VS Code 是直接從下載的安裝映像檔（桌面上的「VS Code」磁碟）打開的。這樣不能自動更新，退出那個磁碟或重開機後就會不見。已經幫你複製一份到「應用程式」資料夾，接下來請：

1. 完全結束 VS Code（`Cmd+Q`）。
2. 從「應用程式」資料夾或 Launchpad 打開 Visual Studio Code。
3. 在 Finder 左側找到「VS Code」磁碟，按旁邊的退出鍵。
4. 選用：在 VS Code 按 `Cmd+Shift+P`，執行 `Shell Command: Install 'code' command in PATH`。之後在終端機打 `code .` 就能用 VS Code 打開資料夾。

第一次打開 C++ 檔案時，C/C++ 和 CodeLLDB 套件會各自下載一些元件，需要網路，等右下角的進度跑完即可。

## 日常使用

**寫講義的題目**：

```bash
./scripts/judge.sh new 3-1              # 建立 solutions/3-1.cpp 並顯示題目
./scripts/judge.sh solutions/3-1.cpp    # 寫完後評測
```

詳細說明見 [judge/README.md](../judge/README.md)。

**寫其他平台的題目**（例如 Codeforces）：

```bash
./scripts/new.sh cf-1900A               # 建立 problems/cf-1900A/
./scripts/run.sh problems/cf-1900A      # 編譯並比對 tests/ 裡的測資
```

在 VS Code 裡，開著 `sol.cpp` 按 `Cmd+Shift+B` 等於執行 run.sh。

## 逐行除錯

1. 在程式碼行號左邊點一下，出現紅點就是中斷點。
2. 按 `F5`，選一個除錯設定：
   - **除錯：講義題目**：輸入用 judge 的範例，檔名要是題號，例如 `solutions/3-1.cpp`。
   - **除錯：自己的題目**：輸入用同資料夾的 `tests/1.in`。
   - **除錯：在終端機自己輸入**：程式停在讀入時，到下方終端機打字輸入。
3. 程式會停在中斷點。左側可以看每個變數的值，滑鼠移到變數上也會顯示。
4. 常用按鍵：`F10` 執行下一行、`F11` 進入函式、`Shift+F11` 跳出函式、`F5` 繼續到下一個中斷點。

除錯版會以 `-O0 -g` 編譯成 `檔名_debug`，這個檔案已經設定成不會被 git 追蹤。

## 常見問題

- **編輯器說找不到 `bits/stdc++.h`**：按 `Cmd+Shift+P` 執行 `Developer: Reload Window`。C/C++ 套件讀到專案的設定後，紅線就會消失。
- **評測時出現 RE，但看不出哪裡錯**：加 `--debug` 重跑，sanitizer 會印出越界的那一行。
- **讀大量資料很慢**：main 開頭加 `ios::sync_with_stdio(false); cin.tie(nullptr);`，輸出用 `'\n'` 而不是 `endl`。
