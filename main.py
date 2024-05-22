import pygame
from classes import *
import keyboard
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((1500, 750))
screen.fill((255, 255, 255))
base = BasicSquareObject((50, 50), 'Black', (725, 355))
target = BasicTriangleObject(30, (200, 200), 90)
robot = Robot((400, 500), 0, 40)
keyboard.add_hotkey('W', lambda: target.move())
button = Button(500, 50, 100, 50, 'ОГО', 'Black')

running = True
while running:
    screen.fill('White')
    base.draw(screen)
    robot.draw(screen)
    target.draw(screen)
    button.draw(screen)
    clock.tick(60)
    button.check_hover(pygame.mouse.get_pos())
    pygame.display.update()
    for event in pygame.event.get():
        button.handle_event(event=event)

        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
    
