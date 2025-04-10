import random
import pygame
from math import cos, sin, radians, sqrt, atan, degrees, pi, ceil
from constants import *


class Point:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y


class BaseSquare:
    def __init__(
        self,
        width,
        height,
        color: str = "Black",
        cords: tuple = (50, 50),
        dir: int = 90,
    ):
        self.width = width
        self.height = height
        self.color = color
        self.x = cords[0]
        self.y = cords[1]
        self.dir = radians(dir)
        self.visible = True

    def update_cords(self, x, y, dir):
        self.x = x
        self.y = y
        self.dir = dir

    def set_cords(self, cords = (0, 0)):
        self.x = cords[0]
        self.y = cords[1]

    def calculate_square_points(self):
        len = sqrt((self.width / 2) ** 2 + (self.height / 2) ** 2)
        angle = atan(self.width / self.height)
        dir = self.dir

        x1 = len * cos(dir + angle) + self.x
        y1 = len * sin(dir + angle) + self.y

        x2 = len * cos(dir + pi - angle) + self.x
        y2 = len * sin(dir + pi - angle) + self.y

        x3 = len * cos(dir + pi + angle) + self.x
        y3 = len * sin(dir + pi + angle) + self.y

        x4 = len * cos(dir - angle) + self.x
        y4 = len * sin(dir - angle) + self.y

        return [x1, y1], [x2, y2], [x3, y3], [x4, y4]

    def draw(self, screen: pygame.Surface):
        if self.visible:
            pygame.draw.polygon(screen, self.color, self.calculate_square_points())


class MainWheel(BaseSquare):
    def __init__(
        self,
        width=MAIN_WHEEL_WIDTH,
        height=MAIN_WHEEL_RADIUS,
        mass=MAIN_WHEEL_MASS,
        color="Black",
        cords=(50, 50),
        dir=90,
    ):
        super().__init__(width, height, color, cords, dir)
        self.mass = mass


class SupportWheel(BaseSquare):
    def __init__(
        self,
        width=SUPPROT_WHEEL_WIDTH,
        height=SUPPORT_WHEEL_RADIUS,
        mass=MAIN_WHEEL_MASS,
        color="Black",
        cords=(50, 50),
        dir=90,
    ):
        super().__init__(width, height, color, cords, dir)
        self.mass = mass


class Base(BaseSquare):
    def __init__(
        self, width=BASE_LENGTH, height=BASE_HEIGHT, color="RED", cords=(50, 50), dir=90
    ):
        super().__init__(width, height, color, cords, dir)


class Robot:

    def __init__(self, x, y, dir):
        self.mass = (
            BASE_MASS + 2 * MAIN_WHEEL_MASS + 2 * SUPPORT_WHEEL_MASS + 2 * MOTOR_MASS
        )
        self.w_nom = 2 * pi * NOMINAL_SPEED / 60
        self.w_wheel = self.w_nom / REDUCTOR_VALUE 
        self.max_ratio_speed = self.w_wheel * MAIN_WHEEL_RADIUS * 0.01 / (BASE_LENGTH * 0.01 / 2)
        self.max_linear_speed = self.w_wheel * MAIN_WHEEL_RADIUS * 0.01 * 10
        self.momentum = MOTOR_POWER / self.w_nom
        self.platform_momentum = (
            1 / 12 * BASE_MASS * ((BASE_HEIGHT * 0.01) ** 2 + (BASE_LENGTH * 0.01) ** 2)
        )
        self.main_wheel_momentum = 1 / 2 * MAIN_WHEEL_MASS * (MAIN_WHEEL_RADIUS * 0.01) ** 2 + MAIN_WHEEL_MASS * (BASE_LENGTH * 0.01/ 2) ** 2
        self.support_wheel_momentum = 1 / 2 * SUPPORT_WHEEL_MASS * (SUPPORT_WHEEL_RADIUS * 0.01) ** 2 + SUPPORT_WHEEL_MASS * (SUPPORT_WHEEL_OFFSET * 0.01) ** 2
        self.ratio_momentum = 2 * self.main_wheel_momentum + self.platform_momentum + 2 * ROTOR_MOMENTUM + 2 * self.support_wheel_momentum
        self.linear_momentum = 2 * ROTOR_MOMENTUM + 2 * self.main_wheel_momentum + 2 * self.support_wheel_momentum
        self.ratio_acc =  5 * self.momentum / self.ratio_momentum / REDUCTOR_VALUE * MAIN_WHEEL_RADIUS * 0.01 / (BASE_LENGTH / 2 * 0.01)
        self.ratio_time = self.max_ratio_speed / self.ratio_acc
        self.linear_acc = 10 * self.momentum / self.linear_momentum / REDUCTOR_VALUE * MAIN_WHEEL_RADIUS * 0.01
        self.linear_time = self.max_linear_speed / self.linear_acc
        self.current_speed = 0
        self.ratio_speed = 0
        self.move_time = 0.
        self.target_x = 0
        self.target_y = 0
        self.brake_distance = 0
        self.brake_time = 0
        self.braking = False
        self.aligned = False
        self.on_target = False
        self.ready_to_move = False
        self.x = x
        self.y = y
        self.dir = radians(dir)
        base = Base(cords=(x, y))
        self.base = base
        main_wheel_l = MainWheel()
        main_wheel_r = MainWheel()
        self.main_wheel_l = main_wheel_l
        self.main_wheel_r = main_wheel_r
        support_wheel_l = SupportWheel()
        support_wheel_r = SupportWheel()
        self.support_wheel_l = support_wheel_l
        self.support_wheel_r = support_wheel_r
        self.visible = True

    @classmethod
    def create_default_robot(cls, x=400, y=400, dir=90):
        robot = Robot(x, y, dir)
        return robot
    
    @classmethod
    def create_random_robot(cls, x_size, y_size):
        robot = Robot(random.randint(0, x_size), random.randint(0, y_size), random.randint(-180, 180))
        return robot

    def update_cords(self, x, y, dir):
        self.x = x
        self.y = y
        self.dir = dir
        angle = self.dir
        self.base.update_cords(x, y, dir)
        self.main_wheel_l.update_cords(
            self.x
            + MAIN_WHEEL_OFFSET * cos(angle)
            - self.main_wheel_l.width / 2 * sin(angle)
            - self.base.width / 2 * sin(angle),
            self.y
            + self.base.width / 2 * cos(angle)
            + self.main_wheel_l.width / 2 * cos(angle)
            + MAIN_WHEEL_OFFSET * sin(angle),
            dir,
        )
        self.main_wheel_r.update_cords(
            self.x
            + MAIN_WHEEL_OFFSET * cos(angle)
            + self.main_wheel_r.width / 2 * sin(angle)
            + self.base.width / 2 * sin(angle),
            self.y
            - self.base.width / 2 * cos(angle)
            - self.main_wheel_l.width / 2 * cos(angle)
            + MAIN_WHEEL_OFFSET * sin(angle),
            dir,
        )
        self.support_wheel_l.update_cords(
            self.x
            - SUPPORT_WHEEL_OFFSET * cos(angle)
            - self.support_wheel_l.width / 2 * sin(angle)
            - SUPPORT_WHEEL_DISTANCE / 2 * sin(angle),
            self.y
            - SUPPORT_WHEEL_OFFSET * sin(angle)
            + SUPPORT_WHEEL_DISTANCE / 2 * cos(angle)
            + self.support_wheel_l.width / 2 * cos(angle),
            dir,
        )
        self.support_wheel_r.update_cords(
            self.x
            - SUPPORT_WHEEL_OFFSET * cos(angle)
            + self.support_wheel_l.width / 2 * sin(angle)
            + SUPPORT_WHEEL_DISTANCE / 2 * sin(angle),
            self.y
            - SUPPORT_WHEEL_OFFSET * sin(angle)
            - SUPPORT_WHEEL_DISTANCE / 2 * cos(angle)
            - self.support_wheel_l.width / 2 * cos(angle),
            dir,
        )

    def draw(self, screen: pygame.Surface):
        self.update_cords(self.x, self.y, self.dir)
        if self.visible:
            self.base.draw(screen)
            self.main_wheel_l.draw(screen)
            self.main_wheel_r.draw(screen)
            self.support_wheel_l.draw(screen)
            self.support_wheel_r.draw(screen)

    def calculate_linear_speed(self, t):
        linear_speed = self.linear_acc * t
        return linear_speed

    def calculate_ratio_speed(self, t):
        ratio_speed = self.ratio_acc * t
        return ratio_speed

    def set_target(self, target_x, target_y):
        self.target_x = target_x
        self.target_y = target_y
        self.on_target = False
        self.aligned = False
        self.braking = False

    def drive_to_target(self):
        if not self.on_target:
            path = sqrt((self.x - self.target_x) ** 2 + (self.y - self.target_y) ** 2)
            if abs(path - self.brake_distance) > 0.06 and not self.braking:
                tau1 = self.move_time
                tau2 = tau1 + 1 / TICKS
                if tau2 > self.linear_time:
                    self.current_speed = self.max_linear_speed
                    self.brake_distance = self.current_speed * self.linear_time - self.linear_acc * self.linear_time ** 2 / 2
                    delta = self.max_linear_speed / TICKS
                else:
                    self.current_speed = self.calculate_linear_speed(tau2)
                    self.brake_distance = self.current_speed * tau2 - self.linear_acc * tau2 ** 2 / 2
                    delta = self.calculate_linear_speed(tau2) * tau2 / 2 - self.calculate_linear_speed(tau1) * tau1 / 2
                self.x = self.x + delta * cos(self.dir)
                self.y = self.y + delta * sin(self.dir)
                self.move_time = tau2
            elif not self.braking:
                self.braking = True
            elif self.braking and path > 0.1:
                tau1 = self.brake_time
                tau2 = tau1 + 1 / TICKS
                delta = self.current_speed * tau2 - self.linear_acc * tau2 ** 2 /2 - self.current_speed * tau1 + self.linear_acc * tau1 ** 2 / 2
                self.brake_time = tau2
                self.x = self.x + delta * cos(self.dir)
                self.y = self.y + delta * sin(self.dir)
            else:
                self.braking = False
                self.brake_time = 0
                self.current_speed = 0
                self.x = self.target_x
                self.y = self.target_y
                self.on_target = True
                self.move_time = 0

    def rotate_to_target(self):
        if not self.aligned:
            if self.dir > pi:
                self.dir = - 2 * pi + self.dir
            target_dir = (
                pi / 2
                if self.target_x - self.x == 0
                else atan((self.target_y - self.y) / (self.target_x - self.x))
            )
            if self.x > self.target_x and self.y < self.target_y:
                target_dir = pi + target_dir
            elif self.x > self.target_x and self.y > self.target_y:
                target_dir = - pi + target_dir
            angle = self.dir
            movement_to = 1 if target_dir > angle else -1
            if abs(abs(target_dir - angle) - self.brake_distance) > 0.02 and not self.braking:
                tau1 = self.move_time
                tau2 = tau1 + 1 / TICKS
                if tau2 > self.ratio_time:
                    self.current_speed = self.max_ratio_speed
                    self.brake_distance = self.current_speed * self.ratio_time - self.ratio_acc * self.ratio_time ** 2 / 2
                    delta = self.max_ratio_speed / TICKS
                else:
                    self.current_speed = self.calculate_ratio_speed(tau2)
                    self.brake_distance = self.current_speed * tau2 - self.ratio_acc * tau2 ** 2 / 2
                    delta = self.calculate_ratio_speed(tau2) * tau2 / 2 - self.calculate_ratio_speed(tau1) * tau1 / 2
                self.dir = self.dir + delta * movement_to
                self.move_time = tau2
            elif not self.braking:
                self.braking = True
            elif self.braking and abs(target_dir - angle) > 0.08:
                tau1 = self.brake_time
                tau2 = tau1 + 1 / TICKS
                delta = self.current_speed * tau2 - self.ratio_acc * tau2 ** 2 / 2 - self.current_speed * tau1 + self.ratio_acc * tau1 ** 2 / 2
                self.dir = self.dir + delta * movement_to
                self.brake_time = tau2
            else:
                self.braking = False
                self.brake_time = 0
                self.current_speed = 0
                self.dir = target_dir
                self.aligned = True
                self.move_time = 0

    def move_to_target(self):
        if not self.aligned:
            self.rotate_to_target()
        else:
            self.drive_to_target()
    
    
    def make_bet(self, point : Point):
        distance = sqrt((self.x - point.x) ** 2 + (self.y - self.y) ** 2)
        angle = atan((point.y - self.y) / (point.x - self.x))
        if self.x >= point.x and self.y <= point.y:
             angle += pi
        elif self.x > point.x and self.y > point.y:
             angle += pi
        distance_bet = distance / 2
        angle_bet = abs(self.dir * -1 - angle) / 10
        return ceil(distance_bet + angle_bet)

# class Robot(BaseSquare):
#     def __init__(self, wheel1 : BaseSquare, wheel2 : BaseSquare, size = (LENGTH, WIDTH), color = "Red", cords = (50, 50), dir : int = 0):
#         super().__init__(size, color, cords)
#         self.rwheel = wheel1
#         self.lwheel = wheel2
#         self.gip = self.length / 2 + wheel1.length / 2
#         self.rwheel.update_cords(self.x + self.gip * cos(radians(self.dir)), self.y + self.gip * sin(radians(self.dir)), dir)
#         self.lwheel.update_cords(self.x - self.gip * cos(radians(self.dir)), self.y - self.gip* sin(radians(self.dir)), dir)

#     def update_cords(self, x, y, dir):
#         super().update_cords(x, y, dir)
#         self.rwheel.update_cords(self.x + self.gip * cos(radians(self.dir)), self.y + self.gip * sin(radians(self.dir)), dir)
#         self.lwheel.update_cords(self.x - self.gip * cos(radians(self.dir)), self.y - self.gip* sin(radians(self.dir)), dir)


#     def draw(self, screen):
#         super().draw(screen)
#         self.rwheel.draw(screen)
#         self.lwheel.draw(screen)


class Button:
    def __init__(self, x, y, width, height, text, text_size, color) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.color = color
        self.text_size = int(text_size)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.is_hovered = False

    def draw(self, screen: pygame.Surface):
        pygame.draw.rect(screen, self.color, self.rect)
        font_surface = pygame.font.Font(
            "fonts/Roboto-Black.ttf", self.text_size
        ).render(self.text, False, "White")
        screen.blit(font_surface, (self.x + self.width / 4, self.y + self.height / 4))

    def check_hover(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def handle_event(self, event):
        if (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and self.is_hovered
        ):
            return True
        else:
            return False


class TriangleTarget:
    def __init__(
        self, radius: int = 25, cords = (1, 1), dir: float = 90
    ) -> None:
        self.color = "Red"
        self.cx = cords[0]
        self.cy = cords[1]
        self.rad = radius
        self.dir = dir
        self.visible = True

    def calculate_triangle_points(self) -> tuple:
        angle = radians(self.dir)
        x1 = self.cx + self.rad * cos(angle)
        y1 = self.cy + self.rad * sin(angle)
        x2 = self.cx + self.rad * cos(angle + pi / 3 * 2)
        y2 = self.cy + self.rad * sin(angle + pi / 3 * 2)
        x3 = self.cx + self.rad * cos(angle + pi / 3 * 4)
        y3 = self.cy + self.rad * sin(angle + pi / 3 * 4)
        return (x1, y1), (x2, y2), (x3, y3)

    def set_cords(self, x, y):
        self.cx = x
        self.cy = y

    def draw(self, screen: pygame.Surface):
        if self.visible:
            pygame.draw.polygon(screen, self.color, self.calculate_triangle_points())


class BaseTarget(Base):
    def __init__(self, width=50, height=50, color="black", cords=(50, 50), dir=90):
        super().__init__(width, height, color, cords, dir)


class MoveTargetButton(Button):
    in_move = False


class StartSimButton(Button):
    in_progress = False


def calculate_points(base: BaseTarget, target: TriangleTarget, len: int):
    distance = sqrt((base.x - target.cx) ** 2 + (base.y - target.cy) ** 2)
    angle = atan((target.cy - base.y) / (target.cx - base.x))
    if base.x >= target.cx and base.y <= target.cy:
        angle += pi
    elif base.x > target.cx and base.y > target.cy:
        angle += pi
    count = ceil(distance / 200) - 1
    if count > 1:
        points = []
        if count <= len:
            delta = distance / count + 1
            for i in range(count - 1):
                x = base.x + delta * cos(angle) * (i + 1)
                y = base.y + delta * sin(angle) * (i + 1)
                tmp_point = Point(x, y)
                points.append(tmp_point)
        else:
            delta = distance / (len + 1)
            for i in range(len):
                x = base.x + delta * cos(angle) * (i + 1)
                y = base.y + delta * sin(angle) * (i + 1)
                tmp_point = Point(x, y)
                points.append(tmp_point)
        return points

    else:
        return []
