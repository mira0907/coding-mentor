#include <bits/stdc++.h>
using namespace std;
const long long MOD = 1e9 + 7;            // 路線數取餘數用
int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);
    int n, m;                              // n = 地點數，m = 車道數
    cin >> n >> m;
    // adj[u]：從 u 出發的車道通往哪些地點
    // radj[v]：哪些地點有車道通往 v（反向圖）
    vector<vector<int>> adj(n + 1), radj(n + 1);
    vector<pair<int,int>> edges(m);        // 所有車道 (u, v)，算有用車道的入度時要再用一次
    for (auto& [u, v] : edges) {           // u → v 是一條單向車道
        cin >> u >> v;
        adj[u].push_back(v);
        radj[v].push_back(u);
    }
    // 回傳從 s 出發、沿著 g 的邊走得到哪些點
    auto bfs = [&](int s, const vector<vector<int>>& g) {
        vector<bool> seen(n + 1, false);   // seen[v] = v 是否已經走到
        queue<int> q;                      // BFS 佇列
        q.push(s); seen[s] = true;
        while (!q.empty()) {
            int u = q.front(); q.pop();    // u = 目前展開的點
            for (int v : g[u])             // v = u 的鄰居
                if (!seen[v]) { seen[v] = true; q.push(v); }
        }
        return seen;
    };
    vector<bool> fromStart = bfs(1, adj);  // fromStart[v] = 從地點 1 騎得到 v
    vector<bool> toEnd = bfs(n, radj);     // toEnd[v] = 從 v 騎得到地點 n（在反向圖上從 n 出發）
    vector<bool> useful(n + 1, false);     // useful[v] = v 落在某條 1 到 n 的路線上
    int total = 0;                         // 有用的點數
    for (int v = 1; v <= n; v++) {         // v = 地點編號
        useful[v] = fromStart[v] && toEnd[v];
        if (useful[v]) total++;
    }
    vector<int> indeg(n + 1, 0);           // indeg[v] = 只算兩端都有用的車道時，v 的入度
    for (auto [u, v] : edges)              // 車道 u → v
        if (useful[u] && useful[v]) indeg[v]++;
    vector<long long> ways(n + 1, 0);      // ways[v] = 從 1 騎到 v 的路線數（取餘數後）
    queue<int> q;                          // q = 入度已經是 0 的有用點
    for (int v = 1; v <= n; v++)           // v = 地點編號
        if (useful[v] && indeg[v] == 0) q.push(v);
    if (useful[1]) ways[1] = 1;            // 起點：不騎任何車道的那一條
    int done = 0;                          // Kahn 取出的有用點數
    while (!q.empty()) {
        int u = q.front(); q.pop();        // u = 依拓撲序處理的點，ways[u] 已經算完
        done++;
        for (int v : adj[u]) {             // v = u 的下一站
            if (!useful[v]) continue;      // 走不到 n 的點不用管
            ways[v] = (ways[v] + ways[u]) % MOD;
            if (--indeg[v] == 0) q.push(v);
        }
    }
    if (done < total) cout << "INFINITE\n"; // 有用的點裡有環，可以繞任意多圈
    else cout << ways[n] << "\n";
}
