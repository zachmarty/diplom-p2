import pygame
from classes import *

pygame.init()
clock = pygame.time.Clock()
info = pygame.display.Info()
w = info.current_w
h = info.current_h
screen = pygame.display.set_mode((w, h), pygame.FULLSCREEN | pygame.SCALED)
screen_size = [screen.get_width(), screen.get_height()]
screen.fill((255, 255, 255))
x_size = screen_size[0] / 4
y_size = screen_size[1] / 3 / 5
target = TriangleTarget(25, (500, 500))
base = BaseTarget()
robots = []
add_button = Button(screen_size[0] - x_size, 0, x_size, y_size, "Добавить", screen_size[1] / 25, "Green")
remove_button = Button(screen_size[0] - x_size, y_size, x_size, y_size, "Удалить",screen_size[1] / 25, "Red")
move_target_button = MoveTargetButton(screen_size[0] - x_size, 2 * y_size, x_size, y_size, "Цель",screen_size[1] / 25, "Red")
move_base_button = MoveTargetButton(screen_size[0] - x_size, 3 * y_size, x_size, y_size, "База", screen_size[1] / 25, "Black")
start_button = StartSimButton(screen_size[0] - x_size, 4 * y_size, x_size, y_size, "Начать",screen_size[1] / 25, "Green")
active_bots = []
inactive_bots = []
running = True
while running:
    screen.fill("White")
    base.draw(screen)
    target.draw(screen)
    if not (StartSimButton.in_progress):
        add_button.draw(screen)
        remove_button.draw(screen)
        move_base_button.draw(screen)
        move_target_button.draw(screen)
        start_button.draw(screen)
    if len(robots) > 0:
        for robot in robots:
            robot.draw(screen)
    if StartSimButton.in_progress:
        flag = True
        for robot in active_bots:
            if not robot.aligned:
                robot.rotate_to_target()
            else:
                if not robot.on_target:
                    robot.drive_to_target()
            robot.draw(screen)
            if not robot.on_target:
                flag = False
        for robot in inactive_bots:
            if not robot.aligned:
                robot.rotate_to_target()
            else:
                if not robot.on_target:
                    robot.drive_to_target()
            robot.draw(screen)
            if not robot.on_target:
                flag = False
        if flag:
            StartSimButton.in_progress = False
            for i in range(len(active_bots)):
                active_bots[0].target_x = None
                active_bots[0].target_y = None
                active_bots[0].aligned = False
                active_bots[0].on_target = False
                robots.append(active_bots[0])
                active_bots.pop(0)
            for i in range(len(inactive_bots)):
                inactive_bots[0].target_x = None
                inactive_bots[0].target_y = None
                inactive_bots[0].aligned = False
                inactive_bots[0].on_target = False
                robots.append(inactive_bots[0])
                inactive_bots.pop(0)
    clock.tick(60)
    add_button.check_hover(pygame.mouse.get_pos())
    remove_button.check_hover(pygame.mouse.get_pos())
    move_target_button.check_hover(pygame.mouse.get_pos())
    move_base_button.check_hover(pygame.mouse.get_pos())
    start_button.check_hover(pygame.mouse.get_pos())
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            cords = pygame.mouse.get_pos()
        if (
            event.type == pygame.MOUSEBUTTONDOWN
            and MoveTargetButton.in_move
            and not (cords[0] in range(int(w - x_size), w) and cords[1] in range(0, int(y_size)))
        ):
            MoveTargetButton.in_move = False
            if base.visible:
                target.set_cords(cords[0], cords[1])
                target.visible = True
            else:
                base.set_cords(pygame.mouse.get_pos())
                base.visible = True
        if (
            add_button.handle_event(event=event)
            and not (MoveTargetButton.in_move)
            and not (StartSimButton.in_progress)
        ):
            robots.append(Robot.create_random_robot(w, h))
        if (
            remove_button.handle_event(event=event)
            and len(robots) > 0
            and not (MoveTargetButton.in_move)
        ) and not (StartSimButton.in_progress):
            robots.pop(random.randint(0, len(robots) - 1))
        if (
            move_target_button.handle_event(event=event)
            and not (MoveTargetButton.in_move)
            and not (StartSimButton.in_progress)
        ):
            MoveTargetButton.in_move = True
            target.visible = False
        if (
            move_base_button.handle_event(event=event)
            and not (MoveTargetButton.in_move)
            and not (StartSimButton.in_progress)
        ):
            MoveTargetButton.in_move = True
            base.visible = False
        if (
            start_button.handle_event(event=event)
            and not (MoveTargetButton.in_move)
            and not (StartSimButton.in_progress)
            and len(robots) > 0
        ):
            StartSimButton.in_progress = True
            points = calculate_points(base, target, len(robots))
            for point in points:
                min_bet = robots[0].make_bet(point)
                for i in range(len(robots)):
                    tmp_bet = robots[i].make_bet(point)
                    if tmp_bet < min_bet:
                        min_bet = tmp_bet
                for i in range(len(robots)):
                    if min_bet == robots[i].make_bet(point):
                        robots[i].target_x = point.x
                        robots[i].target_y = point.y
                        active_bots.append(robots[i])
                        robots.pop(i)
                        break
            for i in range(len(robots)):
                base_distance = sqrt(
                    (robots[0].x - base.x) ** 2 + (robots[0].y - base.y) ** 2
                )
                target_distance = sqrt(
                    (robots[0].x - target.cx) ** 2 + (robots[0].y - target.cy) ** 2
                )
                if base_distance > target_distance:
                    robots[0].target_x = target.cx
                    robots[0].target_y = target.cy
                else:
                    robots[0].target_x = base.x
                    robots[0].target_y = base.y
                inactive_bots.append(robots[0])
                robots.pop(0)

        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
