import pygame
from classes import *

pygame.init() #Инициализация pygame
clock = pygame.time.Clock() #Инициализация блока управления частотой кадров
info = pygame.display.Info() #Получение информации о дисплее
w = info.current_w
h = info.current_h #Запись текущего разрешения
screen = pygame.display.set_mode((w, h), pygame.FULLSCREEN | pygame.SCALED) #Создание объекта рабочей области
screen_size = [screen.get_width(), screen.get_height()]
screen.fill((255, 255, 255))
x_size = screen_size[0] / 4 
y_size = screen_size[1] / 3 / 5 #Установка размеров кнопок
target = TriangleTarget(25, (500, 500)) #Создание объекта цели
base = BaseTarget() #Создание объекта базы

#Создание кнопок
add_button = Button(screen_size[0] - x_size, 0, x_size, y_size, "Добавить", screen_size[1] / 25, "Green")
remove_button = Button(screen_size[0] - x_size, y_size, x_size, y_size, "Удалить",screen_size[1] / 25, "Red")
move_target_button = MoveTargetButton(screen_size[0] - x_size, 2 * y_size, x_size, y_size, "Цель",screen_size[1] / 25, "Red")
move_base_button = MoveTargetButton(screen_size[0] - x_size, 3 * y_size, x_size, y_size, "База", screen_size[1] / 25, "Black")
start_button = StartSimButton(screen_size[0] - x_size, 4 * y_size, x_size, y_size, "Начать",screen_size[1] / 25, "Green")

#Массивы для роботов
robots = [] #Здесь находяться все роботы вне симуляции 
active_bots = [] #Здесь должны хранится все роботы, у которых целью является одна из точек между базой и целевой точкой
inactive_bots = [] #Здесь должны хранится все роботы, у которых целью является целевая точка или база

#Основной цикл программы
running = True
while running:

    #Блок отрисовки объектов
    screen.fill("White")
    base.draw(screen)
    target.draw(screen)
    if not (StartSimButton.in_progress): #Отрисовка кнопок
        add_button.draw(screen)
        remove_button.draw(screen)
        move_base_button.draw(screen)
        move_target_button.draw(screen)
        start_button.draw(screen)
    if len(robots) > 0: #Отрисовка роботов
        for robot in robots:
            robot.draw(screen)
    if StartSimButton.in_progress: #Блок, отвечающий за передвижения роботов
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
        if flag: #Если цель достигнута, сброс целей роботов
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
    clock.tick(TICKS)
    add_button.check_hover(pygame.mouse.get_pos())
    remove_button.check_hover(pygame.mouse.get_pos())
    move_target_button.check_hover(pygame.mouse.get_pos())
    move_base_button.check_hover(pygame.mouse.get_pos())
    start_button.check_hover(pygame.mouse.get_pos())
    pygame.display.update()
    for event in pygame.event.get(): #Проверка событий, таких как нажатие мышкой по кнопке или рабочей области
        if event.type == pygame.MOUSEBUTTONDOWN: #Получение координат курсора при нажатии
            cords = pygame.mouse.get_pos()


        if ( #Установка базы или цели для перемещения по рабочей области
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


        if ( #Добавление робота в случайной позиции на рабочей области
            add_button.handle_event(event=event)
            and not (MoveTargetButton.in_move)
            and not (StartSimButton.in_progress)
        ):
            robots.append(Robot.create_random_robot(w, h))


        if ( #Удаление случайного робота
            remove_button.handle_event(event=event)
            and len(robots) > 0
            and not (MoveTargetButton.in_move)
        ) and not (StartSimButton.in_progress):
            robots.pop(random.randint(0, len(robots) - 1))


        if ( #Перемещение объекта цели
            move_target_button.handle_event(event=event)
            and not (MoveTargetButton.in_move)
            and not (StartSimButton.in_progress)
        ):
            MoveTargetButton.in_move = True
            target.visible = False


        if ( #Перемешение объекта базы
            move_base_button.handle_event(event=event)
            and not (MoveTargetButton.in_move)
            and not (StartSimButton.in_progress)
        ):
            MoveTargetButton.in_move = True
            base.visible = False


        if ( #Начало симуляции
            start_button.handle_event(event=event)
            and not (MoveTargetButton.in_move)
            and not (StartSimButton.in_progress)
            and len(robots) > 0
        ):
            StartSimButton.in_progress = True
            #Ваш код здесь >>>
            ...
            #<<<Ваш код здесь

        #Закрытие окна    
        if event.type == pygame.QUIT: 
            running = False
            pygame.quit()
