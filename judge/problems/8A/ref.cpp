#include <bits/stdc++.h>
using namespace std;
int nL, nR, E;                   // nL = 員工數，nR = 工作數，E = 「會做」的關係數
vector<vector<int>> g;           // g[u] = 員工 u 會做的工作
vector<int> matchR;              // matchR[v] = 負責工作 v 的員工，0 表示還沒人做
vector<bool> vis;                // vis[v] = 這一次找增廣路時，工作 v 是否已經問過
bool tryKuhn(int u) {            // 幫員工 u 找工作；成功回傳 true
    for (int v : g[u]) {         // v = u 會做的工作
        if (vis[v]) continue;
        vis[v] = true;
        if (matchR[v] == 0 || tryKuhn(matchR[v])) { matchR[v] = u; return true; }   // v 沒人做，或原本的人能換工作
    }
    return false;
}
int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);
    cin >> nL >> nR >> E;
    g.assign(nL + 1, {});
    for (int i = 0; i < E; i++) { int u, v; cin >> u >> v; g[u].push_back(v); }   // 員工 u 會做工作 v
    matchR.assign(nR + 1, 0);
    int ans = 0;                     // 已經配成的組數
    for (int u = 1; u <= nL; u++) {  // u = 目前要安排的員工
        vis.assign(nR + 1, false);
        if (tryKuhn(u)) ans++;
    }
    cout << ans << "\n";
}
