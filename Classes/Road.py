class Road:

	def __init__(self,roadID):
		self.edgeID = 0
		self.status = 0
		self.roadID = roadID

	def place(self,edgeID):
		self.edgeID = edgeID
		self.status = 1