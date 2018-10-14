import math
from random import *

from Classes.BoardTile import BoardTile
from Classes.Terrain import Terrain
from Classes.BoardNode import BoardNode
from Classes.TileEdge import TileEdge

class Board:

    # Global board variables
    boardSize = 0
    tileCount = 0

    def __init__(self,boardSizeX,boardSizeY):

        tileID = 0
        self.boardTiles = []
        self.boardNodes = []
        self.tileEdges = []
        terrainCounts = []

        self.boardSizeX = boardSizeX
        self.boardSizeY = boardSizeY

        self.tileCount = math.ceil(boardSizeX*boardSizeY)

        for r in range(0,Terrain.terrainCount):
            terrainCounts.append(0)

        # Setup hexagonal board tile sizes
        for jj in range(1,boardSizeY+1):
            for ii in range(1,boardSizeX+1):

                tileID += 1
                terrainID = 1
                boardTile = BoardTile(terrainID,tileID)
                Terrain.increaseTerrainTileCount(terrainID)
            
                if (ii > 1):
                    boardTile.addNeighbour(5,tileID-1)

                if (ii < boardSizeX):
                    boardTile.addNeighbour(2,tileID+1)

                if (jj > 1):
                    if jj%2 == 1:
                        boardTile.addNeighbour(1,tileID-boardSizeX)
                        if (ii > 1):
                            boardTile.addNeighbour(6,tileID-boardSizeX-1)
                    else:
                        boardTile.addNeighbour(6,tileID-boardSizeX)
                        if (ii < boardSizeX):
                            boardTile.addNeighbour(1,tileID-boardSizeX+1)

                if (jj < boardSizeY):
                    if jj%2 == 0:
                        boardTile.addNeighbour(4,tileID+boardSizeX)
                        if (ii < boardSizeX):
                            boardTile.addNeighbour(3,tileID+boardSizeX+1)
                    else:
                        boardTile.addNeighbour(3,tileID+boardSizeX)
                        if (ii > 1):
                            boardTile.addNeighbour(4,tileID+boardSizeX-1)
                
                #boardTile.showNeighbours()

                boardTile.addLocation(ii,jj)
                
                self.boardTiles.append(boardTile)

        # Lay out volcano somewhere within central area
        self = Board.addVolcano(self)

        # Randomly lay out island around volcano
        self = Board.populateIsland(self)

        # Find and add board nodes
        self = Board.addBoardNodes(self)

        # Find and add board edges
        self = Board.addTileEdges(self)


    def showTerrains(self):
        for r in range(0,Terrain.terrainCount):
            print(
             Terrain.terrainTypes[r], ": ", terrainCounts[r]
            )

    def populateIsland(self):
        for resInd in range(2,Terrain.terrainCount+1):
            counter = 0
            while Terrain.terrainCounts[resInd-1] < Terrain.terrainMaxs[resInd-1] and counter < 500:
                tileID = math.ceil(random()*self.boardSizeX*self.boardSizeY)
                if self.boardTiles[tileID-1].terrain.terrainID == 1:
                    if self.boardTiles[tileID-1].X not in [1,self.boardSizeX] and self.boardTiles[tileID-1].Y not in [1,self.boardSizeY]:
                        self.boardTiles[tileID-1].setTerrain(Terrain(resInd,0))
                        Terrain.increaseTerrainTileCount(resInd)
                        counter += 1
                    #print("Place at ",tileID)
            #print(resInd,"Count:",Terrain.terrainCounts[resInd-1]," Max:",Terrain.terrainMaxs[resInd-1])
        #print(Terrain.terrainCounts)
        #print(Terrain.terrainMaxs)
        return self

    def addVolcano(self):
        volX = math.ceil(random()*(self.boardSizeX/3)) + math.ceil(self.boardSizeX/3)
        volY = math.ceil(random()*(self.boardSizeY/3)) + math.ceil(self.boardSizeY/3)
        volCentral = volX + ((volY - 1)*self.boardSizeX)
        self.boardTiles[volCentral-1].setTerrain(Terrain(7,0))
        Terrain.increaseTerrainTileCount(7)

        neighbours = []
        for neighbour in self.boardTiles[volCentral-1].neighbours:
            self.boardTiles[neighbour-1].setTerrain(Terrain(7,0))
            Terrain.increaseTerrainTileCount(7)
            for neigh in self.boardTiles[neighbour-1].neighbours:
                neighbours.append(neigh)

        #print(neighbours)
        for nei in neighbours:
            if self.boardTiles[nei-1].terrain.terrainID == 1:
                resID = math.ceil(random()*Terrain.terrainCount)
                for add in range(0,Terrain.terrainCount):
                    if Terrain.terrainCounts[resID-1] < Terrain.terrainMaxs[resID-1]:
                        self.boardTiles[nei-1].setTerrain(Terrain(resID,0))
                        Terrain.increaseTerrainTileCount(resID)
                        break
                    resID = ((resID + 1 - 1)%Terrain.terrainCount) + 1
        return self

    def addBoardNodes(self):
        # Add all the board nodes based on tile location

        # Initialise node ID
        nodeID = 1

        for boardTile in self.boardTiles:
            localNodeID = 1 # used to cycle through local node ID's
            for node in boardTile.nodes:
                if (node == 0):
                    #print("Current:",boardTile.tileID, localNodeID, nodeID)
                    self.boardTiles[boardTile.tileID-1].addNode(localNodeID,nodeID) # Set node ID to incremental nodeID
                    
                    n1 = boardTile.tileID
                    nt1 = boardTile.terrain.terrainID
                    n2 = 0
                    nt2 = 0
                    n3 = 0
                    nt3 = 0

                    # Also update neighbour tile nodes
                    if (boardTile.neighbours[localNodeID-1] != 0):
                        #print("N1:",boardTile.neighbours[localNodeID-1], localNodeID, nodeID)
                        n2 = boardTile.neighbours[localNodeID-1]
                        nt2 = self.boardTiles[boardTile.neighbours[localNodeID-1]-1].terrain.terrainID
                        self.boardTiles[boardTile.neighbours[localNodeID-1]-1].addNode(((localNodeID-3)%6)+1,nodeID)

                    if (boardTile.neighbours[(localNodeID-2)%6] != 0): # Use remainder for circular indexing
                        #print("N2:",boardTile.neighbours[(localNodeID-2)%6], localNodeID, nodeID)
                        n3 = boardTile.neighbours[(localNodeID-2)%6]
                        nt2 = self.boardTiles[boardTile.neighbours[(localNodeID-2)%6]-1].terrain.terrainID
                        self.boardTiles[boardTile.neighbours[(localNodeID-2)%6]-1].addNode(((localNodeID+1)%6)+1,nodeID)

                    # Check if neighbouring tiles are sea or land
                    nts = [nt1,nt2,nt3]

                    if nts.count(0) + nts.count(1) >= len(nts):
                        boardNode = BoardNode(nodeID,n1,n2,n3,0)
                    elif nts.count(1) > 0:
                        boardNode = BoardNode(nodeID,n1,n2,n3,1)
                    else:
                        boardNode = BoardNode(nodeID,n1,n2,n3,2)

                    self.boardNodes.append(boardNode)

                    nodeID += 1

                localNodeID += 1

        return self

    def addTileEdges(self):
        edgeID = 1

        for boardTile in self.boardTiles:
            localEdgeID = 1
            for edge in boardTile.edges:
                if edge == 0:
                    self.boardTiles[boardTile.tileID-1].addEdge(localEdgeID,edgeID) # Set node ID to incremental nodeID
                    
                    tile1 = boardTile.tileID
                    tt1 = boardTile.terrain.terrainID
                    tile2 = 0
                    tt2 = 0

                    if boardTile.neighbours[localEdgeID-1] != 0:
                        tile2 = self.boardTiles[boardTile.neighbours[localEdgeID-1]-1].tileID
                        tt2 = self.boardTiles[boardTile.neighbours[localEdgeID-1]-1].terrain.terrainID
                        self.boardTiles[boardTile.neighbours[localEdgeID-1]-1].addEdge(((localEdgeID - 1 + 3)%6) + 1,edgeID)

                    #print(boardTile.neighbours)
                    node1 = boardTile.nodes[localEdgeID - 1]
                    node2 = boardTile.nodes[((localEdgeID + 1 - 1)%6)]

                    # Add edge to surrounding nodes
                    self.boardNodes[node1-1].addEdge(edgeID)
                    self.boardNodes[node2-1].addEdge(edgeID)

                    #print(edgeID,node1,node2,tile1,tile2)
                    tts = [tt1,tt2]

                    if tts.count(0) + tts.count(1) == len(tts):
                        self.tileEdges.append(TileEdge(edgeID,node1,node2,tile1,tile2,0))
                    elif tts.count(1) > 0:
                        self.tileEdges.append(TileEdge(edgeID,node1,node2,tile1,tile2,1))
                    else:
                        self.tileEdges.append(TileEdge(edgeID,node1,node2,tile1,tile2,2))

                    edgeID += 1

                localEdgeID += 1

        return self



    def findEdgeTile(self):

        nodeID = 0

        # Find node on edge
        if random() > 0.5:
            edge1 = round(random())
            if edge1 < 0.5:
                ii = 1
            else:
                ii = self.boardSizeX
            jj = math.ceil(random()*self.boardSizeY)
        else:
            edge2 = round(random())
            if edge2 < 0.5:
                jj = 1
            else:
                jj = self.boardSizeY
            ii = math.ceil(random()*self.boardSizeX)

        for boardTile in self.boardTiles:
            if boardTile.X == ii and boardTile.Y == jj:
                potentialNodes = []
                if ii == 1:
                    potentialNodes.append(4)
                    potentialNodes.append(5)
                    potentialNodes.append(6)
                if ii == self.boardSizeX:
                    potentialNodes.append(3)
                    potentialNodes.append(2)
                    potentialNodes.append(1)
                if jj == 1:
                    potentialNodes.append(6)
                    potentialNodes.append(1)
                    potentialNodes.append(2)
                if jj == self.boardSizeY:
                    potentialNodes.append(3)
                    potentialNodes.append(4)
                    potentialNodes.append(5)

                selectedNode = round(random()*(len(potentialNodes)-1))
                #print(selectedNode,potentialNodes,boardTile.nodes)
                nodeID = boardTile.nodes[potentialNodes[selectedNode]-1]


        return nodeID

    def getTileID(self,X,Y):

        return X + ((Y - 1)*self.boardSizeX)
