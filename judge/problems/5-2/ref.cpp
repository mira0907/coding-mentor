#include <bits/stdc++.h>
using namespace std;
using ll = long long;
int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);
    int n, m;                         // n = 工作數，m = 相依關係數
    cin >> n >> m;
    vector<ll> t(n + 1);              // t[i] = 工作 i 需要幾天
    for (int i = 1; i <= n; i++) cin >> t[i];
    vector<vector<int>> adj(n + 1);   // adj[a] = 要等 a 做完才能開始的工作
    vector<int> indeg(n + 1, 0);      // indeg[b] = b 還在等幾項工作完成
    for (int i = 0; i < m; i++) {     // i = 正在讀第幾條相依關係
        int a, b;                     // a 完成後 b 才能開始
        cin >> a >> b;
        adj[a].push_back(b);
        indeg[b]++;
    }
    vector<ll> start(n + 1, 0);       // start[v] = v 最早可開工的時間
    queue<int> q;                     // q = 前置工作都做完、可以開始的工作
    for (int i = 1; i <= n; i++)
        if (indeg[i] == 0) q.push(i);
    int done = 0;                     // 已經排進時程的工作數
    ll ans = 0;                       // 全部完成的最早時間
    while (!q.empty()) {
        int u = q.front(); q.pop();   // u = 可以開始的工作
        done++;
        ll finish = start[u] + t[u];  // finish = u 最早的完成時間
        ans = max(ans, finish);
        for (int v : adj[u]) {        // v = 在等 u 的工作
            start[v] = max(start[v], finish);   // v 要等所有前置工作中最晚完成的那個
            if (--indeg[v] == 0) q.push(v);
        }
    }
    if (done < n) cout << -1 << "\n";   // 有工作永遠排不進來 → 相依關係有環
    else cout << ans << "\n";
}
