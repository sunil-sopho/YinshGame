import math
import sys
from config import *
import pygame

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

	def __init__(self,Size,ring,gameDisplay,seq=5):
		self.Size = Size
		self.rows = board_sizes[Size]
		self.ring = ring
		self.seq = seq
		self.gameDisplay = gameDisplay
		self.centerx = display_size[Size]/2
		self.centery = display_size[Size]/2
		self.spacing = display_size[Size]/self.rows;
		self.altitude=self.spacing*math.sqrt(3)/2;

		self.oldPlayer = 0
		self.requiredMove = 0
		self.temp = ""
		self.strx =None
		self.stry =None
		self.positions = [None for _ in range(self.rows)]
		for i in range(self.rows):
			self.positions[i] = [None for _ in range(self.rows)];

		self.players = [Player(i) for i in range(2)]

		# ring location tracker help in ringCanvas
		self.ringLoc = [[] for _ in range(2)]

		# canvas for guide
		self.guideCanvas = pygame.Surface((display_size[Size], display_size[Size]), pygame.SRCALPHA, 32)
		self.guideCanvas = self.guideCanvas.convert_alpha()

		self.boardCanvas = pygame.Surface((display_size[Size], display_size[Size]), pygame.SRCALPHA, 32)
		self.boardCanvas = self.boardCanvas.convert_alpha()

		self.ringCanvas = pygame.Surface((display_size[Size], display_size[Size]), pygame.SRCALPHA, 32)
		self.ringCanvas = self.ringCanvas.convert_alpha()

		self.dotCanvas = pygame.Surface((display_size[Size], display_size[Size]), pygame.SRCALPHA, 32)
		self.dotCanvas = self.dotCanvas.convert_alpha()

	def getCurrentPlayer(self):
		return currentPlayer

	def clear(self):
		self.gameDisplay.fill(backgroundColor)

		self.gameDisplay.blit(self.boardCanvas, (0,0))
		self.gameDisplay.blit(self.ringCanvas, (0,0))
		self.gameDisplay.blit(self.guideCanvas, (0,0))
		self.gameDisplay.blit(self.dotCanvas, (0,0))

	def clearGuideSurface(self):
		self.guideCanvas = pygame.Surface((display_size[self.Size], display_size[self.Size]), pygame.SRCALPHA, 32)
		self.guideCanvas = self.guideCanvas.convert_alpha()
		self.clear()

	def clearRingSurface(self):
		self.ringCanvas = pygame.Surface((display_size[self.Size], display_size[self.Size]), pygame.SRCALPHA, 32)
		self.ringCanvas = self.ringCanvas.convert_alpha()


	def clearDotSurface(self):
		self.dotCanvas = pygame.Surface((display_size[self.Size], display_size[self.Size]), pygame.SRCALPHA, 32)
		self.dotCanvas = self.dotCanvas.convert_alpha()


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
		# draw on board Canvas
		pygame.draw.line(self.boardCanvas, color, (p1.x,p1.y), (p2.x,p2.y),wid)

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


	def drawRing(self,point,playerNum,wid=4,size=25):

		color = red
		if playerNum == 1:
			color = blue
		elif playerNum == -1:
			# black guide
			color = black
			size = 10
			pygame.draw.circle(self.guideCanvas,color,(int(point.x),int(point.y)),size,wid)
			return

		pygame.draw.circle(self.ringCanvas,color,(int(point.x),int(point.y)),size,wid)

	def addRing(self,x,y):
		if self.positions[x][y].piece == 0:
			# ring is added
			self.ringLoc[currentPlayer].append(self.positions[x][y])

			self.drawRing(self.positions[x][y],currentPlayer)
			self.players[currentPlayer].boardRings +=1
			self.positions[x][y].piece = math.pow(-1,currentPlayer)*2
			if self.players[currentPlayer].boardRings == self.ring and self.players[1-currentPlayer].boardRings == self.ring:
				self.requiredMove = 1
			switchPlayer()
			return True
		else:
			return False

	def blackGuides(self,x,y,asign,bsign,guide):
		tokenLine = 0
		a=asign
		b=bsign
		while x+a >=0 and x+a < self.rows and y+b>=0 and y+b < self.rows and abs(self.positions[x+a][y+b].piece)!=2 and self.positions[x+a][y+b].x != -1:
			if self.positions[x+a][y+b].piece != 0:
				tokenLine = 1
				a += asign
				b += bsign
				continue
			else:
				self.drawRing(self.positions[x+a][y+b],-1,0)

			self.positions[x+a][y+b].guide = guide
			if tokenLine== 1:
				break
			a += asign
			b += bsign

	def addDot(self,point,player,size=20):
		"""
		player -1 : black dot marks when 5/seq in row
				0 : red
				1 : blue 
		"""
		color = red
		canvas = self.dotCanvas
		if player == 1:
			color = blue
		if player == -1:
			color = black
			size = 16
			canvas = self.guideCanvas
		wid = size//2
		pygame.draw.circle(canvas,color,(int(point.x),int(point.y)),size,0)

		stepSize = wid
		colorGradient = tuple(map(lambda i, j: (i - j)/wid, black, color)) 
		for i in range(stepSize):
			# color = black - i*(colorGradient)
			color = tuple(map(lambda a,b: a-i*b,black,colorGradient))
			
			pygame.draw.circle(canvas,color,(int(point.x),int(point.y)),size-i,1)


	def selectRing(self,x,y):
		if self.positions[x][y].piece == math.pow(-1,currentPlayer)*2:
			
			self.addDot(self.positions[x][y],currentPlayer)

			self.players[currentPlayer].currentRing = [x,y]
			for i in [-1,0,1]:
				for j in [-1,0,1]:
					if i*j == -1 or i==j==0:
						continue
					else:

						self.blackGuides(x,y,i,j,True)
						# print("-----------")
			self.requiredMove = 2
			return True
		else:

			return False

	def sign(self,val):
		if val < 0:
			return -1
		if val > 0:
			return 1
		if val == 0:
			return 0 

		else:
			print(" Stuck in sign")
			while True:
				continue

	def removeBlackGuides(self,x,y,destx,desty,asign,bsign):
		flip = 0
		if self.sign(destx-x) == self.sign(asign) and self.sign(desty - y) == self.sign(bsign):
			flip = 1

		a = asign
		b = bsign
		while x+a >=0 and x+a < self.rows and y+b>=0 and y+b < self.rows and abs(self.positions[x+a][y+b].piece)!=2 and self.positions[x+a][y+b].x != -1:
			if self.positions[x+a][y+b].piece == 0:
				self.positions[x+a][y+b].guide = False

				if x+a == destx and y+b == desty:
					self.positions[x][y].piece = math.pow(-1,currentPlayer)
					self.positions[x+a][y+b].piece = math.pow(-1,currentPlayer)*2

					loc = -1
					for i in range(len(self.ringLoc[currentPlayer])):
						p1 = self.ringLoc[currentPlayer][i]

						if self.positions[x][y].x == p1.x and self.positions[x][y].y == p1.y:
							loc = i

							break

					self.ringLoc[currentPlayer][i] = self.positions[destx][desty]


					flip = 0

			if  flip == 1 and abs(self.positions[x+a][y+b].piece) == 1:

				self.positions[x+a][y+b].piece *= -1 # flip dot


				# plot on board
				# autoplot

			a += asign
			b += bsign

	def checkRows(self):
		for i in range(self.rows):
			for j in range(self.rows-self.seq+1):
				if abs(self.positions[i][j].piece) != 1 or self.positions[i][j].x == -1:
					continue

				isRow = True
				for k in range(1,self.seq):
					if self.positions[i][j].piece != self.positions[i][j+k].piece or self.positions[i][j+k].x == -1 or j+k >= self.rows:
						isRow = False
						break

				if not isRow:
					continue

				rowPlayer = 1
				if self.positions[i][j].piece == 1:
					rowPlayer = 0

				rowComplete = []


				for k in range(self.seq):
					rowComplete.append([i,j+k])

				self.players[rowPlayer].fiveRow.append(rowComplete)


		for i in range(self.rows-self.seq+1):
			for j in range(self.rows):
				if abs(self.positions[i][j].piece) != 1 or self.positions[i][j].x == -1:
					continue

				isRow = True
				for k in range(1,self.seq):
					if self.positions[i][j].piece != self.positions[i+k][j].piece or self.positions[i][j].x == -1 or j+k >= self.rows:
						isRow = False
						break

				if not isRow:
					continue

				rowPlayer = 1
				if self.positions[i][j].piece == 1:
					rowPlayer = 0

				rowComplete = []


				for k in range(self.seq):
					rowComplete.append([i+k,j])

				self.players[rowPlayer].fiveRow.append(rowComplete)

		for i in range(self.rows):
			for j in range(self.rows):
				if abs(self.positions[i][j].piece) != 1 or self.positions[i][j].x == -1:
					continue

				isRow = True
				for k in range(1,self.seq):
					if i+k >= self.rows or j+k >= self.rows or self.positions[i][j].piece != self.positions[i+k][j+k].piece or self.positions[i+k][j+k].x == -1:
						isRow = False
						break

				if not isRow:
					continue

				rowPlayer = 1
				if self.positions[i][j].piece == 1:
					rowPlayer = 0

				rowComplete = []


				for k in range(self.seq):
					rowComplete.append([i+k,j+k])

				self.players[rowPlayer].fiveRow.append(rowComplete)


	def highlightRow(self,state=3):
		# @sunil 1 more command here
		self.clearGuideSurface()
		fiveInRow = len(self.players[currentPlayer].fiveRow)
		if fiveInRow !=0:
			for i in range(fiveInRow):
				for j in range(self.seq):
					xindex = self.players[currentPlayer].fiveRow[i][j][0]
					yindex = self.players[currentPlayer].fiveRow[i][j][1]

					self.addDot(self.positions[xindex][yindex],-1)

			self.requiredMove = state

	def moveRings(self,x,y):
		if self.positions[x][y].guide:
			self.clearGuideSurface()
			for i in [-1,0,1]:
				for j in [-1,0,1]:
					if i*j < 0 or i==j==0:
						continue
					else:
						self.removeBlackGuides(self.players[currentPlayer].currentRing[0],self.players[currentPlayer].currentRing[1],x,y,i,j)

			self.requiredMove = 1
			self.checkRows()
			if debug:
				print("Number of 5 in row : ",len(self.players[currentPlayer].fiveRow))
			self.highlightRow()
			# print(self.requiredMove, "  :: RM")
			if self.requiredMove != 3:
				# print(currentPlayer, "  :: PL")
				switchPlayer()
				# print(currentPlayer ,"  :: PL")

				self.highlightRow(state=6) 

			return True
		else:
			for i in [-1,0,1]:
				for j in [-1,0,1]:
					if i*j < 0 or i==j==0:
						continue
					else:
						self.blackGuides(self.players[currentPlayer].currentRing[0],self.players[currentPlayer].currentRing[1],i,j,False)
			self.clearGuideSurface()
			self.requiredMove = 1

			return False

	def matchPoint(self,x1,y1,x2,y2):
		if x1 == x2 and y1 == y2:
			return True
		return False


	def removeRow(self,x,y,state=4):
		if x == None or y == None:
			return False

		rowCount = 0
		selectRow = -1

		if debug:
			if len(self.players[currentPlayer].fiveRow) == 0:
				print("Remove Row called without 5 in row")
			else:
				print("Remove Row called with : ",x,y)

		for i in range(len(self.players[currentPlayer].fiveRow)):
			fpx = self.players[currentPlayer].fiveRow[i][0][0]
			fpy = self.players[currentPlayer].fiveRow[i][0][1]
			lpx = self.players[currentPlayer].fiveRow[i][self.seq-1][0]
			lpy = self.players[currentPlayer].fiveRow[i][self.seq-1][1]

			if self.matchPoint(x,y,fpx,fpy) or self.matchPoint(x,y,lpx,lpy):
				if state == 4:
					self.requiredMove = 3.5
				else:
					self.requiredMove = 6.5

				if debug:
					print("matchPoint found and requiredMove is : ",self.requiredMove)
				return True

		return False

	def removeRowEnd(self,stx,sty,edx,edy,state=4):
		if stx == None or sty == None or edx == None or edy == None :
			print("Failed in removeRowEnd ")
			print("stx: ",str(stx),"sty: ",sty,"edx: ",edx,"edy: ",edy,"state: ",state)
			return False

		rowCount = 0
		selectRow = -1

		for i in range(len(self.players[currentPlayer].fiveRow)):
			fpx = self.players[currentPlayer].fiveRow[i][0][0]
			fpy = self.players[currentPlayer].fiveRow[i][0][1]
			lpx = self.players[currentPlayer].fiveRow[i][self.seq-1][0]
			lpy = self.players[currentPlayer].fiveRow[i][self.seq-1][1]

			if (self.matchPoint(stx,sty,fpx,fpy) and self.matchPoint(edx,edy,lpx,lpy)) or (self.matchPoint(stx,sty,lpx,lpy) and self.matchPoint(edx,edy,fpx,fpy)):
				selectRow = i
				rowCount +=1

		if rowCount >=1:
			removeList = [selectRow]

			for k in range(self.seq):
				xclear = self.players[currentPlayer].fiveRow[selectRow][k][0]
				yclear = self.players[currentPlayer].fiveRow[selectRow][k][1]
				# @sunil clear rect around this area of piece or dot


				################################################################
				self.positions[xclear][yclear].piece = 0
				# @sunil loop here we not need

			self.players[currentPlayer].fiveRow = []
			self.checkRows()
			self.requiredMove = state

			self.clearGuideSurface()
			return True
		else:
			return False



	def removeRing(self,x,y,state=4):
		if self.positions[x][y].piece == math.pow(-1,currentPlayer)*2:
			self.players[currentPlayer].ringsWon +=1
			self.players[currentPlayer].boardRings -=1

			# @sunil clear ring here
			# self.removeRingSurface(self.positions[x][y])
			loc = -1
			for i in range(len(self.ringLoc[currentPlayer])):
				p1 = self.ringLoc[currentPlayer][i]
				# print(self.positions[x][y].x," : ",self.positions[x][y].y," point")
				if self.positions[x][y].x == p1.x and self.positions[x][y].y == p1.y:
					loc = i
					break
			# print(self.ringLoc[currentPlayer])
			if currentPlayer == 0:
				self.ringLoc[currentPlayer][i] = Point(500+self.players[currentPlayer].ringsWon*20,30)
			else:
				self.ringLoc[currentPlayer][i] = Point(50+self.players[currentPlayer].ringsWon*20,30)

			# @sunil add ring won

			self.positions[x][y].piece = 0

			if self.players[currentPlayer].ringsWon == 3:
				self.requiredMove = 5
				switchPlayer()

			elif len(self.players[currentPlayer].fiveRow) == 0:
				if state != 7:
					switchPlayer()

				if len(self.players[currentPlayer].fiveRow) == 0 :
					self.requiredMove = 1
				else:
					highlightRow(6)

			else:
				highlightRow()

			return True
		else:
			return False

	def drawRingSurface(self):
		self.clearRingSurface()
		for i in range(2):
			for point in self.ringLoc[i]:
				self.drawRing(point,i)


	def drawDotSurface(self):
		self.clearDotSurface()
		for i in range(self.rows):
			for j in range(self.rows):
				if self.positions[i][j].piece == 0 or self.positions[i][j].x == -1:
					continue
				if abs(self.positions[i][j].piece) == 1:
					if self.positions[i][j].piece == 1:
						self.addDot(self.positions[i][j],0)
					else:
						self.addDot(self.positions[i][j],1)

	def complete(self):
		self.drawRingSurface()
		self.drawDotSurface()
		self.clear()


	def between(self,p1,p2):
		if p1.x - self.altitude/2  < p2.x and p1.x + self.altitude/2 > p2.x:
			if p1.y - self.altitude/2  < p2.y and p1.y + self.altitude/2 > p2.y:
				return True
		return False



	def isClickValid(self,mouse):

		for i in range(self.rows):
			for j in range(self.rows):
				if self.positions[i][j].x == -1:
					continue

				if self.between(self.positions[i][j],mouse):

					valid = False
					move = ""

					if self.requiredMove == 0:
						valid = self.addRing(i,j)
						move = "P "+str(i)+" "+str(j)+" "
					elif self.requiredMove == 1:
						valid = self.selectRing(i,j)
						move = "S "+str(i)+" "+str(j)+" "
					elif self.requiredMove == 2:
						valid = self.moveRings(i,j)
						move = "M "+str(i)+" "+str(j)+" "
					elif self.requiredMove == 3:
						valid = self.removeRow(i,j)
						self.strx = i
						self.stry = j
					elif self.requiredMove == 3.5:
						valid = self.removeRowEnd(self.strx,self.stry,i,j)
						move = "RS "+str(self.strx)+" "+str(self.stry)+" RE "+str(i)+" "+str(j)+" "
					elif self.requiredMove == 4:
						valid = self.removeRing(i,j)
						move = "X "+str(i)+" "+str(j)+" "
					elif self.requiredMove == 6:
						valid = self.removeRow(i,j,7)
						self.strx = i
						self.stry = j
					elif self.requiredMove == 6.5:
						valid = self.removeRowEnd(self.strx,self.stry,i,j,7)
						move = "RS "+str(self.strx)+" "+str(self.stry)+" RE "+str(i)+" "+str(j)+" "                    	

					elif self.requiredMove == 7:
						valid = self.removeRing(i,j)
						move = "X "+str(i)+" "+str(j)+" "

					if valid:
						if self.oldPlayer == currentPlayer:
							self.temp += move
						else:
							ret = self.temp + move
							self.temp = ""
							self.oldPlayer = currentPlayer
							self.complete()
							return ret,valid

					if valid:
						self.complete()
						return "",valid

		return "",False

	def execute(self,move):
		if move == "" or move == None:
			sys.stderr.write("Invalid Move : "+move+"\n")
			sys.exit(-1)
		else:
			move = move.split(" ")
			for i in range(len(move)//3):

				mv,val = self.isClickValid(self.positions[int(move[i*3+1])][int(move[i*3+2])])	
				if not val:
					sys.stderr.write("Invalid Move : "+str(move[i*3])+" "+str(move[i*3+1])+" "+str(move[i*3+2])+"\n")
					sys.exit(-1)

	def convertFromHex(self,x,y):
		i=j=0
		x -= self.Size-1
		y -= self.Size-1
		card=dev=shell=0
		if x==0 and y==0:
			return i,j
		elif x>=0 and y < 0:
			card=0
			shell=x-y
			dev=x
		elif x>y and y >=0:
			card=1
			shell=x
			dev=y
		elif x<= y and x>0:
			card=2
			shell=y
			dev=y-x
		elif x<=0 and y>0:
			card=3
			dev =-x
			shell=y-x
		elif x<y and y<=0:
			card=4
			dev =-y
			shell=-x
		else:
			card=5
			shell=-y
			dev=x-y
		return shell,card*shell+dev

	def convertFromHex2(self,shell,position):
		x=self.Size;
		y=self.Size;
		if shell!=0 :
			dev = position % shell;
			card = position // shell;
			print(card,x,y,dev,shell)
			if card==0:
				#straight up
				y=y+shell;
				x+=dev;
			elif card==1:
				#right
				# x+=shell;
				# y+=dev;
				x+=shell
				y+=shell-dev

			elif card==2:
				#right down
				x=x+shell-dev;
				y-=dev;
			elif card==3:
				#straight down
				y-=shell;
				x-=dev
			elif card==4:
				#left
				x-=shell;
				y-=shell-dev;
			else:
				#left up
				x-=shell-dev;
				y+=dev;
		return x,y


	def drawboard(self):
		for i in range(self.rows):
			for j in range(self.rows):
				if self.positions[i][j].x == -1:
					print("x",end=' ')
				else:
					if self.positions[i][j].piece != 0:
						print("1",end=" ",)
					else:
						print(self.positions[i][j].piece,end=' ')
			print()

	def executeHex(self,move):
		val = False
		mv = ""
		if move == "" or move == None:
			sys.stderr.write("Invalid Move : "+str(move)+"\n")
			# sys.exit(-1)
		else:
			move = move.split(" ")
			for i in range(len(move)//3):
				hexi,hexj = self.convertFromHex2(int(move[i*3+1]),int(move[i*3+2]))
				move[i*3+1] = hexi
				move[i*3+2] = hexj
				print(hexi,hexj)
				mv,val = self.isClickValid(self.positions[int(move[i*3+1])][int(move[i*3+2])])	
				if not val:
					sys.stderr.write("Invalid Move : "+str(move[i*3])+" "+str(move[i*3+1])+" "+str(move[i*3+2])+"\n")
					# sys.exit(-1)
		return mv,val