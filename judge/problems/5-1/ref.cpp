#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);
    int n, m;                              // n = 關卡數，m = 解鎖規則數
    cin >> n >> m;
    vector<vector<int>> adj(n + 1);        // adj[a] = 以 a 為前置關卡的關卡
    vector<int> indeg(n + 1, 0);           // indeg[b] = b 還有幾條規則沒被滿足
    for (int i = 0; i < m; i++) {          // i = 正在讀第幾條規則
        int a, b;                          // 要先通過 a 才能挑戰 b
        cin >> a >> b;
        adj[a].push_back(b);
        indeg[b]++;                        // 重複的規則算兩次，之後也會被扣兩次
    }
    queue<int> q;                          // q = 規則全部滿足、可以挑戰的關卡
    for (int i = 1; i <= n; i++)           // i = 關卡編號
        if (indeg[i] == 0) q.push(i);
    vector<bool> cleared(n + 1, false);    // cleared[v] = 關卡 v 最後能不能通過
    while (!q.empty()) {
        int u = q.front(); q.pop();        // u = 這一步通過的關卡
        cleared[u] = true;
        for (int v : adj[u])               // v = 以 u 為前置的關卡，少了一條沒滿足的規則
            if (--indeg[v] == 0) q.push(v);
    }
    vector<int> stuck;                     // stuck = 永遠無法通過的關卡，由小到大
    for (int i = 1; i <= n; i++)           // i = 關卡編號
        if (!cleared[i]) stuck.push_back(i);
    cout << stuck.size() << "\n";
    for (size_t i = 0; i < stuck.size(); i++)   // i = stuck 中的第幾個
        cout << stuck[i] << " \n"[i + 1 == stuck.size()];
}
