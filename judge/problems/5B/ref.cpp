#include <bits/stdc++.h>
using namespace std;
const int MAXN = 30000;                // 點數上限
bitset<MAXN> reach[MAXN];          // reach[u] 的第 v 位 = u 能否到達 v（0-indexed）
int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);
    int n, m;                          // n = 點數，m = 邊數
    cin >> n >> m;
    vector<vector<int>> adj(n);        // adj[a] = a 指向的點（編號從 0 開始）
    vector<int> indeg(n, 0);           // indeg[v] = v 還沒處理的入邊數
    for (int i = 0; i < m; i++) {      // i = 正在讀第幾條邊
        int a, b; cin >> a >> b; a--; b--;   // 邊 a → b，轉成從 0 開始編號
        adj[a].push_back(b); indeg[b]++;
    }
    vector<int> order; queue<int> q;   // order = 拓撲序；q = 入度已經是 0 的點
    for (int i = 0; i < n; i++) if (indeg[i] == 0) q.push(i);
    while (!q.empty()) {
        int u = q.front(); q.pop(); order.push_back(u);
        for (int v : adj[u]) if (--indeg[v] == 0) q.push(v);
    }
    // 反拓撲序：處理 u 時，所有後繼都已算好
    for (int i = n - 1; i >= 0; i--) {
        int u = order[i];              // u = 拓撲序中的第 i 個點，i 由後往前
        reach[u][u] = 1;               // u 一定到得了自己
        for (int v : adj[u]) reach[u] |= reach[v];   // v 到得了的點，u 也都到得了
    }
    for (int i = 0; i < n; i++) cout << reach[i].count() << " \n"[i == n - 1];   // count() = 到得了的點數
}
