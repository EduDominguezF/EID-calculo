import pygame

from settings import PLAYER_LIVES, PLAYER_SPEED


class Player:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.width = 40
        self.height = 40
        self.speed = PLAYER_SPEED
        self.lives = PLAYER_LIVES

    def update(self, keys: pygame.key.ScancodeWrapper) -> None:
        if keys[pygame.K_LEFT]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.x += self.speed
        if keys[pygame.K_UP]:
            self.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.y += self.speed

    def draw(self, screen: pygame.Surface) -> None:
        rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(screen, (100, 200, 255), rect)
