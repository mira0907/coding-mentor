#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);
    // n = 同學人數
    // m = 「互看不順眼」的組數
    int n, m;
    cin >> n >> m;
    vector<vector<int>> adj(n + 1);         // adj[u] = 和 u 互看不順眼的同學
    for (int i = 0; i < m; i++) {           // i = 正在讀第幾組
        // u = 這一組的第一位同學
        // v = 這一組的第二位同學，和 u 必須分在不同隊
        int u, v;
        cin >> u >> v;
        adj[u].push_back(v);
        adj[v].push_back(u);
    }
    vector<int> team(n + 1, 0);             // team[u] = u 被分到第幾隊（1 或 2），0 表示還沒分
    for (int s = 1; s <= n; s++) {          // s 由小到大：s 沒分過時，就是所在連通塊中編號最小的人
        if (team[s]) continue;
        team[s] = 1;                        // 連通塊中編號最小的人放第 1 隊，字典序才會最小
        queue<int> q;                       // q = BFS 佇列
        q.push(s);
        while (!q.empty()) {
            int u = q.front(); q.pop();     // u = 目前處理的同學
            for (int v : adj[u]) {          // v = 和 u 不合的同學，一定要和 u 不同隊
                if (team[v] == 0) { team[v] = 3 - team[u]; q.push(v); }   // 3 − 1 = 2，3 − 2 = 1
                else if (team[v] == team[u]) { cout << "NO\n"; return 0; }   // 不合的兩人同隊 → 有奇環
            }
        }
    }
    cout << "YES\n";
    for (int i = 1; i <= n; i++) cout << team[i] << " \n"[i == n];   // i = 同學編號
}
