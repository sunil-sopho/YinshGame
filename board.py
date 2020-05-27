import math
from config import *
import pygame
requiredMove = 0

currentPlayer = 0



class Player(object):
	def __init__(self,playernum):
		self.playernum = playernum
		self.boardRings = 0
		self.ringsWon =0 
		self.currentRing = [-1,-1]
		self.fiveRow = []

def switchPlayer():
	global currentPlayer
	currentPlayer = 1 - currentPlayer


class Point(object):
	def __init__(self,x,y):
		self.x = x
		self.y = y
		self.guide = False
		self.piece = 0

class Board(object):

	def __init__(self,Size,ring,gameDisplay):
		self.Size = Size
		self.rows = board_sizes[Size]
		self.ring = ring
		self.gameDisplay = gameDisplay
		self.centerx = display_size[Size]/2
		self.centery = display_size[Size]/2
		self.spacing = display_size[Size]/self.rows;
		self.altitude=self.spacing*math.sqrt(3)/2;

		self.positions = [None for _ in range(self.rows)]
		for i in range(self.rows):
			self.positions[i] = [None for _ in range(self.rows)];

		self.players = [Player(i) for i in range(self.rows)]


	def plotPoints(self):
		for i in range(self.rows):
			x = i -self.ring
			low = -self.ring
			high = self.ring
			if x == 0:
				low = 1-self.ring
				high = self.ring -1
			elif x>=1 and x < self.ring:
				low = x - self.ring
			elif x==self.ring:
				low = 1
				high = self.ring - 1
			elif x < 0 and x > -self.ring:
				high = self.ring+x
			elif x== -self.ring:
				low = 1-self.ring
				high = -1

			for j in range(self.rows):
				y = j - self.ring
				if not (y>=low and y<=high):
					self.positions[i][j] = Point(-1,-1)
					continue
				self.positions[i][j]= Point(self.centerx+self.altitude*x,self.centery-self.spacing*(y-x/2))
				self.positions[i][j].valid=True;

	def drawLine(self,p1,p2,color=GREEN,wid=3):
		pygame.draw.line(self.gameDisplay, color, (p1.x,p1.y), (p2.x,p2.y),wid)

	def makeBoard(self):

		# horizontal lines
		for i in range(self.rows):
			begin = 0
			end = self.rows - 1
			j = 0 
			while self.positions[i][j].x==-1 and j < self.rows:
				j+=1
				if j == self.rows:
					break
				
			begin = j
			while self.positions[i][j].x!=-1 and j < self.rows :
				j+=1
				if j==self.rows:
					break
			end=j-1

			self.drawLine(self.positions[i][begin],self.positions[i][end])

		# slant lines
		for j in range(self.rows):
			begin=0;
			end=self.rows-1;
			i=0;

			while self.positions[i][j].x==-1 and i<self.rows:
				i+=1
				if i==self.rows:
					break
				
			
			begin=i;
			while self.positions[i][j].x!=-1 and i < self.rows:
				i+=1
				if(i==self.rows):
					break
			end=i-1;
			self.drawLine(self.positions[begin][j],self.positions[end][j])

		for i in range(self.rows):
			for j in range(self.rows):
				x = i - self.ring
				y = j - self.ring
				ring = self.ring
				if (x == ring or x == -ring) or (y==1 and x==1-ring) or (x==1-ring and y== 1-ring) or (x==1 and y == (1-ring)):
					self.drawLine(self.positions[i][j],self.positions[ring-y][ring-x])


	def drawRing(self,point,playerNum,wid=4):
		# print(point.y)
		color = red
		if playerNum == 1:
			color = blue
		pygame.draw.circle(self.gameDisplay,color,(int(point.x),int(point.y)),25,wid)

	def addRing(self,x,y):
		if self.positions[x][y].piece == 0:
			self.drawRing(self.positions[x][y],currentPlayer)
			if self.players[currentPlayer].boardRings == self.ring and self.players[1-currentPlayer].boardRings == self.ring:
				requiredMove = 1
			switchPlayer()
			return True
		else:
			return False

