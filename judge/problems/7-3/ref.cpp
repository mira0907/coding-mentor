#include <bits/stdc++.h>
using namespace std;
const int LOG = 18;                       // 2^18 > 2×10^5，倍增表的層數
int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);
    int n, q;                             // n = 站點數，q = 配送筆數
    cin >> n >> q;
    vector<vector<int>> adj(n + 1);       // adj[u] = u 的相鄰站點
    for (int i = 0; i < n - 1; i++) {     // i = 正在讀第幾條道路
        int u, v;                         // 道路連接 u、v
        cin >> u >> v;
        adj[u].push_back(v);
        adj[v].push_back(u);
    }
    // 以 BFS 求父節點與深度，避免遞迴過深
    vector<vector<int>> up(LOG, vector<int>(n + 1, 0));   // up[k][u] = u 往上跳 2^k 步的祖先，0 是哨兵
    vector<int> dep(n + 1, 0), order;     // dep[u] = u 的深度；order = BFS 順序，父節點一定在子節點前面
    order.reserve(n);
    vector<bool> seen(n + 1, false);      // seen[v] = v 是否已被 BFS 發現
    queue<int> bq; bq.push(1); seen[1] = true;   // bq = BFS 佇列
    while (!bq.empty()) {
        int u = bq.front(); bq.pop();
        order.push_back(u);
        for (int v : adj[u]) if (!seen[v]) {     // v = u 的子節點
            seen[v] = true; up[0][v] = u; dep[v] = dep[u] + 1; bq.push(v);
        }
    }
    for (int k = 1; k < LOG; k++)
        for (int u = 1; u <= n; u++) up[k][u] = up[k-1][ up[k-1][u] ];
    auto lca = [&](int a, int b) {        // 回傳 a、b 的最近公共祖先，寫法同 7.3 節
        if (dep[a] < dep[b]) swap(a, b);
        int diff = dep[a] - dep[b];       // a 要往上跳幾步才和 b 同深度
        for (int k = 0; k < LOG; k++) if (diff >> k & 1) a = up[k][a];
        if (a == b) return a;
        for (int k = LOG - 1; k >= 0; k--)
            if (up[k][a] != up[k][b]) { a = up[k][a]; b = up[k][b]; }
        return up[0][a];
    };
    vector<long long> d(n + 1, 0);        // d[w] = 差分標記，最後累加成站點 w 的工作量
    for (int i = 0; i < q; i++) {         // i = 第幾筆配送
        int u, v;                         // 這筆配送從 u 送到 v
        cin >> u >> v;
        int l = lca(u, v);                // l = u、v 的最近公共祖先
        d[u]++; d[v]++; d[l]--;
        if (up[0][l]) d[up[0][l]]--;    // 根的父節點是 0，不必扣
    }
    // 依 BFS 序反向累加，等同子樹和
    for (int i = n - 1; i >= 1; i--) {    // i 由後往前：子節點一定比父節點先處理
        int u = order[i];
        d[up[0][u]] += d[u];              // 把 u 的子樹和加到父節點
    }
    cout << *max_element(d.begin() + 1, d.end()) << "\n";   // 工作量最大的站點
}
