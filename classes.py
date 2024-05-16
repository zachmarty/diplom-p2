import pygame
import math


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

    def draw(self, screen: pygame.Surface):
        pygame.draw.rect(screen, self.color, self.rect)


class BasicTriangleObject:
    def __init__(
        self, radius: int = 10, center_cords: tuple = (0, 0), dir: float = 90
    ) -> None:
        self.color = 'Red'
        self.cx = center_cords[0]
        self.cy = center_cords[1]
        self.rad = radius
        self.dir = -dir

    @staticmethod
    def calculate_triangle_points(x: int, y: int, r:int, dir : int) -> tuple:
        x1 = x + r * math.cos(math.radians(dir))
        y1 = y + r * math.sin(math.radians(dir))
        x2 = x + r * math.cos(math.radians(dir + 120))
        y2 = y + r * math.sin(math.radians(dir + 120))
        x3 = x + r * math.cos(math.radians(dir + 240))
        y3 = y + r * math.sin(math.radians(dir + 240))
        return (x1, y1), (x2, y2), (x3, y3)
    
    def draw(self, screen: pygame.Surface):
        pygame.draw.polygon(screen, self.color, BasicTriangleObject.calculate_triangle_points(self.cx, self.cy, self.rad, self.dir))

class Robot:
    def __init__(self, cords : tuple = (10, 10), dir : float = 0, rad : int = 20) -> None:
        self.color = 'Black'
        self.hed_color = 'Red'
        self.dir =  -1 * dir
        self.x = cords[0]
        self.y = cords[1]
        self.rad = rad
        self.head = BasicTriangleObject(self.rad / 2, self.calculate_triangle_head(self.x, self.y, self.rad, self.dir), -self.dir)

    @staticmethod
    def calculate_triangle_head(x, y, rad, dir):
        xc = x + rad * math.cos(math.radians(dir))
        yc = y + rad * math.sin(math.radians(dir))
        return (xc, yc)


    def draw(self, screen: pygame.Surface):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.rad)
        self.head.draw(screen)
        

