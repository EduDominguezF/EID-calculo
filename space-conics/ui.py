import pygame


class UI:
    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen

    def draw_hud(self, score: int, lives: int, wave: int) -> None:
        font = pygame.font.SysFont(None, 24)
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        lives_text = font.render(f"Lives: {lives}", True, (255, 255, 255))
        wave_text = font.render(f"Wave: {wave}", True, (255, 255, 255))

        self.screen.blit(score_text, (20, 20))
        self.screen.blit(lives_text, (20, 45))
        self.screen.blit(wave_text, (20, 70))
