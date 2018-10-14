class BoardNode:

	def __init__(self,nodeID,n1,n2,n3,nodeType):

		self.nodeID = nodeID
		self.tileIDs = [n1,n2,n3]
		self.X = 0
		self.Y = 0
		self.buildingType = 0 # 1=House
		self.status = 0 # 1=Occupied
		self.playerID = 0
		self.edges = []
		self.nodeType = nodeType # 0=Sea, 1=shore, 1=inland

	def addLocation(self,x,y):

	    self.X = x
	    self.Y = y

	def addBuilding(self,buildingType,playerID):

		self.status = 1
		self.buildingType = 1
		self.playerID = playerID

	def addEdge(self,edgeID):

		if edgeID not in self.edges:
			self.edges.append(edgeID)


