import pygame


class Enemy:
    def __init__(self, x: int, y: int, health: int = 1) -> None:
        self.x = x
        self.y = y
        self.health = health
        self.width = 30
        self.height = 30

    def update(self) -> None:
        self.y += 1

    def draw(self, screen: pygame.Surface) -> None:
        rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(screen, (255, 100, 100), rect)
