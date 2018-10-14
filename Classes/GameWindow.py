from tkinter import *
from tkinter.ttk import *

from Classes.GameBoard import *
from Classes.SetupGame import SetupGame
from Classes.SimulateGame import SimulateGame
from Classes.Turns import Turns

class GameWindow(Frame):

    gameBoard = None
  
    def __init__(self):

        super().__init__()

        self.turnText = StringVar()
         
        self.initUI()
        
    
    def initUI(self):
        # Set windows parameters
        self.master.title("Sikeloi Modelling")
        self.style = Style()
        self.style.theme_use("default")

        # Initialise Game Board
        GameWindow.gameBoard = GameBoard(self)
        gameSetup = SetupGame()
        GameWindow.gameBoard.visualiseGameBoard(self)

        # Initialise turns
        Turns()
        self.turnText.set(["Turn: ",Turns.turnNum])
        
        # Reposition the current elements to fill window
        self.pack(fill=BOTH, expand=1)

        # Add a simulation button - Runs Simulation
        simulateButton = Button(self, text="Simulate",
            command=self.simulate)
        simulateButton.pack(side=LEFT, padx=5, pady=5)

        # Add a clear button - Clears current canvas frame
        clearButton = Button(self, text="Reset",
            command=self.clear)
        clearButton.pack(side=LEFT, padx=5, pady=5)

        # Add a progress button - Progresses game by 1 turn
        progressButton = Button(self, text="Progress",
            command=self.progress)
        progressButton.pack(side=RIGHT, padx=5, pady=5)

        self.lbl1 = Label(self, textvariable=self.turnText, width=20)
        self.lbl1.pack(side=RIGHT, padx=5, pady=5)  

    def simulate(self):
        print("Simulation started...")
        Turns()
        Terrain.resetTerrainCounts()
        gameSetup = SetupGame()
        simulation = SimulateGame()

        # Clear canvas and draw new simulation
        GameWindow.gameBoard.clearCanvas()
        GameWindow.gameBoard.visualiseGameBoard(self)

        self.turnText.set(["Turn: ",Turns.turnNum])

    def clear(self):
        print("Board Reset.")
        Turns()
        Terrain.resetTerrainCounts()
        gameSetup = SetupGame()
        GameWindow.gameBoard.clearCanvas()
        GameWindow.gameBoard.visualiseGameBoard(self)

    def progress(self):
        print("Progress to turn ", Turns.turnNum)
        Turns.takeTurn()
        GameWindow.gameBoard.clearCanvas()
        GameWindow.gameBoard.visualiseGameBoard(self) 

        self.turnText.set(["Turn: ",Turns.turnNum])
        
