class Villager:

	def __init__(self,villagerID):
		self.tileID = None
		self.status = 0
		self.villagerID = villagerID
		self.boardPieceType = 1 # Villager type ID

	def place(self,tileID):
		self.tileID = tileID
		self.status = 1

	def remove(self):
		self.tileID = 0
		self.status = 0