#include <bits/stdc++.h>
using namespace std;
using ll = long long;
int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);
    int n;                                  // n = 路口數
    cin >> n;
    vector<ll> c(n + 1);                    // c[i] = 在路口 i 裝監視器的費用
    for (int i = 1; i <= n; i++) cin >> c[i];
    vector<vector<int>> adj(n + 1);         // adj[u] = 和路口 u 有道路相連的路口
    for (int i = 0; i < n - 1; i++) {       // i = 正在讀第幾條道路
        // u = 道路的一端
        // v = 道路的另一端
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
    // take[u] = u 裝監視器時，u 的子樹裡所有道路都被拍到的最少花費
    // skip[u] = u 不裝監視器時，u 的子樹裡所有道路都被拍到的最少花費
    vector<ll> take(c), skip(n + 1, 0);     // take 先放 u 自己的費用，再加上子節點的部分
    for (int i = n - 1; i >= 1; i--) {      // i 由後往前：子節點一定比父節點先算完
        int v = order[i];                   // v = 目前的點，它的子樹已經算完
        int p = par[v];                     // p = v 的父節點
        take[p] += min(take[v], skip[v]);   // p 有裝：道路 p–v 已被拍到，v 裝不裝都可以，取便宜的
        skip[p] += take[v];                 // p 沒裝：道路 p–v 只能靠 v 來拍，v 一定要裝
    }
    cout << min(take[1], skip[1]) << "\n";  // 根裝或不裝，取比較便宜的
}
