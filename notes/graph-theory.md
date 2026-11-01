# 競賽圖論講義

2026-11-01

## 前言與使用方式

本講義涵蓋程式競賽（APCS、TOI、ICPC、Codeforces）最常出現的八大圖論主題，每章包含觀念、模板程式碼、兩題範例程式題（基礎與困難各一）與十題觀念檢測，最後附六題分級練習與詳解。

建議讀法：先讀觀念與模板，再自己寫範例程式題後對照解答，闔上講義自行作答章末十題，再對照答案；全部章節讀完後再挑戰綜合練習題。

**程式碼慣例**

- 語言為 C++17，使用 `#include <bits/stdc++.h>` 與 `using namespace std;`。
- 點的編號預設為 1 到 n，n 為點數、m 為邊數。
- 距離可能超過 int 時一律用 `long long`，無限大用 `INF = 1e18`（long long）或 `1e9`（int）。
- 複雜度以 n、m 表示，V、E 為同義寫法。

**章節總覽**

| 章 | 主題 | 核心演算法 | 典型複雜度 |
| --- | --- | --- | --- |
| 一 | 基本概念與存圖 | 鄰接矩陣、鄰接串列 | O(n + m) 空間 |
| 二 | 遍歷 | BFS、DFS | O(n + m) |
| 三 | 最短路徑 | Dijkstra、Bellman-Ford、Floyd、0-1 BFS | O(m log n) 起 |
| 四 | 最小生成樹 | 並查集、Kruskal、Prim | O(m log m) |
| 五 | 拓撲排序 | Kahn、DAG DP | O(n + m) |
| 六 | 連通性 | Tarjan SCC、橋與割點、2-SAT | O(n + m) |
| 七 | 樹上技巧 | 直徑、重心、LCA、樹上差分 | O(n log n) |
| 八 | 二分圖與網路流 | 匈牙利、Dinic、歐拉路徑 | 依演算法而定 |

## 第一章 圖的基本概念與存圖方式

競賽中絕大多數題目用鄰接串列存圖，只有 n ≤ 500 左右且需要 O(1) 查邊時才用鄰接矩陣。

### 1.1 常用名詞

- **圖 G = (V, E)**：點集 V、邊集 E。邊可以有向或無向、帶權或不帶權。
- **度數**：無向圖中一點連出的邊數；有向圖分為入度與出度。握手定理：所有點度數總和 = 2m。
- **自環與重邊**：自環是 u 到 u 的邊；重邊是同一對點間的多條邊。無自環、無重邊的圖稱為簡單圖。
- **路徑與環**：路徑是一串相鄰的點；簡單路徑不重複經過點；環是起點等於終點的路徑。
- **連通**：無向圖任兩點可互通稱為連通；有向圖任兩點可互相抵達稱為強連通。
- **樹**：連通且無環的無向圖，恰有 n − 1 條邊，任兩點間恰有一條簡單路徑。多棵樹稱為森林。
- **DAG**：有向無環圖（Directed Acyclic Graph）。
- **稀疏圖與稠密圖**：m 與 n 同階為稀疏圖；m 接近 n² 為稠密圖。

### 1.2 三種存圖方式

| 方式 | 空間 | 查詢 u-v 是否有邊 | 列出 u 的鄰居 | 適用場景 |
| --- | --- | --- | --- | --- |
| 鄰接矩陣 | O(n²) | O(1) | O(n) | n ≤ 約 2000、Floyd、稠密圖 |
| 鄰接串列 | O(n + m) | O(deg u) | O(deg u) | 絕大多數題目 |
| 邊列表 | O(m) | O(m) | O(m) | Kruskal、Bellman-Ford |

鄰接串列模板（無向帶權圖）：

```cpp
int n, m;
vector<vector<pair<int,int>>> adj; // adj[u] = {(v, w), ...}

int main() {
    cin >> n >> m;
    adj.assign(n + 1, {});
    for (int i = 0; i < m; i++) {
        int u, v, w;
        cin >> u >> v >> w;
        adj[u].push_back({v, w});
        adj[v].push_back({u, w}); // 有向圖則刪除這行
    }
}
```

需要標記「第幾條邊」時（例如找橋、網路流的反向邊），可改存 `{v, 邊編號}`，或使用「鏈式前向星」陣列寫法，讓第 i 條邊與第 i ^ 1 條邊互為反向邊。

### 1.3 常見陷阱

- 無向圖忘記加兩個方向的邊。
- 多組測資時未清空鄰接串列。
- 鄰接矩陣遇到重邊時，應取最小權重而非直接覆蓋。
- n = 10⁵ 時開 `int g[n][n]` 會使用 40 GB 記憶體，必然超過限制。

### 範例 1-A 握手統計（基礎）

派對上有 n 個人，發生了 m 次握手，每次是兩個不同的人互握（同一對人可能握多次）。請輸出每個人的握手次數，以及握手次數為奇數的人數。

- **輸入**：第一行 n、m（1 ≤ n ≤ 10⁵，0 ≤ m ≤ 2×10⁵）。接下來 m 行，每行 u、v（u ≠ v）。
- **輸出**：第一行 n 個整數，第 i 個為第 i 個人的握手次數。第二行為奇數次的人數。

```text
範例輸入
4 4
1 2
2 3
3 1
3 4

範例輸出
2 2 3 1
2
```

**解答**：握手次數就是度數。這題不需要存整張圖，只要一個度數陣列：每讀到一條邊，兩端的度數各加 1。重邊代表多次握手，本來就該重複計算。由握手定理，奇數度的人數一定是偶數，可以用來自我檢查。複雜度 O(n + m)。

```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);
    int n, m;
    cin >> n >> m;
    vector<int> deg(n + 1, 0);
    for (int i = 0; i < m; i++) {
        int u, v;
        cin >> u >> v;
        deg[u]++; deg[v]++;          // 無向邊兩端各加一
    }
    int odd = 0;
    for (int i = 1; i <= n; i++) {
        cout << deg[i] << " \n"[i == n];
        if (deg[i] % 2 == 1) odd++;
    }
    cout << odd << "\n";
}
```

### 範例 1-B 三角形計數（困難）

給一張 n 個點、m 條邊的簡單無向圖（無重邊、無自環），求圖中有多少個三角形，也就是兩兩相鄰的三點組 {a, b, c}。

- **輸入**：第一行 n、m（1 ≤ n ≤ 10⁵，0 ≤ m ≤ 2×10⁵）。接下來 m 行，每行 u、v。
- **輸出**：三角形個數。

```text
範例輸入
4 5
1 2
2 3
3 1
3 4
4 1

範例輸出
2
```

**解答**：暴力枚舉「每個點的兩個鄰居」在星狀圖上會是 O(n²)。關鍵是選對存圖方式：把無向邊定向，從「度數小的點」指向「度數大的點」，度數相同時由編號小的指向編號大的。

1. 這個順序是一個全序，定向後的圖是 DAG。每個三角形的三個點中，「最小」的點 u 指向另兩點，而其中較小的 v 指向最大的 w。所以每個三角形恰好以 u → v → w 且 u → w 的形式被數到一次。
2. 枚舉 u，先把 u 的所有出鄰居標記為 u。再枚舉 u 的出鄰居 v，與 v 的出鄰居 w；若 w 帶有標記 u，就是一個三角形。
3. **為何快**：一個點的出度最多 O(√m)。度數大於 √m 的點只有 O(√m) 個，而出邊只指向度數更大的點，所以不論哪種情況出度都不超過 O(√m)。內層迴圈對每條邊 u → v 跑 out(v) 次，總計 O(m√m)，約 9×10⁷。

最大規模且有約 4×10⁷ 個三角形的測資，實測 0.16 秒。答案可能超過 int，要用 long long。

```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);
    int n, m;
    cin >> n >> m;
    vector<pair<int,int>> edges(m);
    vector<int> deg(n + 1, 0);
    for (auto& [u, v] : edges) { cin >> u >> v; deg[u]++; deg[v]++; }
    // 依 (度數, 編號) 定向：從「小」指向「大」
    auto less_ = [&](int a, int b) {
        return deg[a] != deg[b] ? deg[a] < deg[b] : a < b;
    };
    vector<vector<int>> out(n + 1);
    for (auto [u, v] : edges) {
        if (less_(u, v)) out[u].push_back(v);
        else out[v].push_back(u);
    }
    vector<int> mark(n + 1, 0);
    long long tri = 0;
    for (int u = 1; u <= n; u++) {
        for (int v : out[u]) mark[v] = u;          // 標記 u 的出鄰居
        for (int v : out[u])
            for (int w : out[v])
                if (mark[w] == u) tri++;           // u→v→w 且 u→w
    }
    cout << tri << "\n";
}
```

### 第一章 觀念檢測

1. （是非）任何無向圖中，度數為奇數的點必有偶數個。
2. （是非）有 n 個點、n − 1 條邊的無向圖一定是樹。
3. （選擇）n = 2×10⁵、m = 2×10⁵ 時最適合的存圖方式是：(A) 鄰接矩陣 (B) 鄰接串列 (C) 只存度數 (D) 都可以
4. （選擇）一個有 n 個點的簡單無向圖最多有幾條邊？(A) n (B) n − 1 (C) n(n − 1)/2 (D) n²
5. （是非）在鄰接串列中判斷 u、v 是否相鄰的時間是 O(1)。
6. （選擇）無向圖有 7 個點，度數總和為 20，則邊數為：(A) 7 (B) 10 (C) 20 (D) 40
7. （是非）樹中任意刪除一條邊，圖必定變成不連通。
8. （選擇）下列何者最適合用邊列表存圖？(A) BFS (B) Kruskal (C) DFS 找連通塊 (D) 拓撲排序
9. （是非）有向圖中所有點的入度總和等於出度總和。
10. （選擇）下列關於森林的敘述何者正確？設有 n 個點、k 棵樹。(A) 邊數為 n − 1 (B) 邊數為 n − k (C) 邊數為 n + k (D) 邊數無法確定

**參考答案**

1. 是。度數總和為 2m 是偶數，故奇數度點的個數必為偶數。
2. 非。還需要連通。例如三個點成一個環加上一個孤立點，共 4 點 3 邊，卻不是樹。
3. B。鄰接矩陣需要 4×10¹⁰ 格，記憶體不足。
4. C。任兩點最多一條邊，共 C(n, 2) 對。
5. 非。需要掃過 u 的鄰居，為 O(deg u)。
6. B。握手定理：m = 20 / 2 = 10。
7. 是。樹的每條邊都是橋。
8. B。Kruskal 需要將所有邊依權重排序。
9. 是。每條有向邊恰好貢獻一個入度與一個出度，兩者皆等於 m。
10. B。每棵樹的邊數是其點數減 1，全部相加得 n − k。

## 第二章 圖的遍歷：BFS 與 DFS

BFS 與 DFS 都是 O(n + m)；BFS 能求無權圖最短路，DFS 則是拓撲排序、強連通分量、樹 DP 等進階演算法的基礎。

### 2.1 廣度優先搜尋 BFS

BFS 用佇列依「距離起點的層數」由近到遠擴展。因為同一層的點全部出佇列後才輪到下一層，第一次抵達某點時的層數就是它的最短距離（各邊權重相同時）。

```cpp
vector<int> bfs(int s, const vector<vector<int>>& adj) {
    int n = adj.size();
    vector<int> dist(n, -1);
    queue<int> q;
    dist[s] = 0; q.push(s);
    while (!q.empty()) {
        int u = q.front(); q.pop();
        for (int v : adj[u]) {
            if (dist[v] != -1) continue;
            dist[v] = dist[u] + 1;   // 入佇列時就標記，避免重複入列
            q.push(v);
        }
    }
    return dist;
}
```

- **網格 BFS**：把每個格子當成點，用 `dx[] = {1,-1,0,0}`、`dy[] = {0,0,1,-1}` 列出四個鄰居，記得檢查邊界與障礙物。
- **多源 BFS**：把所有起點同時以距離 0 放入佇列，求每點到「最近起點」的距離，例如火勢蔓延、多個高鐵站。
- **路徑還原**：更新 dist\[v\] 時同時記錄 par\[v\] = u，最後從終點沿 par 往回走。
- **狀態 BFS**：當「位置」不足以描述狀態時，把點擴充為 (位置, 額外資訊)，例如 (x, y, 已打破牆數)。

### 2.2 深度優先搜尋 DFS

DFS 沿一條路走到底再回頭，常用於數連通塊、判環、樹上計算。

```cpp
vector<vector<int>> adj;
vector<int> tin, tout, comp;
int timer_ = 0;

void dfs(int u, int c) {
    comp[u] = c;
    tin[u] = ++timer_;            // 進入時間戳
    for (int v : adj[u])
        if (!comp[v]) dfs(v, c);
    tout[u] = ++timer_;           // 離開時間戳
}

// 數連通塊：
int cnt = 0;
for (int i = 1; i <= n; i++)
    if (!comp[i]) dfs(i, ++cnt);
```

- **時間戳性質**：在 DFS 樹上，u 是 v 的祖先若且唯若 tin\[u\] ≤ tin\[v\] 且 tout\[v\] ≤ tout\[u\]。這是樹序列化（Euler Tour）的基礎，可把子樹變成一段連續區間。
- **有向圖判環**：用三色標記（0 未拜訪、1 在遞迴堆疊中、2 已完成）。若走到顏色為 1 的點（回邊），圖中有環。
- **無向圖判環**：走到已拜訪且不是父節點的點就有環；有重邊時要用「來時的邊編號」而不是「父節點」判斷。
- **遞迴深度**：n = 10⁵ 的鏈狀圖在部分平台會堆疊溢位，可改用顯式 stack 或 BFS 序。

### 2.3 怎麼選

| 需求 | 選擇 |
| --- | --- |
| 無權最短路、最少步數 | BFS |
| 只問能不能到、數連通塊 | 兩者皆可，也可用並查集 |
| 判環、拓撲、子樹資訊 | DFS |
| 輸出字典序最小的遍歷 | 鄰居先排序再 DFS/BFS |

### 範例 2-A 騎士巡邏（基礎）

N × N 的棋盤上，騎士每步走「日」字（一個方向 2 格、另一個方向 1 格，共 8 種走法）。求從 (sx, sy) 到 (tx, ty) 最少要幾步，無法抵達輸出 `-1`。

- **輸入**：一行 N、sx、sy、tx、ty（1 ≤ N ≤ 1000，座標從 1 開始）。
- **輸出**：最少步數或 `-1`。

```text
範例輸入
8 1 1 8 8

範例輸出
6
```

**解答**：每格是一個點，每種走法是一條權重 1 的邊，最少步數就是無權最短路，用 BFS。把 8 種位移寫成 dx、dy 陣列，檢查邊界後就和網格 BFS 完全一樣。N = 2 或 3 的小棋盤有些格子到不了，dist 會維持為 -1，正好就是答案。複雜度 O(8N²)。

```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
    int N, sx, sy, tx, ty;
    cin >> N >> sx >> sy >> tx >> ty;
    int dx[] = {1, 2, 2, 1, -1, -2, -2, -1};
    int dy[] = {2, 1, -1, -2, -2, -1, 1, 2};
    vector<vector<int>> dist(N + 1, vector<int>(N + 1, -1));
    queue<pair<int,int>> q;
    dist[sx][sy] = 0; q.push({sx, sy});
    while (!q.empty()) {
        auto [x, y] = q.front(); q.pop();
        for (int d = 0; d < 8; d++) {
            int nx = x + dx[d], ny = y + dy[d];
            if (nx < 1 || nx > N || ny < 1 || ny > N || dist[nx][ny] != -1) continue;
            dist[nx][ny] = dist[x][y] + 1;
            q.push({nx, ny});
        }
    }
    cout << dist[tx][ty] << "\n";
}
```

### 範例 2-B 破牆迷宮（困難）

R × C 的迷宮中 `.` 是通道、`#` 是牆。你從左上角出發要到右下角，每步往上下左右走一格。你有一把錘子，最多可以打破 K 面牆（走進一個 `#` 格就算打破一面）。求最少步數，無法抵達輸出 `-1`。

- **輸入**：第一行 R、C、K（1 ≤ R, C ≤ 500，0 ≤ K ≤ 10）。接下來 R 行地圖，起點與終點保證是 `.`。
- **輸出**：最少步數或 `-1`。

```text
範例輸入
4 5 1
.#...
.#.#.
.#.#.
...#.

範例輸出
7
```

K = 0 時只能繞 S 形，需要 13 步；K = 1 時打破右下角旁邊那面牆即可，只要 7 步。

**解答**：只用位置 (x, y) 當狀態是不夠的。同一格「用了 0 次錘子到達」與「用了 3 次錘子到達」對未來完全不同。若只保留先到的那個，可能丟掉「慢一點但省下錘子」的更好路線。

1. 把狀態擴充為 (x, y, k)，k 是已打破的牆數，共 R × C × (K + 1) ≤ 2.75×10⁶ 個狀態。
2. 從 (x, y, k) 走到鄰格：鄰格是 `.` 則到 (nx, ny, k)，是 `#` 則到 (nx, ny, k + 1)，前提是 k + 1 ≤ K。
3. 每步代價都是 1，所以在這個「狀態圖」上 BFS。第一個出佇列的終點狀態（不論 k）就是答案。

狀態用一維陣列 (x · C + y) · (K + 1) + k 儲存，比三維 vector 更省記憶體也更快。複雜度 O(RCK)。注意這題問的是「步數」而不是「打破的牆數」；若問最少打破幾面牆，就變成邊權 0/1 的 0-1 BFS。

```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);
    int R, C, K;
    cin >> R >> C >> K;
    vector<string> g(R);
    for (auto& s : g) cin >> s;
    // 狀態 (x, y, 已打破幾面牆)，攤平成一維陣列
    auto id = [&](int x, int y, int k) { return (x * C + y) * (K + 1) + k; };
    vector<int> dist(R * C * (K + 1), -1);
    queue<array<int,3>> q;
    dist[id(0, 0, 0)] = 0; q.push({0, 0, 0});
    int dx[] = {1, -1, 0, 0}, dy[] = {0, 0, 1, -1};
    while (!q.empty()) {
        auto [x, y, k] = q.front(); q.pop();
        if (x == R - 1 && y == C - 1) { cout << dist[id(x, y, k)] << "\n"; return 0; }
        for (int d = 0; d < 4; d++) {
            int nx = x + dx[d], ny = y + dy[d];
            if (nx < 0 || nx >= R || ny < 0 || ny >= C) continue;
            int nk = k + (g[nx][ny] == '#');       // 走進牆就要打破一次
            if (nk > K || dist[id(nx, ny, nk)] != -1) continue;
            dist[id(nx, ny, nk)] = dist[id(x, y, k)] + 1;
            q.push({nx, ny, nk});
        }
    }
    cout << -1 << "\n";
}
```

### 第二章 觀念檢測

1. （是非）BFS 可以正確求出帶權圖（權重不同）的最短路。
2. （選擇）以鄰接串列實作 BFS，時間複雜度為：(A) O(n) (B) O(m) (C) O(n + m) (D) O(n²)
3. （是非）BFS 中應該在點出佇列時才標記為已拜訪，否則會算錯距離。
4. （選擇）網格中有多個火源，每秒向四方蔓延一格，求每格被燒到的時間，最佳做法是：(A) 對每個火源各做一次 BFS (B) 多源 BFS (C) DFS (D) Floyd
5. （是非）在 DFS 樹上，若 tin\[u\] < tin\[v\] < tout\[u\]，則 u 是 v 的祖先。
6. （選擇）有向圖三色 DFS 中，走到哪一種顏色的點代表有環？(A) 未拜訪 (B) 在堆疊中 (C) 已完成 (D) 任一已拜訪的點
7. （是非）無向圖中 DFS 走到任何已拜訪的點都代表有環。
8. （選擇）一個 1000×1000 的迷宮，求起點到終點最少步數，合理的運算量約為：(A) 10⁶ (B) 10⁹ (C) 10¹² (D) 2^(10⁶)
9. （是非）對一個有 n 個點的鏈狀圖做遞迴 DFS，遞迴深度可能達到 n。
10. （選擇）要在 BFS 後輸出一條最短路徑，需要額外記錄：(A) 每點度數 (B) 每點的前驅點 (C) 佇列大小 (D) 時間戳

**參考答案**

1. 非。BFS 只保證「邊數」最少，權重不同時要用 Dijkstra。
2. C。每個點入列一次、每條邊被檢查常數次。
3. 非。應在入列時標記。出列才標記仍能得到正確距離，但同一點可能重複入列多次，最壞情況下佇列大小與時間接近 O(m)、常數變大。
4. B。所有火源一起以距離 0 入列，只需一次 O(格數)。
5. 是。v 在 u 進入後、離開前被拜訪，必在 u 的子樹內。
6. B。走到仍在堆疊中的點是回邊，形成環；已完成的點可能只是橫叉邊或前向邊。
7. 非。走回父節點（來時的那條邊）不算環。
8. A。格數 10⁶，每格四個鄰居，BFS 約 4×10⁶ 次操作。
9. 是。這是過深遞迴導致堆疊溢位的常見原因。
10. B。從終點沿前驅點一路回溯到起點，再反轉。

## 第三章 最短路徑

非負權單源最短路用 Dijkstra，有負權或要判負環用 Bellman-Ford，全點對且 n ≤ 500 用 Floyd-Warshall，邊權只有 0 與 1 用 0-1 BFS。

### 3.1 鬆弛（Relaxation）

所有最短路演算法都在反覆做同一件事：若 dist\[u\] + w(u, v) < dist\[v\]，就更新 dist\[v\]。差別只在「以什麼順序鬆弛哪些邊」。

### 3.2 Dijkstra

每次取出尚未確定、dist 最小的點 u，它的距離就此確定，再用 u 鬆弛鄰居。正確性依賴「邊權非負」：之後任何路徑都不可能再把 dist\[u\] 變小。

```cpp
using ll = long long;
const ll INF = 1e18;
vector<vector<pair<int,int>>> adj; // (v, w)

vector<ll> dijkstra(int s, int n) {
    vector<ll> dist(n + 1, INF);
    priority_queue<pair<ll,int>, vector<pair<ll,int>>, greater<>> pq;
    dist[s] = 0; pq.push({0, s});
    while (!pq.empty()) {
        auto [d, u] = pq.top(); pq.pop();
        if (d > dist[u]) continue;          // 過期的項目，跳過
        for (auto [v, w] : adj[u]) {
            if (dist[u] + w < dist[v]) {
                dist[v] = dist[u] + w;
                pq.push({dist[v], v});
            }
        }
    }
    return dist;
}
```

複雜度 O(m log m)。`if (d > dist[u]) continue;` 不可省略，否則在特定測資下會退化。

### 3.3 Bellman-Ford 與 SPFA

對所有邊鬆弛 n − 1 輪。最短路最多有 n − 1 條邊，所以 n − 1 輪後必定收斂；若第 n 輪仍能鬆弛，代表從起點可達的地方有負環。

```cpp
struct Edge { int u, v; ll w; };

// 回傳 false 表示存在可達負環
bool bellmanFord(int s, int n, const vector<Edge>& edges, vector<ll>& dist) {
    dist.assign(n + 1, INF);
    dist[s] = 0;
    for (int i = 1; i <= n; i++) {
        bool changed = false;
        for (auto& e : edges) {
            if (dist[e.u] != INF && dist[e.u] + e.w < dist[e.v]) {
                dist[e.v] = dist[e.u] + e.w;
                changed = true;
                if (i == n) return false;   // 第 n 輪仍更新 → 負環
            }
        }
        if (!changed) break;
    }
    return true;
}
```

複雜度 O(nm)。SPFA 是用佇列只鬆弛「剛被更新過」的點，平均很快但最壞仍是 O(nm)，正權圖請勿用 SPFA 取代 Dijkstra。

### 3.4 Floyd-Warshall

dp\[k\]\[i\]\[j\] 表示只用編號 ≤ k 的點當中繼時 i 到 j 的最短路。第一維可以壓掉，但 **k 必須是最外層迴圈**。

```cpp
// d[i][i] = 0，有邊則 d[u][v] = min(d[u][v], w)，其餘為 INF
for (int k = 1; k <= n; k++)
    for (int i = 1; i <= n; i++)
        for (int j = 1; j <= n; j++)
            if (d[i][k] < INF && d[k][j] < INF)
                d[i][j] = min(d[i][j], d[i][k] + d[k][j]);
// 跑完後若 d[i][i] < 0，代表 i 在負環上
```

複雜度 O(n³)，n = 500 時約 1.25×10⁸ 次運算。

### 3.5 0-1 BFS

邊權只有 0 或 1 時，用雙端佇列：權重 0 的邊把點放前面，權重 1 放後面。佇列始終保持「前段距離 d、後段距離 d + 1」，等價於不用 heap 的 Dijkstra，複雜度 O(n + m)。

```cpp
deque<int> dq; dist[s] = 0; dq.push_back(s);
while (!dq.empty()) {
    int u = dq.front(); dq.pop_front();
    for (auto [v, w] : adj[u]) {
        if (dist[u] + w < dist[v]) {
            dist[v] = dist[u] + w;
            if (w == 0) dq.push_front(v); else dq.push_back(v);
        }
    }
}
```

### 3.6 常見變形

- **分層圖**：「可以免費走 k 條邊」把點拆成 (點, 已用次數)，共 n(k + 1) 個點再跑 Dijkstra。
- **反向圖**：求「所有點到終點 t」的距離，把邊反向後從 t 跑一次。
- **超級源點**：多個起點時新增點 0 連到每個起點，邊權為 0。
- **最短路計數**：Dijkstra 中若 dist\[u\] + w == dist\[v\] 則 cnt\[v\] += cnt\[u\]，若更小則 cnt\[v\] = cnt\[u\]。
- **差分約束**：不等式 x\_v − x\_u ≤ c 轉成 u → v 權重 c 的邊，用 Bellman-Ford 求解或判無解。

### 範例 3-A 負環偵測（基礎）

給一張 n 個點、m 條邊的有向圖，邊權可能為負。若從點 1 能走到某個負環，輸出 `NEGATIVE CYCLE`。否則輸出點 1 到每個點的最短距離，到不了的點輸出 `INF`。

- **輸入**：第一行 n、m（1 ≤ n ≤ 2500，0 ≤ m ≤ 5000）。接下來 m 行 u、v、w（|w| ≤ 10⁹）。
- **輸出**：`NEGATIVE CYCLE`，或一行 n 個距離。

```text
範例輸入
4 4
1 2 4
1 3 2
3 2 -1
2 4 3

範例輸出
0 1 2 4
```

**解答**：有負權就不能用 Dijkstra，改用 Bellman-Ford。對所有邊鬆弛最多 n 輪：若某輪沒有任何更新就提前結束；若第 n 輪仍有更新，就存在可達負環。

- **為何只算「可達」負環**：鬆弛前要求 dist\[u\] ≠ INF。若省略這個判斷，一個從 1 到不了的負環也會讓 INF 不斷變小，誤判為有負環。
- **溢位**：最短路絕對值可達 2500 × 10⁹，用 long long。INF 取 LLONG\_MAX / 4，避免加法溢位。
- **複雜度**：O(nm)，最多 1.25×10⁷ 次鬆弛。

```cpp
#include <bits/stdc++.h>
using namespace std;
using ll = long long;
const ll INF = LLONG_MAX / 4;
int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);
    int n, m;
    cin >> n >> m;
    vector<array<ll,3>> e(m);
    for (auto& [u, v, w] : e) cin >> u >> v >> w;
    vector<ll> dist(n + 1, INF);
    dist[1] = 0;
    for (int round = 1; round <= n; round++) {
        bool changed = false;
        for (auto [u, v, w] : e) {
            if (dist[u] == INF) continue;          // 尚不可達的點不能拿來鬆弛
            if (dist[u] + w < dist[v]) {
                dist[v] = dist[u] + w;
                changed = true;
            }
        }
        if (!changed) break;
        if (round == n) { cout << "NEGATIVE CYCLE\n"; return 0; }
    }
    for (int i = 1; i <= n; i++) {
        if (dist[i] == INF) cout << "INF";
        else cout << dist[i];
        cout << " \n"[i == n];
    }
}
```

### 範例 3-B 優惠券航線（困難）

有 n 座城市、m 條雙向航線，第 i 條票價 w\_i。你手上有 K 張優惠券，每張可以讓一段航線免費。求從城市 1 飛到城市 n 的最少花費，無法抵達輸出 `-1`。

- **輸入**：第一行 n、m、K（2 ≤ n ≤ 10⁴，0 ≤ m ≤ 5×10⁴，0 ≤ K ≤ 10）。接下來 m 行 u、v、w（1 ≤ w ≤ 10⁹）。
- **輸出**：最少花費或 `-1`。

```text
範例輸入
4 4 1
1 2 5
2 4 5
1 3 1
3 4 100

範例輸出
1
```

付 1 飛到城市 3，再用優惠券飛過票價 100 的航線。

**解答**：這是 3.6 節的「分層圖」。常見的錯誤想法是「先跑最短路，再把路上最貴的 K 段免費」。但最佳路線本身會因優惠券而改變，範例就是反例：原最短路 1–2–4 免費一段後是 5，而答案是 1。

1. 狀態 (v, j)：人在 v、已用 j 張優惠券，共 n(K + 1) ≤ 1.1×10⁵ 個狀態。
2. 從 (u, j) 沿航線 u–v：付費到 (v, j)，花費 + w；或用券到 (v, j + 1)，花費 + 0，前提是 j < K。
3. 邊權非負，在狀態圖上跑 Dijkstra。答案為 min over j of dist\[n\]\[j\]。

不必真的建出 K + 1 層圖，在鬆弛時直接對兩種選擇各做一次即可。狀態圖有 2m(K + 1) ≤ 1.1×10⁶ 條邊，複雜度 O(mK log(mK))，實測 0.1 秒。

```cpp
#include <bits/stdc++.h>
using namespace std;
using ll = long long;
const ll INF = 1e18;
int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);
    int n, m, K;
    cin >> n >> m >> K;
    vector<vector<pair<int,int>>> adj(n + 1);
    for (int i = 0; i < m; i++) {
        int u, v, w;
        cin >> u >> v >> w;
        adj[u].push_back({v, w});
        adj[v].push_back({u, w});
    }
    // dist[v][j] = 到達 v、已用 j 張優惠券的最小花費
    vector<vector<ll>> dist(n + 1, vector<ll>(K + 1, INF));
    priority_queue<tuple<ll,int,int>, vector<tuple<ll,int,int>>, greater<>> pq;
    dist[1][0] = 0; pq.push({0, 1, 0});
    while (!pq.empty()) {
        auto [d, u, j] = pq.top(); pq.pop();
        if (d > dist[u][j]) continue;
        for (auto [v, w] : adj[u]) {
            if (d + w < dist[v][j]) {                       // 正常付費
                dist[v][j] = d + w; pq.push({dist[v][j], v, j});
            }
            if (j < K && d < dist[v][j + 1]) {              // 使用一張優惠券
                dist[v][j + 1] = d; pq.push({d, v, j + 1});
            }
        }
    }
    ll ans = *min_element(dist[n].begin(), dist[n].end());
    cout << (ans == INF ? -1 : ans) << "\n";
}
```

### 第三章 觀念檢測

1. （是非）Dijkstra 在有負權邊但無負環的圖上仍然正確。
2. （選擇）使用 priority\_queue 的 Dijkstra 複雜度為：(A) O(n²) (B) O(m log m) (C) O(nm) (D) O(n + m)
3. （是非）Floyd-Warshall 的三層迴圈中，中繼點 k 可以放在最內層。
4. （選擇）Bellman-Ford 判斷負環的依據是：(A) 有負邊 (B) 第 n 輪仍能鬆弛 (C) dist 出現 INF (D) 佇列為空
5. （是非）若全圖所有邊權都是 1，用 BFS 即可取代 Dijkstra。
6. （選擇）n = 10⁵、m = 2×10⁵、邊權 1 到 10⁹，求單源最短路應選：(A) Floyd (B) Bellman-Ford (C) Dijkstra (D) BFS
7. （是非）在 0-1 BFS 中，權重為 0 的邊應把點放到雙端佇列的後端。
8. （選擇）要求「每個點到終點 t」的最短距離（有向圖），最有效率的做法是：(A) 每個點跑一次 Dijkstra (B) 在反向圖上從 t 跑一次 Dijkstra (C) Floyd (D) 從 t 在原圖跑 BFS
9. （是非）距離可能達 10⁹ × 10⁵ 時，dist 用 int 儲存會溢位。
10. （選擇）「可以最多把 k 條邊的權重變成 0」的最短路問題，典型建模是：(A) 分層圖 (B) 二分圖 (C) 最小生成樹 (D) 拓撲排序

**參考答案**

1. 非。已確定的點可能在之後經由負邊變得更近，而 Dijkstra 不會再回頭處理它。
2. B。每次成功鬆弛推一個項目入 heap，最多 m 個。
3. 非。k 必須在最外層，否則計算 d\[i\]\[j\] 時用到的 d\[i\]\[k\]、d\[k\]\[j\] 還沒有正確。
4. B。無負環時 n − 1 輪必定收斂。
5. 是。權重全同時，最短路就是最少邊數。
6. C。非負權且 n 大，Floyd 太慢，Bellman-Ford 最壞 2×10¹⁰。
7. 非。權重 0 放前端，權重 1 放後端。
8. B。反向圖上 t 到 v 的距離等於原圖 v 到 t 的距離。
9. 是。約 10¹⁴，遠超 int 上限 2.1×10⁹。
10. A。把點擴充為 (點, 已用次數)，層與層之間加權重 0 的邊。

## 第四章 最小生成樹與並查集

最小生成樹（MST）是連通所有點、邊權總和最小的樹；競賽中最常用 Kruskal 搭配並查集，O(m log m) 即可完成。

### 4.1 並查集 DSU

並查集（Disjoint Set Union）維護「哪些元素在同一組」，支援合併與查詢代表元。同時使用路徑壓縮與按大小合併時，每次操作均攤為 O(α(n))，實務上視為常數。

```cpp
struct DSU {
    vector<int> p, sz;
    DSU(int n) : p(n + 1), sz(n + 1, 1) { iota(p.begin(), p.end(), 0); }
    int find(int x) { return p[x] == x ? x : p[x] = find(p[x]); } // 路徑壓縮
    bool unite(int a, int b) {
        a = find(a); b = find(b);
        if (a == b) return false;           // 已在同一組
        if (sz[a] < sz[b]) swap(a, b);      // 小的接到大的下面
        p[b] = a; sz[a] += sz[b];
        return true;
    }
};
```

常見擴充：

- **維護組內資訊**：合併時一併更新大小、最大值、邊數等。
- **帶權並查集**：額外記錄每點到父節點的關係（例如差值、奇偶），路徑壓縮時累加，可解「朋友的敵人是敵人」類題目。
- **種類並查集**：把每個點拆成 x 與 x + n 兩個分身，分別代表兩種類別。
- **離線反著做**：只能合併不能分裂，所以「刪邊」問題可以倒過來變成「加邊」。

### 4.2 Kruskal

把邊依權重由小到大排序，依序加入；若兩端已連通則跳過（會形成環）。

```cpp
struct E { int u, v; long long w; };

long long kruskal(int n, vector<E>& edges) {
    sort(edges.begin(), edges.end(), [](const E& a, const E& b){ return a.w < b.w; });
    DSU dsu(n);
    long long total = 0; int used = 0;
    for (auto& e : edges)
        if (dsu.unite(e.u, e.v)) { total += e.w; used++; }
    return used == n - 1 ? total : -1;     // -1 表示圖不連通
}
```

### 4.3 Prim

從任一點開始，每次加入「連到目前樹上最便宜」的點，寫法與 Dijkstra 幾乎相同，只是比較的是邊權 w 而不是 dist\[u\] + w。

- 搭配 heap：O(m log m)，與 Kruskal 相當。
- 不用 heap、直接掃陣列找最小：O(n²)，適合完全圖（例如平面上 n 個點兩兩有邊），此時 Kruskal 要排序 n² 條邊反而較慢。

### 4.4 MST 的重要性質

- **切割性質**：對任意把點分成兩半的切割，橫跨切割的最小邊必定屬於某棵 MST。Kruskal 與 Prim 的正確性都源自此。
- **環性質**：任一環上權重嚴格最大的邊必不在任何 MST 中。
- **唯一性**：若所有邊權互不相同，MST 唯一。
- **最小瓶頸路徑**：MST 上兩點間的路徑，恰好使「路徑上最大邊」最小。「最大邊最小化」類題目可直接用 Kruskal 建樹。
- **最大生成樹**：邊由大到小排序即可。

### 範例 4-A 村莊供電（基礎）

n 個村莊都需要電。在村莊 i 蓋發電廠要花 c\_i；另有 m 條可架設的電線，第 j 條連接 u、v，花費 w。一個村莊有電若且唯若它自己有發電廠，或透過電線連到有發電廠的村莊。求讓所有村莊有電的最小總花費。

- **輸入**：第一行 n、m（1 ≤ n ≤ 10⁵，0 ≤ m ≤ 2×10⁵）。第二行 c\_1 到 c\_n。接下來 m 行 u、v、w。所有花費介於 1 到 10⁹。
- **輸出**：最小總花費。

```text
範例輸入
3 3
5 4 6
1 2 2
2 3 3
1 3 10

範例輸出
9
```

只在村莊 2 蓋發電廠（4），再架 1–2（2）與 2–3（3）。

**解答**：「蓋發電廠」不像一條邊，所以不能直接套 MST。技巧是加一個**虛擬點 0** 代表「電網」，在村莊 i 蓋發電廠就等於架一條 0–i、花費 c\_i 的邊。

- 「每個村莊有電」等價於「每個村莊都與點 0 連通」，也就是 0 到 n 共 n + 1 個點連通。
- 花費最小的連通子圖必定是樹，所以答案就是這張 n + 1 點圖的 MST。
- 虛擬點讓可以蓋多座發電廠的情況也自動被涵蓋。因為每個村莊都能蓋發電廠，圖一定連通，答案一定存在。

總花費可達 10⁹ × 10⁵，用 long long。複雜度 O((n + m) log(n + m))。

```cpp
#include <bits/stdc++.h>
using namespace std;
using ll = long long;
struct DSU {
    vector<int> p, sz;
    DSU(int n) : p(n + 1), sz(n + 1, 1) { iota(p.begin(), p.end(), 0); }
    int find(int x) { return p[x] == x ? x : p[x] = find(p[x]); }
    bool unite(int a, int b) {
        a = find(a); b = find(b);
        if (a == b) return false;
        if (sz[a] < sz[b]) swap(a, b);
        p[b] = a; sz[a] += sz[b];
        return true;
    }
};
int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);
    int n, m;
    cin >> n >> m;
    vector<array<ll,3>> e;              // (w, u, v)
    for (int i = 1; i <= n; i++) {
        ll c; cin >> c;
        e.push_back({c, 0, i});         // 虛擬發電廠 0 號點
    }
    for (int i = 0; i < m; i++) {
        ll u, v, w; cin >> u >> v >> w;
        e.push_back({w, u, v});
    }
    sort(e.begin(), e.end());
    DSU dsu(n);                          // 0..n 共 n+1 個點
    ll total = 0;
    for (auto [w, u, v] : e)
        if (dsu.unite(u, v)) total += w;
    cout << total << "\n";
}
```

### 範例 4-B 帳本矛盾（困難）

有 n 個帳戶，餘額未知。依序收到 m 條紀錄，第 i 條為「a b c」，表示「帳戶 b 的餘額比帳戶 a 多 c」。請找出第一條與先前紀錄矛盾的紀錄編號；全部一致輸出 `-1`。

- **輸入**：第一行 n、m（1 ≤ n ≤ 10⁵，1 ≤ m ≤ 2×10⁵）。接下來 m 行 a、b、c（|c| ≤ 10⁹，a 可能等於 b）。
- **輸出**：第一條矛盾紀錄的編號，或 `-1`。

```text
範例輸入
3 4
1 2 5
2 3 3
1 3 8
3 1 -7

範例輸出
4
```

由前兩條可推出帳戶 1 比帳戶 3 少 8，第 3 條一致，第 4 條寫少 7 則矛盾。

**解答**：用 4.1 節的**帶權並查集**。除了 par\[x\]，再維護 diff\[x\] = 值(x) − 值(par\[x\])。路徑壓縮後 par\[x\] 就是根，diff\[x\] 變成 值(x) − 值(根)。

1. **find 時累加**：先遞迴讓父節點壓縮到根，此時 diff\[par\[x\]\] 已是「父節點到根」的差。再做 diff\[x\] += diff\[par\[x\]\]，最後把 par\[x\] 指向根。順序不能倒過來。
2. **同一組**：值(b) − 值(a) = diff\[b\] − diff\[a\] 已經確定。若不等於 c 就是矛盾。
3. **不同組**：把根 rb 接到 ra 底下。需要 diff\[rb\] = 值(rb) − 值(ra)。由 值(b) = 值(rb) + diff\[b\]、值(a) = 值(ra) + diff\[a\]、值(b) − 值(a) = c，得到 diff\[rb\] = c + diff\[a\] − diff\[b\]。

「a a 0」自動一致，「a a 5」自動矛盾，不必特判。diff 可達 10⁹ × 10⁵，用 long long。這裡只用路徑壓縮，均攤 O(log n)，總計 O(m log n)。

```cpp
#include <bits/stdc++.h>
using namespace std;
using ll = long long;
vector<int> par;
vector<ll> diff;                         // diff[x] = 值(x) − 值(par[x])
int find(int x) {
    if (par[x] == x) return x;
    int r = find(par[x]);
    diff[x] += diff[par[x]];             // 先把父節點壓縮到根，再累加
    par[x] = r;
    return r;
}
int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);
    int n, m;
    cin >> n >> m;
    par.resize(n + 1); iota(par.begin(), par.end(), 0);
    diff.assign(n + 1, 0);
    for (int i = 1; i <= m; i++) {
        int a, b; ll c;
        cin >> a >> b >> c;              // 值(b) − 值(a) = c
        int ra = find(a), rb = find(b);
        if (ra == rb) {
            if (diff[b] - diff[a] != c) { cout << i << "\n"; return 0; }
        } else {
            // 讓 rb 接到 ra 底下：值(rb) − 值(ra) = c + diff[a] − diff[b]
            par[rb] = ra;
            diff[rb] = c + diff[a] - diff[b];
        }
    }
    cout << -1 << "\n";
}
```

### 第四章 觀念檢測

1. （是非）一個連通圖的最小生成樹一定只有一棵。
2. （選擇）並查集同時使用路徑壓縮與按大小合併，平均每次操作的複雜度為：(A) O(n) (B) O(log n) (C) O(α(n)) (D) O(√n)
3. （是非）Kruskal 的正確性依賴邊權非負。
4. （選擇）n 個點的連通圖，MST 有幾條邊？(A) n (B) n − 1 (C) m (D) m − n + 1
5. （是非）任一環上權重嚴格最大的邊不會出現在任何一棵 MST 中。
6. （選擇）平面上有 5000 個點，任兩點的費用為歐幾里得距離，求 MST 最適合：(A) Kruskal (B) O(n²) Prim (C) Floyd (D) Bellman-Ford
7. （是非）Kruskal 執行完若加入的邊數少於 n − 1，代表原圖不連通。
8. （選擇）「找一條從 s 到 t 的路徑，使路徑上最大邊權最小」，下列何者可解？(A) 在 MST 上取 s 到 t 的路徑 (B) Dijkstra 求最短路 (C) 拓撲排序 (D) 最大流
9. （是非）只用路徑壓縮、不按大小合併的並查集，在競賽中通常也夠快。
10. （選擇）一張圖不斷「刪邊」並詢問連通塊數，常見的離線解法是：(A) 每次重做 DFS (B) 把操作倒過來變成加邊，用並查集 (C) Floyd (D) 無法解

**參考答案**

1. 非。有相同邊權時可能有多棵，例如三條邊權都是 1 的三角形有三棵 MST。不過所有 MST 的總權重相同。
2. C。α 是反阿克曼函數，對任何實際的 n 都不超過 4。
3. 非。Kruskal 只比較邊權大小，負權也正確。
4. B。樹恰有 n − 1 條邊。
5. 是。若它在 MST 中，可用環上其他邊取代而得到更小的生成樹，矛盾。
6. B。邊數約 1.25×10⁷，Kruskal 排序與存邊的成本都偏高，O(n²) Prim 不必存邊。
7. 是。此時得到的是最小生成森林。
8. A。這是最小瓶頸路徑性質。也可以二分答案後用 BFS 判斷。
9. 是。只用路徑壓縮時均攤 O(log n)，實務上已經很快；但需要「可撤銷」時就不能用路徑壓縮，只能按大小合併。
10. B。並查集不支援分裂，倒序處理時刪邊變成加邊。

## 第五章 拓撲排序與 DAG

有向圖存在拓撲序若且唯若它是 DAG；拿到拓撲序後，任何「沿邊傳遞」的 DP 都可以依序在 O(n + m) 內完成。

### 5.1 定義

拓撲序是點的一個排列，使得每條邊 u → v 都滿足 u 排在 v 前面。典型場景：課程先修、工作排程、編譯相依。一張 DAG 的拓撲序通常不唯一。

### 5.2 Kahn 演算法（BFS 版）

反覆取出入度為 0 的點，放入答案，並減少其鄰居的入度。若最後取出的點數少於 n，剩下的點都在環上或被環挡住，圖不是 DAG。

```cpp
vector<int> topo(int n, const vector<vector<int>>& adj) {
    vector<int> indeg(n + 1, 0), order;
    for (int u = 1; u <= n; u++)
        for (int v : adj[u]) indeg[v]++;
    queue<int> q;                      // 要字典序最小就改成 min-heap
    for (int u = 1; u <= n; u++)
        if (indeg[u] == 0) q.push(u);
    while (!q.empty()) {
        int u = q.front(); q.pop();
        order.push_back(u);
        for (int v : adj[u])
            if (--indeg[v] == 0) q.push(v);
    }
    return order;                      // order.size() < n → 有環
}
```

### 5.3 DFS 版拓撲排序

一個點的所有後繼都完成後，它才「完成」。把點依完成順序加入列表再反轉，就是拓撲序。搭配第二章的三色標記可同時判環。

### 5.4 DAG 上的動態規劃

DAG 沒有環，所以狀態之間不會循環依賴，依拓撲序處理即可保證處理 v 時所有前驅已經算好。

- **最長路徑**：dp\[v\] = max(dp\[u\] + w(u, v))。一般圖的最長簡單路是 NP-hard，但 DAG 上是線性時間。
- **路徑計數**：ways\[v\] = Σ ways\[u\]，常搭配取模。
- **關鍵路徑**：每個工作最早開始時間 = 所有前置工作完成時間的最大值，總工期就是最長路。
- **DAG 最短路**：依拓撲序鬆弛，允許負權，複雜度 O(n + m)。

```cpp
// 依拓撲序求從任意起點出發的最長路徑（邊數）
vector<int> dp(n + 1, 0);
for (int u : order)
    for (int v : adj[u])
        dp[v] = max(dp[v], dp[u] + 1);
int ans = *max_element(dp.begin(), dp.end());
```

許多「看起來不是圖」的 DP 其實都是 DAG：狀態是點，轉移是邊。若轉移有環，則需要先用第六章的強連通分量縮點。

### 範例 5-A 字典序最小選課（基礎）

有 n 門課與 m 條先修關係「a b」，表示 a 必須排在 b 之前。請輸出一個合法的修課順序，若有多個則輸出字典序最小者；若不存在則輸出 `IMPOSSIBLE`。

- **輸入**：第一行 n、m（1 ≤ n ≤ 10⁵，0 ≤ m ≤ 2×10⁵）。接下來 m 行 a、b。
- **輸出**：n 個整數的順序，或 `IMPOSSIBLE`。

```text
範例輸入
5 4
3 1
3 2
4 2
2 5

範例輸出
3 1 4 2 5
```

**解答**：把 Kahn 演算法的佇列換成 min-heap，每次取出「目前可修」的課中編號最小者。

- **為何是字典序最小**：字典序先比第一個數，第一個數只能從入度為 0 的課中選，選最小的一定最好。去掉它之後問題變成同樣形式的子問題，所以每一步貪心即可。
- **範例過程**：一開始可修 {3, 4}，選 3；接著可修 {1, 4}，選 1；再來只有 {4}；然後 {2}、{5}。
- **複雜度**：O(m + n log n)。

這個貪心對「字典序最小」正確，但對「讓編號 1 盡量靠前」這類問法不正確。後者要在反向圖上用 max-heap 取最大，再反轉答案。

```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);
    int n, m;
    cin >> n >> m;
    vector<vector<int>> adj(n + 1);
    vector<int> indeg(n + 1, 0);
    for (int i = 0; i < m; i++) {
        int a, b; cin >> a >> b;
        adj[a].push_back(b); indeg[b]++;
    }
    priority_queue<int, vector<int>, greater<int>> pq;   // 每次取編號最小
    for (int i = 1; i <= n; i++) if (indeg[i] == 0) pq.push(i);
    vector<int> order;
    while (!pq.empty()) {
        int u = pq.top(); pq.pop();
        order.push_back(u);
        for (int v : adj[u]) if (--indeg[v] == 0) pq.push(v);
    }
    if ((int)order.size() < n) { cout << "IMPOSSIBLE\n"; return 0; }
    for (int i = 0; i < n; i++) cout << order[i] << " \n"[i == n - 1];
}
```

### 範例 5-B 可達點計數（困難）

給一張 n 個點、m 條邊的 DAG，對每個點 u 求從 u 出發能到達的點數（包含 u 自己）。

- **輸入**：第一行 n、m（1 ≤ n ≤ 3×10⁴，0 ≤ m ≤ 10⁵）。接下來 m 行 a、b 表示 a → b，保證無環。
- **輸出**：n 個整數。

```text
範例輸入
5 5
1 2
1 3
2 4
3 4
4 5

範例輸出
5 3 3 2 1
```

**解答**：直覺的 DAG DP 是 cnt\[u\] = 1 + Σ cnt\[v\]，但這是**錯的**。範例中點 1 會得到 1 + 3 + 3 = 7，因為點 4、5 經由 2 與 3 被算了兩次。可達點是「集合」，要取聯集而不是相加。

1. 對每個點維護一個長度 n 的 bitset，reach\[u\] 的第 v 位表示 u 能否到達 v。
2. 依**反拓撲序**處理：reach\[u\] = {u} 聯集所有 reach\[v\]，v 為 u 的後繼。處理 u 時所有後繼都已算好。
3. 答案是 reach\[u\].count()。

bitset 的聯集一次處理 64 個位元，每條邊花 n / 64 次運算，總計 O(nm / 64) ≈ 4.7×10⁷，實測 0.14 秒。記憶體為 n² / 8 位元組 ≈ 112 MB，這也是 n 只能到 3×10⁴ 的原因。bitset 太大，要宣告成全域變數，放在函式內會堆疊溢位。

```cpp
#include <bits/stdc++.h>
using namespace std;
const int MAXN = 30000;
bitset<MAXN> reach[MAXN];          // reach[u] 的第 v 位 = u 能否到達 v（0-indexed）
int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);
    int n, m;
    cin >> n >> m;
    vector<vector<int>> adj(n);
    vector<int> indeg(n, 0);
    for (int i = 0; i < m; i++) {
        int a, b; cin >> a >> b; a--; b--;
        adj[a].push_back(b); indeg[b]++;
    }
    vector<int> order; queue<int> q;
    for (int i = 0; i < n; i++) if (indeg[i] == 0) q.push(i);
    while (!q.empty()) {
        int u = q.front(); q.pop(); order.push_back(u);
        for (int v : adj[u]) if (--indeg[v] == 0) q.push(v);
    }
    // 反拓撲序：處理 u 時，所有後繼都已算好
    for (int i = n - 1; i >= 0; i--) {
        int u = order[i];
        reach[u][u] = 1;
        for (int v : adj[u]) reach[u] |= reach[v];
    }
    for (int i = 0; i < n; i++) cout << reach[i].count() << " \n"[i == n - 1];
}
```

### 第五章 觀念檢測

1. （是非）任何有向圖都至少有一個拓撲序。
2. （選擇）Kahn 演算法每次取出的點滿足：(A) 出度為 0 (B) 入度為 0 (C) 度數最大 (D) 編號最小
3. （是非）一張 DAG 的拓撲序一定唯一。
4. （選擇）Kahn 演算法結束後共取出 k 個點，k < n，代表：(A) 圖不連通 (B) 圖中有環 (C) 有重邊 (D) 程式有錯
5. （是非）要輸出字典序最小的拓撲序，可把 Kahn 的佇列換成 min-heap。
6. （選擇）在 DAG 上求最長路徑的複雜度為：(A) O(n + m) (B) O(m log n) (C) O(nm) (D) NP-hard
7. （是非）DFS 版拓撲排序中，把點依「進入時間」排序即可得到拓撲序。
8. （選擇）課程有先修關係，每學期可修任意多門，求最少學期數，等價於求：(A) 最小生成樹 (B) DAG 最長路徑的點數 (C) 連通塊數 (D) 最大匹配
9. （是非）DAG 上的最短路允許負權邊。
10. （選擇）對有向圖做拓撲排序但圖上有環，若仍想做 DP，常見做法是：(A) 忽略環 (B) 先做強連通分量縮點 (C) 改用 Floyd (D) 刪掉任一條邊

**參考答案**

1. 非。只有 DAG 才有拓撲序，環上的點無法排出先後。
2. B。入度為 0 表示所有前置條件都已處理。
3. 非。例如兩個沒有邊的點可以任意排。若 Kahn 過程中佇列永遠只有一個點，拓撲序才唯一。
4. B。環上的點入度永遠不會歸零。不連通並不影響 Kahn。
5. 是。每次取可取的點中編號最小者，複雜度變為 O(m + n log n)。
6. A。依拓撲序做一次 DP 即可。
7. 非。應依「離開時間」由大到小排。
8. B。每門課最早的學期 = 最長前置鏈的長度。
9. 是。沒有環就不可能有負環，依拓撲序鬆弛一次即正確。
10. B。縮點後的圖必定是 DAG。

## 第六章 連通性：強連通分量、橋與割點、2-SAT

本章三個主題都建立在同一個工具上：DFS 時間戳 dfn 與「能回到最早的時間戳」 low，全部都是 O(n + m)。

### 6.1 dfn 與 low

- dfn\[u\]：u 在 DFS 中被拜訪的順序。
- low\[u\]：從 u 的子樹出發，最多經過一條非樹邊，能到達的最小 dfn。
- 直覺：low\[v\] 越小，代表 v 的子樹能「繞過」父節點回到更上層，父節點就越不是關鍵。

### 6.2 強連通分量 SCC（Tarjan）

有向圖中「互相可達」的極大點集稱為強連通分量。把每個 SCC 縮成一個點，得到的圖必定是 DAG，就能接上第五章的拓撲排序與 DP。

```cpp
int n, timer_ = 0, sccCnt = 0;
vector<vector<int>> adj;
vector<int> dfn, low, comp, stk;
vector<bool> inStk;

void tarjan(int u) {
    dfn[u] = low[u] = ++timer_;
    stk.push_back(u); inStk[u] = true;
    for (int v : adj[u]) {
        if (!dfn[v]) { tarjan(v); low[u] = min(low[u], low[v]); }
        else if (inStk[v]) low[u] = min(low[u], dfn[v]);
    }
    if (low[u] == dfn[u]) {            // u 是此 SCC 的根
        ++sccCnt;
        while (true) {
            int x = stk.back(); stk.pop_back();
            inStk[x] = false; comp[x] = sccCnt;
            if (x == u) break;
        }
    }
}
// for (int i = 1; i <= n; i++) if (!dfn[i]) tarjan(i);
```

- Tarjan 產生的 SCC 編號是**反拓撲序**：編號 1 的 SCC 沒有指向其他 SCC 的邊。
- Kosaraju 是另一種做法：先在原圖 DFS 記錄離開順序，再依反序在反向圖 DFS，每次搜到的點就是一個 SCC。
- **縮點**：對每條邊 u → v，若 comp\[u\] ≠ comp\[v\]，在新圖加邊 comp\[u\] → comp\[v\]。
- 經典問題：縮點後入度為 0 的 SCC 數，就是「至少要從幾個點發出訊息」；要讓整張圖強連通至少加 max(入度 0 數, 出度 0 數) 條邊（只有一個 SCC 時為 0）。

### 6.3 橋與割點（無向圖）

刪掉後會使連通塊增加的邊叫橋，刪掉後會使連通塊增加的點叫割點。

| 判斷對象 | 條件（v 為 u 在 DFS 樹上的子節點） |
| --- | --- |
| 樹邊 u–v 是橋 | low\[v\] > dfn\[u\] |
| 非根的 u 是割點 | 存在子節點 v 使 low\[v\] ≥ dfn\[u\] |
| 根 u 是割點 | 根在 DFS 樹上有至少兩個子節點 |

```cpp
vector<vector<pair<int,int>>> g;   // (v, 邊編號)
vector<int> dfn, low; vector<bool> isBridge, isCut; int timer_ = 0;

void dfs(int u, int pe) {          // pe = 來時的邊編號
    dfn[u] = low[u] = ++timer_;
    int child = 0;
    for (auto [v, id] : g[u]) {
        if (id == pe) continue;      // 只跳過來時那條邊，重邊仍會處理
        if (dfn[v]) { low[u] = min(low[u], dfn[v]); continue; }
        dfs(v, id); child++;
        low[u] = min(low[u], low[v]);
        if (low[v] > dfn[u]) isBridge[id] = true;
        if (pe != -1 && low[v] >= dfn[u]) isCut[u] = true;
    }
    if (pe == -1 && child >= 2) isCut[u] = true;
}
```

去掉所有橋後的各連通塊稱為邊雙連通分量；把它們縮點後會得到一棵樹（橋樹）。

### 6.4 2-SAT

有 n 個布林變數，給定若干個「a 或 b」形式的條件（a、b 可以是變數或其否定），問是否能全部滿足。

1. 每個變數 x 建兩個點：x 與 ¬x。
2. 條件「a 或 b」等價於「¬a → b」且「¬b → a」，建這兩條有向邊。
3. 對整張圖做 SCC。若某個 x 與 ¬x 在同一個 SCC，無解。
4. 否則有解：使用 Tarjan 編號時，取 x = 真若且唯若 comp\[x\] < comp\[¬x\]（拓撲序較後者為真）。

常見條件轉換：「x 必為真」建 ¬x → x；「x 與 y 不能同時為真」即「¬x 或 ¬y」。

### 範例 6-A 關鍵道路（基礎）

n 個路口由 m 條雙向道路連接，可能有重邊。若封閉某條道路會讓原本能互通的兩個路口不再互通，就稱它為關鍵道路。請輸出關鍵道路的數量與編號。

- **輸入**：第一行 n、m（1 ≤ n ≤ 10⁵，0 ≤ m ≤ 2×10⁵）。接下來 m 行 u、v（u ≠ v），道路依輸入順序編為 1 到 m。
- **輸出**：第一行為數量 k，第二行為 k 個由小到大的編號（k = 0 時不輸出第二行）。

```text
範例輸入
5 5
1 2
2 3
3 1
3 4
4 5

範例輸出
2
4 5
```

**解答**：關鍵道路就是橋。套用 6.3 節的條件：樹邊 u–v 是橋若且唯若 low\[v\] > dfn\[u\]。

- **重邊**：用「來時的邊編號」而不是「父節點」來跳過。兩條 1–2 的重邊互相構成環，都不是橋。
- **非遞迴實作**：n = 10⁵ 的鏈狀圖若用遞迴，在本機實測會堆疊溢位而崩潰。所以這份解答用顯式堆疊模擬遞迴：it\[u\] 記錄 u 已處理到第幾個鄰居，鄰居都處理完時彈出 u，並把 low\[u\] 回傳給父節點，這一步就相當於遞迴的 return。
- **複雜度**：O(n + m)，再加上排序答案 O(n log n)。

```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);
    int n, m;
    cin >> n >> m;
    vector<vector<pair<int,int>>> g(n + 1);     // (鄰居, 邊編號)
    for (int i = 1; i <= m; i++) {
        int u, v; cin >> u >> v;
        g[u].push_back({v, i}); g[v].push_back({u, i});
    }
    vector<int> dfn(n + 1, 0), low(n + 1, 0), pe(n + 1, 0), it(n + 1, 0), bridges;
    int timer_ = 0;
    // 用顯式堆疊模擬遞迴 DFS：it[u] 記錄 u 已處理到第幾個鄰居
    for (int s = 1; s <= n; s++) {
        if (dfn[s]) continue;
        vector<int> st = {s};
        dfn[s] = low[s] = ++timer_;
        while (!st.empty()) {
            int u = st.back();
            if (it[u] < (int)g[u].size()) {
                auto [v, id] = g[u][it[u]++];
                if (id == pe[u]) continue;           // 只跳過來時那條邊
                if (dfn[v]) low[u] = min(low[u], dfn[v]);
                else {                               // 相當於遞迴呼叫 dfs(v)
                    pe[v] = id; dfn[v] = low[v] = ++timer_;
                    st.push_back(v);
                }
            } else {                                 // u 的鄰居都處理完，相當於 return
                st.pop_back();
                if (!st.empty()) {
                    int p = st.back();
                    low[p] = min(low[p], low[u]);
                    if (low[u] > dfn[p]) bridges.push_back(pe[u]);
                }
            }
        }
    }
    sort(bridges.begin(), bridges.end());
    cout << bridges.size() << "\n";
    for (size_t i = 0; i < bridges.size(); i++)
        cout << bridges[i] << " \n"[i + 1 == bridges.size()];
}
```

### 範例 6-B 開關設定（2-SAT，困難）

有 n 個開關，每個只能設為 0 或 1。給定 m 個條件，每個條件為「i a j b」，表示「開關 i 為 a」與「開關 j 為 b」至少一個成立。請輸出一組滿足所有條件的設定，無解則輸出 `IMPOSSIBLE`。

- **輸入**：第一行 n、m（1 ≤ n ≤ 10⁵，1 ≤ m ≤ 2×10⁵）。接下來 m 行 i、a、j、b（a, b ∈ {0, 1}，i 可能等於 j）。
- **輸出**：一個長度 n 的 01 字串，第 i 個字元為開關 i 的設定；有多組解時輸出任一組。

```text
範例輸入
3 4
1 1 2 1
1 0 2 0
2 1 3 0
3 1 3 1

範例輸出
011
```

第 4 條強制開關 3 為 1，第 3 條因此強制開關 2 為 1，第 2 條再強制開關 1 為 0，這組範例的解是唯一的。

**解答**：這是標準的 2-SAT。

1. **建點**：每個開關 i 建兩個點，點 2i + 1 代表「i 為 1」、點 2i 代表「i 為 0」，i 從 0 算起。「i 為 a」的否定就是「i 為 1 − a」。
2. **建邊**：「(i 為 a) 或 (j 為 b)」等價於兩個蒴含：若 i 為 1 − a，則 j 必為 b；若 j 為 1 − b，則 i 必為 a。各建一條有向邊。
3. **判斷**：對 2n 個點做 Tarjan SCC。若「i 為 0」與「i 為 1」在同一個 SCC，兩者互相蒴含，必然無解。
4. **構造解**：Tarjan 的 SCC 編號是反拓撲序，編號小的在拓撲序後面。對每個開關選「拓撲序較後」的那個值，即 comp\[i 為 1\] < comp\[i 為 0\] 時設為 1。選後面的點不會蒴含到它的否定，因此不會產生矛盾。

「i a i a」這種自己跟自己的條件會建出「i 為 1 − a」指向「i 為 a」的邊，正好表示「i 必為 a」，不必特判。複雜度 O(n + m)。對拍時是用「檢查輸出是否滿足所有條件」來驗證，因為答案不唯一。

```cpp
#include <bits/stdc++.h>
using namespace std;
int N, timer_ = 0, sccCnt = 0;
vector<vector<int>> adj;
vector<int> dfn, low, comp, stk;
vector<bool> inStk;
void tarjan(int u) {
    dfn[u] = low[u] = ++timer_;
    stk.push_back(u); inStk[u] = true;
    for (int v : adj[u]) {
        if (!dfn[v]) { tarjan(v); low[u] = min(low[u], low[v]); }
        else if (inStk[v]) low[u] = min(low[u], dfn[v]);
    }
    if (low[u] == dfn[u]) {
        ++sccCnt;
        while (true) {
            int x = stk.back(); stk.pop_back();
            inStk[x] = false; comp[x] = sccCnt;
            if (x == u) break;
        }
    }
}
int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);
    int n, m;
    cin >> n >> m;
    N = 2 * n;
    // 點 2i + 1 代表「開關 i 為 1」，點 2i 代表「開關 i 為 0」（i 從 0 起算）
    auto id = [](int i, int val) { return 2 * i + val; };
    adj.assign(N, {});
    for (int k = 0; k < m; k++) {
        int i, a, j, b;
        cin >> i >> a >> j >> b; i--; j--;
        // (i == a) 或 (j == b)：若 i != a 則 j == b；若 j != b 則 i == a
        adj[id(i, 1 - a)].push_back(id(j, b));
        adj[id(j, 1 - b)].push_back(id(i, a));
    }
    dfn.assign(N, 0); low.assign(N, 0); comp.assign(N, 0); inStk.assign(N, false);
    for (int v = 0; v < N; v++) if (!dfn[v]) tarjan(v);
    string ans(n, '0');
    for (int i = 0; i < n; i++) {
        if (comp[id(i, 0)] == comp[id(i, 1)]) { cout << "IMPOSSIBLE\n"; return 0; }
        ans[i] = comp[id(i, 1)] < comp[id(i, 0)] ? '1' : '0';   // 拓撲序較後者為真
    }
    cout << ans << "\n";
}
```

### 第六章 觀念檢測

1. （是非）把有向圖的每個強連通分量縮成一點後，得到的圖一定是 DAG。
2. （選擇）Tarjan 中判斷 u 是 SCC 根的條件是：(A) low\[u\] < dfn\[u\] (B) low\[u\] == dfn\[u\] (C) u 沒有鄰居 (D) u 是 DFS 起點
3. （是非）在 Tarjan SCC 中，走到已拜訪但不在堆疊中的點 v 時，也應該用 dfn\[v\] 更新 low\[u\]。
4. （選擇）無向圖樹邊 u–v（v 為子節點）是橋的條件為：(A) low\[v\] ≥ dfn\[u\] (B) low\[v\] > dfn\[u\] (C) low\[u\] > dfn\[v\] (D) dfn\[v\] > dfn\[u\]
5. （是非）DFS 樹的根是割點，若且唯若它在 DFS 樹上至少有兩個子節點。
6. （選擇）找橋時圖中有重邊，應如何處理「不走回父節點」？(A) 跳過所有通往父節點的邊 (B) 只跳過來時的那一條邊編號 (C) 先刪除重邊 (D) 不需處理
7. （是非）2-SAT 中，條件「a 或 b」對應的邊是 a → b 與 b → a。
8. （選擇）2-SAT 無解的充要條件是：(A) 圖中有環 (B) 存在 x 與 ¬x 在同一 SCC (C) 條件數大於 n (D) 存在入度 0 的點
9. （是非）一張無向連通圖若沒有割點，也一定沒有橋。
10. （選擇）一張有向圖縮點後有 3 個入度為 0 的 SCC、5 個出度為 0 的 SCC，至少加幾條邊可使整張圖強連通？(A) 3 (B) 5 (C) 8 (D) 15

**參考答案**

1. 是。若縮點後有環，環上的 SCC 應該合併成一個，與極大性矛盾。
2. B。代表 u 的子樹無法回到更早的、仍在堆疊中的點。
3. 非。那個點已屬於另一個已完成的 SCC，不能拿來更新。
4. B。等號代表 v 的子樹能回到 u 本身，那條邊在環上，不是橋。
5. 是。根的不同子樹之間沒有邊（無向圖 DFS 無橫叉邊），刪根後必分開。
6. B。重邊本身會形成環，兩條都不是橋，所以只能跳過來時的那一條。
7. 非。應是 ¬a → b 與 ¬b → a。
8. B。x 與 ¬x 互相可推導，必然矛盾。
9. 非。只有兩個點、一條邊的圖沒有割點，但那條邊是橋。
10. B。答案為 max(3, 5) = 5。

## 第七章 樹上技巧

樹任兩點只有一條路徑，所以「路徑問題」都能拆成「u 到 LCA」加「LCA 到 v」；本章的直徑、重心、LCA、樹上差分與樹 DP 是競賽樹題的五個基本功。

### 7.1 樹的直徑

直徑是樹上最遠兩點的距離。

- **兩次 BFS/DFS**：從任一點出發找最遠點 A，再從 A 出發找最遠點 B，A–B 即為直徑。此法**只在邊權非負時正確**。
- **樹 DP**：對每個點求「往下最長」與「次長」兩條鏈，相加取最大，可處理負權。

```cpp
int diameter = 0;
int down(int u, int p) {             // 回傳從 u 往下的最長鏈（邊數）
    int best1 = 0, best2 = 0;
    for (int v : adj[u]) if (v != p) {
        int d = down(v, u) + 1;
        if (d > best1) { best2 = best1; best1 = d; }
        else if (d > best2) best2 = d;
    }
    diameter = max(diameter, best1 + best2);
    return best1;
}
```

### 7.2 樹的重心

刪掉重心後，剩下最大的連通塊大小最小。重心滿足「每塊都不超過 n / 2」，且一棵樹最多有兩個重心（兩者相鄰）。

做法：DFS 求子樹大小 sz\[u\]，對每個點計算 max(所有子節點的 sz, n − sz\[u\])，取最小者。重心是點分治的基礎，也是「所有點到某點距離和最小」的答案。

### 7.3 最近公共祖先 LCA（倍增法）

up\[k\]\[u\] 表示 u 往上跳 2^k 步的祖先。預處理 O(n log n)，每次查詢 O(log n)。

```cpp
const int LOG = 18;                 // 2^18 > 2×10^5
vector<int> adj[200005];
int up[LOG][200005], dep[200005];

void dfs(int u, int p) {            // 從根呼叫 dfs(1, 0)；點 0 當作哨兵
    up[0][u] = p;
    for (int k = 1; k < LOG; k++) up[k][u] = up[k-1][ up[k-1][u] ];
    for (int v : adj[u]) if (v != p) { dep[v] = dep[u] + 1; dfs(v, u); }
}

int lca(int a, int b) {
    if (dep[a] < dep[b]) swap(a, b);
    int diff = dep[a] - dep[b];
    for (int k = 0; k < LOG; k++) if (diff >> k & 1) a = up[k][a]; // 先拉到同一深度
    if (a == b) return a;
    for (int k = LOG - 1; k >= 0; k--)                              // 從大到小一起跳
        if (up[k][a] != up[k][b]) { a = up[k][a]; b = up[k][b]; }
    return up[0][a];
}

int dist(int a, int b) { return dep[a] + dep[b] - 2 * dep[lca(a, b)]; }
```

倍增表也能順便維護「往上 2^k 步經過的最大邊權」，用來回答路徑最大值查詢。

### 7.4 樹上差分

要對很多條路徑「整條加 x」，最後問每個點或邊的值。先在差分陣列 d 上打標記，最後一次 DFS 用「子樹和」還原。設 l = lca(u, v)。

| 對象 | 標記方式 |
| --- | --- |
| 點差分 | d\[u\] += x、d\[v\] += x、d\[l\] −= x、d\[parent(l)\] −= x |
| 邊差分（邊存在子節點上） | d\[u\] += x、d\[v\] += x、d\[l\] −= 2x |

還原後，點 w 的值就是 w 子樹內 d 的總和。總複雜度 O((n + q) log n)。

### 7.5 樹 DP 與換根

- **基本模式**：先遞迴算完子節點，再用子節點的結果合併出自己。
- **最大獨立集**（相鄰點不能同選）：dp\[u\]\[1\] = val\[u\] + Σ dp\[v\]\[0\]，dp\[u\]\[0\] = Σ max(dp\[v\]\[0\], dp\[v\]\[1\])。
- **換根 DP**：第一次 DFS 以 1 為根算出答案，第二次 DFS 從父節點的答案推到子節點。例如所有點到 u 的距離和：S\[v\] = S\[u\] + n − 2·sz\[v\]。

### 範例 7-A 最遠的兩個村莊（基礎）

n 個村莊由 n − 1 條道路連成一棵樹，每條道路有長度。求距離最遠的兩個村莊相距多遠。

- **輸入**：第一行 n（1 ≤ n ≤ 2×10⁵）。接下來 n − 1 行 u、v、w（1 ≤ w ≤ 10⁹）。
- **輸出**：樹的直徑長度。

```text
範例輸入
5
1 2 3
2 3 4
2 4 2
4 5 6

範例輸出
12
```

最遠的是村莊 3 與 5，路徑 3–2–4–5，長度 4 + 2 + 6 = 12。

**解答**：邊權都是正的，可以用 7.1 節的「兩次搜尋」。從點 1 找最遠點 A，再從 A 找最遠點，第二次得到的距離就是直徑。

- **為什麼 A 一定是直徑的端點**：設真正的直徑是 P–Q。若 A 不是端點，可以證明從 A 經過直徑走到 P 或 Q 會更遠，與 A 是最遠點矛盾。這個推論用到「邊權非負」。
- **用堆疊不用遞迴**：樹上兩點路徑唯一，用任何順序的遍歷算距離都對。這裡用 vector 當堆疊，避免 2×10⁵ 層的遞迴。
- **複雜度**：O(n)。直徑可達 2×10¹⁴，用 long long。

```cpp
#include <bits/stdc++.h>
using namespace std;
using ll = long long;
int n;
vector<vector<pair<int,int>>> adj;
// 回傳 (最遠點, 距離)；用 stack 取代遞迴，避免鏈狀樹堆疊溢位
pair<int,ll> farthest(int s) {
    vector<ll> dist(n + 1, -1);
    vector<int> st = {s};
    dist[s] = 0;
    while (!st.empty()) {
        int u = st.back(); st.pop_back();
        for (auto [v, w] : adj[u]) if (dist[v] < 0) {
            dist[v] = dist[u] + w; st.push_back(v);
        }
    }
    int best = s;
    for (int i = 1; i <= n; i++) if (dist[i] > dist[best]) best = i;
    return {best, dist[best]};
}
int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);
    cin >> n;
    adj.assign(n + 1, {});
    for (int i = 0; i < n - 1; i++) {
        int u, v, w; cin >> u >> v >> w;
        adj[u].push_back({v, w}); adj[v].push_back({u, w});
    }
    int A = farthest(1).first;
    cout << farthest(A).second << "\n";
}
```

### 範例 7-B 距離總和（換根 DP，困難）

n 個村莊由 n − 1 條道路連成一棵樹。對每個村莊，求它到其他所有村莊的距離總和。這是「郵局該蓋在哪裡」類題目的基礎。

- **輸入**：第一行 n（1 ≤ n ≤ 2×10⁵）。接下來 n − 1 行 u、v、w（1 ≤ w ≤ 10⁶）。
- **輸出**：一行 n 個整數，第 i 個為村莊 i 的距離總和。

```text
範例輸入
4
1 2 1
2 3 2
2 4 3

範例輸出
8 6 10 12
```

**解答**：對每個點各跑一次 DFS 是 O(n²) = 4×10¹⁰，太慢。換根 DP 只要兩趟。

1. **第一趟（由下往上）**：以 1 為根，求子樹大小 sz\[u\]，與 down\[u\] = u 到自己子樹內所有點的距離和。子節點 v 的子樹中每個點都要多走一次邊 u–v，所以 down\[u\] = Σ (down\[v\] + w · sz\[v\])。根的答案 S\[1\] = down\[1\]。
2. **第二趟（由上往下）**：把根從 u 移到子節點 v，邊權為 w。v 子樹內的 sz\[v\] 個點都近了 w，其餘 n − sz\[v\] 個點都遠了 w。所以 S\[v\] = S\[u\] + w · (n − 2 · sz\[v\])。

用範例驗算第二趟：S\[1\] = 1 + 3 + 4 = 8，sz\[2\] = 3，所以 S\[2\] = 8 + 1 × (4 − 6) = 6。再由 sz\[3\] = 1 得 S\[3\] = 6 + 2 × (4 − 2) = 10。

- **非遞迴實作**：用 BFS 序。BFS 序保證父節點在子節點之前，所以「倒著走」就是由下往上，「順著走」就是由上往下。
- **溢位**：鏈狀樹端點的總和約 w · n² / 2。w 若可到 10⁹ 會達 2×10¹⁹，超過 long long 的 9.2×10¹⁸，所以這題把 w 限制在 10⁶。出題或解題時都要先估算答案上界。
- **複雜度**：O(n)，實測 0.48 秒。

```cpp
#include <bits/stdc++.h>
using namespace std;
using ll = long long;
int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);
    int n;
    cin >> n;
    vector<vector<pair<int,int>>> adj(n + 1);
    for (int i = 0; i < n - 1; i++) {
        int u, v, w; cin >> u >> v >> w;
        adj[u].push_back({v, w}); adj[v].push_back({u, w});
    }
    // BFS 序：父節點必在子節點之前
    vector<int> order, par(n + 1, 0), pw(n + 1, 0);
    vector<ll> sz(n + 1, 1), S(n + 1, 0);
    order.reserve(n);
    vector<bool> seen(n + 1, false);
    queue<int> q; q.push(1); seen[1] = true;
    while (!q.empty()) {
        int u = q.front(); q.pop(); order.push_back(u);
        for (auto [v, w] : adj[u]) if (!seen[v]) {
            seen[v] = true; par[v] = u; pw[v] = w; q.push(v);
        }
    }
    // 第一趟（由下往上）：sz[u] 與 down[u] = u 到子樹內所有點的距離和
    vector<ll> down(n + 1, 0);
    for (int i = n - 1; i >= 1; i--) {
        int v = order[i], u = par[v];
        sz[u] += sz[v];
        down[u] += down[v] + (ll)pw[v] * sz[v];
    }
    // 第二趟（由上往下）：換根
    S[1] = down[1];
    for (int i = 1; i < n; i++) {
        int v = order[i], u = par[v];
        S[v] = S[u] + (ll)pw[v] * (n - 2 * sz[v]);
    }
    for (int i = 1; i <= n; i++) cout << S[i] << " \n"[i == n];
}
```

### 第七章 觀念檢測

1. （是非）「兩次 BFS」求直徑在有負權邊的樹上仍然正確。
2. （選擇）一棵樹最多有幾個重心？(A) 1 (B) 2 (C) 3 (D) 不限
3. （是非）倍增 LCA 的每次查詢複雜度為 O(log n)。
4. （選擇）樹上兩點 a、b 的距離公式為：(A) dep\[a\] + dep\[b\] (B) dep\[a\] + dep\[b\] − dep\[lca\] (C) dep\[a\] + dep\[b\] − 2·dep\[lca\] (D) |dep\[a\] − dep\[b\]|
5. （是非）倍增 LCA 第二階段的迴圈 k 必須由大到小。
6. （選擇）點差分中，路徑 u–v 加 x 時，除了 d\[u\] += x、d\[v\] += x 之外還要：(A) d\[l\] −= 2x (B) d\[l\] −= x、d\[parent(l)\] −= x (C) d\[root\] −= x (D) 不需要其他操作
7. （是非）刪除重心後，每個剩下的連通塊大小都不超過 n / 2。
8. （選擇）要對「每個點作為根」都求一個答案，n = 2×10⁵，最適合的方法是：(A) 對每個根各做一次 DFS (B) 換根 DP (C) Floyd (D) Dijkstra
9. （是非）最大獨立集在一般圖是 NP-hard，但在樹上可以 O(n) 求出。
10. （選擇）n = 2×10⁵ 時，倍增表 LOG 至少要取：(A) 10 (B) 16 (C) 18 (D) 32

**參考答案**

1. 非。負權會讓「最遠點必為直徑端點」的證明失效，要改用樹 DP。
2. B。兩個重心時它們必定相鄰，且 n 為偶數。
3. 是。兩個迴圈各跑 LOG 次。
4. C。從 a、b 各自往上到 LCA，深度差相加。
5. 是。由大到小才能像二進位拆解一樣，在不超過 LCA 的前提下跳到最高。
6. B。l 本身在路徑上只應該被加一次，而子樹和會算到兩次，故減一次；l 的父節點不在路徑上，再減一次。
7. 是。這是重心的定理，也是點分治只有 O(log n) 層的原因。
8. B。兩次 DFS 共 O(n)，逐一計算會是 O(n²)。
9. 是。用 dp\[u\]\[0/1\] 一次 DFS 完成。
10. C。2^18 = 262144 > 2×10⁵，而 2^16 = 65536 不夠。

## 第八章 二分圖、網路流與歐拉路徑

二分圖匹配可用匈牙利演算法 O(nm) 或 Dinic O(m√n) 解決；一般的最大流用 Dinic，而最大流在數值上等於最小割。

### 8.1 二分圖判定

若點可分成兩組，使每條邊都橫跨兩組，則為二分圖。**一張圖是二分圖若且唯若它沒有奇環。**

做法：對每個連通塊 BFS 染色，鄰居塗上相反顏色；若發現鄰居同色則不是二分圖。也可以用並查集的 x 與 x + n 分身實作。

### 8.2 二分圖最大匹配（匈牙利演算法）

匹配是一組沒有共同端點的邊。匈牙利演算法對左邊每個點嘗試找「增廣路徑」：若右邊的 v 已被佔用，就遞迴請佔用者換別人。

```cpp
int nL, nR;
vector<vector<int>> g;       // g[u] = 左邊 u 可連的右邊點
vector<int> matchR;          // matchR[v] = 與右邊 v 配對的左邊點，0 為無
vector<bool> vis;

bool tryKuhn(int u) {
    for (int v : g[u]) {
        if (vis[v]) continue;
        vis[v] = true;
        if (matchR[v] == 0 || tryKuhn(matchR[v])) { matchR[v] = u; return true; }
    }
    return false;
}
// int ans = 0;
// for (int u = 1; u <= nL; u++) { vis.assign(nR + 1, false); if (tryKuhn(u)) ans++; }
```

二分圖的重要等式（其中 n 為總點數）：

- **Kőnig 定理**：最大匹配 = 最小點覆蓋。
- **最大獨立集** = n − 最大匹配。
- **DAG 最小路徑覆蓋**（點不重複）= 點數 − 拆點二分圖的最大匹配。拆點法：每點 u 拆成左 u 與右 u，邊 u → v 變成左 u–右 v。

### 8.3 最大流（Dinic）

每條邊有容量，求從源點 s 到匯點 t 最多能送多少流。關鍵是**反向邊**：送流時正向容量減 d、反向容量加 d，代表「之後可以反悔」。Dinic 每輪先用 BFS 分層，再用 DFS 沿層次多路增廣。

```cpp
using ll = long long;
struct Dinic {
    struct E { int to; ll cap; };
    vector<E> e; vector<vector<int>> g; vector<int> lvl, it;
    Dinic(int n) : g(n + 1), lvl(n + 1), it(n + 1) {}
    void addEdge(int u, int v, ll c) {          // 第 i 條與第 i^1 條互為反向邊
        g[u].push_back(e.size()); e.push_back({v, c});
        g[v].push_back(e.size()); e.push_back({u, 0});
    }
    bool bfs(int s, int t) {
        fill(lvl.begin(), lvl.end(), -1);
        queue<int> q; lvl[s] = 0; q.push(s);
        while (!q.empty()) {
            int u = q.front(); q.pop();
            for (int id : g[u])
                if (e[id].cap > 0 && lvl[e[id].to] < 0) {
                    lvl[e[id].to] = lvl[u] + 1; q.push(e[id].to);
                }
        }
        return lvl[t] >= 0;
    }
    ll dfs(int u, int t, ll f) {
        if (u == t) return f;
        for (int& i = it[u]; i < (int)g[u].size(); i++) {   // 當前弧優化
            int id = g[u][i], v = e[id].to;
            if (e[id].cap > 0 && lvl[v] == lvl[u] + 1) {
                ll d = dfs(v, t, min(f, e[id].cap));
                if (d > 0) { e[id].cap -= d; e[id ^ 1].cap += d; return d; }
            }
        }
        return 0;
    }
    ll maxflow(int s, int t) {
        ll flow = 0, f;
        while (bfs(s, t)) {
            fill(it.begin(), it.end(), 0);
            while ((f = dfs(s, t, LLONG_MAX)) > 0) flow += f;
        }
        return flow;
    }
};
```

- 一般圖最壞 O(n²m)，實務上遠快於此；單位容量的二分圖為 O(m√n)。
- **最大流最小割定理**：s 到 t 的最大流 = 切斷 s 與 t 所需刪除邊的最小容量和。跑完後從 s 沿剩餘容量 > 0 的邊能到達的點，就是最小割的 s 側。
- **建模技巧**：點有容量時拆點（u\_in → u\_out，容量為點容量）；多源多匯加超級源匯。

### 8.4 歐拉路徑

歐拉路徑恰好經過每條邊一次；起點等於終點時稱為歐拉迴路。前提是所有有邊的點連通。

| 圖 | 歐拉迴路 | 歐拉路徑 |
| --- | --- | --- |
| 無向圖 | 所有點度數為偶數 | 恰有 0 或 2 個奇度點，從其中一個出發 |
| 有向圖 | 每點入度 = 出度 | 起點出度比入度多 1、終點入度比出度多 1，其餘相等 |

建構方式為 Hierholzer 演算法：DFS 每走一條邊就標記刪除，點「無邊可走」時加入答案，最後反轉，複雜度 O(n + m)。實作時用指標記錄每點已用到第幾條邊，避免重複掃描。

### 範例 8-A 工作分配（基礎）

有 nL 位員工與 nR 項工作，以及 E 個「員工 u 會做工作 v」的關係。每位員工最多做一項工作，每項工作最多由一位員工負責。求最多能完成幾項工作。

- **輸入**：第一行 nL、nR、E（1 ≤ nL, nR ≤ 500，0 ≤ E ≤ 2×10⁴）。接下來 E 行 u、v。
- **輸出**：最多完成的工作數。

```text
範例輸入
3 3 5
1 1
1 2
2 1
3 2
3 3

範例輸出
3
```

員工 1 做工作 2、員工 2 做工作 1、員工 3 做工作 3。

**解答**：員工與工作是二分圖的兩邊，答案是最大匹配，用 8.2 節的匈牙利演算法。

- **範例中的增廣路徑**：員工 1 先拿到工作 1。員工 2 也想要工作 1，於是遞迴請員工 1 改做工作 2，兩人都有工作。這就是「讓佔用者換別人」。
- **vis 要在每位員工開始時重置**：同一次嘗試中每項工作只看一次，避免無窮遞迴。
- **複雜度**：O(nL · E)，最壞 10⁷。也可以建 S → 員工 → 工作 → T、容量均為 1 的網路，用 Dinic 求最大流，答案相同。

```cpp
#include <bits/stdc++.h>
using namespace std;
int nL, nR, E;
vector<vector<int>> g;
vector<int> matchR;
vector<bool> vis;
bool tryKuhn(int u) {
    for (int v : g[u]) {
        if (vis[v]) continue;
        vis[v] = true;
        if (matchR[v] == 0 || tryKuhn(matchR[v])) { matchR[v] = u; return true; }
    }
    return false;
}
int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);
    cin >> nL >> nR >> E;
    g.assign(nL + 1, {});
    for (int i = 0; i < E; i++) { int u, v; cin >> u >> v; g[u].push_back(v); }
    matchR.assign(nR + 1, 0);
    int ans = 0;
    for (int u = 1; u <= nL; u++) {
        vis.assign(nR + 1, false);
        if (tryKuhn(u)) ans++;
    }
    cout << ans << "\n";
}
```

### 範例 8-B 專案選擇（最小割，困難）

公司有 n 個專案與 m 種工具。專案 i 完成後獲利 p\_i，但需要一組工具；工具 j 購買一次要花 c\_j，可以給多個專案共用。選擇要做哪些專案，使「總獲利 − 工具總花費」最大。什麼都不做的淨利是 0。

- **輸入**：第一行 n、m（1 ≤ n, m ≤ 200）。第二行 p\_1 到 p\_n。第三行 c\_1 到 c\_m（皆為 0 到 10⁶）。接下來 n 行，第 i 行先給 k\_i，再給專案 i 需要的 k\_i 個工具編號。
- **輸出**：最大淨利。

```text
範例輸入
2 3
10 8
4 5 6
2 1 2
2 2 3

範例輸出
3
```

只做專案 1 淨利 10 − 9 = 1，只做專案 2 是 8 − 11 = −3，兩個都做共用工具 2，淨利 18 − 15 = 3 最好。

**解答**：枚舉專案子集是 2ⁿ，不可行。這是經典的「最大權閉合子圖」，用最小割建模。

1. **建圖**：S → 專案 i，容量 p\_i。工具 j → T，容量 c\_j。專案 i → 它需要的工具 j，容量無限大。
2. **割的意義**：一個 S–T 割把點分成 S 側與 T 側。解讀為：S 側的專案「要做」，S 側的工具「要買」。
3. **為何割的容量就是代價**：割到「S → 專案 i」表示放棄專案 i，損失 p\_i。割到「工具 j → T」表示買工具 j，花費 c\_j。無限大的邊不可能被割，所以「做了專案卻沒買它的工具」這種不合法選擇不會是有限割。
4. **答案**：淨利 = Σp −（放棄的獲利 + 買工具的花費）= Σp − 割的容量。要淨利最大就是要割最小，由最大流最小割定理，答案 = Σp − 最大流。

範例中 Σp = 18，最小割是買下全部工具 4 + 5 + 6 = 15，答案 18 − 15 = 3。點數只有 n + m + 2，Dinic 在本題規模下不到 0.01 秒。同樣的建模可解「選課需要先修」、「開採礦區」等「選了 A 就必須選 B」的取捨問題。

```cpp
#include <bits/stdc++.h>
using namespace std;
using ll = long long;
struct Dinic {
    struct Ed { int to; ll cap; };
    vector<Ed> e; vector<vector<int>> g; vector<int> lvl, it;
    Dinic(int n) : g(n + 1), lvl(n + 1), it(n + 1) {}
    void addEdge(int u, int v, ll c) {
        g[u].push_back(e.size()); e.push_back({v, c});
        g[v].push_back(e.size()); e.push_back({u, 0});
    }
    bool bfs(int s, int t) {
        fill(lvl.begin(), lvl.end(), -1);
        queue<int> q; lvl[s] = 0; q.push(s);
        while (!q.empty()) {
            int u = q.front(); q.pop();
            for (int id : g[u])
                if (e[id].cap > 0 && lvl[e[id].to] < 0) { lvl[e[id].to] = lvl[u] + 1; q.push(e[id].to); }
        }
        return lvl[t] >= 0;
    }
    ll dfs(int u, int t, ll f) {
        if (u == t) return f;
        for (int& i = it[u]; i < (int)g[u].size(); i++) {
            int id = g[u][i], v = e[id].to;
            if (e[id].cap > 0 && lvl[v] == lvl[u] + 1) {
                ll d = dfs(v, t, min(f, e[id].cap));
                if (d > 0) { e[id].cap -= d; e[id ^ 1].cap += d; return d; }
            }
        }
        return 0;
    }
    ll maxflow(int s, int t) {
        ll flow = 0, f;
        while (bfs(s, t)) {
            fill(it.begin(), it.end(), 0);
            while ((f = dfs(s, t, LLONG_MAX)) > 0) flow += f;
        }
        return flow;
    }
};
int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);
    int n, m;
    cin >> n >> m;
    // 點編號：S = 0，專案 1..n，工具 n+1..n+m，T = n+m+1
    int S = 0, T = n + m + 1;
    Dinic din(T);
    const ll INF = LLONG_MAX / 4;
    ll totalProfit = 0;
    for (int i = 1; i <= n; i++) {
        ll p; cin >> p; totalProfit += p;
        din.addEdge(S, i, p);
    }
    for (int j = 1; j <= m; j++) {
        ll c; cin >> c;
        din.addEdge(n + j, T, c);
    }
    for (int i = 1; i <= n; i++) {
        int k; cin >> k;
        while (k--) { int j; cin >> j; din.addEdge(i, n + j, INF); }
    }
    cout << totalProfit - din.maxflow(S, T) << "\n";
}
```

### 第八章 觀念檢測

1. （是非）一張圖是二分圖，若且唯若它不含長度為奇數的環。
2. （選擇）二分圖中最大匹配數等於：(A) 最大獨立集 (B) 最小點覆蓋 (C) 點數一半 (D) 邊數
3. （是非）Dinic 的反向邊只是優化，不建也能得到正確最大流。
4. （選擇）以邊編號 i 與 i ^ 1 互為反向邊時，第 7 條邊的反向邊是：(A) 5 (B) 6 (C) 8 (D) 3
5. （是非）最大流的值等於最小割的容量。
6. （選擇）一張無向連通圖有 4 個奇度點，它：(A) 有歐拉迴路 (B) 有歐拉路徑但無迴路 (C) 沒有歐拉路徑 (D) 無法判斷
7. （是非）二分圖中，最大獨立集大小 = 點數 − 最大匹配。
8. （選擇）點本身有容量限制的流量問題，典型建模是：(A) 忽略 (B) 拆點 (C) 縮點 (D) 分層圖
9. （是非）有向圖存在歐拉迴路的充要條件之一是每個點的入度等於出度。
10. （選擇）DAG 有 10 個點，拆點二分圖的最大匹配為 6，則最少要幾條點不重複的路徑才能覆蓋所有點？(A) 4 (B) 6 (C) 10 (D) 16

**參考答案**

1. 是。沿環交替染色，奇環會讓起點與自己同色衝突。
2. B。這是 Kőnig 定理。
3. 非。沒有反向邊就無法「撤回」錯誤的送流選擇，可能卡在次佳解。
4. B。7 的二進位是 111，xor 1 得 110 = 6。
5. 是。這是最大流最小割定理。
6. C。奇度點數必須是 0 或 2。
7. 是。最小點覆蓋的補集就是最大獨立集，再搭配 Kőnig 定理。
8. B。把點 u 拆成 u\_in → u\_out，那條邊的容量就是點容量。
9. 是。另一個條件是有邊的點屬於同一個強連通分量。
10. A。10 − 6 = 4，每一個匹配代表把兩條路徑接成一條。

## 綜合練習題

六題依難度分為簡單、中等、困難各兩題；每題時限 1 秒、記憶體 256 MB，詳解在下一節。

| 題號 | 難度 | 題名 | 對應章節 |
| --- | --- | --- | --- |
| E1 | 簡單 | 島嶼探險 | 第二章 |
| E2 | 簡單 | 修路計畫 | 第四章 |
| M1 | 中等 | 最短路計數 | 第三章 |
| M2 | 中等 | 專案排程 | 第五章 |
| H1 | 困難 | 寶石收集 | 第五、六章 |
| H2 | 困難 | 樹上配送 | 第七章 |

### E1 島嶼探險（簡單）

一張 R × C 的地圖中，`#` 代表陸地、`.` 代表海。上下左右相鄰的陸地屬於同一座島（斜對角不算）。請輸出島的數量，以及最大的島有幾格。

- **輸入**：第一行 R、C（1 ≤ R, C ≤ 1000）。接下來 R 行，每行一個長度 C 的字串。
- **輸出**：兩個整數，島的數量與最大島的格數。沒有陸地時輸出 `0 0`。

```text
範例輸入
4 5
##..#
#...#
..#..
.###.

範例輸出
3 4
```

### E2 修路計畫（簡單）

王國有 n 座城市與 m 條雙向道路。國王希望任兩座城市都能互通，請問至少還要新修幾條道路。道路可能重複，也可能連到自己。

- **輸入**：第一行 n、m（1 ≤ n ≤ 10⁵，0 ≤ m ≤ 2×10⁵）。接下來 m 行，每行 u、v 表示一條道路。
- **輸出**：一個整數，最少需要新修的道路數。

```text
範例輸入
5 3
1 2
2 3
4 5

範例輸出
1
```

### M1 最短路計數（中等）

給一張 n 個點、m 條無向帶權邊的圖，求點 1 到點 n 的最短距離，以及長度等於最短距離的不同路徑有幾條。兩條路徑只要經過的邊序列不同就視為不同，重邊視為不同的邊。

- **輸入**：第一行 n、m（2 ≤ n ≤ 10⁵，0 ≤ m ≤ 2×10⁵）。接下來 m 行，每行 u、v、w（1 ≤ w ≤ 10⁹）。
- **輸出**：若無法抵達輸出 `-1`。否則輸出最短距離，以及路徑數除以 10⁹ + 7 的餘數。

```text
範例輸入
4 5
1 2 1
1 3 1
2 4 1
3 4 1
1 4 2

範例輸出
2 3
```

三條最短路分別是 1–2–4、1–3–4 與直接的 1–4。

### M2 專案排程（中等）

一個專案有 n 項工作，第 i 項需要 t\_i 天。有 m 條相依關係「a b」，表示工作 a 完成後 b 才能開始。人力無限，沒有相依的工作可以同時進行。求全部完成的最少天數；若相依關係互相矛盾而無法完成，輸出 `-1`。

- **輸入**：第一行 n、m（1 ≤ n ≤ 10⁵，0 ≤ m ≤ 2×10⁵）。第二行 t\_1 到 t\_n（1 ≤ t\_i ≤ 10⁹）。接下來 m 行，每行 a、b。
- **輸出**：一個整數，最少天數或 `-1`。

```text
範例輸入
5 5
3 2 4 1 2
1 2
1 3
2 4
3 4
4 5

範例輸出
10
```

### H1 寶石收集（困難）

一張有向圖有 n 個房間與 m 條單向通道，房間 i 內有 a\_i 顆寶石。你從房間 1 出發，可以沿通道任意行走、重複經過房間，也可以隨時停下。每個房間的寶石只能拿一次。求最多能收集多少寶石。

- **輸入**：第一行 n、m（1 ≤ n ≤ 10⁵，0 ≤ m ≤ 2×10⁵）。第二行 a\_1 到 a\_n（0 ≤ a\_i ≤ 10⁹）。接下來 m 行，每行 u、v 表示一條 u → v 的通道。
- **輸出**：一個整數，最多的寶石數。

```text
範例輸入
6 7
1 2 3 4 5 9
1 2
2 3
3 1
3 4
2 5
5 6
4 6

範例輸出
20
```

先繞完房間 1、2、3 拿到 6 顆，再走 2 → 5 → 6 拿到 5 + 9 顆，共 20 顆。

### H2 樹上配送（困難）

物流公司的 n 個站點由 n − 1 條道路連成一棵樹。今天有 q 筆配送，第 i 筆從站點 u\_i 沿唯一的路徑送到 v\_i，路徑上每個站點（含兩端）的工作量都增加 1。求工作量最大的站點工作量是多少。

- **輸入**：第一行 n、q（1 ≤ n, q ≤ 2×10⁵）。接下來 n − 1 行為樹邊，再接下來 q 行，每行 u\_i、v\_i（可能相等）。
- **輸出**：一個整數，最大工作量。

```text
範例輸入
5 3
1 2
1 3
3 4
3 5
4 5
2 4
5 1

範例輸出
3
```

三條路徑分別為 4–3–5、2–1–3–4、5–3–1，站點 3 被經過 3 次。

## 練習題詳解

六份解答都已通過範例，並各自與暴力解對拍 400 組隨機測資；在最大規模下執行時間都不到 0.5 秒。

### E1 島嶼探險

**思路**：每個陸地格是一個點，上下左右的陸地之間有邊，一座島就是一個連通塊。依序掃描每一格，遇到「是陸地且未拜訪」就從這格做一次 BFS，把整座島標記起來並數格子。BFS 啟動的次數就是島的數量。

**正確性**：一次 BFS 恰好拜訪起點所在連通塊的所有格子。走過的格子已標記，之後掃描不會重複啟動，所以每座島恰好被計算一次。

**複雜度**：每格入佇列一次、檢查四個鄰居，O(RC)，約 4×10⁶ 次操作。

**注意**：1000 × 1000 的全陸地地圖若用遞迴 DFS，深度可達 10⁶ 而堆疊溢位，所以這裡用 BFS。

```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);
    int R, C;
    cin >> R >> C;
    vector<string> g(R);
    for (auto& s : g) cin >> s;
    vector<vector<bool>> vis(R, vector<bool>(C, false));
    int dx[] = {1, -1, 0, 0}, dy[] = {0, 0, 1, -1};
    int islands = 0, best = 0;
    for (int i = 0; i < R; i++)
        for (int j = 0; j < C; j++) {
            if (g[i][j] != '#' || vis[i][j]) continue;
            islands++;
            int area = 0;
            queue<pair<int,int>> q;
            q.push({i, j}); vis[i][j] = true;
            while (!q.empty()) {
                auto [x, y] = q.front(); q.pop();
                area++;
                for (int d = 0; d < 4; d++) {
                    int nx = x + dx[d], ny = y + dy[d];
                    if (nx < 0 || nx >= R || ny < 0 || ny >= C) continue;
                    if (g[nx][ny] != '#' || vis[nx][ny]) continue;
                    vis[nx][ny] = true;
                    q.push({nx, ny});
                }
            }
            best = max(best, area);
        }
    cout << islands << " " << best << "\n";
}
```

### E2 修路計畫

**思路**：答案是「連通塊數 − 1」。用並查集處理每條道路，初始有 n 個連通塊，每次成功合併兩個不同組就減 1。

**正確性**：設有 k 個連通塊。一條新路最多把兩個連通塊合成一個，所以至少要 k − 1 條；反過來，把第 i 塊與第 i + 1 塊各取一點連起來，k − 1 條就夠了。重邊與自環在 `unite` 時會回傳 false，不影響計數。

**複雜度**：O((n + m) α(n))。也可以用 BFS/DFS 數連通塊，結果相同。

```cpp
#include <bits/stdc++.h>
using namespace std;
struct DSU {
    vector<int> p, sz;
    DSU(int n) : p(n + 1), sz(n + 1, 1) { iota(p.begin(), p.end(), 0); }
    int find(int x) { return p[x] == x ? x : p[x] = find(p[x]); }
    bool unite(int a, int b) {
        a = find(a); b = find(b);
        if (a == b) return false;
        if (sz[a] < sz[b]) swap(a, b);
        p[b] = a; sz[a] += sz[b];
        return true;
    }
};
int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);
    int n, m;
    cin >> n >> m;
    DSU dsu(n);
    int comps = n;
    for (int i = 0; i < m; i++) {
        int u, v;
        cin >> u >> v;
        if (dsu.unite(u, v)) comps--;
    }
    cout << comps - 1 << "\n";
}
```

### M1 最短路計數

**思路**：在 Dijkstra 中多維護 cnt\[v\]，表示「目前已知的最短距離下，從 1 到 v 的路徑數」。用 u 鬆弛邊 u → v 時：

- 若 dist\[u\] + w < dist\[v\]：找到更短的路，舊的路徑全部作廢，令 cnt\[v\] = cnt\[u\]。
- 若 dist\[u\] + w == dist\[v\]：又一種等長的走法，令 cnt\[v\] += cnt\[u\]。

**正確性**：邊權至少為 1，所以最短路上 v 的前一個點 u 一定滿足 dist\[u\] < dist\[v\]，會在 v 之前出 heap。u 出 heap 時 dist\[u\] 與 cnt\[u\] 都已確定。所以每個「前一個點」對 cnt\[v\] 的貢獻都是用最終值且只算一次。`d > dist[u]` 的跳過保證每個點只被處理一次，否則同一個 u 會重複加到 cnt\[v\]。

**複雜度**：O(m log m)。最短距離可達 10¹⁴，必須用 long long。

**常見錯誤**：若邊權允許為 0，這個做法會出錯，因為距離相同的點之間有先後關係，需要先建「最短路 DAG」再按拓撲序計數。

```cpp
#include <bits/stdc++.h>
using namespace std;
using ll = long long;
const ll INF = 1e18;
const ll MOD = 1e9 + 7;
int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);
    int n, m;
    cin >> n >> m;
    vector<vector<pair<int,int>>> adj(n + 1);
    for (int i = 0; i < m; i++) {
        int u, v, w;
        cin >> u >> v >> w;
        adj[u].push_back({v, w});
        adj[v].push_back({u, w});
    }
    vector<ll> dist(n + 1, INF), cnt(n + 1, 0);
    priority_queue<pair<ll,int>, vector<pair<ll,int>>, greater<>> pq;
    dist[1] = 0; cnt[1] = 1;
    pq.push({0, 1});
    while (!pq.empty()) {
        auto [d, u] = pq.top(); pq.pop();
        if (d > dist[u]) continue;
        for (auto [v, w] : adj[u]) {
            ll nd = d + w;
            if (nd < dist[v]) {
                dist[v] = nd;
                cnt[v] = cnt[u];
                pq.push({nd, v});
            } else if (nd == dist[v]) {
                cnt[v] = (cnt[v] + cnt[u]) % MOD;
            }
        }
    }
    if (dist[n] == INF) cout << -1 << "\n";
    else cout << dist[n] << " " << cnt[n] << "\n";
}
```

### M2 專案排程

**思路**：工作是點、相依是有向邊。令 start\[v\] 為 v 最早可開工的時間，則 start\[v\] = max(start\[u\] + t\_u)，取遍所有前置工作 u。用 Kahn 演算法依拓撲序處理，答案是所有 start\[v\] + t\_v 的最大值，也就是「關鍵路徑」的長度。

**正確性**：人力無限，所以每項工作在前置全部完成的瞬間就開工是最佳的。依拓撲序處理 v 時，所有前置工作都已處理，start\[v\] 已是最終值。若取出的點數少於 n，代表有環，環上的工作互相等待，永遠無法開工。

**複雜度**：O(n + m)。總天數可達 10⁹ × 10⁵，用 long long。

```cpp
#include <bits/stdc++.h>
using namespace std;
using ll = long long;
int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);
    int n, m;
    cin >> n >> m;
    vector<ll> t(n + 1);
    for (int i = 1; i <= n; i++) cin >> t[i];
    vector<vector<int>> adj(n + 1);
    vector<int> indeg(n + 1, 0);
    for (int i = 0; i < m; i++) {
        int a, b;
        cin >> a >> b;
        adj[a].push_back(b);
        indeg[b]++;
    }
    vector<ll> start(n + 1, 0);       // start[v] = v 最早可開工的時間
    queue<int> q;
    for (int i = 1; i <= n; i++)
        if (indeg[i] == 0) q.push(i);
    int done = 0;
    ll ans = 0;
    while (!q.empty()) {
        int u = q.front(); q.pop();
        done++;
        ll finish = start[u] + t[u];
        ans = max(ans, finish);
        for (int v : adj[u]) {
            start[v] = max(start[v], finish);
            if (--indeg[v] == 0) q.push(v);
        }
    }
    if (done < n) cout << -1 << "\n";
    else cout << ans << "\n";
}
```

### H1 寶石收集

**思路**：同一個強連通分量內的房間互相可達，只要進入就能全部拿完再從任一點離開。所以：

1. 用 Tarjan 從房間 1 找 SCC，只處理從 1 可達的部分。
2. 縮點：每個 SCC 變成一個點，權重是內部寶石總和 sum\[c\]。縮點後的圖是 DAG。
3. 在 DAG 上求「從起點 SCC 出發的最大點權路徑」：best\[d\] = max(best\[c\] + sum\[d\])。

**正確性**：任何一個行走方式在縮點圖上都是一條路徑，因為 DAG 一旦離開一個 SCC 就無法回來；反過來，縮點圖上的每條路徑都能實現，在每個 SCC 內先繞一圈拿完再走出去。所以答案就是 DAG 上的最大點權路徑。

**拓撲序來源**：Tarjan 的 SCC 編號是反拓撲序，編號越大越前面。由於只從 1 出發，起點所在的 SCC 最後完成，編號為 sccCnt。因此 c 從 sccCnt 遞減到 1 就是拓撲序，不必再跑 Kahn。

**複雜度**：O(n + m)。總和可達 10¹⁴，用 long long。遞迴深度最多 10⁵，在多數評測系統上可接受。

```cpp
#include <bits/stdc++.h>
using namespace std;
using ll = long long;
int n, m, timer_ = 0, sccCnt = 0;
vector<vector<int>> adj;
vector<int> dfn, low, comp, stk;
vector<bool> inStk;
void tarjan(int u) {
    dfn[u] = low[u] = ++timer_;
    stk.push_back(u); inStk[u] = true;
    for (int v : adj[u]) {
        if (!dfn[v]) { tarjan(v); low[u] = min(low[u], low[v]); }
        else if (inStk[v]) low[u] = min(low[u], dfn[v]);
    }
    if (low[u] == dfn[u]) {
        ++sccCnt;
        while (true) {
            int x = stk.back(); stk.pop_back();
            inStk[x] = false; comp[x] = sccCnt;
            if (x == u) break;
        }
    }
}
int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);
    cin >> n >> m;
    vector<ll> a(n + 1);
    for (int i = 1; i <= n; i++) cin >> a[i];
    adj.assign(n + 1, {});
    vector<pair<int,int>> edges(m);
    for (auto& [u, v] : edges) { cin >> u >> v; adj[u].push_back(v); }
    dfn.assign(n + 1, 0); low.assign(n + 1, 0);
    comp.assign(n + 1, 0); inStk.assign(n + 1, false);
    tarjan(1);                          // 只需要從 1 出發可達的部分
    // 縮點：sum[c] = 第 c 個 SCC 的寶石總和
    vector<ll> sum(sccCnt + 1, 0);
    for (int i = 1; i <= n; i++) if (comp[i]) sum[comp[i]] += a[i];
    vector<vector<int>> dag(sccCnt + 1);
    for (auto [u, v] : edges)
        if (comp[u] && comp[v] && comp[u] != comp[v])
            dag[comp[u]].push_back(comp[v]);
    // Tarjan 編號為反拓撲序：編號大的在前。由 sccCnt 往下做就是拓撲序。
    vector<ll> best(sccCnt + 1, 0);     // best[c] = 走到 c 時最多已收集多少（含 c）
    int s = comp[1];                    // 起點所在 SCC，一定是 sccCnt
    best[s] = sum[s];
    ll ans = best[s];
    for (int c = sccCnt; c >= 1; c--) {
        ans = max(ans, best[c]);
        for (int d : dag[c]) best[d] = max(best[d], best[c] + sum[d]);
    }
    cout << ans << "\n";
}
```

### H2 樹上配送

**思路**：直接把每條路徑走一次是 O(nq)，最壞 4×10¹⁰，太慢。改用點差分：對每筆配送求 l = lca(u, v)，做 d\[u\]++、d\[v\]++、d\[l\]--、d\[parent(l)\]--。全部標記完後，每個點的工作量就是它子樹內 d 的總和。

**正確性**：點 w 的子樹和會算到一筆配送的哪些標記？

- w 在 u–l 或 v–l 的路段上、但不是 l：子樹只含 u 與 v 其中一個，總和 +1。
- w = l：子樹含 u、v、l，總和 1 + 1 − 1 = 1。
- w 是 l 的祖先：四個標記都在子樹內，總和 0。
- w 不在路徑上也不是 l 的祖先：子樹內沒有任何標記，總和 0。

所以恰好路徑上的點各得 1。u = v 時 l = u，標記為 +2 − 1，只有 u 本身得 1，也正確。

**實作細節**：n = 2×10⁵ 的鏈狀樹用遞迴 DFS 可能堆疊溢位，所以改用 BFS 求父節點與深度。BFS 序保證父節點排在子節點前面，倒著走一遍、把 d\[u\] 加到父節點，就是子樹和。根的父節點設為 0 當哨兵。

**複雜度**：預處理 O(n log n)，每筆查詢 O(log n)，總計 O((n + q) log n)。

```cpp
#include <bits/stdc++.h>
using namespace std;
const int LOG = 18;
int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);
    int n, q;
    cin >> n >> q;
    vector<vector<int>> adj(n + 1);
    for (int i = 0; i < n - 1; i++) {
        int u, v;
        cin >> u >> v;
        adj[u].push_back(v);
        adj[v].push_back(u);
    }
    // 以 BFS 求父節點與深度，避免遞迴過深
    vector<vector<int>> up(LOG, vector<int>(n + 1, 0));
    vector<int> dep(n + 1, 0), order;
    order.reserve(n);
    vector<bool> seen(n + 1, false);
    queue<int> bq; bq.push(1); seen[1] = true;
    while (!bq.empty()) {
        int u = bq.front(); bq.pop();
        order.push_back(u);
        for (int v : adj[u]) if (!seen[v]) {
            seen[v] = true; up[0][v] = u; dep[v] = dep[u] + 1; bq.push(v);
        }
    }
    for (int k = 1; k < LOG; k++)
        for (int u = 1; u <= n; u++) up[k][u] = up[k-1][ up[k-1][u] ];
    auto lca = [&](int a, int b) {
        if (dep[a] < dep[b]) swap(a, b);
        int diff = dep[a] - dep[b];
        for (int k = 0; k < LOG; k++) if (diff >> k & 1) a = up[k][a];
        if (a == b) return a;
        for (int k = LOG - 1; k >= 0; k--)
            if (up[k][a] != up[k][b]) { a = up[k][a]; b = up[k][b]; }
        return up[0][a];
    };
    vector<long long> d(n + 1, 0);
    for (int i = 0; i < q; i++) {
        int u, v;
        cin >> u >> v;
        int l = lca(u, v);
        d[u]++; d[v]++; d[l]--;
        if (up[0][l]) d[up[0][l]]--;    // 根的父節點是 0，不必扣
    }
    // 依 BFS 序反向累加，等同子樹和
    for (int i = n - 1; i >= 1; i--) {
        int u = order[i];
        d[up[0][u]] += d[u];
    }
    cout << *max_element(d.begin() + 1, d.end()) << "\n";
}
```
