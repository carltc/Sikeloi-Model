from tkinter import *
from tkinter.ttk import *
import math

from Classes.Terrain import Terrain
from Classes.SetupGame import SetupGame

class GameBoard(Frame):

    VisualiseIndices = 0

    def __init__(self,frameHandle):
        super().__init__()

        #self.initBoard(frameHandle,gameSetup)

        self.canvas = Canvas(frameHandle)

    def visualiseGameBoard(self,frameHandle):

        canvas = self.canvas

        scale = 6
        
        nodeY = 6;
        nodeX = math.cos(30*math.pi/180)*nodeY
        
        # Draw board tiles
        for boardTile in SetupGame.mainBoard.boardTiles:
            offSetX = (boardTile.X*nodeX*2*scale) + ((1-(boardTile.Y%2))*nodeX*scale)
            offSetY = (boardTile.Y*12*scale) - ((boardTile.Y-1)*3*scale)
            
            if boardTile.hidden == 1:
                canvas.create_polygon((scale*0)+offSetX, (scale*nodeY)+offSetY,
                                      (scale*nodeX)+offSetX, (scale*nodeY/2)+offSetY,
                                      (scale*nodeX)+offSetX, (-scale*nodeY/2)+offSetY,
                                      (scale*0)+offSetX, (-scale*nodeY)+offSetY,
                                      (-scale*nodeX)+offSetX, (-scale*nodeY/2)+offSetY,
                                      (-scale*nodeX)+offSetX, (scale*nodeY/2)+offSetY,
                                      outline="#000000",
                                      fill="#383838",
                                      width=2)
                #rockImage = PhotoImage(file="rock.png")
                #canvas.create_image(offSetX, offSetY, image=rockImage, anchor=CENTER)
            else:
                canvas.create_polygon((scale*0)+offSetX, (scale*nodeY)+offSetY,
                                      (scale*nodeX)+offSetX, (scale*nodeY/2)+offSetY,
                                      (scale*nodeX)+offSetX, (-scale*nodeY/2)+offSetY,
                                      (scale*0)+offSetX, (-scale*nodeY)+offSetY,
                                      (-scale*nodeX)+offSetX, (-scale*nodeY/2)+offSetY,
                                      (-scale*nodeX)+offSetX, (scale*nodeY/2)+offSetY,
                                      outline=Terrain.terrainColour[boardTile.terrain.terrainID-1],
                                      fill=Terrain.terrainBorderColour[boardTile.terrain.terrainID-1],
                                      width=2)
                #if boardTile.terrain.resource.resourceID != 0:
                    #canvas.create_image(offSetX, offSetY, image=boardTile.terrain.resource.image, anchor=CENTER)

            if GameBoard.VisualiseIndices == 1:
                canvas.create_text(offSetX, offSetY, font=("Purisa", 20),
                    text=boardTile.tileID)
            
            canvas.pack(fill=BOTH, expand=1)

            # Show nodes
            #boardTile.showNodes()

            # Draw board nodes
            if GameBoard.VisualiseIndices == 1:
                canvas.create_text((scale*0)+offSetX, (scale*nodeY)+offSetY,
                    font="Purisa",
                    text=boardTile.nodes[3])
                canvas.create_text((scale*nodeX)+offSetX, (scale*nodeY/2)+offSetY,
                    font="Purisa",
                    text=boardTile.nodes[2])
                canvas.create_text((scale*nodeX)+offSetX, (-scale*nodeY/2)+offSetY,
                    font="Purisa",
                    text=boardTile.nodes[1])
                canvas.create_text((scale*0)+offSetX, (-scale*nodeY)+offSetY,
                    font="Purisa",
                    text=boardTile.nodes[0])
                canvas.create_text((-scale*nodeX)+offSetX, (-scale*nodeY/2)+offSetY,
                    font="Purisa",
                    text=boardTile.nodes[5])
                canvas.create_text((-scale*nodeX)+offSetX, (scale*nodeY/2)+offSetY,
                    font="Purisa",
                    text=boardTile.nodes[4])

            SetupGame.mainBoard.boardNodes[boardTile.nodes[3]-1].addLocation(
                (scale*0)+offSetX, (scale*nodeY)+offSetY)
            SetupGame.mainBoard.boardNodes[boardTile.nodes[2]-1].addLocation(
                (scale*nodeX)+offSetX, (scale*nodeY/2)+offSetY)
            SetupGame.mainBoard.boardNodes[boardTile.nodes[1]-1].addLocation(
                (scale*nodeX)+offSetX, (-scale*nodeY/2)+offSetY)
            SetupGame.mainBoard.boardNodes[boardTile.nodes[0]-1].addLocation(
                (scale*0)+offSetX, (-scale*nodeY)+offSetY)
            SetupGame.mainBoard.boardNodes[boardTile.nodes[5]-1].addLocation(
                (-scale*nodeX)+offSetX, (-scale*nodeY/2)+offSetY)
            SetupGame.mainBoard.boardNodes[boardTile.nodes[4]-1].addLocation(
                (-scale*nodeX)+offSetX, (scale*nodeY/2)+offSetY)
            
            # Draw tile edges
            #print(boardTile.edges)
            for edge in boardTile.edges:

                tileEdge = SetupGame.mainBoard.tileEdges[edge-1]
                node1 = SetupGame.mainBoard.boardNodes[tileEdge.nodes[0]-1]
                node2 = SetupGame.mainBoard.boardNodes[tileEdge.nodes[1]-1]
                #print(tileEdge.edgeID,node1.nodeID,node2.nodeID)
                edgeX = ((node2.X - node1.X)/2) + node1.X
                edgeY = ((node2.Y - node1.Y)/2) + node1.Y
                SetupGame.mainBoard.tileEdges[edge-1].addLocation(edgeX,edgeY)
                tileEdge = SetupGame.mainBoard.tileEdges[edge-1]

                if GameBoard.VisualiseIndices == 1:
                    canvas.create_text(tileEdge.X,tileEdge.Y,
                        font=("Purisa", 10),
                        text=edge)

            # Draw villagers
            if boardTile.villager == 1:
                player = SetupGame.players[boardTile.playerID-1]
                canvas.create_oval(offSetX - (scale*4), offSetY - (scale*3), offSetX - (scale*2), offSetY + (scale*3),
                    outline="#000000",
                    fill=player.colour,
                    width=2)
            # Draw Scouts
            if boardTile.scout == 1:
                player = SetupGame.players[boardTile.playerID-1]
                canvas.create_polygon(offSetX + (scale*2), offSetY - (scale*1),
                    offSetX + (scale*1), offSetY + (scale*2),
                    offSetX + (scale*3), offSetY + (scale*2),
                    outline="#000000",
                    fill=player.colour,
                    width=2)


        # Draw node buildings
        for boardNode in SetupGame.mainBoard.boardNodes:
            if boardNode.status == 1:
                if boardNode.buildingType == 1:
                    nodeX = 2
                    nodeY = 2
                    offSetX = (boardNode.X)
                    offSetY = (boardNode.Y)

                    #print(boardNode.X,boardNode.Y,scale,offSetX,offSetY)

                    player = SetupGame.players[boardNode.playerID-1]

                    canvas.create_polygon((scale*-nodeX)+offSetX, (scale*-nodeY)+offSetY,
                                  (scale*nodeX)+offSetX, (scale*-nodeY)+offSetY,
                                  (scale*nodeX)+offSetX, (scale*nodeY)+offSetY,
                                  (scale*-nodeX)+offSetX, (scale*nodeY)+offSetY,
                                  outline="#000000",
                                  fill=player.colour,
                                  width=2)

        # Draw roads
        for tileEdge in SetupGame.mainBoard.tileEdges:
            if tileEdge.status == 1:

                node1 = SetupGame.mainBoard.boardNodes[tileEdge.nodes[0]-1]
                node2 = SetupGame.mainBoard.boardNodes[tileEdge.nodes[1]-1]

                player = SetupGame.players[tileEdge.playerID-1]

                #print(node1.X, node1.Y, node2.X, node2.Y)

                canvas.create_line(node1.X, node1.Y, node2.X, node2.Y,
                    fill=player.colour,
                    width=8)

    def clearCanvas(self):
        self.canvas.delete("all")
        

        

    
