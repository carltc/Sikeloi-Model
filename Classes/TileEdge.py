class TileEdge:

	def __init__(self,edgeID,nodeID1,nodeID2,tileID1,tileID2,edgeType):

		self.edgeID = edgeID
		self.nodes = [nodeID1,nodeID2]
		self.tiles = [tileID1,tileID2]
		self.edgeType = edgeType # 0=Sea, 1=Shore, 2=inland

		self.status = 0 # 0=No Road, 1=Road

	def addLocation(self,x,y):

		self.X = x
		self.Y = y

	def addRoad(self,playerID):

		self.status = 1
		self.playerID = playerID

