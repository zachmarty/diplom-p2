import pygame
from classes import *

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((1500, 750))
screen.fill((255, 255, 255))
base = BasicSquareObject((50, 50), "Black", (725, 355))
target = BasicTriangleObject(30, [200, 200], 90)
robots = []
add_button = Button(1200, 0, 300, 50, "Добавить", "Green")
remove_button = Button(1200, 50, 300, 50, "Удалить", "Red")
move_target_button = MoveTargetButton(1200, 100, 300, 50, "Цель", "Black")
move_base_button = MoveTargetButton(1200, 150, 300, 50, "База", "Yellow")

running = True
while running:
    screen.fill("White")
    base.draw(screen)
    target.draw(screen)
    add_button.draw(screen)
    remove_button.draw(screen)
    move_base_button.draw(screen)
    move_target_button.draw(screen)
    if len(robots) > 0:
        for robot in robots:
            robot.draw(screen)
    clock.tick(60)
    add_button.check_hover(pygame.mouse.get_pos())
    remove_button.check_hover(pygame.mouse.get_pos())
    move_target_button.check_hover(pygame.mouse.get_pos())
    move_base_button.check_hover(pygame.mouse.get_pos())
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            cords = pygame.mouse.get_pos()
        if (
            event.type == pygame.MOUSEBUTTONDOWN
            and MoveTargetButton.in_move
            and not (cords[0] in range(1200, 1500) and cords[1] in range(0, 300))
        ):
            MoveTargetButton.in_move = False
            if base.visible:
                target.set_cords(cords=cords)
                target.visible = True
            else:
                base.set_cords(pygame.mouse.get_pos())
                base.visible = True
        if add_button.handle_event(event=event) and not (MoveTargetButton.in_move):
            robots.append(Robot.add_random_robot())
        if (
            remove_button.handle_event(event=event)
            and len(robots) > 0
            and not (MoveTargetButton.in_move)
        ):
            robots.pop(random.randint(0, len(robots) - 1))
        if move_target_button.handle_event(event=event) and not (
            MoveTargetButton.in_move
        ):
            MoveTargetButton.in_move = True
            target.visible = False
        if move_base_button.handle_event(event=event) and not (
            MoveTargetButton.in_move
        ):
            MoveTargetButton.in_move = True
            base.visible = False

        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
