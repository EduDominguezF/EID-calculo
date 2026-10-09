import pygame


class UI:
    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        self.title_font = pygame.font.SysFont("arial", 48)
        self.message_font = pygame.font.SysFont("arial", 26)
        self.small_font = pygame.font.SysFont("arial", 20)

    def draw_centered_text(
        self,
        text: str,
        font: pygame.font.Font,
        color: tuple[int, int, int],
        y: int,
    ) -> None:
        rendered_text = font.render(text, True, color)
        text_rect = rendered_text.get_rect(center=(self.screen.get_width() // 2, y))
        self.screen.blit(rendered_text, text_rect)

    def draw_menu(self) -> None:
        self.draw_centered_text("SPACE CONICS", self.title_font, (100, 200, 255), 190)
        self.draw_centered_text("Presiona ENTER o ESPACIO para comenzar", self.message_font, (255, 255, 255), 280)
        self.draw_centered_text("ESC para salir", self.small_font, (180, 180, 180), 325)

    def draw_playing(self, elapsed_time: float) -> None:
        self.draw_centered_text("Partida en curso", self.title_font, (255, 255, 255), 230)
        self.draw_centered_text(f"Tiempo: {elapsed_time:.1f} s", self.message_font, (180, 180, 180), 285)

    def draw_hud(
        self,
        score: int,
        lives: int,
        wave: int,
        boss_health: int | None = None,
    ) -> None:
        score_text = self.small_font.render(f"Puntaje: {score}", True, (255, 255, 255))
        lives_text = self.small_font.render(f"Vidas: {lives}", True, (255, 255, 255))
        wave_text = self.small_font.render(f"Oleada: {wave}", True, (255, 255, 255))

        self.screen.blit(score_text, (20, 20))
        self.screen.blit(lives_text, (20, 45))
        self.screen.blit(wave_text, (20, 70))

        if boss_health is not None:
            boss_text = self.small_font.render(
                f"Vida del jefe: {max(0, boss_health)}",
                True,
                (255, 150, 150),
            )
            boss_rect = boss_text.get_rect(center=(self.screen.get_width() // 2, 30))
            self.screen.blit(boss_text, boss_rect)

    def draw_result(self, won: bool) -> None:
        title = "VICTORIA" if won else "DERROTA"
        color = (100, 255, 140) if won else (255, 100, 100)
        self.draw_centered_text(title, self.title_font, color, 220)
        self.draw_centered_text("ENTER o ESPACIO para volver al menu", self.message_font, (255, 255, 255), 285)
        self.draw_centered_text("ESC para salir", self.small_font, (180, 180, 180), 325)
