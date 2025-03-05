import random
import pygame
import math
from math import cos, sin, radians, sqrt, atan, degrees, pi


class Point:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y


class BaseSquare:
    def __init__(self, size : tuple = (10, 10), color : str = "Black", cords : tuple = (50, 50), dir : int = 0):
        self.length = size[0]
        self.width = size[1]
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
        len = sqrt((self.length / 2) ** 2 + (self.width / 2) ** 2)
        angle = atan(self.width / self.length)
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
            pygame.draw.polygon(
                screen,
                self.color,
                self.calculate_square_points()
            )

class Robot(BaseSquare):
    def __init__(self, wheel1 : BaseSquare, wheel2 : BaseSquare, size = (10, 10), color = "Black", cords = (50, 50), dir : int = 0):
        super().__init__(size, color, cords)
        self.rwheel = wheel1
        self.lwheel = wheel2
        self.gip = sqrt((self.length / 4 + wheel1.length / 2) ** 2 + (self.width / 4 + wheel1.width / 2) ** 2)
        self.rwheel.update_cords(self.x + self.gip * cos(radians(self.dir)), self.y + self.gip * sin(radians(self.dir)), dir)
        self.lwheel.update_cords(self.x - self.gip * cos(radians(self.dir + 180)), self.y + self.gip * sin(radians(self.dir + 180)), dir + 180)

    def update_cords(self, x, y, dir):
        super().update_cords(x, y, dir)
        self.rwheel.update_cords(self.x + self.gip * cos(radians(self.dir)), self.y + self.gip * sin(radians(self.dir)), dir)
        self.lwheel.update_cords(self.x - self.gip * cos(radians(self.dir)), self.y - self.gip* sin(radians(self.dir)), dir)


    def draw(self, screen):
        super().draw(screen)
        self.rwheel.draw(screen)
        self.lwheel.draw(screen)
        

class BasicSquareObject:
    def __init__(
        self, size: tuple = (10, 10), color: str = "Black", cords: tuple = (0, 0)
    ) -> None:
        self.width = size[0]
        self.height = size[1]
        self.color = color
        self.x = cords[0]
        self.y = cords[1]
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.visible = True

    def draw(self, screen: pygame.Surface):
        if self.visible:
            pygame.draw.rect(screen, self.color, self.rect)
        else:
            pygame.draw.rect(screen, "White", self.rect)

    def set_cords(self, cords):
        self.x, self.y = cords
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)


class BasicTriangleObject:
    def __init__(
        self, radius: int = 10, center_cords: list = [0, 0], dir: float = 90
    ) -> None:
        self.color = "Red"
        self.cx = center_cords[0]
        self.cy = center_cords[1]
        self.rad = radius
        self.dir = dir
        self.visible = True

    @staticmethod
    def calculate_triangle_points(x: int, y: int, r: int, dir: int) -> tuple:
        x1 = x + r * math.cos(math.radians(dir))
        y1 = y + r * math.sin(math.radians(dir))
        x2 = x + r * math.cos(math.radians(dir + 120))
        y2 = y + r * math.sin(math.radians(dir + 120))
        x3 = x + r * math.cos(math.radians(dir + 240))
        y3 = y + r * math.sin(math.radians(dir + 240))
        return (x1, y1), (x2, y2), (x3, y3)

    def set_cords(self, cords):
        self.cx = cords[0]
        self.cy = cords[1]

    def draw(self, screen: pygame.Surface):
        if self.visible:
            pygame.draw.polygon(
                screen,
                self.color,
                BasicTriangleObject.calculate_triangle_points(
                    self.cx, self.cy, self.rad, self.dir
                ),
            )


# class Robot:
#     def __init__(self, cords: tuple = (10, 10), dir: float = 0, rad: int = 20) -> None:
#         self.color = "Black"
#         self.hed_color = "Red"
#         self.dir = dir
#         self.x = cords[0]
#         self.y = cords[1]
#         self.rad = rad
#         self.target = None
#         self.aligned = False
#         self.on_target = False
#         self.delta = 0

#     def make_bet(self, point : Point):
#         distance = math.sqrt((self.x - point.x) ** 2 + (self.y - self.y) ** 2)
#         angle = math.atan((point.y - self.y) / (point.x - self.x))
#         if self.x >= point.x and self.y <= point.y:
#             angle += math.pi
#         elif self.x > point.x and self.y > point.y:
#             angle += math.pi
#         distance_bet = distance / 10
#         angle_bet = abs(math.radians(self.dir) * -1 - angle) / 20
#         return math.ceil(distance_bet + angle_bet)

#     @staticmethod
#     def add_random_robot():
#         return Robot(
#             (random.randint(0, 1500), random.randint(0, 750)),
#             random.randint(0, 359),
#             20,
#         )

#     @staticmethod
#     def calculate_triangle_head(x, y, rad, dir):
#         xc = x + rad * math.cos(math.radians(dir))
#         yc = y + rad * math.sin(math.radians(dir))
#         return (xc, yc)

#     def draw(self, screen: pygame.Surface):
#         pygame.draw.circle(screen, self.color, (self.x, self.y), self.rad)
#         head_x = self.x + self.rad * math.cos(self.dir)
#         head_y = self.y + self.rad * math.sin(self.dir)
#         pygame.draw.polygon(screen, "Red", BasicTriangleObject.calculate_triangle_points(head_x, head_y, self.rad/2, math.degrees(self.dir)))

#     def rotate(self):
#         if not self.aligned:
#             angle = math.atan((self.target.y - self.y) / (self.target.x - self.x))
#             if self.x >= self.target.x and self.y <= self.target.y:
#                 angle += math.pi
#             elif self.x > self.target.x and self.y > self.target.y:
#                 angle += math.pi
#             if angle < self.dir:
#                 self.dir -= 0.02
#             else:
#                 self.dir += 0.02
#             if abs(angle - self.dir) <=0.05:
#                 self.aligned = True
#                 self.dir = angle

#     def move_to_target(self):
#         self.x += 2 * math.cos(self.dir)
#         self.y += 2 * math.sin(self.dir)
#         remain_distance = math.sqrt( (self.x - self.target.x) ** 2 + (self.y - self.target.y) ** 2)
#         if  remain_distance <= self.delta:
#             self.on_target = True



class Button:
    def __init__(self, x, y, width, height, text, color) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.color = color
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.is_hovered = False
        

    def draw(self, screen: pygame.Surface):
        pygame.draw.rect(screen, self.color, self.rect)
        font_surface = pygame.font.Font("fonts/Roboto-Black.ttf", 30).render(
            self.text, False, "White"
        )
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


class MoveTargetButton(Button):
    in_move = False


class StartSimButton(Button):
    in_progress = False


def calculate_points(base: BasicSquareObject, target: BasicTriangleObject, len : int):
    distance = math.sqrt((base.x - target.cx) ** 2 + (base.y - target.cy) ** 2)
    angle = math.atan((target.cy - base.y) / (target.cx - base.x))
    if base.x >= target.cx and base.y <= target.cy:
        angle += math.pi
    elif base.x > target.cx and base.y > target.cy:
        angle += math.pi
    count = math.ceil(distance / 200) - 1
    if count >1 :
        points = []
        if count <= len:
            delta = distance / count + 1
            for i in range(count - 1):
                x = base.x + delta * math.cos(angle) * (i + 1)
                y = base.y + delta * math.sin(angle) * (i + 1)
                tmp_point = Point(x, y)
                points.append(tmp_point)
        else:
            delta = distance / (len + 1)
            for i in range(len):
                x = base.x + delta * math.cos(angle) * (i + 1)
                y = base.y + delta * math.sin(angle) * (i + 1)
                tmp_point = Point(x, y)
                points.append(tmp_point)
        return points
        
    else:
        return []
    # line = Line()
