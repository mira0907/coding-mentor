#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);
    int n, m;                              // n = 課程數，m = 先修關係數
    cin >> n >> m;
    vector<vector<int>> adj(n + 1);        // adj[a] = 以 a 為先修的課程
    vector<int> indeg(n + 1, 0);           // indeg[b] = b 還有幾門先修課沒修
    for (int i = 0; i < m; i++) {          // i = 正在讀第幾個先修關係
        int a, b; cin >> a >> b;           // 要先修 a 才能修 b
        adj[a].push_back(b); indeg[b]++;
    }
    priority_queue<int, vector<int>, greater<int>> pq;   // pq = 現在可以修的課；每次取編號最小
    for (int i = 1; i <= n; i++) if (indeg[i] == 0) pq.push(i);
    vector<int> order;                     // 選課順序
    while (!pq.empty()) {
        int u = pq.top(); pq.pop();        // u = 現在可以修、編號最小的課
        order.push_back(u);
        for (int v : adj[u]) if (--indeg[v] == 0) pq.push(v);   // v 的先修少了一門，修完了就能加入
    }
    if ((int)order.size() < n) { cout << "IMPOSSIBLE\n"; return 0; }   // 有課永遠修不到 → 先修關係有環
    for (int i = 0; i < n; i++) cout << order[i] << " \n"[i == n - 1];
}
