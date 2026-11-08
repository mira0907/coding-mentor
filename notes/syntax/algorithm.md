# algorithm：處理陣列的常用函式

這些函式都在 `<algorithm>`，`accumulate` 和 `iota` 在 `<numeric>`。`#include <bits/stdc++.h>` 已經全部包含。

## 先懂迭代器：begin、end 與半開區間

迭代器是指向某一格的「位置」。

- `a.begin()`：指向第 0 格。
- `a.end()`：指向**最後一格的下一格**。這一格不存在，不能取值。
- `*it`：取出位置 it 上的值。
- `it - a.begin()`：it 是第幾格。
- `a.begin() + k`：第 k 格的位置。

所有函式都吃「從 first 到 last 前一格」的範圍，寫成 [first, last)，叫做半開區間。所以 `sort(a.begin(), a.end())` 是整個陣列，`sort(a.begin(), a.begin() + 3)` 是前三格。

```cpp
vector<int> a = {10, 20, 30, 40};   // 範例陣列
auto it = a.begin() + 2;            // it：指向第 2 格
cout << *it << '\n';                // 取出第 2 格的值
cout << it - a.begin() << '\n';     // it 是第幾格
cout << a.end() - a.begin() << '\n';    // 整個範圍的長度，等於 a.size()
```

輸出：

```text
30
2
4
```

## find：在範圍內找某個值

- **用途**：找某個值第一次出現在哪裡。
- **語法**：`find(first, last, x)`
- **回傳**：第一個等於 x 的位置；找不到就回傳 `last`。
- **複雜度**：O(n)，從頭一格一格比。

```cpp
vector<int> path = {4, 2, 0, 1, 2};               // 這一趟走過的點
auto it = find(path.begin(), path.end(), 0);      // it：0 第一次出現的位置
cout << it - path.begin() << '\n';                // 0 在第幾格
auto it2 = find(path.begin(), path.end(), 2);     // it2：只會找到第一個 2
cout << it2 - path.begin() << '\n';
auto it3 = find(path.begin(), path.end(), 9);     // it3：找不到 9
cout << (it3 == path.end()) << '\n';              // 找不到時等於 end()，印出 1
```

輸出：

```text
2
1
1
```

在 pair 陣列裡找，要寫出型態：

```cpp
vector<pair<int, int>> bre = {{1, 2}, {3, 1}};    // bre：停駛的航線
// x：要查的第一座島
// com：要查的第二座島
int x = 3, com = 1;
cout << (find(bre.begin(), bre.end(), make_pair(x, com)) != bre.end()) << '\n';       // 找得到 {3, 1}
cout << (find(bre.begin(), bre.end(), pair<int, int>{com, x}) != bre.end()) << '\n';  // {1, 3} 不在陣列裡
```

輸出：

```text
1
0
```

**常見錯誤**

- **沒檢查找不到的情況**：找不到時回傳 `end()`，對它取值 `*it` 會 RE。不確定一定找得到時，先判斷 `it != a.end()`。
- **直接傳大括號 `{x, y}`**：`find(b.begin(), b.end(), {x, y})` 會編譯錯誤（`no matching function for call to 'find'`）。`find` 要從傳入的值推斷型態，而 `{x, y}` 沒有型態。要寫成 `make_pair(x, y)` 或 `pair<int,int>{x, y}`。
- **放在迴圈裡用**：每次都是 O(n)，放在 n 次的迴圈裡就變成 O(n²)。要常常查「某個值在哪裡」時，改用陣列記錄位置，例如 `pos[x] = 第幾格`。

**出現在**：1-2

## distance：兩個迭代器差幾格

- **語法**：`distance(first, last)`
- **回傳**：從 first 走到 last 要走幾步。
- **複雜度**：vector 是 O(1)；`list`、`set` 這類不能跳著走的容器是 O(n)。

vector 的迭代器可以直接相減，所以 `distance(a.begin(), it)` 和 `it - a.begin()` 結果相同。`set` 的迭代器不能相減，只能用 `distance`。

```cpp
vector<int> path = {5, 4, 3, 1, 2};               // 這一趟走過的點
auto it = find(path.begin(), path.end(), 3);      // it：3 的位置
int index = distance(path.begin(), it);           // index：3 在第幾格
cout << index << ' ' << it - path.begin() << '\n';    // 兩種寫法相同
cout << distance(it, path.end()) << '\n';         // 從 3 到結尾有幾格，也就是 1-2 的圈長
```

輸出：

```text
2 2
3
```

**出現在**：1-2

## count：數某個值出現幾次

- **語法**：`count(first, last, x)`
- **複雜度**：O(n)

```cpp
vector<int> a = {1, 3, 1, 2, 1};             // 範例陣列
cout << count(a.begin(), a.end(), 1) << '\n';    // 1 出現幾次
```

輸出：

```text
3
```

## sort：排序

- **語法**：
  - `sort(first, last)`：由小到大
  - `sort(first, last, greater<int>())`：由大到小
  - `sort(first, last, [](const T& x, const T& y) { return ...; })`：自訂順序，x 要排在 y 前面時回傳 true
- **複雜度**：O(n log n)

`pair` 會先比 first，一樣再比 second。

```cpp
vector<int> a = {3, 1, 4, 1, 5};      // 要排序的陣列
sort(a.begin(), a.end());
for (int x : a) cout << x << ' ';
cout << '\n';
sort(a.begin(), a.end(), greater<int>());
for (int x : a) cout << x << ' ';
cout << '\n';
// e：每條邊存成 {權重, 編號}
vector<pair<int, int>> e = {{5, 0}, {2, 1}, {5, 2}, {1, 3}};
// 依權重由小到大，權重一樣時編號大的在前
sort(e.begin(), e.end(), [](const pair<int, int>& x, const pair<int, int>& y) {
    if (x.first != y.first) return x.first < y.first;
    return x.second > y.second;
});
for (auto [w, id] : e) cout << w << ',' << id << ' ';   // w：權重；id：編號
cout << '\n';
```

輸出：

```text
1 1 3 4 5 
5 4 3 1 1 
1,3 2,1 5,2 5,0 
```

**常見錯誤**

- **自訂比較寫成 `<=`**：兩個元素相等時必須回傳 false，寫 `<=` 可能讓程式 RE。

## reverse：反轉

- **語法**：`reverse(first, last)`
- **複雜度**：O(n)

常見用法：沿著 parent 從終點走回起點，得到反過來的路徑，再 reverse 一次。

```cpp
vector<int> route = {4, 2, 1};     // 從終點往回走得到的路徑
reverse(route.begin(), route.end());
for (int x : route) cout << x << ' ';
cout << '\n';
```

輸出：

```text
1 2 4 
```

## max_element、min_element：最大與最小

- **語法**：`max_element(first, last)`、`min_element(first, last)`
- **回傳**：位置，不是值。要取值就加 `*`。有好幾個最大值時，回傳第一個。
- **複雜度**：O(n)

```cpp
vector<int> a = {3, 9, 2, 9};                     // 範例陣列
auto it = max_element(a.begin(), a.end());        // it：最大值的位置
cout << *it << ' ' << it - a.begin() << '\n';     // 最大值與它在第幾格
cout << *min_element(a.begin(), a.end()) << '\n';
```

輸出：

```text
9 1
2
```

**常見錯誤**

- **陣列是空的**：會回傳 `end()`，再取 `*` 就會 RE。

## accumulate：加總

- **語法**：`accumulate(first, last, 初始值)`
- **複雜度**：O(n)

**結果的型態跟初始值一樣**。寫 `0` 就用 int 算，總和超過約 2.1×10⁹ 就會溢位；要 long long 就寫 `0LL`。

```cpp
vector<int> a = {2000000000, 2000000000};      // 兩個很大的數
cout << accumulate(a.begin(), a.end(), 0LL) << '\n';   // 用 long long 加總
```

輸出：

```text
4000000000
```

## lower_bound、upper_bound：在排序好的陣列二分搜

- **語法**：
  - `lower_bound(first, last, x)`：第一個 **≥ x** 的位置
  - `upper_bound(first, last, x)`：第一個 **> x** 的位置
- **回傳**：位置；全部都比 x 小時回傳 `last`。
- **複雜度**：O(log n)

陣列**一定要先排序**，不然答案是錯的。

```cpp
vector<int> a = {1, 3, 3, 3, 7};     // 已排序的陣列
int lo = lower_bound(a.begin(), a.end(), 3) - a.begin();   // lo：第一個 ≥ 3 在第幾格
int hi = upper_bound(a.begin(), a.end(), 3) - a.begin();   // hi：第一個 > 3 在第幾格
cout << lo << ' ' << hi << ' ' << hi - lo << '\n';         // hi - lo 就是 3 出現幾次
cout << lower_bound(a.begin(), a.end(), 8) - a.begin() << '\n';   // 沒有 ≥ 8 的數，得到 a.size()
```

輸出：

```text
1 4 3
5
```

## unique：去除相鄰的重複

- **語法**：`a.erase(unique(a.begin(), a.end()), a.end());`
- **複雜度**：O(n)

`unique` 只會把**相鄰**重複的擠掉，所以要先 `sort`。它不會真的縮短陣列，只把不重複的搬到前面，並回傳新的結尾，所以要再 `erase` 後面多出來的部分。常用在座標壓縮。

```cpp
vector<int> a = {3, 1, 3, 2, 1};    // 有重複的陣列
sort(a.begin(), a.end());           // 變成 1 1 2 3 3
a.erase(unique(a.begin(), a.end()), a.end());
for (int x : a) cout << x << ' ';
cout << '\n';
```

輸出：

```text
1 2 3 
```

## fill、iota：填值

- **語法**：
  - `fill(first, last, x)`：整段填成 x
  - `iota(first, last, start)`：依序填 start、start+1、start+2……。常用在並查集初始化 `parent[i] = i`。
- **複雜度**：O(n)

```cpp
vector<int> dist(4);                       // 每個點的距離
fill(dist.begin(), dist.end(), -1);        // 全部設成 -1，代表還沒走到
for (int x : dist) cout << x << ' ';
cout << '\n';
vector<int> parent(5);                     // 並查集：每個點的父節點
iota(parent.begin(), parent.end(), 0);     // parent[i] = i
for (int x : parent) cout << x << ' ';
cout << '\n';
```

輸出：

```text
-1 -1 -1 -1 
0 1 2 3 4 
```
