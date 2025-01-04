import matplotlib.pyplot as plt
from collections import defaultdict

# Class for a tile.
class Tile:
    def __init__(self, points, edges, connections):
        self.points = points            # List of points (x, y) that make up the tile.
        self.edges = edges              # List of edges (tuple of 2 indices from list of points) that make up the tile
        self.connections = connections  # Subset of edges (just list of indices from list of edges) that show which points are paired.

        self.triangles = self._computeTriangles()
        self.triangles_color = self._colorTriangles()

        # Find the edge points of the tile
        self.left_edge = []
        self.right_edge = []
        self.top_edge = []
        self.bottom_edge = []
        for p in points:
            if p[0] == 0:
                self.left_edge.append(p)
            if p[0] == 3:
                self.right_edge.append(p)
            if p[1] == 0:
                self.bottom_edge.append(p)
            if p[1] == 3:
                self.top_edge.append(p)
        
        # Sort the edge points
        self.left_edge.sort(key=lambda x: x[1])
        self.right_edge.sort(key=lambda x: x[1])
        self.top_edge.sort(key=lambda x: x[0])
        self.bottom_edge.sort(key=lambda x: x[0])

        # Neighbouring tiles. Default is None. This is later updated when constructing the map.
        self.left_neighbour = None
        self.right_neighbour = None
        self.top_neighbour = None
        self.bottom_neighbour = None

        # x and y coordinates of the tile in the map. Default is 0.
        self.x = 0
        self.y = 0

        # Size of the tile. As the tile is always square, this is just max of x or y coordinate of the points.
        self.size = max(self.points, key=lambda x: x[0])[0]

    def __str__(self):
        return f"Tile at ({self.x}, {self.y})"

    def __repr__(self):
        return self.__str__()
    
    # Function to compute all triangles from list of edges.
    def _computeTriangles(self):
        # Create an adjacency list
        adjacency = defaultdict(set)
        for edge in self.edges:
            u, v = edge
            adjacency[u].add(v)
            adjacency[v].add(u)

        # Find all triangles
        triangles = set()
        for u, v in self.edges:
            # Check neighbors of u and v for a common vertex
            common_neighbors = adjacency[u].intersection(adjacency[v])
            for w in common_neighbors:
                # Ensure unique triangle representation (sorted order)
                triangle = tuple(sorted([u, v, w]))
                triangles.add(triangle)

        return list(triangles)
    
    def _colorTriangles(self):
        # Find the starting triangle
        start_point_index = self.points.index((0, 0))
        start_triangle = None
        for t in self.triangles:
            if start_point_index in t:
                start_triangle = t
                break

        if start_triangle is None:
            raise ValueError("Starting triangle not found.")

        # Initialize colors and visited set
        triangle_colors = {}
        visited = set()

        # Use a queue for BFS
        queue = [(start_triangle, 0)]  # (triangle, color)
        triangle_colors[tuple(start_triangle)] = 0  # Start triangle is blue

        while queue:
            current_triangle, current_color = queue.pop(0)
            visited.add(tuple(current_triangle))

            # Find neighbors
            for neighbor in self.triangles:
                if tuple(neighbor) in visited:
                    continue

                # Check if the current triangle and neighbor share an edge
                shared_edge = [
                    edge
                    for edge in [(current_triangle[i], current_triangle[j]) for i in range(3) for j in range(i + 1, 3)]
                    if edge in [(neighbor[i], neighbor[j]) for i in range(3) for j in range(i + 1, 3)] or
                    edge[::-1] in [(neighbor[i], neighbor[j]) for i in range(3) for j in range(i + 1, 3)]
                ]
                if not shared_edge:
                    continue

                shared_edge_index = self.edges.index(shared_edge[0])
                if shared_edge_index in self.connections:
                    neighbor_color = 1 - current_color
                else:
                    neighbor_color = current_color

                # Color the neighbor and add it to the queue
                triangle_colors[tuple(neighbor)] = neighbor_color
                queue.append((neighbor, neighbor_color))
                visited.add(tuple(neighbor))

        return triangle_colors

    def plot(self, clear=False, show=False, color=False):
        x = self.x * self.size
        y = self.y * self.size

        if clear:
            plt.clf()

        for edge in self.edges:
            plt.plot([self.points[edge[0]][0]+x, self.points[edge[1]][0]+x], [self.points[edge[0]][1]+y, self.points[edge[1]][1]+y], 'k-', linewidth=0.5)

        for connection in self.connections:
            point1 = self.edges[connection][0]
            point2 = self.edges[connection][1]
            plt.plot([self.points[point1][0]+x, self.points[point2][0]+x], [self.points[point1][1]+y, self.points[point2][1]+y], 'k-', linewidth=3)

            plt.plot(self.points[point1][0]+x, self.points[point1][1]+y, 'ko', markersize=8)  # Dot for point1
            plt.plot(self.points[point2][0]+x, self.points[point2][1]+y, 'ko', markersize=8)  # Dot for point2

        if color:
            for triangle in self.triangles:
                color = 'b' if self.triangles_color[tuple(triangle)] == 0 else 'g'
                plt.fill([self.points[triangle[0]][0]+x, self.points[triangle[1]][0]+x, self.points[triangle[2]][0]+x], 
                         [self.points[triangle[0]][1]+y, self.points[triangle[1]][1]+y, self.points[triangle[2]][1]+y], color, alpha=0.5)

        if show:
            plt.show()

    def setNeighbour(self, direction, tile: 'Tile'):
        if direction == 'left':
            self.left_neighbour = tile
        elif direction == 'right':
            self.right_neighbour = tile
        elif direction == 'top':
            self.top_neighbour = tile
        elif direction == 'bottom':
            self.bottom_neighbour = tile

    def getTriangleNeighbours(self):
        dict = {}
        for triangle in self.triangles:
            t = self.globalTriangleRepresentation(tuple(triangle))
            dict[t] = []
            for neighbour in self.triangles:
                if neighbour == triangle:
                    continue
                shared_edge = [
                    edge
                    for edge in [(triangle[i], triangle[j]) for i in range(3) for j in range(i + 1, 3)]
                    if edge in [(neighbour[i], neighbour[j]) for i in range(3) for j in range(i + 1, 3)] or
                    edge[::-1] in [(neighbour[i], neighbour[j]) for i in range(3) for j in range(i + 1, 3)]
                ]
                if shared_edge:
                    shared_edge_index = self.edges.index(shared_edge[0])
                    if not shared_edge_index in self.connections:
                        dict[t].append(self.globalTriangleRepresentation(neighbour))

            commonLeft = self.trianglePointsOnLeftEdge(triangle)
            commonRight = self.trianglePointsOnRightEdge(triangle)
            commonTop = self.trianglePointsOnTopEdge(triangle)
            commonBottom = self.trianglePointsOnBottomEdge(triangle)
            if len(commonLeft) == 2:
                if self.left_neighbour is not None:
                    commonLeft = [(x + 3, y) for (x, y) in commonLeft]
                    dict[t].append(self.left_neighbour.globalTriangleRepresentation(self.left_neighbour.findTriangleWithPoints(commonLeft)))
            elif len(commonRight) == 2:
                if self.right_neighbour is not None:
                    commonRight = [(x - 3, y) for (x, y) in commonRight]
                    dict[t].append(self.right_neighbour.globalTriangleRepresentation(self.right_neighbour.findTriangleWithPoints(commonRight)))

            if len(commonTop) == 2:
                if self.top_neighbour is not None:
                    commonTop = [(x, y - 3) for (x, y) in commonTop]
                    dict[t].append(self.top_neighbour.globalTriangleRepresentation(self.top_neighbour.findTriangleWithPoints(commonTop)))
            elif len(commonBottom) == 2:
                if self.bottom_neighbour is not None:
                    commonBottom = [(x, y + 3) for (x, y) in commonBottom]
                    dict[t].append(self.bottom_neighbour.globalTriangleRepresentation(self.bottom_neighbour.findTriangleWithPoints(commonBottom)))

        return dict

    def globalTriangleRepresentation(self, triangle):
        p1 = triangle[0]
        p2 = triangle[1]
        p3 = triangle[2]
        return (self.get_global_coordinates(self.points[p1]), self.get_global_coordinates(self.points[p2]), self.get_global_coordinates(self.points[p3]))

    def get_global_coordinates(self, point):
        return (point[0] + self.x * self.size, point[1] + self.y * self.size)
    
    def findTriangleWithPoints(self, points):
        for triangle in self.triangles:
            common = 0
            for i in triangle:
                if self.points[i] in points:
                    common += 1
            if common == 2:
                return triangle
        raise ValueError("Triangle not found.")

    def trianglePointsOnLeftEdge(self, triangle):
        common = []
        for i in triangle:
            if self.points[i] in self.left_edge:
                common.append(self.points[i])
        return common
    
    def trianglePointsOnRightEdge(self, triangle):
        common = []
        for i in triangle:
            if self.points[i] in self.right_edge:
                common.append(self.points[i])
        return common
    
    def trianglePointsOnTopEdge(self, triangle):
        common = []
        for i in triangle:
            if self.points[i] in self.top_edge:
                common.append(self.points[i])
        return common
    
    def trianglePointsOnBottomEdge(self, triangle):
        common = []
        for i in triangle:
            if self.points[i] in self.bottom_edge:
                common.append(self.points[i])
        return common
    
    def getTriangleColor(self, triangle):
        index1 = self.points.index(triangle[0])
        index2 = self.points.index(triangle[1])
        index3 = self.points.index(triangle[2])
        return self.triangles_color[(index1, index2, index3)]