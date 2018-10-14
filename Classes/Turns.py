from Classes.SetupGame import SetupGame

class Turns:

	turnNum = 0

	def __init__(self):

		Turns.turnNum = 0

	def takeTurn():

		if (Turns.turnNum == 0):
			for playerTurn in range(0,len(SetupGame.players)):

				# Players make initial move
				currentPlayer = SetupGame.players[SetupGame.currentPlayer-1]
				currentPlayer.makeFirstMove()
				SetupGame.nextPlayerSwap()

		else:

			# Progress Season
			SetupGame.progressSeason()

			# Resource collection
			SetupGame.resourceCollection()

			# Player turns
			for playerTurn in range(0,len(SetupGame.players)):

				#Player make random moves
				currentPlayer = SetupGame.players[SetupGame.currentPlayer-1]
				currentPlayer.makeMove()
				SetupGame.nextPlayerSwap()

		Turns.turnNum += 1

	def getTurnNum():
		return Turns.turnNum



