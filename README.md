# Graph-Implementation

Implementation of both directed and undirected graph ADTs in Python.


**Undirected Graph**

Implementation method: Adjacency list with unweighted edges

Implemented functions:

- Add a vertex

- Add an edge between two vertices

- Remove an existing edge

- Remove a vertex and any existing edges to that vertex
  
- Get vertices - returns a list of all vertices
  
- Get edges - returns a list of existing edges as a tuple of starting and ending vertices (eg [('A', 'B'), ...])
  
- Determine whether a given path through the graph is valid
  
- Depth first search from a starting vertex to an optional ending vertex or the end of the graph

- Breadth first search from a starting vertex to an optional ending vertex or the end of the graph

- Count the number of connected components in the graph

- Determine whether or not there is at least 'one' cycle in the graph



**Direct Graph**

Implementation method: Adjacency matrix with weighted edges

Implemented functions:

- Add a vertex

- Add an edge between two vertices

- Remove an existing edge

- Get vertices - returns a list of all vertices
  
- Get edges - returns a list of existing edges as a tuple of starting/ending vertices and edge weight (eg [('1', '3', '15'), ...])

- Determine whether a given path through the graph is valid

- Depth first search from a starting vertex to an optional ending vertex or the end of the graph

- Breadth first search from a starting vertex to an optional ending vertex or the end of the graph

- Determine whether or not there is at least 'one' cycle in the graph

- Dijkstra's algorithm
