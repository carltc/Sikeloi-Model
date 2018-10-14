from Classes.Resource import Resource

class Terrain:

    terrainTypes = ["Sea","Arable","Lake","Pastoral","Forest","Quarry","Volcano","Barbarian","Myth"] # ID: 1, 2, 3, 4
    terrainCount = len(terrainTypes)
    terrainBorderColour = ['#4FA3E2','#A3FF0D','#001182','#629908','#238200','#6A6A6B','#FF5C0D','#272928','#CC3DB2']
    terrainColour = ['#4FA3E2','#000000','#000000','#000000','#000000','#000000','#000000','#000000','#000000']
    terrainCounts = [0,0,0,0,0,0,0,0,0]
    terrainMaxs = [0,6,6,6,12,8,0,4,4]

    def __init__(self, terrainID, quantity):
        self.terrainID = terrainID
        self.quantity = quantity

        if terrainID in [2,3,4]:
            self.resource = Resource(1,0)
        elif terrainID == 5:
            self.resource = Resource(2,0)
        elif terrainID == 6:
            self.resource = Resource(3,0)
        elif terrainID == 7:
            self.resource = Resource(4,0)
        else:
            self.resource = Resource(0,0)

    def increaseTerrainTileCount(terrainID):
        Terrain.terrainCounts[terrainID-1] += 1

    def displayterrain(self):
        print("terrain: ", Terrain.terrainTypes[self.terrainID-1], "\n",
              "Quantity: ", self.quantity, "\n")

    def getCount(self):
        return self.quantity
              
    def add(self, count):
        self.quantity += count

    def remove(self, count):
        self.quantity -= count

    def getColours(self):
        return Terrain.terrainColour

    def getBorderColours(self):
        return Terrain.terrainBorderColours

    def resetTerrainCounts():
        for terID in range(0,len(Terrain.terrainCounts)):
            Terrain.terrainCounts[terID] = 0

        
    
