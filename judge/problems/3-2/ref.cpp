#include <bits/stdc++.h>
using namespace std;
using ll = long long;
const ll INF = 1e18;                 // 代表走不到
const ll MOD = 1e9 + 7;              // 路徑數取餘數用
int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);
    int n, m;                        // n = 點數，m = 邊數
    cin >> n >> m;
    vector<vector<pair<int,int>>> adj(n + 1);   // adj[u] = (v, w)：u、v 之間邊權 w 的邊
    for (int i = 0; i < m; i++) {    // i = 正在讀第幾條邊
        int u, v, w;                 // 這條邊連接 u、v，邊權 w
        cin >> u >> v >> w;
        adj[u].push_back({v, w});
        adj[v].push_back({u, w});
    }
    // dist[v]：點 1 到 v 的最短距離；cnt[v]：長度等於 dist[v] 的路徑數（取餘數後）
    vector<ll> dist(n + 1, INF), cnt(n + 1, 0);
    priority_queue<pair<ll,int>, vector<pair<ll,int>>, greater<>> pq;   // (距離, 點)，距離小的先出來
    dist[1] = 0; cnt[1] = 1;
    pq.push({0, 1});
    while (!pq.empty()) {
        auto [d, u] = pq.top(); pq.pop();   // u = 取出的點，d = 它當時的距離
        if (d > dist[u]) continue;
        for (auto [v, w] : adj[u]) {        // 邊 u–v，邊權 w
            ll nd = d + w;                  // nd = 經由 u 走到 v 的距離
            if (nd < dist[v]) {             // 找到更短的路：舊的路徑數作廢
                dist[v] = nd;
                cnt[v] = cnt[u];
                pq.push({nd, v});
            } else if (nd == dist[v]) {     // 一樣短：路徑數相加
                cnt[v] = (cnt[v] + cnt[u]) % MOD;
            }
        }
    }
    if (dist[n] == INF) cout << -1 << "\n";
    else cout << dist[n] << " " << cnt[n] << "\n";
}
