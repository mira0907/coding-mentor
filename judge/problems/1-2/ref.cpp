#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);
    int n;                               // n = 人數
    cin >> n;
    vector<int> a(n + 1);                // a[i] = 第 i 個人會把消息傳給誰
    for (int i = 1; i <= n; i++) cin >> a[i];
    // state[v]：0 = 還沒走過，1 = 在這一輪正在走的路上，2 = 答案已經算好
    vector<int> state(n + 1, 0);
    vector<int> pos(n + 1, 0);           // pos[v] = v 在這一輪路徑 path 裡的位置
    vector<int> ans(n + 1, 0);           // ans[v] = 從 v 開始傳，總共有幾個人聽到
    vector<int> path;                    // 這一輪從起點一路跳過的點，依先後順序
    for (int s = 1; s <= n; s++) {       // s = 這一輪的起點
        if (state[s] != 0) continue;
        path.clear();
        int v = s;                       // v = 目前跳到的人
        while (state[v] == 0) {          // 一直往下一個人跳，直到遇到走過的人
            state[v] = 1;
            pos[v] = path.size();
            path.push_back(v);
            v = a[v];
        }
        int k = path.size();             // k = path 裡還沒算好答案的部分的長度
        if (state[v] == 1) {             // 撞到這一輪自己走過的點：path[pos[v]] 之後是一個新的環
            int len = k - pos[v];        // len = 環的長度
            for (int i = pos[v]; i < k; i++) {   // i = 環上的點在 path 裡的位置
                ans[path[i]] = len;      // 環上的人：消息繞一圈就停，剛好 len 個人
                state[path[i]] = 2;
            }
            k = pos[v];                  // 環前面那一段還沒算
        }
        for (int i = k - 1; i >= 0; i--) {   // 從靠近環的那一端往回算，i = 在 path 裡的位置
            int u = path[i];             // u = 正在算答案的人
            ans[u] = ans[a[u]] + 1;      // 自己 1 人，加上從下一個人開始會聽到的人
            state[u] = 2;
        }
    }
    for (int i = 1; i <= n; i++)         // i = 目前輸出的人
        cout << ans[i] << " \n"[i == n];
}
