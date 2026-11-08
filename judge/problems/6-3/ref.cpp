#include <bits/stdc++.h>
using namespace std;
using ll = long long;
// n = 房間數，m = 通道數；timer_ = Tarjan 時間戳；sccCnt = SCC 個數
int n, m, timer_ = 0, sccCnt = 0;
vector<vector<int>> adj;              // adj[u] = 從 u 可以走到的房間
// dfn、low：Tarjan 用的時間戳
// comp[u]：u 屬於第幾個 SCC，0 表示從房間 1 走不到
// stk：還沒分進 SCC 的點
vector<int> dfn, low, comp, stk;
vector<bool> inStk;                   // inStk[u] = u 是否在 stk 裡
void tarjan(int u) {                  // u = 目前拜訪的房間
    dfn[u] = low[u] = ++timer_;
    stk.push_back(u); inStk[u] = true;
    for (int v : adj[u]) {            // v = u 可以走到的房間
        if (!dfn[v]) { tarjan(v); low[u] = min(low[u], low[v]); }
        else if (inStk[v]) low[u] = min(low[u], dfn[v]);
    }
    if (low[u] == dfn[u]) {           // u 是一個 SCC 的根
        ++sccCnt;
        while (true) {
            int x = stk.back(); stk.pop_back();   // x = 屬於這個 SCC 的房間
            inStk[x] = false; comp[x] = sccCnt;
            if (x == u) break;
        }
    }
}
int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);
    cin >> n >> m;
    vector<ll> a(n + 1);                // a[i] = 房間 i 的寶石數
    for (int i = 1; i <= n; i++) cin >> a[i];
    adj.assign(n + 1, {});
    vector<pair<int,int>> edges(m);     // 所有通道 (u, v)，縮點時要再用一次
    for (auto& [u, v] : edges) { cin >> u >> v; adj[u].push_back(v); }
    dfn.assign(n + 1, 0); low.assign(n + 1, 0);
    comp.assign(n + 1, 0); inStk.assign(n + 1, false);
    tarjan(1);                          // 只需要從 1 出發可達的部分
    // 縮點：sum[c] = 第 c 個 SCC 的寶石總和
    vector<ll> sum(sccCnt + 1, 0);
    for (int i = 1; i <= n; i++) if (comp[i]) sum[comp[i]] += a[i];   // i = 房間編號
    vector<vector<int>> dag(sccCnt + 1);   // dag[c] = 縮點後從 SCC c 走得到的 SCC
    for (auto [u, v] : edges)
        if (comp[u] && comp[v] && comp[u] != comp[v])
            dag[comp[u]].push_back(comp[v]);
    // Tarjan 編號為反拓撲序：編號大的在前。由 sccCnt 往下做就是拓撲序。
    vector<ll> best(sccCnt + 1, 0);     // best[c] = 走到 c 時最多已收集多少（含 c）
    int s = comp[1];                    // 起點所在 SCC，一定是 sccCnt
    best[s] = sum[s];
    ll ans = best[s];                   // ans = 目前最多能收集的寶石數
    for (int c = sccCnt; c >= 1; c--) { // c = 依拓撲序處理的 SCC
        ans = max(ans, best[c]);
        for (int d : dag[c]) best[d] = max(best[d], best[c] + sum[d]);   // d = c 走得到的 SCC
    }
    cout << ans << "\n";
}
