#include <bits/stdc++.h>
using namespace std;
using ll = long long;
int n,m;
queue<int> mylist;
priority_queue<int,vector<int>,greater<int>> ans;
vector<pair<int,int>> bre;
#ifdef LOCAL
#define dbg(x) cerr << #x << " = " << (x) << '\n'
#else
#define dbg(x)
#endif

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    cin>>n>>m;
    for(int i=0;i<n;i++){
        mylist.push(i);
    }
    vector<int>out(n,false);
    vector<vector<int>> stop(n);
    for(int i=0;i<m;i++){
        int a,b;
        cin>>a>>b;
        stop[a-1].push_back(b-1);
        stop[b-1].push_back(a-1);
        bre.push_back({a-1,b-1});
    }
    while(!mylist.empty()){
        int save=1;
        int x=mylist.front();
        mylist.pop();
        queue<int> bfs;
        bfs.push(x);
        while(!bfs.empty()){
            int s=bfs.front();
            bfs.pop();
            int len=mylist.size();
            vector<bool> mark(n,false);
            for(int i=0;i<stop[s].size();i++){
                mark[stop[s][i]]=true;
            }
            for(int i=0;i<len;i++){
                int com=mylist.front();
                if (mark[com]){
                    mylist.push(com);
                }
                else {bfs.push(com); save++;}
                mylist.pop();
            }
        }
        ans.push(save);
    }
    cout<<ans.size()<<endl;
    while(!ans.empty()){
        cout<<ans.top()<<" ";
        ans.pop();
    }
    return 0;
}
