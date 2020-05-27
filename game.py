import pygame,sys
import math
from board import Board,Player
from config import *
Size = 5
ring = 5


gameDisplay = pygame.display.set_mode((display_size[Size],display_size[Size]))
gameDisplay.fill(backgroundColor)
pygame.display.set_caption('A bit Racey')
clock = pygame.time.Clock()
crashed = False


board = Board(Size,ring,gameDisplay)




board.plotPoints()
board.makeBoard()
board.addRing(5,6)
board.addRing(5,9)
while not crashed:

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			crashed = True
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_q:
				crashed = True

		# pygame.draw.lines(gameDisplay, GREEN, True, [[0, 80], [50, 90], [200, 80], [220, 30]], 3)
		# pygame.draw.aaline(gameDisplay, GREEN, [0, 50],[50, 80], True)
		# pygame.draw.line(gameDisplay, GREEN, (100,200), (300,450),5)
		print(event)

	pygame.display.update()
	clock.tick(60)

pygame.quit()
quit()

