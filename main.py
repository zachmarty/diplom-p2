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
move_target_button = MoveTargetButton(1200, 150, 300, 50, "Цель", "Red")
move_base_button = MoveTargetButton(1200, 100, 300, 50, "База", "Black")
start_button = StartSimButton(1200, 200, 300, 50, "Начать", "Green")
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
                robot.rotate()
            else:
                if not robot.on_target:
                    robot.move_to_target()
            robot.draw(screen)
            if not robot.on_target:
                flag = False
        for robot in inactive_bots:
            if not robot.aligned:
                robot.rotate()
            else:
                if not robot.on_target:
                    robot.move_to_target()
            robot.draw(screen)
            if not robot.on_target:
                flag = False
        if flag:
            StartSimButton.in_progress = False
            for i in range(len(active_bots)):
                active_bots[0].target = None
                active_bots[0].aligned = False
                active_bots[0].on_target = False
                active_bots[0].delta = 0
                robots.append(active_bots[0])
                active_bots.pop(0)
            for i in range(len(inactive_bots)):
                inactive_bots[0].target = None
                inactive_bots[0].aligned = False
                inactive_bots[0].on_target = False
                inactive_bots[0].delta = 0
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
            and not (cords[0] in range(1200, 1500) and cords[1] in range(0, 300))
        ):
            MoveTargetButton.in_move = False
            if base.visible:
                target.set_cords(cords=cords)
                target.visible = True
            else:
                base.set_cords(pygame.mouse.get_pos())
                base.visible = True
        if (
            add_button.handle_event(event=event)
            and not (MoveTargetButton.in_move)
            and not (StartSimButton.in_progress)
        ):
            robots.append(Robot.add_random_robot())
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
                        robots[i].target = point
                        robots[i].delta = 5
                        active_bots.append(robots[i])
                        robots.pop(i)
                        break
            for i in range(len(robots)):
                base_distance = math.sqrt(
                    (robots[0].x - base.x) ** 2 + (robots[0].y - base.y) ** 2
                )
                target_distance = math.sqrt(
                    (robots[0].x - target.cx) ** 2 + (robots[0].y - target.cy) ** 2
                )
                if base_distance > target_distance:
                    robots[0].target = Point(target.cx, target.cy)
                else:
                    robots[0].target = Point(base.x, base.y)
                robots[0].delta = 50
                inactive_bots.append(robots[0])
                robots.pop(0)
            for robot in active_bots:
                robot.dir = math.radians(robot.dir)
            for robot in inactive_bots:
                robot.dir = math.radians(robot.dir)

        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
