from tile import Tile
from map import Map
import copy
import random

# First two tiles
t1 = Tile([(0,0),(3,0),(3,3),(0,3),(1,0),(2,0),(0,1),(0,2),(1,3),(2,3),(3,1),(3,2),(1.5,1.5)], 
        [(11, 12), (8, 9), (7, 12), (1, 10), (10, 11), (1, 5), (5, 12), (2, 9), (10, 12), 
        (6, 7), (8, 12), (2, 11), (7, 8), (4, 5), (0, 4), (3, 7), (6, 12), (5, 10), (4, 6), 
        (9, 11), (9, 12), (0, 6), (3, 8), (4, 12)], 
        [18,17,12,19])

t2 = Tile([(0,0),(3,0),(3,3),(0,3),(1,0),(2,0),(0,1),(0,2),(1,3),(2,3),(3,1),(3,2),(1.5,2.5),(1.5,0.5)], 
        [(8, 9), (7, 12), (1, 10), (10, 11), (1, 5), (2, 9), (5, 13), (6, 7), 
         (10, 13), (8, 12), (2, 11), (7, 8), (4, 5), (0, 4), (3, 7), (6, 10), (5, 10), 
         (4, 6), (9, 11), (9, 12), (0, 6), (3, 8), (4, 13),(11, 12),(7, 11),(7, 10),(6, 13)], 
        [24,15,6,22,9,19])

l = [t1, t2] # List of all tiles

random.seed(2)

map = Map(7, 2, "plane")   # Possible types: "plane", "cylinder", "torus"

for j in range(map.m):
    for i in range(map.n):
        t = copy.copy(l[random.choice([0, 1])])
        t.x = i
        t.y = j
        map.setTile(t, i, j)

map.updateNeighbours()

tile = map.getTile(0, 0)
print(tile)
print("Left: " + str(tile.left_neighbour))
print("Right: " + str(tile.right_neighbour))
print("Top: " + str(tile.top_neighbour))
print("Bottom: " + str(tile.bottom_neighbour))

print("**********")
tile = map.getTile(0, 1)
print(tile)
print("Left: " + str(tile.left_neighbour))
print("Right: " + str(tile.right_neighbour))
print("Top: " + str(tile.top_neighbour))
print("Bottom: " + str(tile.bottom_neighbour))
map.plot()