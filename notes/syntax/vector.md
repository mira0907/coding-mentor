# vector

`vector` 是可以變長的陣列，競賽中幾乎所有陣列都用它。

## 建立 vector

- **語法**：
  - `vector<int> a;`：空的
  - `vector<int> a(n);`：n 格，全部是 0
  - `vector<int> a(n, x);`：n 格，全部是 x
  - `vector<int> a = {3, 1, 2};`：直接給內容
- **複雜度**：O(n)

```cpp
int n = 4;                    // 陣列長度
vector<int> a(n, -1);         // 4 格，全部是 -1
vector<int> b = {3, 1, 2};    // 直接給內容
for (int x : a) cout << x << ' ';   // x：依序是 a 的每一格
cout << '\n';
for (int x : b) cout << x << ' ';
cout << '\n';
```

輸出：

```text
-1 -1 -1 -1 
3 1 2 
```

**常見錯誤**

- **還沒讀入 n 就建立**：`int n; vector<int> a(n); cin >> n;` 建立時 n 還沒有值，陣列大小是亂的。一定要先 `cin >> n;` 再建立。

**出現在**：1-2

## push_back、pop_back、back、empty：在尾端加入與刪除

- **用途**：不知道最後會有幾個元素時，一個一個加在尾端。
- **語法**：
  - `a.push_back(x)`：在尾端加入 x
  - `a.pop_back()`：刪掉最後一個
  - `a.back()`：最後一個元素
  - `a.empty()`：是不是空的
- **複雜度**：都是 O(1)

```cpp
vector<int> path;        // 走過的點
path.push_back(5);
path.push_back(4);
path.push_back(3);
cout << path.size() << ' ' << path.back() << '\n';
path.pop_back();         // 刪掉 3
cout << path.size() << ' ' << path.back() << '\n';
cout << path.empty() << '\n';   // 不是空的，印出 0
```

輸出：

```text
3 3
2 4
0
```

**常見錯誤**

- **對空的 vector 取 `a[0]`、`a.back()` 或 `pop_back()`**：會 RE。先用 `if (!a.empty())` 檢查。

**出現在**：1-1、1-2

## size()：無號整數的陷阱

- **用途**：取得元素個數。
- **回傳**：`size_t`，這是**無號**整數，不會是負的。
- **複雜度**：O(1)

無號整數會造成兩個問題：

1. `for (int j = 0; j < a.size(); j++)` 在比較 `int` 和無號整數，編譯器會出現 `-Wsign-compare` 警告。寫成 `(int)a.size()` 就好。
2. a 是空的時，`a.size() - 1` 不是 -1，而是一個超大的數字。

```cpp
vector<int> a;                       // 空的 vector
cout << (a.size() - 1 > 100) << '\n';    // 無號整數 0 - 1 變成超大的數，印出 1
cout << ((int)a.size() - 1) << '\n';     // 先轉成 int，得到 -1
vector<int> b = {7, 8, 9};           // 有三個元素的 vector
for (int j = 0; j < (int)b.size(); j++) cout << b[j] << ' ';   // j：第幾格
cout << '\n';
```

輸出：

```text
1
-1
7 8 9 
```

**出現在**：1-2

## 二維 vector 與 vector 陣列

- **語法**：
  - `vector<vector<int>> g(n);`：n 個空的 vector，常用來存鄰接串列
  - `vector<vector<int>> d(n, vector<int>(m, 0));`：n × m 的表格，全部是 0

```cpp
int n = 3;                       // 點的數量
vector<vector<int>> g(n);        // g[u]：u 的所有鄰居
g[0].push_back(1);
g[0].push_back(2);
g[2].push_back(0);
for (int u = 0; u < n; u++) {    // u：目前的點
    cout << u << ':';
    for (int v : g[u]) cout << ' ' << v;   // v：u 的一個鄰居
    cout << '\n';
}
vector<vector<int>> d(2, vector<int>(3, 0));   // 2 列 3 行的表格
d[1][2] = 5;
cout << d[1][2] << ' ' << d[0][0] << '\n';
```

輸出：

```text
0: 1 2
1:
2: 0
5 0
```

## assign、resize、clear：改變大小或重設

- **語法**：
  - `a.assign(n, x)`：變成 n 格，全部是 x。多組測資時用來重設陣列。
  - `a.resize(n)`：改成 n 格，多出來的補 0，少掉的直接刪掉。
  - `a.clear()`：清空，size 變成 0。
- **複雜度**：O(n)

```cpp
vector<int> a = {1, 2, 3};   // 要調整的陣列
a.resize(5);                 // 補兩個 0
for (int x : a) cout << x << ' ';
cout << '\n';
a.assign(2, 9);              // 變成兩個 9
for (int x : a) cout << x << ' ';
cout << '\n';
a.clear();
cout << a.size() << '\n';
```

輸出：

```text
1 2 3 0 0 
9 9 
0
```
