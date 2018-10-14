from Classes.House import House
from Classes.Road import Road
from Classes.Hoplite import Hoplite
from Classes.Villager import Villager
from Classes.Scout import Scout

class Assets:

	def __init__(self):

		self.houses = []
		self.roads = []
		self.hoplites = []
		self.villagers = []
		self.scouts = []

		self.houses = [House(1), House(2), House(3), House(4)]

		for roadCount in range(0,16):
			self.roads.append(Road(roadCount+1))

		self.hoplites = [Hoplite(1), Hoplite(2)]
		self.villagers = [Villager(1), Villager(2)]
		self.scouts = [Scout(1), Scout(2)]