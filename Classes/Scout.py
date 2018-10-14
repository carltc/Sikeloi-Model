class Scout:

	def __init__(self,scoutID):
		self.tileID = None
		self.status = 0
		self.scoutID = scoutID
		self.boardPieceType = 3 # Scout type ID

	def place(self,tileID):
		self.tileID = tileID
		self.status = 1