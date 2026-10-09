import pygame


class Projectile:
    def __init__(self, x: int, y: int, speed: int, radius: int = 5, color: tuple[int, int, int] = (255, 220, 100)) -> None:
        self.x = x
        self.y = y
        self.speed = speed
        self.radius = radius
        self.color = color

    def update(self) -> None:
        self.y -= self.speed

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
