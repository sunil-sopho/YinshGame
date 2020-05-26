import pygame,sys


## game details

board_sizes = { 5 : 11, 6 : 13, 7 : 15 } # Rings : Board Size
display_size = { 5 : 650, 6 : 750, 7 : 850 } # Rings : Pixels

gameDisplay = pygame.display.set_mode((800,600))
pygame.display.set_caption('A bit Racey')
clock = pygame.time.Clock()
crashed = False



while not crashed:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True

        # print(event)

    pygame.display.update()
    clock.tick(60)

pygame.quit()
quit()

