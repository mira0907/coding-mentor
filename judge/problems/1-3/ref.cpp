#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);
    // n = 島數
    // m = 停駛航線的紀錄筆數
    int n, m;
    cin >> n >> m;
    vector<vector<int>> stop(n + 1);     // stop[u] = 和 u 之間航線停駛的島（只存停駛的，O(n + m)）
    for (int i = 0; i < m; i++) {        // i = 正在讀第幾筆停駛紀錄
        // u = 停駛航線的一端
        // v = 停駛航線的另一端
        int u, v;
        cin >> u >> v;
        stop[u].push_back(v);
        stop[v].push_back(u);
    }
    vector<int> rest(n);                 // rest = 還沒分進任何航運圈的島
    iota(rest.begin(), rest.end(), 1);   // 一開始是 1 到 n 全部
    vector<int> keep;                    // 掃描 rest 時，暫存這次留下來的島
    vector<int> mark(n + 1, 0);          // mark[v] == u 代表 u–v 停駛，處理 u 時 v 不能直接到
    vector<int> sizes;                   // sizes[i] = 第 i 個航運圈的島數
    queue<int> q;                        // BFS 佇列，存已分進目前航運圈、還沒展開的島
    while (!rest.empty()) {
        int s = rest.back(); rest.pop_back();   // s = 新航運圈的第一座島
        q.push(s);
        int cnt = 1;                     // 目前這個航運圈的島數
        while (!q.empty()) {
            int u = q.front(); q.pop();  // u = 正在展開的島
            for (int v : stop[u]) mark[v] = u;   // 標記和 u 停駛的島
            keep.clear();
            for (int v : rest) {         // v = 每座還沒分組的島
                if (mark[v] == u) keep.push_back(v);   // u–v 停駛，先留著
                else { q.push(v); cnt++; }             // u–v 有航線，v 和 u 同一圈
            }
            rest.swap(keep);             // 留下來的島成為新的 rest
        }
        sizes.push_back(cnt);
    }
    sort(sizes.begin(), sizes.end());
    cout << sizes.size() << "\n";
    for (int i = 0; i < (int)sizes.size(); i++)   // i = 第幾個航運圈（已由小到大排好）
        cout << sizes[i] << " \n"[i + 1 == (int)sizes.size()];
}
