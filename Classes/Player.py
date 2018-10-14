from random import *
import math

from Classes.Resource import Resource
from Classes.Assets import Assets

class Player:
    'Common base class for all players'
    playerCount = 0
    playerColours = ["#F7054D","#FBE50F","#2B6CC4","#008000"] # Red, Yellow, Blue, Green
    playerColourNames = ["Red","Yellow","Blue","Green"]

    def __init__(self, playerID, name, colour, gameState):
        self.playerID = playerID
        self.name = name
        self.colour = Player.playerColours[playerID-1]
        self.colourName = Player.playerColourNames[playerID-1]
        self.resources = []
        self.assets = []
        self.gameState = gameState
        self.potentialEdges = []
        self.potentialNodes = []
        self.potentialTiles = []

        # Supply starting resources
        for r in range(1,Resource.resourceCount+1):
           self.resources.append(Resource(r,2))
        Player.playerCount += 1

        # Supply starting assets
        self.assets = Assets()
     
    def displayCount(self):
        print("Total Players %d" % Player.playerCount)

    def displayPlayer(self):
        print(
            "Name : ", self.name,
            ", Colour: ", self.colourName)
        for r in range(1,Resource.resourceCount+1):
           print(
               Resource.resourceTypes[r-1], ": ", self.resources[r-1].getCount()
               )

    def makeFirstMove(self):
        # Place 1st house
        houseNodeID = self.gameState.placeInitialHouse(self.playerID)
        self.assets.houses[0].place(houseNodeID)
        self.initialNode = houseNodeID

        # Initiate potential nodes, edges and tiles
        node = self.gameState.mainBoard.boardNodes[houseNodeID-1]
        self.potentialEdges = node.edges
        self.potentialTiles = node.tileIDs

        # Place 1st villager
        for potTi in self.potentialTiles:
            if self.gameState.mainBoard.boardTiles[potTi-1].terrain.terrainID not in [0,1,8,9]:
                self.gameState.placeVillager(potTi,self.playerID)
                self.assets.villagers[0].place(potTi)
                break

    def makeMove(self):
        # 1 Move consists of 2 actions
        for action in range(0,2):
            # actions consist of: move, build, recruit, attack
            actionID = math.ceil(random()*4)
            for actionAttempt in range(0,4):
                if self.attemptMove(actionID):
                    break
                actionID = ((actionID + 1 - 1)%4) + 1

        # # Build as many roads as possible
        # while self.attemptMove(1):
        #     pass

        # # Build as mant settlements as possible
        # while self.attemptMove(2):
        #     pass
            
        # # Move villager once
        # self.attemptMove(3)

    def attemptMove(self,actionID):
        if actionID == 1: #build road
            numMoves = 3
            moveID = math.ceil(random()*numMoves)
            for moveAttempt in range(0,numMoves):
                if self.move(moveID):
                    return 1
                else:
                    moveID = ((moveID + 1 - 1)%numMoves) + 1
            
        elif actionID == 2: # place house
            numBuilds = 2
            buildID = math.ceil(random()*numBuilds)
            for buildAttempt in range(0,numBuilds):
                if self.build(buildID):
                    return 1
                else:
                    buildID = ((buildID + 1 - 1)%numBuilds) + 1
            
        elif actionID == 3:
            numRecruits = 3
            recruitID = math.ceil(random()*numRecruits)
            for recruitAttempt in range(0,numRecruits):
                if self.recruit(recruitID):
                    return 1
                else:
                    recruitID = ((recruitID + 1 - 1)%numRecruits) + 1

        elif actionID == 4:
            numAttacks = 1
            attackID = math.ceil(random()*numAttacks)
            for attackAttempt in range(0,numAttacks):
                if self.attack(attackID):
                    return 1
                else:
                    attackID = ((attackID + 1 - 1)%numAttacks) + 1

        return 0

    def move(self,unitType):
        if unitType == 1:
            for villager in self.assets.villagers:
                if villager.status == 1:
                    surroundingTiles = self.gameState.mainBoard.boardTiles[villager.tileID-1].neighbours
                    for tileInd in range(0,len(surroundingTiles)):
                        randAdd = math.ceil(random()*len(surroundingTiles))
                        tile = surroundingTiles[(tileInd+randAdd)%len(surroundingTiles)]
                        if tile != villager.tileID and tile != 0:
                            if self.gameState.mainBoard.boardTiles[tile-1].villager == 0 and self.gameState.mainBoard.boardTiles[tile-1].terrain.terrainID not in [0,1,8,9]:
                                #print("Player:",self.playerID," move from ",villager.tileID," to ",tile)
                                self.gameState.moveVillager(villager.tileID,tile,self.playerID)
                                self.assets.villagers[villager.villagerID-1].place(tile)
                                return 1
        elif unitType == 3:
            for scout in self.assets.scouts:
                if scout.status == 1:
                    surroundingTiles = self.gameState.mainBoard.boardTiles[scout.tileID-1].neighbours
                    for tileInd in range(0,len(surroundingTiles)):
                        randAdd = math.ceil(random()*len(surroundingTiles))
                        tile = surroundingTiles[(tileInd+randAdd)%len(surroundingTiles)]
                        if tile != scout.tileID and tile != 0:
                            if self.gameState.mainBoard.boardTiles[tile-1].scout == 0 and self.gameState.mainBoard.boardTiles[tile-1].terrain.terrainID not in [0,1,8,9]:
                                #print("Player:",self.playerID," move from ",scout.tileID," to ",tile)
                                self.gameState.moveScout(scout.tileID,tile,self.playerID)
                                self.assets.scouts[scout.scoutID-1].place(tile)
                                return 1
        return 0

    def build(self,buildID):
        if buildID == 1: # Road
            if self.resources[1].quantity > 0: #check wood
                if self.resources[2].quantity > 0: #check stone
                    for road in self.assets.roads:
                        if road.status == 0:
                            #maxPotEd = 0
                            #maxDist = 0
                            potEdInd = math.ceil(random()*len(self.potentialEdges))
                            for addPotEd in self.potentialEdges:
                                potEd = self.potentialEdges[potEdInd-1]
                                if self.gameState.checkEdge(potEd) and self.gameState.mainBoard.tileEdges[potEd-1].edgeType != 0:
                                    #edge = self.gameState.mainBoard.tileEdges[potEd-1]
                                    #node = self.gameState.mainBoard.boardNodes[self.initialNode]
                                    #if maxDist < self.getDistance(edge.X,edge.Y,node.X,node.Y):
                                    #    maxDist = self.getDistance(edge.X,edge.Y,node.X,node.Y)
                                    #    maxPotEd = potEd

                            #if maxPotEd != 0:
                                # Place road
                                    self.gameState.placeRoad(potEd,self.playerID)
                                    self.assets.roads[road.roadID-1].place(potEd)

                                    # Add new nodes
                                    self.addPotentialNodes(self.gameState.mainBoard.tileEdges[potEd-1].nodes)

                                    # Remove spent resources
                                    self.resources[1].remove(1)
                                    self.resources[2].remove(1)
                                    return 1
                                else:
                                    potEdInd = ((potEdInd - 1 + 1)%len(self.potentialEdges)) + 1

        elif buildID == 2: # House
            #if self.resources[0].quantity > 0: #check food
            if self.resources[1].quantity > 1: #check wood
                if self.resources[2].quantity > 0: #check stone
                    if self.resources[3].quantity > 0: #check silver
                        for house in self.assets.houses:
                            if house.status == 0:
                                for nodeInd in range(0,len(self.potentialNodes)):
                                    randAdd = math.ceil(random()*len(self.potentialNodes))
                                    potNo = self.potentialNodes[(nodeInd+randAdd)%len(self.potentialNodes)]
                                    if self.gameState.checkNode(potNo):
                                        # Place House
                                        self.gameState.placeHouse(potNo,self.playerID)
                                        self.assets.houses[house.houseID-1].place(potNo)

                                        # Add new tiles and edges
                                        self.addPotentialEdges(self.gameState.mainBoard.boardNodes[potNo-1].edges)
                                        self.addPotentialTiles(self.gameState.mainBoard.boardNodes[potNo-1].tileIDs)

                                        # Remove spent resources
                                        self.resources[1].remove(2) # wood
                                        self.resources[2].remove(1) # stone
                                        self.resources[3].remove(1) # silver
                                        #print("Player ",self.playerID," place house", house.houseID," at ",potNo)
                                        return 1

        #print("didn't build")
        return 0

    def recruit(self,recruitID):

        if recruitID == 1: # Villager
            if self.resources[0].quantity > 1: # check food
                for villager in self.assets.villagers:
                    if villager.status == 0:
                        for tileInd in range(0,len(self.potentialTiles)):
                            randAdd = math.ceil(random()*len(self.potentialTiles))
                            poTi = self.potentialTiles[(tileInd+randAdd)%len(self.potentialTiles)]
                            if self.gameState.checkTile(poTi,villager.boardPieceType,self.playerID):
                                # Place villager
                                self.gameState.placeVillager(poTi,self.playerID)
                                self.assets.villagers[villager.villagerID-1].place(poTi)

                                # Remove spent resources
                                self.resources[0].remove(2) # food

                                return 1

        elif recruitID == 3: # Scout
            if self.resources[3].quantity > 2: # Gold
                for scout in self.assets.scouts:
                    if scout.status == 0:
                        for tileInd in range(0,len(self.potentialTiles)):
                            randAdd = math.ceil(random()*len(self.potentialTiles))
                            poTi = self.potentialTiles[(tileInd+randAdd)%len(self.potentialTiles)]
                            if self.gameState.checkTile(poTi,scout.boardPieceType,self.playerID):
                                # Place scout
                                self.gameState.placeScout(poTi,self.playerID)
                                self.assets.scouts[scout.scoutID-1].place(poTi)

                                # Remove spent resources
                                self.resources[3].remove(2) # gold

                                return 1

        return 0

    def attack(self,attackID):

        for scout in self.assets.scouts:
            if scout.status == 1:
                for neiTi in self.gameState.mainBoard.boardTiles[scout.tileID-1].neighbours:
                    enemyUnit = self.gameState.checkTileForEnemy(neiTi,self.playerID)
                    if enemyUnit in [1,2]:
                        diceRoll = self.gameState.rollDice()
                        if diceRoll <= 3: # Attack kills unit
                            print("Villager killed.")
                            self.gameState.killUnit(neiTi,enemyUnit,self.playerID)
                        else: # Attack captures unit
                            print("Villager captured.")
                            self.gameState.captureUnit(neiTi,enemyUnit,self.playerID)
                        self.gameState.moveScout(scout.tileID,neiTi,self.playerID)
                        self.assets.scouts[scout.scoutID-1].place(neiTi)


    def addPotentialNodes(self,nodes):
        for node in nodes:
            if node not in self.potentialNodes:
                self.potentialNodes.append(node)

                # Add edges opened up at this node
                edges = self.gameState.mainBoard.boardNodes[node-1].edges
                self.addPotentialEdges(edges)

    def addPotentialEdges(self,edges):
        for edge in edges:
            if edge not in self.potentialEdges:
                self.potentialEdges.append(edge)

    def addPotentialTiles(self,tiles):
        for tile in tiles:
            if tile not in self.potentialTiles:
                self.potentialTiles.append(tile)

    def getDistance(self,X1,Y1,X2,Y2):
        return (((X1-X2)**2) + ((Y1-Y2)**2))**0.5



                

    




        

