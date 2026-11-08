#include <bits/stdc++.h>
using namespace std;
using ll = long long;
const ll INF = 1e18;                          // 代表走不到

// s = 起點，g = 要在上面跑的圖（g[u] 存 (v, w) 表示 u → v、時間 w）
// 回傳 dist[v] = 在圖 g 上 s 到 v 的最短時間，走不到時為 INF
vector<ll> dijkstra(int s, const vector<vector<pair<int,int>>>& g) {
    int n = (int)g.size() - 1;                // n = 點數，編號 1 到 n
    vector<ll> dist(n + 1, INF);              // dist[v] = 目前找到的 s 到 v 最短時間
    // pq 存 (時間, 點)，greater<> 讓時間最小的先出來
    priority_queue<pair<ll,int>, vector<pair<ll,int>>, greater<>> pq;
    dist[s] = 0; pq.push({0, s});
    while (!pq.empty()) {
        auto [d, u] = pq.top(); pq.pop();     // u = 取出的點，d = 放進堆積時它的時間
        if (d > dist[u]) continue;            // 過期的項目，跳過
        for (auto [v, w] : g[u]) {            // 每條邊 u → v，時間 w
            if (d + w < dist[v]) {
                dist[v] = d + w;
                pq.push({dist[v], v});
            }
        }
    }
    return dist;
}

int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);
    // n = 夜市數
    // m = 單向道路數
    // t = 開會的夜市
    int n, m, t;
    cin >> n >> m >> t;
    vector<vector<pair<int,int>>> g(n + 1);   // g[u] = 原圖的出邊 (v, w)：u → v 要 w 分鐘
    vector<vector<pair<int,int>>> rg(n + 1);  // rg[v] = 反向圖的出邊 (u, w)：原圖的 u → v 反過來存
    for (int i = 0; i < m; i++) {             // i = 正在讀第幾條道路
        // u = 道路起點
        // v = 道路終點
        // w = 走這條路要幾分鐘
        int u, v, w;
        cin >> u >> v >> w;
        g[u].push_back({v, w});
        rg[v].push_back({u, w});
    }
    vector<ll> back = dijkstra(t, g);         // back[i] = 從 t 回到 i 的最短時間（回程）
    vector<ll> go = dijkstra(t, rg);          // go[i] = 從 i 走到 t 的最短時間（去程）
    for (int i = 1; i <= n; i++) {            // i = 要輸出的夜市
        if (go[i] == INF || back[i] == INF) cout << -1;   // 去不了或回不來
        else cout << go[i] + back[i];
        cout << " \n"[i == n];
    }
}
