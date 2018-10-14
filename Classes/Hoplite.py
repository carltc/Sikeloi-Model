class Hoplite:

	def __init__(self,hopliteID):
		self.tileID = None
		self.status = 0
		self.hopliteID = hopliteID

	def place(self,tileID):
		self.tileID = tileID
		self.status = 1