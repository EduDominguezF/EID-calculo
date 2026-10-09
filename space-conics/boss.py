import pygame


class Boss:
    def __init__(self, x: int, y: int, health: int = 20) -> None:
        self.x = x
        self.y = y
        self.health = health
        self.width = 120
        self.height = 80

    def update(self) -> None:
        self.x += 1

    def draw(self, screen: pygame.Surface) -> None:
        rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(screen, (220, 50, 50), rect)
