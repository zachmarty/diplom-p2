import random
import pygame
from math import cos, sin, radians, sqrt, atan, degrees, pi
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
        self.dir = dir
        self.visible = True

    def update_cords(self, x, y, dir):
        self.x = x
        self.y = y
        self.dir = dir

    def calculate_square_points(self):
        len = sqrt((self.width / 2) ** 2 + (self.height / 2) ** 2)
        angle = atan(self.width / self.height)
        dir = radians(self.dir)

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
        self.wheel_momentum = 1 / 2 * MAIN_WHEEL_MASS * (MAIN_WHEEL_RADIUS * 0.01) ** 2
        self.motor_momentum = MOTOR_POWER / NOMINAL_SPEED * REDUCTOR_VALUE
        self.platform_momentum = (
            1 / 12 * BASE_MASS * ((BASE_HEIGHT * 0.01) ** 2 + (BASE_LENGTH * 0.01) ** 2)
        )
        self.ratio_momentum = 2 * self.wheel_momentum + self.platform_momentum
        self.linear_momentum = 2 * self.motor_momentum + 2 * self.wheel_momentum + self.platform_momentum
        self.linear_speed = 0
        self.ratio_speed = 0
        self.move_time = 0.0
        self.target_x = 0
        self.target_y = 0
        self.aligned = False
        self.on_target = False
        self.max_linear_speed = 2 * pi * MAIN_WHEEL_RADIUS * 0.01 * NOMINAL_SPEED / 60
        print(self.max_linear_speed)
        self.max_ratio_speed = 2 * self.max_linear_speed / (BASE_LENGTH * 0.01)
        print(self.max_ratio_speed)
        self.ready_to_move = False
        self.x = x
        self.y = y
        self.dir = dir
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

    def update_cords(self, x, y, dir):
        self.x = x
        self.y = y
        self.dir = dir
        angle = radians(dir)
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
        linear_speed = (
            2 * self.motor_momentum * REDUCTOR_VALUE / self.mass / (MAIN_WHEEL_RADIUS * 0.01) * t
        )
        return linear_speed

    def calculate_ratio_speed(self, t):
        ratio_speed = (
            2
            * self.motor_momentum
            * REDUCTOR_VALUE
            * (BASE_LENGTH * 0.01 + SUPPORT_WHEEL_DISTANCE * 0.01)
            / self.platform_momentum
            * t
        )
        return ratio_speed

    def set_target(self, target_x, target_y):
        self.target_x = target_x
        self.target_y = target_y
        self.on_target = False
        self.aligned = False

    def rotate_to_target(self):
        if not self.aligned:
            self.dir = self.dir % 360
            target_dir = (
                pi / 2
                if self.target_x - self.x == 0
                else atan((self.target_y - self.y) / (self.target_x - self.x))
            )
            angle = radians(self.dir)
            if abs(target_dir - angle) > 0.01:
                movement_to = 1 if target_dir > angle else -1
                tau1 = self.move_time
                tau2 = tau1 + 1 / TICKS
                if self.calculate_ratio_speed(tau2) <= self.max_ratio_speed:
                    delta = (
                        self.calculate_ratio_speed(tau2) * tau2 / 2
                        - self.calculate_ratio_speed(tau1) * tau1 / 2
                    )
                else:
                    delta = self.max_ratio_speed * 1 / TICKS
                self.dir = self.dir + delta * movement_to
                # print(delta)
                self.move_time = tau2
            else:
                self.dir = degrees(target_dir)
                self.aligned = True
                self.move_time = 0

    def move_to_target(self, target_x, target_y):
        self.rotate_to_target(target_x, target_y)


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
        self, radius: int = 25, x: int = 500, y: int = 300, dir: float = 90
    ) -> None:
        self.color = "Red"
        self.cx = x
        self.cy = y
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
        self.x = x
        self.y = y

    def draw(self, screen: pygame.Surface):
        if self.visible:
            pygame.draw.polygon(screen, self.color, self.calculate_triangle_points())


class BaseTarget(Base):
    def __init__(self, width=50, height=50, color="black", cords=(50, 50), dir=90):
        super().__init__(width, height, color, cords, dir)


# class MoveTargetButton(Button):
#     in_move = False


# class StartSimButton(Button):
#     in_progress = False


# def calculate_points(base: BasicSquareObject, target: BasicTriangleObject, len: int):
#     distance = math.sqrt((base.x - target.cx) ** 2 + (base.y - target.cy) ** 2)
#     angle = math.atan((target.cy - base.y) / (target.cx - base.x))
#     if base.x >= target.cx and base.y <= target.cy:
#         angle += math.pi
#     elif base.x > target.cx and base.y > target.cy:
#         angle += math.pi
#     count = math.ceil(distance / 200) - 1
#     if count > 1:
#         points = []
#         if count <= len:
#             delta = distance / count + 1
#             for i in range(count - 1):
#                 x = base.x + delta * math.cos(angle) * (i + 1)
#                 y = base.y + delta * math.sin(angle) * (i + 1)
#                 tmp_point = Point(x, y)
#                 points.append(tmp_point)
#         else:
#             delta = distance / (len + 1)
#             for i in range(len):
#                 x = base.x + delta * math.cos(angle) * (i + 1)
#                 y = base.y + delta * math.sin(angle) * (i + 1)
#                 tmp_point = Point(x, y)
#                 points.append(tmp_point)
#         return points

#     else:
#         return []
#     # line = Line()
