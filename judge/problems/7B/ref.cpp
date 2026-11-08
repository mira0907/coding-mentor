#include <bits/stdc++.h>
using namespace std;
using ll = long long;
int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);
    int n;                                      // n = 村莊數
    cin >> n;
    vector<vector<pair<int,int>>> adj(n + 1);   // adj[u] = (v, w)：u、v 之間有長度 w 的道路
    for (int i = 0; i < n - 1; i++) {           // i = 正在讀第幾條道路
        int u, v, w; cin >> u >> v >> w;
        adj[u].push_back({v, w}); adj[v].push_back({u, w});
    }
    // BFS 序：父節點必在子節點之前
    // order：以 1 為根的 BFS 順序；par[v]：v 的父節點；pw[v]：v 到父節點那條道路的長度
    vector<int> order, par(n + 1, 0), pw(n + 1, 0);
    // sz[u]：u 的子樹有幾個點；S[u]：所有村莊到 u 的距離總和（答案）
    vector<ll> sz(n + 1, 1), S(n + 1, 0);
    order.reserve(n);
    vector<bool> seen(n + 1, false);            // seen[v] = v 是否已經被 BFS 發現
    queue<int> q; q.push(1); seen[1] = true;    // q = BFS 佇列
    while (!q.empty()) {
        int u = q.front(); q.pop(); order.push_back(u);
        for (auto [v, w] : adj[u]) if (!seen[v]) {   // v = u 的子節點
            seen[v] = true; par[v] = u; pw[v] = w; q.push(v);
        }
    }
    // 第一趟（由下往上）：sz[u] 與 down[u] = u 到子樹內所有點的距離和
    vector<ll> down(n + 1, 0);
    for (int i = n - 1; i >= 1; i--) {          // i 由後往前：子節點一定比父節點先處理
        int v = order[i], u = par[v];           // v = 目前的點，u = 它的父節點
        sz[u] += sz[v];
        down[u] += down[v] + (ll)pw[v] * sz[v]; // v 子樹裡每個點到 u 都要多走 pw[v]
    }
    // 第二趟（由上往下）：換根
    S[1] = down[1];
    for (int i = 1; i < n; i++) {               // i 由前往後：父節點的答案一定先算好
        int v = order[i], u = par[v];
        S[v] = S[u] + (ll)pw[v] * (n - 2 * sz[v]);   // sz[v] 個點近了 pw[v]，其餘 n − sz[v] 個點遠了 pw[v]
    }
    for (int i = 1; i <= n; i++) cout << S[i] << " \n"[i == n];
}
