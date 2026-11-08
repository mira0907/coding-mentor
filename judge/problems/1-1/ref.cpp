#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);
    // n = 路口數
    // m = 道路紀錄筆數
    int n, m;
    cin >> n >> m;
    vector<pair<int,int>> roads;         // roads[i] = 第 i 條非自環道路，存成 (小編號, 大編號)
    int loops = 0;                       // 自環的條數
    for (int i = 0; i < m; i++) {        // i = 正在讀第幾筆紀錄
        // u = 這筆紀錄的一端
        // v = 這筆紀錄的另一端
        int u, v;
        cin >> u >> v;
        if (u == v) { loops++; continue; }      // 自環直接丟掉
        roads.push_back({min(u, v), max(u, v)}); // 統一小的在前，(2, 1) 和 (1, 2) 才會一樣
    }
    sort(roads.begin(), roads.end());    // 排序後，同一對路口的紀錄會排在一起
    int dup = 0;                         // 多餘的重複道路條數
    vector<int> deg(n + 1, 0);           // deg[x] = 整理後路口 x 的度數
    for (int i = 0; i < (int)roads.size(); i++) {   // i = 排序後的第幾條道路
        if (i > 0 && roads[i] == roads[i - 1]) { dup++; continue; }   // 和前一條相同，是重邊
        deg[roads[i].first]++;           // 第一次出現的道路才保留，兩端度數各加 1
        deg[roads[i].second]++;
    }
    cout << loops << " " << dup << "\n";
    for (int x = 1; x <= n; x++)         // x = 目前輸出的路口
        cout << deg[x] << " \n"[x == n];
}
