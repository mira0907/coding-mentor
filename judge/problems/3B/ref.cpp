#include <bits/stdc++.h>
using namespace std;
using ll = long long;
const ll INF = 1e18;                          // 代表走不到
int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);
    int n, m, K;                              // n = 城市數，m = 航線數，K = 優惠券張數
    cin >> n >> m >> K;
    vector<vector<pair<int,int>>> adj(n + 1); // adj[u] = (v, w)：u 和 v 之間有航線，票價 w
    for (int i = 0; i < m; i++) {             // i = 正在讀第幾條航線
        int u, v, w;                          // 這條航線連接 u、v，票價 w
        cin >> u >> v >> w;
        adj[u].push_back({v, w});
        adj[v].push_back({u, w});
    }
    // dist[v][j] = 到達 v、已用 j 張優惠券的最小花費
    vector<vector<ll>> dist(n + 1, vector<ll>(K + 1, INF));
    // pq 存 (花費, 城市, 已用張數)，花費最小的先出來
    priority_queue<tuple<ll,int,int>, vector<tuple<ll,int,int>>, greater<>> pq;
    dist[1][0] = 0; pq.push({0, 1, 0});
    while (!pq.empty()) {
        auto [d, u, j] = pq.top(); pq.pop();  // 在城市 u、已用 j 張券、花費 d
        if (d > dist[u][j]) continue;
        for (auto [v, w] : adj[u]) {          // 從 u 飛到 v，票價 w
            if (d + w < dist[v][j]) {                       // 正常付費
                dist[v][j] = d + w; pq.push({dist[v][j], v, j});
            }
            if (j < K && d < dist[v][j + 1]) {              // 使用一張優惠券
                dist[v][j + 1] = d; pq.push({d, v, j + 1});
            }
        }
    }
    ll ans = *min_element(dist[n].begin(), dist[n].end());   // 到達 n 時用幾張券都可以，取最小
    cout << (ans == INF ? -1 : ans) << "\n";
}
