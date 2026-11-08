# C++ 語法記錄庫

寫題目時遇到的新語法都收在這裡。每個語法一個小節，格式都一樣：用途、語法、範例與輸出、複雜度、常見錯誤、在哪一題用過。

## 目錄

| 檔案 | 內容 |
|------|------|
| [vector.md](vector.md) | 建立、加入與刪除、`size()` 的陷阱、二維 vector |
| [algorithm.md](algorithm.md) | 迭代器觀念，以及 `find`、`distance`、`count`、`sort`、`reverse`、`max_element`、`accumulate`、`lower_bound`、`unique`、`fill`、`iota` |

## 速查

| 想做的事 | 寫法 | 檔案 |
|----------|------|------|
| 找某個值在第幾格 | `find(a.begin(), a.end(), x) - a.begin()` | [algorithm.md](algorithm.md#find在範圍內找某個值) |
| 兩個迭代器差幾格 | `distance(it1, it2)` | [algorithm.md](algorithm.md#distance兩個迭代器差幾格) |
| 由小到大排序 | `sort(a.begin(), a.end())` | [algorithm.md](algorithm.md#sort排序) |
| 最大值與它的位置 | `max_element(a.begin(), a.end())` | [algorithm.md](algorithm.md#max_elementmin_element最大與最小) |
| 加總 | `accumulate(a.begin(), a.end(), 0LL)` | [algorithm.md](algorithm.md#accumulate加總) |
| 已排序陣列中找 ≥ x 的第一個 | `lower_bound(a.begin(), a.end(), x)` | [algorithm.md](algorithm.md#lower_boundupper_bound在排序好的陣列二分搜) |
| 去除重複 | `sort` 後 `a.erase(unique(...), a.end())` | [algorithm.md](algorithm.md#unique去除相鄰的重複) |
| 用 `size()` 寫迴圈不出警告 | `for (int i = 0; i < (int)a.size(); i++)` | [vector.md](vector.md#size無號整數的陷阱) |

## 怎麼新增一個語法

1. 判斷屬於哪一類，加到對應的檔案；沒有合適的就照 [_template.md](_template.md) 開新檔案，並加進上面的目錄。
2. 照模板寫：用途、語法、範例、輸出、複雜度、常見錯誤、出現在哪題。
3. **範例一定要自己跑過**，把真正的輸出貼進「輸出」區塊。
4. 常用的寫法加進上面的「速查」表。

範例程式只寫 `main` 裡面的內容，前面預設已經有 `#include <bits/stdc++.h>` 與 `using namespace std;`。

用 `python3 -I notes/syntax/check.py` 可以一次編譯並執行所有範例，檢查「輸出」區塊是否正確。
