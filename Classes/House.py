class House:

	def __init__(self,houseID):

		self.nodeID = 0
		self.status = 0
		self.houseID = houseID

	def place(self,nodeID):
		self.nodeID = nodeID
		self.status = 1
