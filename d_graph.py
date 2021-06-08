# Course: CS261 - Data Structures
# Author:
# Assignment:
# Description:


import heapq
from collections import deque


class DirectedGraph:
    """
    Class to implement directed weighted graph
    - duplicate edges not allowed
    - loops not allowed
    - only positive edge weights
    - vertex names are integers
    """

    def __init__(self, start_edges=None):
        """
        Store graph info as adjacency matrix
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.v_count = 0
        self.adj_matrix = []

        # populate graph with initial vertices and edges (if provided)
        # before using, implement add_vertex() and add_edge() methods
        if start_edges is not None:
            v_count = 0
            for u, v, _ in start_edges:
                v_count = max(v_count, u, v)
            for _ in range(v_count + 1):
                self.add_vertex()
            for u, v, weight in start_edges:
                self.add_edge(u, v, weight)

    def __str__(self):
        """
        Return content of the graph in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if self.v_count == 0:
            return 'EMPTY GRAPH\n'
        out = '   |'
        out += ' '.join(['{:2}'.format(i) for i in range(self.v_count)]) + '\n'
        out += '-' * (self.v_count * 3 + 3) + '\n'
        for i in range(self.v_count):
            row = self.adj_matrix[i]
            out += '{:2} |'.format(i)
            out += ' '.join(['{:2}'.format(w) for w in row]) + '\n'
        out = f"GRAPH ({self.v_count} vertices):\n{out}"
        return out

    # ------------------------------------------------------------------ #
    def _valid_vertex(self, vertex):
        """
        Helper function which returns True if a vertex is valid, otherwise False.
        """
        if 0 <= vertex < self.v_count:
            return True
        else:
            return False

    def add_vertex(self) -> int:
        """
        Adds a new vertex to the graph and returns the number of vertices in the graph.
        """
        self.v_count += 1
        while len(self.adj_matrix) < self.v_count:
            self.adj_matrix.append([])
            for i in range(len(self.adj_matrix)):
                while len(self.adj_matrix[i]) < self.v_count:
                    self.adj_matrix[i].append(0)

        return self.v_count

    def add_edge(self, src: int, dst: int, weight=1) -> None:
        """
        Adds an edge to the graph. If the edge already exists, the weight of the edge is updated.
        """
        for entry in [src, dst]:
            if not self._valid_vertex(entry):
                return

        if weight < 0 or src == dst:
            return

        self.adj_matrix[src][dst] = weight



    def remove_edge(self, src: int, dst: int) -> None:
        """
        Removes an edge between provided source and destination vertices
        """
        for entry in [src, dst]:
            if not self._valid_vertex(entry):
                return

        self.adj_matrix[src][dst] = 0


    def get_vertices(self) -> []:
        """
        Returns a list of vertices in the graph
        """
        vertex_list = []

        for v in range(len(self.adj_matrix)):
            vertex_list.append(v)

        return vertex_list

    def get_edges(self) -> []:
        """
        Returns a list of edges as a tuple of incident vertices and weight of their connecting edge.
        """
        edge_list = []

        for i in range(len(self.adj_matrix)):
            for j in range(len(self.adj_matrix[i])):
                if self.adj_matrix[i][j] != 0:
                    edge_list.append((i, j, self.adj_matrix[i][j]))

        return edge_list

    def is_valid_path(self, path: []) -> bool:
        """
        Determines whether a given path is valid and represents True if it is, otherwise returns False
        """
        if not path:
            return True
        elif len(path) == 1 and 0 <= path[0] < self.v_count:
            return True
        else:
            src, dest = 0, 1
            while dest < len(path):
                if self.adj_matrix[path[src]][path[dest]] == 0:
                    return False
                src += 1
                dest += 1
        return True

    def dfs(self, v_start, v_end=None) -> []:
        """
        Performs a depth-first search of the graph and returns a list of vertices in the order they were visited.
        If the starting vertex is not a valid vertex, returns an empty list. Accepts an optional end vertex parameter,
        if provided, search will conclude when it explores the end vertex.
        """
        if not self._valid_vertex(v_start):
            return []

        visited_vertices = []
        dfs_stack = [v_start]
        while len(dfs_stack) != 0:
            v = dfs_stack.pop()
            if v not in visited_vertices:
                visited_vertices.append(v)
                for vertex in range(len(self.adj_matrix[v]) - 1, -1, -1):
                    if self.adj_matrix[v][vertex] != 0:
                        dfs_stack.append(vertex)
            if v == v_end:
                return visited_vertices

        return visited_vertices

    def bfs(self, v_start, v_end=None) -> []:
        """
        Performs a breadth-first search the graph and returns a list of vertices in the order they were visited.
        If the starting vertex is not a valid vertex, returns an empty list. Accepts an optional end vertex parameter,
        if provided, search will conclude when it explores the end vertex.
        """
        if not self._valid_vertex(v_start):
            return []

        visited_vertices = []
        bfs_queue = deque()
        bfs_queue.append(v_start)
        while len(bfs_queue) != 0:
            v = bfs_queue.popleft()
            if v not in visited_vertices:
                visited_vertices.append(v)
                for vertex in range(len(self.adj_matrix[v])):
                    if self.adj_matrix[v][vertex] != 0 and vertex not in self.adj_matrix:
                        bfs_queue.append(vertex)
            if v == v_end:
                return visited_vertices

        return visited_vertices

    def has_cycle(self):
        """
        If a graph contains at least one cycle, returns True, otherwise False.
        """
        for v in range(len(self.adj_matrix)):
            base_node = v
            visited_vertices = []
            dfs_stack = [v]
            par = v
            while len(dfs_stack) != 0:
                temp = par
                par = v
                v = dfs_stack.pop()
                if v == par:
                    par = temp
                if len(visited_vertices) > 1 and v == base_node or base_node in dfs_stack:
                    return True
                elif v not in visited_vertices:
                    visited_vertices.append(v)
                    for vertex in range(len(self.adj_matrix[v]) - 1, -1, -1):
                        if self.adj_matrix[v][vertex] != 0 and vertex not in dfs_stack:
                            dfs_stack.append(vertex)

        return False

    def dijkstra(self, src: int) -> []:
        """
        Uses dijkstra's algorithm to determine the shortest path from a source vertex to each other vertex in the
        graph. If a vertex is unreachable, "inf" is displayed.
        """
        if not self._valid_vertex(src):
            return []
        else:
            visited_vertices = {}
            nodes = [(0, src)]
            while len(nodes) != 0:
                d, v = heapq.heappop(nodes)
                if v not in visited_vertices:
                    visited_vertices[v] = d
                    for vertex in range(len(self.adj_matrix[v])):
                        if self.adj_matrix[v][vertex] != 0:
                            d_i = d + self.adj_matrix[v][vertex]
                            heapq.heappush(nodes, (d_i, vertex))
            distances = []
            for key in range(self.v_count):
                if key not in visited_vertices:
                    distances.append(float('inf'))
                else:
                    distances.append(visited_vertices[key])

            return distances

if __name__ == '__main__':

    print("\nPDF - method add_vertex() / add_edge example 1")
    print("----------------------------------------------")
    g = DirectedGraph()
    print(g)
    for _ in range(5):
        g.add_vertex()
    print(g)

    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    for src, dst, weight in edges:
        g.add_edge(src, dst, weight)
    print(g)


    print("\nPDF - method get_edges() example 1")
    print("----------------------------------")
    g = DirectedGraph()
    print(g.get_edges(), g.get_vertices(), sep='\n')
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    print(g.get_edges(), g.get_vertices(), sep='\n')


    print("\nPDF - method is_valid_path() example 1")
    print("--------------------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    test_cases = [[0, 1, 4, 3], [1, 3, 2, 1], [0, 4], [4, 0], [], [2]]
    for path in test_cases:
        print(path, g.is_valid_path(path))


    print("\nPDF - method dfs() and bfs() example 1")
    print("--------------------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    for start in range(5):
        print(f'{start} DFS:{g.dfs(start)} BFS:{g.bfs(start)}')


    print("\nPDF - method has_cycle() example 1")
    print("----------------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)

    edges_to_remove = [(3, 1), (4, 0), (3, 2)]
    for src, dst in edges_to_remove:
        g.remove_edge(src, dst)
        print(g.get_edges(), g.has_cycle(), sep='\n')

    edges_to_add = [(4, 3), (2, 3), (1, 3), (4, 0)]
    for src, dst in edges_to_add:
        g.add_edge(src, dst)
        print(g.get_edges(), g.has_cycle(), sep='\n')
    print('\n', g)

    print("\nGradeScope - method has_cycle() example 2")
    print("---------------------------------------")
    edges = [(0, 3, 1), (1, 2, 1), (1, 6, 1), (8, 11, 1), (9, 6, 1), (10, 0, 1), (10, 1, 1),
             (9, 10, 1), (9, 11, 1), (11, 1, 1), (11, 7, 1), (12, 4, 1)]
    g = DirectedGraph(edges)

    print(g.has_cycle())


    print("\nPDF - dijkstra() example 1")
    print("--------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    for i in range(5):
        print(f'DIJKSTRA {i} {g.dijkstra(i)}')
    g.remove_edge(4, 3)
    print('\n', g)
    for i in range(5):
        print(f'DIJKSTRA {i} {g.dijkstra(i)}')
