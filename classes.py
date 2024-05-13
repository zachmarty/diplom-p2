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
        self.rect = self.form_rect()

    def get_size(self):
        return (self.width, self.height)

    def get_cords(self):
        return (self.x, self.y)

    def form_rect(self):
        rect = pygame.Rect(self.x, self.y, self.width, self.height)
        return rect

    def draw(self, screen: pygame.Surface):
        pygame.draw.rect(screen, self.color, self.rect)


class BasicTriangleObject:
    def __init__(
        self, radius: int = 10, color: str = "Black", center_cords: tuple = (0, 0)
    ) -> None:
        self.color = color
        self.cx = center_cords[0]
        self.cy = center_cords[1]
        self.rad = radius

    @staticmethod
    def calculate_triangle_points(x: int, y: int, r:int) -> tuple:
        x1 = x + r * math.cos(math.radians(30))
        y1 = y + r * math.sin(math.radians(30))
        x2 = x + r * math.cos(math.radians(150))
        y2 = y + r * math.sin(math.radians(150))
        x3 = x + r * math.cos(math.radians(270))
        y3 = y + r * math.sin(math.radians(270))
        return (x1, y1), (x2, y2), (x3, y3)

    def move(self, delta_X : int, delta_y: int):
        self.cx += delta_X
        self.cy += delta_y 
    
    def draw(self, screen: pygame.Surface):
        pygame.draw.polygon(screen, self.color, BasicTriangleObject.calculate_triangle_points(self.cx, self.cy, self.rad))
