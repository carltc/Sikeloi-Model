import math
from random import *

from Classes.Player import Player
from Classes.Board import Board

class SetupGame:

    # Global game state variables
    players = []
    mainBoard = []
    currentPlayer = 0
    nextPlayer = 0
    season = 0 # 1=Summer, 2=Autumn, 3=Winter, 4=Spring

    def __init__(self):
        # Setup players
        pl1 = Player(1,"Carl","Red",self)
        pl2 = Player(2,"Naish","Blue",self)
        pl3 = Player(3,"Mark","Yellow",self)
        pl4 = Player(4,"Greeny","Green",self)

        SetupGame.players = [pl1, pl2, pl3, pl4]
    
        # Setup Game Board
        SetupGame.mainBoard = Board(12,10)

        # Select next player
        SetupGame.currentPlayer = math.ceil((random()*len(SetupGame.players)))
        SetupGame.nextPlayer = (SetupGame.currentPlayer + 1 - 1)%len(SetupGame.players) + 1

        # Set starting season
        season = math.ceil(random()*4)

    def rollDice(self):
        return math.ceil(random()*6)

    def nextPlayerSwap():
        # Move current player along and change variables
        SetupGame.currentPlayer = (SetupGame.currentPlayer + 1 - 1)%len(SetupGame.players) + 1
        SetupGame.nextPlayer = (SetupGame.currentPlayer + 1 - 1)%len(SetupGame.players) + 1

    def placeInitialHouse(self,playerID):
        testTileID = math.ceil(random()*self.mainBoard.boardSizeX*self.mainBoard.boardSizeY)
        for tT in range(0,self.mainBoard.boardSizeX*self.mainBoard.boardSizeY):
            if self.mainBoard.boardTiles[((testTileID+tT)%self.mainBoard.tileCount)-1].terrain.terrainID not in [7,8,9]: # dont place on myth,volcano or barbarian
                for node in self.mainBoard.boardTiles[((testTileID+tT)%self.mainBoard.tileCount)-1].nodes:
                    if self.checkNodeNeighbourTerrain(node,[7,8,9]):
                        if self.mainBoard.boardNodes[node-1].nodeType == 1:
                            SetupGame.placeHouse(self,node,playerID)
                            return node

    def placeHouse(self,nodeID,playerID):
        SetupGame.mainBoard.boardNodes[nodeID-1].addBuilding(1,playerID)
        self.unhideNeighbourTiles(SetupGame.mainBoard.boardNodes[nodeID-1].tileIDs)

    def placeRoad(self,edgeID,playerID):
        SetupGame.mainBoard.tileEdges[edgeID-1].addRoad(playerID)
        self.unhideNeighbourTiles(SetupGame.mainBoard.boardNodes[SetupGame.mainBoard.tileEdges[edgeID-1].nodes[0]-1].tileIDs)
        self.unhideNeighbourTiles(SetupGame.mainBoard.boardNodes[SetupGame.mainBoard.tileEdges[edgeID-1].nodes[1]-1].tileIDs)

    def placeVillager(self,tileID,playerID):
        SetupGame.mainBoard.boardTiles[tileID-1].addVillager(playerID)
        self.unhideNeighbourTiles(SetupGame.mainBoard.boardTiles[tileID-1].neighbours)

    def placeScout(self,tileID,playerID):
        SetupGame.mainBoard.boardTiles[tileID-1].addScout(playerID)
        self.unhideNeighbourTiles(SetupGame.mainBoard.boardTiles[tileID-1].neighbours)

    def moveVillager(self,oldTileID,newTileID,playerID):
        SetupGame.mainBoard.boardTiles[oldTileID-1].removeVillager(playerID)
        SetupGame.mainBoard.boardTiles[newTileID-1].addVillager(playerID)
        self.unhideNeighbourTiles(SetupGame.mainBoard.boardTiles[newTileID-1].neighbours)

    def moveScout(self,oldTileID,newTileID,playerID):
        SetupGame.mainBoard.boardTiles[oldTileID-1].removeScout(playerID)
        SetupGame.mainBoard.boardTiles[newTileID-1].addScout(playerID)
        self.unhideNeighbourTiles(SetupGame.mainBoard.boardTiles[newTileID-1].neighbours)

    def unhideNeighbourTiles(self,neighbourTileIDs):
        # Unhide neighbours
        for nTileID in neighbourTileIDs:
            SetupGame.mainBoard.boardTiles[nTileID-1].unhide()

    def progressSeason():
        #print("Season",SetupGame.season," ended.")
        SetupGame.season = ((SetupGame.season - 1 + 1)%4) + 1
        #print("Season",SetupGame.season," started!")

    def resourceCollection():
        # Perform resource collection per player
        for player in SetupGame.players:

            # House resource collection
            for house in player.assets.houses:
                if house.status == 1:
                    houseNode = SetupGame.mainBoard.boardNodes[house.nodeID-1]
                    for tileID in houseNode.tileIDs:
                        if tileID != 0:
                            #print("TileID: ", tileID)
                            tile = SetupGame.mainBoard.boardTiles[tileID-1]
                            resourceCount = SetupGame.checkSeasonResource(tile.terrain)
                            SetupGame.players[player.playerID-1].resources[tile.terrain.resource.resourceID-1].add(resourceCount)
            
            # Villager resource collection
            for villager in player.assets.villagers:
                if villager.status == 1:
                    villagerTile = SetupGame.mainBoard.boardTiles[villager.tileID-1]
                    resourceCount = SetupGame.checkSeasonResource(villagerTile.terrain)
                    SetupGame.players[player.playerID-1].resources[villagerTile.terrain.resource.resourceID-1].add(resourceCount)


    def checkSeasonResource(terrain):
        if terrain.terrainID == 2: # Arable
            if SetupGame.season == 1: # Summer
                return 1
            elif SetupGame.season == 2: # Autumn
                return 2

        elif terrain.terrainID == 3: # Lake
            if SetupGame.season == 2: # Autumn
                return 1
            elif SetupGame.season == 3: # Winter
                return 1

        elif terrain.terrainID == 4: # Pastoral
            if SetupGame.season == 4: # Spring
                return 2
            elif SetupGame.season == 1: # Summer
                return 1

        elif terrain.terrainID == 5: # Forest
            if SetupGame.season == 1: # Summer
                return 1
            elif SetupGame.season == 2: # Autumn
                return 1
            elif SetupGame.season == 4: # Spring
                return 1

        elif terrain.terrainID == 6: # Quarry
            if SetupGame.season == 1: # Summer
                return 1
            elif SetupGame.season == 2: # Autumn
                return 1
            elif SetupGame.season == 3: # Autumn
                return 1

        elif terrain.terrainID == 7: # Volcano
            return 1

        return 0

    def checkEdge(self,edgeID):
        if SetupGame.mainBoard.tileEdges[edgeID-1].status == 0:
            return 1
        else:
            return 0

    def checkNode(self,nodeID):
        if SetupGame.mainBoard.boardNodes[nodeID-1].status == 0:
            if SetupGame.mainBoard.boardNodes[nodeID-1].nodeType != 0:
                if self.checkNodeNeighbourTerrain(nodeID,[7,8,9]):
                    return 1
        else:
            return 0

    def checkTile(self,tileID,boardPieceType,playerID):
        # Check if board piece type can go on this tile
        if boardPieceType == 1: # if villager
            if SetupGame.mainBoard.boardTiles[tileID-1].playerID in [0,playerID]:
                if SetupGame.mainBoard.boardTiles[tileID-1].villager == 0:
                    if SetupGame.mainBoard.boardTiles[tileID-1].terrain.terrainID not in [1,8,9]:
                        return 1
        elif boardPieceType == 3:
            if SetupGame.mainBoard.boardTiles[tileID-1].playerID in [0,playerID]:
                if SetupGame.mainBoard.boardTiles[tileID-1].scout == 0:
                    if SetupGame.mainBoard.boardTiles[tileID-1].terrain.terrainID not in [1,8,9]:
                        return 1
        return 0

    def checkNodeNeighbourTerrain(self,nodeID,undesired):
        # Check all node neighbour tiles
        n1 = SetupGame.mainBoard.boardTiles[SetupGame.mainBoard.boardNodes[nodeID-1].tileIDs[0]-1].terrain.terrainID
        n2 = SetupGame.mainBoard.boardTiles[SetupGame.mainBoard.boardNodes[nodeID-1].tileIDs[1]-1].terrain.terrainID
        n3 = SetupGame.mainBoard.boardTiles[SetupGame.mainBoard.boardNodes[nodeID-1].tileIDs[2]-1].terrain.terrainID

        if n1 not in undesired and n2 not in undesired and n3 not in undesired:
            return 1
        else:
            return 0

    def checkTileForEnemy(self,tileID,playerID):
        tilePlayerID = SetupGame.mainBoard.boardTiles[tileID-1].playerID
        if tilePlayerID != 0 and tilePlayerID != playerID:
            if SetupGame.mainBoard.boardTiles[tileID-1].villager:
                return 1
            if SetupGame.mainBoard.boardTiles[tileID-1].peasant:
                return 2
            if SetupGame.mainBoard.boardTiles[tileID-1].scout:
                return 3
            if SetupGame.mainBoard.boardTiles[tileID-1].hoplite:
                return 4
            if SetupGame.mainBoard.boardTiles[tileID-1].cavalry:
                return 5

        return 0

    def killUnit(self,tileID,unitType,playerID):
        tile = SetupGame.mainBoard.boardTiles[tileID-1]
        if unitType == 1:
            if tile.villager == 1 and tile.playerID != playerID:
                SetupGame.mainBoard.boardTiles[tileID-1].removeVillager(tile.playerID)
                for villager in SetupGame.players[tile.playerID-1].assets.villagers:
                    if villager.tileID == tileID:
                        SetupGame.players[tile.playerID-1].assets.villagers[villager.villagerID-1].remove()
                        return 1

        return 0

    def captureUnit(self,tileID,unitType,playerID):
        tile = SetupGame.mainBoard.boardTiles[tileID-1]
        if unitType == 1:
            if tile.villager == 1 and tile.playerID != playerID:
                SetupGame.mainBoard.boardTiles[tileID-1].removeVillager(tile.playerID)
                for villager in SetupGame.players[tile.playerID-1].assets.villagers:
                    if villager.tileID == tileID:
                        SetupGame.players[tile.playerID-1].assets.villagers[villager.villagerID-1].remove()
                        
                        # Add villager to current player
                        nextVillagerID = len(SetupGame.players[playerID-1].assets.villagers) + 1
                        SetupGame.players[playerID-1].villagers.append(Villager(nextVillagerID))
                        SetupGame.placeVillager(tileID,playerID)
                        SetupGame.players[playerID-1].assets.villagers[nextVillagerID-1].place(tileID)

        return 0



