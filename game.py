import pygame,sys
import math
Size = 5
ring = 5
## game details

board_sizes = { 5 : 11, 6 : 13, 7 : 15 } # Rings : Board Size
display_size = { 5 : 650, 6 : 750, 7 : 850 } # Rings : Pixels

gameDisplay = pygame.display.set_mode((display_size[Size],display_size[Size]))
pygame.display.set_caption('A bit Racey')
clock = pygame.time.Clock()
crashed = False
rows = board_sizes[Size]

positions = [None for _ in range(rows)]
for i in range(rows):
  positions[i] = [None for _ in range(rows)];

# colors
GREEN = (  255, 255,  255)

centerx = display_size[Size]/2
centery = display_size[Size]/2
spacing = display_size[Size]/rows;
altitude=spacing*math.sqrt(3)/2;

class Point(object):
	def __init__(self,x,y):
		self.x = x
		self.y = y
		self.guide = False
		self.piece = 0

def plotPoints():
	for i in range(rows):
		x = i -ring
		low = -ring
		high = ring
		if x == 0:
			low = 1-ring
			high = ring -1
		elif x>=1 and x < ring:
			low = x-ring
		elif x==ring:
			low = 1
			high = ring - 1
		elif x < 0 and x > -ring:
			high = ring+x
		elif x== -ring:
			low = 1-ring
			high = -1

		for j in range(rows):
			y = j -ring
			if not (y>=low and y<=high):
				positions[i][j] = Point(-1,-1)
				continue
			positions[i][j]= Point(centerx+altitude*x,centery-spacing*(y-x/2));
			positions[i][j].valid=True;

def drawLine(p1,p2,color=GREEN,wid=3):
	pygame.draw.line(gameDisplay, color, (p1.x,p1.y), (p2.x,p2.y),wid)

def makeBoard():

	# horizontal lines
	for i in range(rows):
		begin = 0
		end = rows - 1
		j = 0 
		while(positions[i][j].x==-1 and j<rows):
			j+=1
			if j==rows:
				break
			
		begin = j
		while positions[i][j].x!=-1 and j<rows :
			j+=1
			if j==rows:
				break
		end=j-1

		drawLine(positions[i][begin],positions[i][end],)

	# slant lines
	for j in range(rows):
		begin=0;
		end=rows-1;
		i=0;

		while(positions[i][j].x==-1 and i<rows):
			i+=1
			if i==rows:
				break
			
		
		begin=i;
		while(positions[i][j].x!=-1 and i<rows):
			i+=1
			if(i==rows):
				break
		end=i-1;
		drawLine(positions[begin][j],positions[end][j])

	for i in range(rows):
		for j in range(rows):
			x = i-ring
			y = j-ring
			if (x == ring or x == -ring) or (y==1 and x==1-ring) or (x==1-ring and y== 1-ring) or (x==1 and y == (1-ring)):
				drawLine(positions[i][j],positions[ring-y][ring-x])
plotPoints()
makeBoard()

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

