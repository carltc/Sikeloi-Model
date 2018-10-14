from random import *

from Classes.Terrain import Terrain

class BoardTile:

    neighbourCount = 6

    def __init__(self,terrain,tileID):
        self.tileID = tileID
        self.terrain = Terrain(terrain,0)

        # Neighbours: 1=North-East, 2=East, 3=South-East, 4=South-West, 5=West, 6=North-West
        self.neighbours = [0,0,0,0,0,0]

        # Nodes: 1=North, 2=North-East, 3=South-East, 4=South, 5=South-West, 6=North-West
        self.nodes = [0,0,0,0,0,0]

        # Edges: 1=NE, 2=E, 3=SE, 4=SW, 5=W, 6=NW
        self.edges = [0,0,0,0,0,0]

        # Status of buildings on tile
        self.building = 0

        # Status of units on tile
        self.villager = 0
        self.peasant = 0
        self.scout = 0
        self.hoplite = 0
        self.cavalry = 0
        
        self.hidden = 0
        self.playerID = 0

    def addNeighbour(self,neighbourNum,neighbourID):
        self.neighbours[neighbourNum-1] = neighbourID

    def showNeighbours(self):
        print("Neighbours: ", self.neighbours)

    def addNode(self,nodeNum,nodeID):
        self.nodes[nodeNum-1] = nodeID

    def showNodes(self):
        print("Nodes: ", self.nodes)

    def addEdge(self,edgeNum,edgeID):
        self.edges[edgeNum-1] = edgeID

    def showEdges(self):
        print("Edges: ", self.edges)

    def addLocation(self,X,Y):
        self.X = X
        self.Y = Y

    def addVillager(self,playerID):
        self.villager = 1 # 1=Villager
        self.playerID = playerID
        self.hidden = 0

    def removeVillager(self,playerID):
        self.villager = 0
        self.playerID = 0

    def addScout(self,playerID):
        self.scout = 1
        self.playerID = playerID

    def removeScout(self,playerID):
        self.scout = 0
        self.playerID = 0

    def unhide(self):
        self.hidden = 0

    def setTerrain(self,Terrain):
        self.terrain = Terrain
        #print("Terrain: ", self.terrain.terrainID)
        if self.terrain.terrainID not in [0,1,7]:
            self.hidden = 1
        else:
            self.hidden = 0
