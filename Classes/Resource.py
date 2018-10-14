from tkinter import PhotoImage

class Resource:

    resourceTypes = ["Food","Wood","Stone","Silver"] # ID: 1, 2, 3, 4
    resourceCount = len(resourceTypes)
    resourceCounts = [0,0,0,0,0,0,0,0,0]
    resourceMaxs = [0,6,6,6,12,8,0,4,4]
    resourceImages = ["field.png","wood.png","landslide.png","gold.png"]

    def __init__(self, resourceID, quantity):
        self.resourceID = resourceID
        self.quantity = quantity
        #if resourceID != 0:
        #    self.image = PhotoImage(file=Resource.resourceImages[resourceID-1])

    def increaseResourceTileCount(resourceID):
        Resource.resourceCounts[resourceID-1] += 1

    def displayResource(self):
        print("Resource: ", resourceTypes[self.resourceID-1], "\n",
              "Quantity: ", self.quantity, "\n")

    def getCount(self):
        return self.quantity
              
    def add(self, count):
        self.quantity += count

    def remove(self, count):
        self.quantity -= count

    def getImage(self):
        return self.image

    def resetResourceCounts():
        for resID in range(0,len(Resource.resourceCounts)):
            Resource.resourceCounts[resID] = 0

        
    
