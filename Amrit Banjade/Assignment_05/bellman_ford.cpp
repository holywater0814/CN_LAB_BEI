#include <iostream>
#include <vector>
#include <climits>

using namespace std;

class Solution {
public:
    int findCheapestPrice(int n, vector<vector<int> >& flights, int src, int dst, int K) {
        // Initialize distances array with infinity
        vector<int> distances(n, INT_MAX);
        distances[src] = 0;

        // Perform Bellman-Ford algorithm for K+1 iterations (K stops means K+1 edges)
        for (int i = 0; i <= K; ++i) {
            // Create a temporary copy of distances to update distances without affecting current iteration's calculations
            vector<int> temp_distances = distances;
            for (const auto& flight : flights) {
                int u = flight[0], v = flight[1], w = flight[2];
                if (distances[u] == INT_MAX) {
                    continue;
                }
                if (distances[u] + w < temp_distances[v]) {
                    temp_distances[v] = distances[u] + w;
                }
            }
            distances = temp_distances;
        }

        // If the distance to destination is still infinity, it means there is no such route
        return distances[dst] == INT_MAX ? -1 : distances[dst];
    }
};

int main() {
    int n, m, src, dst, K;
    
    cout << "Enter the number of cities (n): ";
    cin >> n;
    
    cout << "Enter the number of flights (m): ";
    cin >> m;
    
    vector<vector<int> > flights(m, vector<int>(3));
    
    cout << "Enter the flights (from, to, price) one by one:" << endl;
    for (int i = 0; i < m; ++i) {
        cin >> flights[i][0] >> flights[i][1] >> flights[i][2];
    }
    
    cout << "Enter the source city (src): ";
    cin >> src;
    
    cout << "Enter the destination city (dst): ";
    cin >> dst;
    
    cout << "Enter the maximum number of stops (K): ";
    cin >> K;
    
    Solution sol;
    int result = sol.findCheapestPrice(n, flights, src, dst, K);
    
    if (result != -1) {
        cout << "The cheapest price is: " << result << endl;
    } else {
        cout << "There is no such route." << endl;
    }
    
    return 0;
}

// Use -std=c++11 flag 