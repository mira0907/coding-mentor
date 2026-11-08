#include <bits/stdc++.h>
using namespace std;
using ll = long long;
const ll INF = LLONG_MAX / 4;                 // 代表走不到；除以 4 留下空間，避免加上邊權時溢位
int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);
    int n, m;                                 // n = 點數，m = 邊數
    cin >> n >> m;
    vector<array<ll,3>> e(m);                 // e[i] = 第 i 條有向邊 {u, v, w}：u → v，邊權 w
    for (auto& [u, v, w] : e) cin >> u >> v >> w;
    vector<ll> dist(n + 1, INF);              // dist[v] = 點 1 到 v 目前的最短距離
    dist[1] = 0;
    for (int round = 1; round <= n; round++) {   // round = 第幾輪鬆弛
        bool changed = false;                 // 這一輪有沒有任何距離被更新
        for (auto [u, v, w] : e) {
            if (dist[u] == INF) continue;          // 尚不可達的點不能拿來鬆弛
            if (dist[u] + w < dist[v]) {
                dist[v] = dist[u] + w;
                changed = true;
            }
        }
        if (!changed) break;
        if (round == n) { cout << "NEGATIVE CYCLE\n"; return 0; }   // 第 n 輪還在更新 → 有負環
    }
    for (int i = 1; i <= n; i++) {            // i = 要輸出的點
        if (dist[i] == INF) cout << "INF";
        else cout << dist[i];
        cout << " \n"[i == n];
    }
}
