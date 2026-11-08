#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);
    int n;                                  // n = 變電所數
    cin >> n;
    vector<vector<int>> adj(n + 1);         // adj[u] = 和 u 有電纜相連的變電所
    for (int i = 0; i < n - 1; i++) {       // i = 正在讀第幾條電纜
        // u = 電纜的一端
        // v = 電纜的另一端
        int u, v;
        cin >> u >> v;
        adj[u].push_back(v);
        adj[v].push_back(u);
    }
    // 以 1 為根做 BFS，求父節點與 BFS 順序，避免鏈狀樹讓遞迴太深
    vector<int> par(n + 1, 0);              // par[v] = v 的父節點，根的父節點是 0
    vector<int> order;                      // order = BFS 順序，父節點一定排在子節點前面
    order.reserve(n);
    vector<bool> seen(n + 1, false);        // seen[v] = v 是否已被 BFS 發現
    queue<int> q;                           // q = BFS 佇列
    q.push(1); seen[1] = true;
    while (!q.empty()) {
        int u = q.front(); q.pop();         // u = 目前處理的點
        order.push_back(u);
        for (int v : adj[u]) if (!seen[v]) {   // v = u 的子節點
            seen[v] = true; par[v] = u; q.push(v);
        }
    }
    vector<int> sz(n + 1, 1);               // sz[u] = 以 1 為根時 u 的子樹大小
    vector<int> big(n + 1, 0);              // big[u] = u 的子節點裡最大的子樹大小
    for (int i = n - 1; i >= 1; i--) {      // i 由後往前：子節點一定比父節點先處理
        int v = order[i];                   // v = 目前的點
        int p = par[v];                     // p = v 的父節點
        sz[p] += sz[v];
        big[p] = max(big[p], sz[v]);
    }
    vector<int> part(n + 1);                // part[u] = 拆掉 u 之後最大那一塊的大小
    int best = n;                           // best = 所有 part[u] 的最小值，也就是第一行的答案
    for (int u = 1; u <= n; u++) {          // u = 考慮停機的變電所
        part[u] = max(big[u], n - sz[u]);   // 往下最大的一塊，和往上的那一塊（n − sz[u] 個點）比較
        best = min(best, part[u]);
    }
    vector<int> ans;                        // ans = 所有 part[u] == best 的變電所，編號由小到大
    for (int u = 1; u <= n; u++) if (part[u] == best) ans.push_back(u);
    cout << best << "\n";
    for (int i = 0; i < (int)ans.size(); i++)   // i = ans 的第幾個
        cout << ans[i] << " \n"[i + 1 == (int)ans.size()];
}
