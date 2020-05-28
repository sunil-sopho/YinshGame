import pygame,sys
import math
from board import Board,Player,Point
from config import *
from client import client
Size = 5
ring = 5


gameDisplay = pygame.display.set_mode((display_size[Size],display_size[Size]))
gameDisplay.fill(backgroundColor)
pygame.display.set_caption('A bit Racey')
clock = pygame.time.Clock()
crashed = False


board = Board(Size,ring,gameDisplay)

plays = []

def killPlayers():
	global plays
	for player in plays:
		player.closeChild()
	plays = []
	
board.plotPoints()
board.makeBoard()
# for i in range(8):
# 	board.addRing(5,1+i)
# board.addRing(4,4)
# board.addRing(4,5)

pygame.init()
fl = open("./Logs/log","w")
fl2 = open("./Logs/log2","w")
flOld = open("./Logs/oldLog","r")

moves = flOld.readlines()
movesHex = [] #fl2.readlines()

def gameWin(player):
	font = pygame.font.Font('freesansbold.ttf', 32) 
  

	text = font.render('Player '+str(player+1)+" wins", True, green, blue) 

	textRect = text.get_rect()  
	textRect.center = (300, 20)
	gameDisplay.blit(text, textRect)  

# draw board only one time
gameDisplay.blit(board.boardCanvas,(0,0))
while not crashed:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			crashed = True
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_q:
				crashed = True
				killPlayers()

			if event.key == pygame.K_r:
				pygame.display.flip()
			if event.key == pygame.K_d:
				# board.addRing(5,9)
				# print("again enterin")
				board.selectRing(5,2)
				# print("Learvin")

			# if event.key == pygame.K_w:
			if event.key == pygame.K_c:
				board.drawboard()

			if event.key == pygame.K_a:
				# auto execution code
				for move in moves:
					board.execute(move)
			if event.key == pygame.K_w:
				gameWin(1)
			if event.key == pygame.K_g:
				if len(movesHex) > 0:
					move = movesHex.pop(0)
					print(move)
					board.executeHex(move)
					board.drawboard()
				else:
					print("moveHex is empty")
			if event.key == pygame.K_j:
				for move in movesHex:
					board.executeHex(move)
					
			if event.key == pygame.K_s:
				plays.append(client("sh","run1.sh",1,5,120,5))
				plays.append(client("sh","run1.sh",2,5,120,5))
				print(plays)
			if event.key == pygame.K_d:
				while board.requiredMove != 5:
					pygame.display.update()
					cPlayer = board.getCurrentPlayer()
					move = plays[cPlayer].recieveData()
					move = move.decode()
					print("Player ",cPlayer," played :",move)
					mv,val = board.executeHex(move)
					if not val:
						print("Wrong move by :",cPlayer,' : ',move)
						# sys.exit(-1)
						killPlayers()
						break
					else:
						fl.write(str(mv)+"\n")
						fl2.write(str(move.strip())+"\n")
						plays[1-cPlayer].sendData(move)
				if board.requiredMove == 5:
					killPlayers()
					gameWin(cPlayer)

		if event.type == pygame.MOUSEBUTTONUP:
			
			pos = pygame.mouse.get_pos()
			move,val = board.isClickValid(Point(pos[0],pos[1]))
			if move :
				print(move)
				print(type(move))
				# fl.write(move)
			# print(pos," mouse click")
		# pygame.draw.lines(gameDisplay, GREEN, True, [[0, 80], [50, 90], [200, 80], [220, 30]], 3)
		# pygame.draw.aaline(gameDisplay, GREEN, [0, 50],[50, 80], True)
		# pygame.draw.line(gameDisplay, GREEN, (100,200), (300,450),5)
		# print(event)

	# gameDisplay.blit(board.guideCanvas,(0,0))
	# gameDisplay.blit(board.ringCanvas,(0,0))
	pygame.display.update()
	# gameDisplay.fill(red)

	clock.tick(60)

pygame.quit()
fl.close()
fl2.close()
flOld.close()
quit()

