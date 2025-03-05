import pygame
from classes import *
from constants import *

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WINDOW_LENGTH, WINDOW_HEIGHT))
screen.fill((255, 255, 255))
wheels = [BaseSquare(size=(WHEEL_WIDTH, DIAMETER), color="black"), BaseSquare(size=(WHEEL_WIDTH, DIAMETER), color="black")]
base = Robot(wheel1=wheels[0], wheel2=wheels[1], size = (LENGTH, WIDTH), cords=(500, 100), color='red')


running = True
while running:
    screen.fill("White")
    base.draw(screen)
    clock.tick(60)
    pygame.display.update()
    base.update_cords(500, 100, base.dir + 1)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()