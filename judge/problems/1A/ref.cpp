#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);
    int n, m;                        // n = 人數（點數），m = 握手次數（邊數）
    cin >> n >> m;
    vector<int> deg(n + 1, 0);       // deg[i] = 第 i 個人握了幾次手，也就是點 i 的度數
    for (int i = 0; i < m; i++) {    // i = 正在讀第幾次握手
        int u, v;                    // 這次握手的兩個人
        cin >> u >> v;
        deg[u]++; deg[v]++;          // 無向邊兩端各加一
    }
    int odd = 0;                     // 握手次數是奇數的人數
    for (int i = 1; i <= n; i++) {   // i = 目前輸出的是第幾個人
        cout << deg[i] << " \n"[i == n];   // 最後一個人後面換行，其他人後面接空白
        if (deg[i] % 2 == 1) odd++;
    }
    cout << odd << "\n";
}
