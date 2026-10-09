import pygame

from boss import Boss
from enemies import Enemy
from player import Player
from projectiles import Projectile
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
        self.player = Player(WIDTH // 2 - 20, HEIGHT - 70)
        self.projectiles: list[Projectile] = []
        self.enemies: list[Enemy] = []
        self.boss: Boss | None = None

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
            self.player.update(pygame.key.get_pressed())
            self.player.x = max(0, min(self.player.x, WIDTH - self.player.width))
            self.player.y = max(0, min(self.player.y, HEIGHT - self.player.height))

            for projectile in self.projectiles:
                projectile.update()
            self.projectiles = [
                projectile
                for projectile in self.projectiles
                if not (
                    projectile.x + projectile.radius < 0
                    or projectile.x - projectile.radius > WIDTH
                    or projectile.y + projectile.radius < 0
                    or projectile.y - projectile.radius > HEIGHT
                )
            ]

            for enemy in self.enemies:
                enemy.update()
            self.enemies = [
                enemy
                for enemy in self.enemies
                if not (
                    enemy.x + enemy.width < 0
                    or enemy.x > WIDTH
                    or enemy.y + enemy.height < 0
                    or enemy.y > HEIGHT
                )
            ]

            if self.boss is not None:
                self.boss.update()
                self.boss.x = max(0, min(self.boss.x, WIDTH - self.boss.width))
                self.boss.y = max(0, min(self.boss.y, HEIGHT - self.boss.height))

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
            self.player.draw(self.screen)
            for projectile in self.projectiles:
                projectile.draw(self.screen)
            for enemy in self.enemies:
                enemy.draw(self.screen)
            if self.boss is not None:
                self.boss.draw(self.screen)
            self.ui.draw_playing(self.elapsed_time)
        else:
            self.ui.draw_result(self.state == self.VICTORY)
        pygame.display.flip()
