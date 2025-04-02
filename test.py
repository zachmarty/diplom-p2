import pygame
from classes import *
from constants import *

pygame.init()
info = pygame.display.Info()
w = info.current_w
h = info.current_h

clock = pygame.time.Clock()
screen = pygame.display.set_mode((w, h), pygame.FULLSCREEN | pygame.SCALED)
screen_size = [screen.get_width(), screen.get_height()]
screen.fill((255, 255, 255))
robot = Robot.create_default_robot(dir = 0)
x_size = screen_size[0] / 4
y_size = screen_size[1] / 3 / 5
button = Button(screen_size[0] - x_size, 0, x_size, y_size, 'test', screen_size[1] / 25, 'black')
target = TriangleTarget(25, 500, 500)
base = BaseTarget()
robot.set_target(400, 499)
running = True
while running:
    screen.fill("White")
    clock.tick(TICKS)
    base.draw(screen)
    robot.draw(screen)
    button.draw(screen)
    target.draw(screen)
    if not robot.aligned:
        robot.rotate_to_target()
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()