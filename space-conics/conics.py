import pygame


class Conic:
    def __init__(self, x: int, y: int, radius: int, color: tuple[int, int, int]) -> None:
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
