#include <bits/stdc++.h>
using namespace std;
using ll = long long;
vector<bool> vis;
#ifdef LOCAL
#define dbg(x) cerr << #x << " = " << (x) << '\n'
#else
#define dbg(x)
#endif
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin>>n;
    vector<int> adj(n,-1);
    vector<int> ans(n,1);
    vector<int> check(n,0);
    for(int i=0;i<n;i++){
        int a;
        cin>>a;
        adj[i]=a-1;
    }
    for(int i=0;i<n;i++){
        /*if (check[i]==0 and i==adj[i]){
            check[i]=2;
        }
        else if (check[adj[i]]==1){
            ans[i]=ans[adj[i]]++;
            check[i]=2;
            check[adj[i]]=2;
        }
        else{
            check[i]=1;
            ans[i]++;
        }*/
        int u=i;
        vector<int> path;
        while(check[u]==0){
            check[u]=1;
            path.push_back(u);
            u=adj[u];
            if (check[u]==1){
                auto it=find(path.begin(),path.end(),u);
                int index=distance(path.begin(),it);
                for(int j=0;j<path.size();j++){
                    ans[path[j]]=path.size()-index;
                    if (j<index) ans[path[j]]+=index-j;
                    check[path[j]]=2;
                }
                break;
            }
            else if (check[u]==2){
                for(int j=0;j<path.size();j++){
                    ans[path[j]]=path.size()-j+ans[u];
                    check[path[j]]=2;
                }
            }
        }
    }
    for(int i=0;i<n;i++) cout<<ans[i]<<" ";
    return 0;
}
