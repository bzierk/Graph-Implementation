# Course: CS 261
# Author: Bryan Zierk
# Assignment: Project 6 - Graph Implementation
# Description: Implementation of an undirected graph which allows users to add/remove edges and vertices, get veritices
# and edges, establish if there is a valid path, perform DFS/BFS, count connected components, and determine whether
# or not there is are specific cycles.

import heapq
from collections import deque


class UndirectedGraph:
    """
    Class to implement undirected graph
    - duplicate edges not allowed
    - loops not allowed
    - no edge weights
    - vertex names are strings
    """

    def __init__(self, start_edges=None):
        """
        Store graph info as adjacency list
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.adj_list = dict()

        # populate graph with initial vertices and edges (if provided)
        # before using, implement add_vertex() and add_edge() methods
        if start_edges is not None:
            for u, v in start_edges:
                self.add_edge(u, v)

    def __str__(self):
        """
        Return content of the graph in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = [f'{v}: {self.adj_list[v]}' for v in self.adj_list]
        out = '\n  '.join(out)
        if len(out) < 70:
            out = out.replace('\n  ', ', ')
            return f'GRAPH: {{{out}}}'
        return f'GRAPH: {{\n  {out}}}'

    # ------------------------------------------------------------------ #
    def _is_adjacent(self, u: str, v: str):
        """
        Helper function which returns True of two vertices are adjacent, otherwise returns False
        """
        if u not in self.adj_list or v not in self.adj_list:
            return False
        elif u in self.adj_list[v]:
            return True
        else:
            return False

    def _get_degree(self, v: str):
        """
        Helper function which returns the degree of a vertex
        """
        return len(self.adj_list[v])

    def add_vertex(self, v: str) -> None:
        """
        Adds a new unique vertex to the graph. If a vertex with the same value already exists, method does nothing.
        """
        self.adj_list.setdefault(v, [])

    def add_edge(self, u: str, v: str) -> None:
        """
        Add edge to the graph
        """
        if u != v:
            for vertex in [u, v]:
                self.add_vertex(vertex)
            if not self._is_adjacent(u, v):
                self.adj_list[u].append(v)
                self.adj_list[v].append(u)
                self.adj_list[u].sort()
                self.adj_list[v].sort()

    def remove_edge(self, v: str, u: str) -> None:
        """
        Remove edge from the graph
        """
        if not self._is_adjacent(u, v):
            return

        self.adj_list[u].remove(v)
        self.adj_list[v].remove(u)

    def remove_vertex(self, v: str) -> None:
        """
        Remove vertex and all connected edges
        """
        if v not in self.adj_list:
            return

        for vertex in self.adj_list:
            if v in self.adj_list[vertex]:
                self.adj_list[vertex].remove(v)

        self.adj_list.pop(v, None)

    def get_vertices(self) -> []:
        """
        Return list of vertices in the graph (any order)
        """
        vertex_list = []

        for v in self.adj_list:
            vertex_list.append(v)

        return vertex_list

    def get_edges(self) -> []:
        """
        Return list of edges in the graph (any order)
        """
        edge_list = []

        for v in self.adj_list:
            for u in self.adj_list[v]:
                if (u, v) not in edge_list:
                    edge_list.append((v, u))

        return edge_list
        

    def is_valid_path(self, path: []) -> bool:
        """
        Return true if provided path is valid, False otherwise
        """
        if not path:
            return True
        else:
            if len(path) == 1:
                if path[0] not in self.adj_list:
                    return False
            u, v = 0, 1
            while v <= len(path) - 1:
                if not self._is_adjacent(path[u], path[v]):
                    return False
                else:
                    u += 1
                    v += 1

            return True

    def dfs(self, v_start, v_end=None) -> []:
        """
        Return list of vertices visited during DFS search
        Vertices are picked in alphabetical order
        """
        if v_start not in self.adj_list:
            return []

        visited_vertices = []
        dfs_stack = [v_start]
        while len(dfs_stack) != 0:
            v = dfs_stack.pop()
            if v not in visited_vertices:
                visited_vertices.append(v)
                for vertex in reversed(self.adj_list[v]):
                    if vertex not in visited_vertices:
                        dfs_stack.append(vertex)
            if v == v_end:
                return visited_vertices

        return visited_vertices

    def bfs(self, v_start, v_end=None) -> []:
        """
        Return list of vertices visited during BFS search
        Vertices are picked in alphabetical order
        """
        if v_start not in self.adj_list:
            return []

        visited_vertices = []
        bfs_queue = deque()
        bfs_queue.append(v_start)
        while len(bfs_queue) != 0:
            v = bfs_queue.popleft()
            if v not in visited_vertices:
                visited_vertices.append(v)
                for vertex in self.adj_list[v]:
                    if vertex not in visited_vertices:
                        bfs_queue.append(vertex)
            if v == v_end:
                return visited_vertices

        return visited_vertices
        

    def count_connected_components(self):
        """
        Return number of connected componets in the graph
        """
        count = 0
        counted_vertices = []
        for v in self.adj_list:
            if v not in counted_vertices:
                counted_vertices = counted_vertices + self.dfs(v)
                count += 1

        return count

    def has_cycle(self):
        """
        Return True if graph contains a cycle, False otherwise
        """
        for v in self.adj_list:
            visited_vertices = []
            dfs_stack = [v]
            par = v
            while len(dfs_stack) != 0:
                temp = par
                par = v
                v = dfs_stack.pop()
                if v == par:
                    par = temp
                if v in visited_vertices and v != par:
                    return True

                if v not in visited_vertices:
                    visited_vertices.append(v)
                    for vertex in reversed(self.adj_list[v]):
                        if vertex not in visited_vertices:
                            dfs_stack.append(vertex)

        return False


if __name__ == '__main__':

    print("\nPDF - method add_vertex() / add_edge example 1")
    print("----------------------------------------------")
    g = UndirectedGraph()
    print(g)

    for v in 'ABCDE':
        g.add_vertex(v)
    print(g)

    g.add_vertex('A')
    print(g)

    for u, v in ['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE', ('B', 'C')]:
        g.add_edge(u, v)
    print(g)


    print("\nPDF - method remove_edge() / remove_vertex example 1")
    print("----------------------------------------------------")
    g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE'])
    g.remove_vertex('DOES NOT EXIST')
    g.remove_edge('A', 'B')
    g.remove_edge('X', 'B')
    print(g)
    g.remove_vertex('D')
    print(g)


    print("\nPDF - method get_vertices() / get_edges() example 1")
    print("---------------------------------------------------")
    g = UndirectedGraph()
    print(g.get_edges(), g.get_vertices(), sep='\n')
    g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE'])
    print(g.get_edges(), g.get_vertices(), sep='\n')


    print("\nPDF - method is_valid_path() example 1")
    print("--------------------------------------")
    g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE'])
    test_cases = ['ABC', 'ADE', 'ECABDCBE', 'ACDECB', '', 'D', 'Z']
    for path in test_cases:
        print(list(path), g.is_valid_path(list(path)))


    print("\nPDF - method dfs() and bfs() example 1")
    print("--------------------------------------")
    edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    g = UndirectedGraph(edges)
    test_cases = 'ABCDEGH'
    for case in test_cases:
        print(f'{case} DFS:{g.dfs(case)} BFS:{g.bfs(case)}')
    print('-----')
    for i in range(1, len(test_cases)):
        v1, v2 = test_cases[i], test_cases[-1 - i]
        print(f'{v1}-{v2} DFS:{g.dfs(v1, v2)} BFS:{g.bfs(v1, v2)}')


    print("\nPDF - method count_connected_components() example 1")
    print("---------------------------------------------------")
    edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    g = UndirectedGraph(edges)
    test_cases = (
        'add QH', 'remove FG', 'remove GQ', 'remove HQ',
        'remove AE', 'remove CA', 'remove EB', 'remove CE', 'remove DE',
        'remove BC', 'add EA', 'add EF', 'add GQ', 'add AC', 'add DQ',
        'add EG', 'add QH', 'remove CD', 'remove BD', 'remove QG')
    for case in test_cases:
        command, edge = case.split()
        u, v = edge
        g.add_edge(u, v) if command == 'add' else g.remove_edge(u, v)
        print(g.count_connected_components(), end=' ')
    print()


    print("\nPDF - method has_cycle() example 1")
    print("----------------------------------")
    edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    g = UndirectedGraph(edges)
    test_cases = (
        'add QH', 'remove FG', 'remove GQ', 'remove HQ',
        'remove AE', 'remove CA', 'remove EB', 'remove CE', 'remove DE',
        'remove BC', 'add EA', 'add EF', 'add GQ', 'add AC', 'add DQ',
        'add EG', 'add QH', 'remove CD', 'remove BD', 'remove QG',
        'add FG', 'remove GE')
    for case in test_cases:
        command, edge = case.split()
        u, v = edge
        g.add_edge(u, v) if command == 'add' else g.remove_edge(u, v)
        print('{:<10}'.format(case), g.has_cycle())
