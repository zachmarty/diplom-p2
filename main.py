import pygame
from classes import *

pygame.init()
screen = pygame.display.set_mode((1500, 750))
screen.fill((255, 255, 255))
base = BasicSquareObject((50, 50), 'Black', (725, 355))
target = BasicTriangleObject(30, 'red', (200, 200))

running = True
while running:

    base.draw(screen)
    target.draw(screen)
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
