import pygame

from settings import BACKGROUND_COLOR, FPS, HEIGHT, TITLE, WIDTH
from ui import UI


class Game:
    MENU = "menu"
    PLAYING = "playing"
    VICTORY = "victory"
    DEFEAT = "defeat"

    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.ui = UI(self.screen)
        self.running = True
        self.state = self.MENU
        self.delta_time = 0.0
        self.elapsed_time = 0.0

    def run(self) -> None:
        try:
            while self.running:
                self.delta_time = self.clock.tick(FPS) / 1000
                self.handle_events()
                self.update()
                self.draw()
        finally:
            pygame.quit()

    def handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif self.state == self.MENU and event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    self.start_game()
                elif self.state in (self.VICTORY, self.DEFEAT) and event.key in (
                    pygame.K_RETURN,
                    pygame.K_SPACE,
                ):
                    self.state = self.MENU

    def update(self) -> None:
        if self.state == self.PLAYING:
            self.elapsed_time += self.delta_time

    def start_game(self) -> None:
        self.elapsed_time = 0.0
        self.state = self.PLAYING

    def finish_game(self, won: bool) -> None:
        self.state = self.VICTORY if won else self.DEFEAT

    def draw(self) -> None:
        self.screen.fill(BACKGROUND_COLOR)
        if self.state == self.MENU:
            self.ui.draw_menu()
        elif self.state == self.PLAYING:
            self.ui.draw_playing(self.elapsed_time)
        else:
            self.ui.draw_result(self.state == self.VICTORY)
        pygame.display.flip()
