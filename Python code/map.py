from tile import Tile
import matplotlib.pyplot as plt
import networkx as nx
from collections import defaultdict

class Map:
    def __init__(self, n:int, m:int, type:str):
        l = []
        for _ in range(m):
            k = []
            for _ in range(n):
                k.append(None)
            l.append(k)

        self.n = n  # Number of tiles in x direction
        self.m = m  # Number of tiles in y direction
        self.tiles = l  # 2D array of tiles of size n x m
        self.type = type

    def __str__(self):
        return "Map"
    
    def __repr__(self):
        return self.tiles
    
    def __iter__(self):
        """Allows iteration over all Tile objects in the Map."""
        for row in self.tiles:
            for tile in row:
                yield tile
    
    def setTile(self, tile: Tile, x: int, y: int):
        tile.x = x
        tile.y = y
        self.tiles[y][x] = tile

    def getTile(self, x: int, y: int) -> Tile:
        return self.tiles[y][x]
    
    def updateNeighbours(self):
        if self.type == "plane":
            for j in range(self.m):
                for i in range(self.n):
                    t = self.tiles[j][i]
                    if i > 0:
                        t.setNeighbour("left", self.tiles[j][i-1])
                    if i < self.n - 1:
                        t.setNeighbour("right", self.tiles[j][i+1])
                    if j > 0:
                        t.setNeighbour("bottom", self.tiles[j-1][i])
                    if j < self.m - 1:
                        t.setNeighbour("top", self.tiles[j+1][i])
        elif self.type == "cylinder":
            for j in range(self.m):
                for i in range(self.n):
                    t = self.tiles[j][i]
                    # Wrap horizontally
                    t.setNeighbour("left", self.tiles[j][(i-1) % self.n])
                    t.setNeighbour("right", self.tiles[j][(i+1) % self.n])
                    # No vertical wrapping
                    if j > 0:
                        t.setNeighbour("bottom", self.tiles[j-1][i])
                    else:
                        t.setNeighbour("bottom", None)  # No neighbor below the bottom row
                    if j < self.m - 1:
                        t.setNeighbour("top", self.tiles[j+1][i])
                    else:
                        t.setNeighbour("top", None)  # No neighbor above the top row
        elif self.type == "torus":
            for j in range(self.m):
                for i in range(self.n):
                    t = self.tiles[j][i]
                    t.setNeighbour("left", self.tiles[j][(i-1) % self.n])  # Wrap horizontally
                    t.setNeighbour("right", self.tiles[j][(i+1) % self.n])  # Wrap horizontally
                    t.setNeighbour("bottom", self.tiles[(j-1) % self.m][i])  # Wrap vertically
                    t.setNeighbour("top", self.tiles[(j+1) % self.m][i])  # Wrap vertically

    def plot(self, color=False):
        plt.clf()
        for j in range(len(self.tiles)):
            for i in range(len(self.tiles[j])):
                t = self.tiles[j][i]
                t.plot(color=color)
        
        plt.axis('equal')
        plt.show()

    def count_1d_components(self) -> int:
        """
        Counts the number of 1-dimensional components in a map of tiles.

        Args:
            tile_map: A Map of Tile objects.

        Returns:
            (int, int): Tuple of number of simple closed curves and non-closed curves.
        """
        # Graph structure to store all connections
        graph = defaultdict(list)

        # Add intra-tile connections
        for tile in self:
            for edge_index in tile.connections:
                local_edge = tile.edges[edge_index]
                p1_global = tile.get_global_coordinates(tile.points[local_edge[0]])
                p2_global = tile.get_global_coordinates(tile.points[local_edge[1]])
                graph[p1_global].append(p2_global)
                graph[p2_global].append(p1_global)

        # Add inter-tile connections
        for i in range(self.m):  # Iterate over rows
            for j in range(self.n):  # Iterate over columns
                tile = self.tiles[i][j]
                edge_connections = []
                for e in [tile.edges[edge_index] for edge_index in tile.connections]:
                    edge_connections.extend(e)

                # Match left edge with right edge of the left neighbour
                if tile.left_neighbour is not None:
                    left_neighbour = tile.left_neighbour
                    for p1, p2 in zip(tile.left_edge, left_neighbour.right_edge):
                        p1_index = tile.points.index(p1)
                        if p1_index in edge_connections:
                            p1_global = tile.get_global_coordinates(p1)
                            p2_global = left_neighbour.get_global_coordinates(p2)
                            if p1_global != p2_global:
                                graph[p1_global].append(p2_global)
                                graph[p2_global].append(p1_global)
                
                # Match right edge with left edge of the right neighbour
                if tile.right_neighbour is not None:
                    right_neighbour = tile.right_neighbour
                    for p1, p2 in zip(tile.right_edge, right_neighbour.left_edge):
                        p1_index = tile.points.index(p1)
                        if p1_index in edge_connections:
                            p1_global = tile.get_global_coordinates(p1)
                            p2_global = right_neighbour.get_global_coordinates(p2)
                            if p1_global != p2_global:
                                graph[p1_global].append(p2_global)
                                graph[p2_global].append(p1_global)
                
                # Match top edge with bottom edge of the top neighbour
                if tile.top_neighbour is not None:
                    top_neighbour = tile.top_neighbour
                    for p1, p2 in zip(tile.top_edge, top_neighbour.bottom_edge):
                        p1_index = tile.points.index(p1)
                        if p1_index in edge_connections:
                            p1_global = tile.get_global_coordinates(p1)
                            p2_global = top_neighbour.get_global_coordinates(p2)
                            if p1_global != p2_global:
                                graph[p1_global].append(p2_global)
                                graph[p2_global].append(p1_global)
                
                # Match bottom edge with top edge of the bottom neighbour
                if tile.bottom_neighbour is not None:
                    bottom_neighbour = tile.bottom_neighbour
                    for p1, p2 in zip(tile.bottom_edge, bottom_neighbour.top_edge):
                        p1_index = tile.points.index(p1)
                        if p1_index in edge_connections:
                            p1_global = tile.get_global_coordinates(p1)
                            p2_global = bottom_neighbour.get_global_coordinates(p2)
                            if p1_global != p2_global:
                                graph[p1_global].append(p2_global)
                                graph[p2_global].append(p1_global)

        #visualize_graph(graph)

        def path_type(point):
            """
            Determines if starting at `point`, we can find a simple closed curve (cycle).
            Returns:
                - "Loop" if a cycle (closed curve) is found.
                - "Open" if it's an open path (non-closed curve).
                - None if the point beloongs to a previously detected path.
            """
            current = point
            prev = None  # Keep track of the previous point to avoid reversing the path
            while True:
                visited.add(current)
                neighbours = graph[current]  # At most length 2 (every point has at most 2 connections)
                if len(neighbours) < 2:
                    return "Open"  # Open path, not a cycle
                # Find the next point in the path that isn't the previous point
                next_point = neighbours[0] if neighbours[0] != prev else neighbours[1]
                if next_point in visited:
                    if next_point == point:
                        return "Loop"  # Cycle found
                    return None  # Already visited point, not a cycle
                prev = current
                current = next_point

        # Initialize counters for loops (closed curves) and open paths (non-closed curves)
        loops = 0
        open_paths = 0

        visited = set()

        # Traverse all nodes
        for point in graph.keys():
            if point not in visited:
                type = path_type(point)
                if type == "Loop":  # If a cycle is detected
                    loops += 1
                elif type == "Open":  # If it's an open path
                    open_paths += 1

        return (loops, open_paths / 2) # We overcounted open paths by a factor of 2

    def count_2d_components(self) -> int:
        # Graph structure to store all connections
        graph = defaultdict(list)

        for tile in self:
            triangle_neighbors = tile.getTriangleNeighbours()
            for t, neighbours in triangle_neighbors.items():
                graph[t] = []
                for neighbor in neighbours:
                    graph[t].append(neighbor)

        # Create a networkx graph
        G = nx.Graph()

        # Add all nodes to the graph
        for node in graph.keys():
            G.add_node(node)

        # Add edges to the graph
        for node, neighbors in graph.items():
            for neighbor in neighbors:
                G.add_edge(node, neighbor)

        components = list(nx.connected_components(G))
        land = 0
        water = 0
        for component in components:
            # First triangle in the component
            t = component.pop()
            # Compute centroid
            x = (t[0][0] + t[1][0] + t[2][0]) / 3
            y = (t[0][1] + t[1][1] + t[2][1]) / 3
            # Compute tile coordinates
            x = int(x//3)
            y = int(y//3)
            # Get tile
            tile = self.getTile(x, y)
            # Get triangle in tile coordinates
            triangle = [(x - tile.x*tile.size, y - tile.y*tile.size) for (x,y) in t]
            triangle_color = tile.getTriangleColor(triangle)
            if triangle_color == 0:
                water += 1
            else:
                land += 1
        return (water, land)

####################################################################################################        
def visualize_graph(graph):
    """
    Visualizes the graph using networkx and matplotlib.

    Args:
        graph (defaultdict): A defaultdict containing the graph adjacency list.
    """
    # Create a networkx graph
    G = nx.Graph()

    # Add all nodes to the graph
    for node in graph.keys():
        G.add_node(node)

    # Add edges to the graph
    for node, neighbors in graph.items():
        for neighbor in neighbors:
            G.add_edge(node, neighbor)

    # Draw the graph
    plt.figure(figsize=(10, 10))
    pos = nx.spring_layout(G)  # Use spring layout for better spacing
    nx.draw(
        G,
        pos,
        with_labels=True,
        node_color='lightblue',
        node_size=500,
        font_size=10,
        font_color='black',
        edge_color='gray'
    )
    plt.title("Graph Visualization")
    plt.show()