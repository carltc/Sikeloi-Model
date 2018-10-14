from Classes.Turns import Turns
from Classes.SetupGame import SetupGame

class SimulateGame:

    def __init__(self):

        self.simulate()

    def simulate(self):

        for turnNum in range(0,50):

            Turns.takeTurn()

        for player in SetupGame.players:
            player.displayPlayer()

        
