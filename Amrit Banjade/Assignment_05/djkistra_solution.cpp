#include <iostream>
#include <vector>
#include <queue>
#include <climits>

using namespace std;

// Define the structure for a graph edge
struct Edge {
    int to, weight;
};

// Define the graph as an adjacency list
typedef vector<vector<Edge> > Graph; // Note the space between the right angle brackets

// Function to perform Dijkstra's algorithm
void dijkstra(const Graph &graph, int start, vector<int> &dist) {
    int n = graph.size();
    dist.assign(n, INT_MAX);
    dist[start] = 0;
    
    priority_queue<pair<int, int>, vector<pair<int, int> >, greater<pair<int, int> > > pq; // Note the space between the right angle brackets
    pq.push(make_pair(0, start));

    while (!pq.empty()) {
        int d = pq.top().first;
        int u = pq.top().second;
        pq.pop();

        if (d > dist[u]) continue;

        for (const Edge &edge : graph[u]) {
            int v = edge.to;
            int weight = edge.weight;
            if (dist[u] + weight < dist[v]) {
                dist[v] = dist[u] + weight;
                pq.push(make_pair(dist[v], v));
            }
        }
    }
}

// Main function to read input and execute the algorithm
int main() {
    int n, k, m;
    cout << "Enter number of nodes, start node, and number of edges: ";
    cin >> n >> k >> m;

    Graph graph(n + 1);

    cout << "Enter the edges (source, destination, weight):\n";
    for (int i = 0; i < m; ++i) {
        int u, v, w;
        cin >> u >> v >> w;
        graph[u].push_back((Edge){v, w}); // Construct the Edge object properly
    }

    vector<int> dist;
    dijkstra(graph, k, dist);

    int max_time = -1;
    for (int i = 1; i <= n; ++i) {
        if (dist[i] == INT_MAX) {
            cout << "-1\n";
            return 0;
        }
        if (dist[i] > max_time)
            max_time = dist[i];
    }

    cout << max_time << endl;
    return 0;
}

// Use -std=c++11 flag  so that it won't give you warning

