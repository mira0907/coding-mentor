# GitHub 使用指南

給第一次用 Git 與 GitHub 的自己：這份指南只講這個專案每天會用到的操作。

## 1. 四個基本觀念

| 名詞 | 意思 | 在這個專案裡 |
| --- | --- | --- |
| repo（倉庫） | 一個被 Git 追蹤版本的資料夾 | 本機的 `cp-practice`，以及 GitHub 上的 `mira0907/coding-mentor` |
| commit（提交） | 一次「存檔點」，記錄這次改了什麼、為什麼改 | 例如「新增 cf-1900A 解答」 |
| push（推送） | 把本機的 commit 上傳到 GitHub | 上傳後網站上才看得到 |
| pull（拉取） | 把 GitHub 上較新的 commit 下載到本機 | 換電腦或在網站上改過檔案時用 |

重點：**存檔不等於 commit，commit 也不等於上傳**。檔案改完要先 commit，再 push，GitHub 上才會更新。

## 2. 每天的流程：寫一題、存一題

### 用終端機

```bash
./scripts/new.sh cf-1900A            # 1. 建立新題目資料夾
# 2. 寫 problems/cf-1900A/sol.cpp、填 tests/ 測資與 README.md
./scripts/run.sh problems/cf-1900A   # 3. 編譯並跑測資

git status                           # 4. 看哪些檔案有變動
git add problems/cf-1900A            # 5. 把這題加入「準備提交」的清單
git commit -m "新增 cf-1900A：二分搜尋邊界寫錯的紀錄"   # 6. 建立存檔點
git push                             # 7. 上傳到 GitHub
```

### 用 VS Code 的按鈕（不用打指令）

1. 點左側欄的「原始檔控制」圖示（分岔的線），或按 `Ctrl+Shift+G`。
2. 「變更」底下列出改過的檔案。點檔案可以看到改了哪幾行。
3. 滑到檔案上按 `+`，把它加入「暫存的變更」。等於 `git add`。
4. 在上方輸入框寫 commit 訊息，按「提交」。等於 `git commit`。
5. 按「同步變更」。等於 `git pull` 加 `git push`。

兩種方式效果完全一樣，可以混用。

## 3. commit 訊息怎麼寫

一個 commit 只做一件事，訊息寫「做了什麼」，必要時補「為什麼」。

| 好的寫法 | 不好的寫法 |
| --- | --- |
| 新增 cf-1900A 解答與卡關紀錄 | update |
| 修正 run.sh 在沒有測資時當掉 | 改了一些東西 |
| 講義第三章補充 0-1 BFS 範例 | aaa |

半年後回頭看歷史紀錄，你會感謝現在認真寫訊息的自己。

## 4. 在 GitHub 網站上能做什麼

- **瀏覽檔案**：`README.md` 與 `.md` 檔會自動排版成網頁，講義 `notes/graph-theory.md` 可以直接在網站上閱讀，右上角有自動目錄。
- **看歷史**：點檔案列表上方的 commits 數字，可以看到每一次 commit 改了哪些行。
- **線上修改**：點檔案右上角的鉛筆圖示可以直接編輯並 commit。改完之後，本機要先 `git pull` 才會同步。
- **分享**：repo 是公開的，網址 `https://github.com/mira0907/coding-mentor` 給誰都看得到。

## 5. 換一台電腦繼續寫

第一次在新電腦上，把整個 repo 下載下來：

```bash
git clone https://github.com/mira0907/coding-mentor.git
cd coding-mentor
```

之後每次開始寫之前，先拉一次最新版本：

```bash
git pull
```

習慣是：**開始前 pull，結束後 push**。兩台電腦輪流寫時就不會衝突。

## 6. 常見狀況與救法

**改壞了某個檔案，還沒 commit，想回到上次 commit 的樣子**

```bash
git restore 檔案路徑
```

注意：這會丟掉該檔案還沒 commit 的修改，無法復原。

**`git add` 加錯檔案，想從暫存清單拿掉**（檔案本身不受影響）

```bash
git restore --staged 檔案路徑
```

**commit 訊息打錯，而且還沒 push**

```bash
git commit --amend -m "正確的訊息"
```

已經 push 的 commit 就不要改了，直接再 commit 一次修正即可。

**push 時出現 `rejected` 或 `fetch first`**

代表 GitHub 上有你本機沒有的 commit，例如你在網站上改過檔案。先拉下來再推：

```bash
git pull --rebase
git push
```

**push 時要求輸入帳號密碼，或一直卡住**

密碼欄要貼「個人存取權杖」，不是 GitHub 登入密碼。最簡單的做法是改用 VS Code 的「同步變更」按鈕，它會用瀏覽器幫你登入 GitHub。

**想看某個檔案以前的樣子**

```bash
git log --oneline -- 檔案路徑      # 列出改過這個檔案的 commit
git show <commit 編號>:檔案路徑     # 顯示當時的內容
```

## 7. 哪些東西不要上傳

- **密碼、權杖、金鑰**：repo 是公開的，一旦 push 就要當作已經外流，刪掉也可能已被別人存下。
- **編譯產物**：`sol` 執行檔、`.dSYM` 資料夾等已經寫在 `.gitignore`，Git 會自動忽略。
- **大型測資**：超過幾 MB 的測資檔不要放，GitHub 單檔上限是 100 MB。

想讓 Git 忽略其他檔案，就把檔名或規則加進 `.gitignore`。

## 8. 指令速查

| 想做的事 | 指令 |
| --- | --- |
| 看目前狀態 | `git status` |
| 看改了哪些行 | `git diff` |
| 加入暫存清單 | `git add 路徑`（全部：`git add .`） |
| 建立存檔點 | `git commit -m "訊息"` |
| 上傳到 GitHub | `git push` |
| 從 GitHub 下載更新 | `git pull` |
| 看歷史紀錄 | `git log --oneline` |
| 丟掉未 commit 的修改 | `git restore 路徑` |
| 下載整個 repo | `git clone 網址` |
