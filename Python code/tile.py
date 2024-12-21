import matplotlib.pyplot as plt

# Class for a tile.
class Tile:
    def __init__(self, points, edges, connections):
        self.points = points            # List of points (x, y) that make up the tile.
        self.edges = edges              # List of edges (tuple of 2 indices from list of points) that make up the tile
        self.connections = connections  # Subset of edges (just list of indices from list of edges) that show which points are paired.

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
        self.size = max(self.points, key=lambda x: x[0])[0] + 1

    def __str__(self):
        return f"Tile at ({self.x}, {self.y})"

    def __repr__(self):
        return self.__str__()

    def plot(self, clear=False, show=False):
        x = self.x * (self.size - 1)
        y = self.y * (self.size - 1)

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
