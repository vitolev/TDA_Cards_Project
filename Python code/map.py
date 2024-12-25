from tile import Tile
import matplotlib.pyplot as plt

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
    
    def setTile(self, tile: Tile, x: int, y: int):
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
            ...
        elif self.type == "torus":
            ...

    def plot(self, color=False):
        plt.clf()
        for j in range(len(self.tiles)):
            for i in range(len(self.tiles[j])):
                t = self.tiles[j][i]
                t.plot(color=color)
        
        plt.axis('equal')
        plt.show()