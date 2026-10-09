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
        self.score = 0
        self.current_wave = 1

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
            self.check_collisions()

            if self.boss is not None:
                self.boss.update()
                self.boss.x = max(0, min(self.boss.x, WIDTH - self.boss.width))
                self.boss.y = max(0, min(self.boss.y, HEIGHT - self.boss.height))

    def check_collisions(self) -> None:
        remaining_projectiles: list[Projectile] = []
        for projectile in self.projectiles:
            hit_enemy = False
            for enemy in self.enemies:
                closest_x = max(enemy.x, min(projectile.x, enemy.x + enemy.width))
                closest_y = max(enemy.y, min(projectile.y, enemy.y + enemy.height))
                distance_x = projectile.x - closest_x
                distance_y = projectile.y - closest_y
                if distance_x * distance_x + distance_y * distance_y <= projectile.radius * projectile.radius:
                    enemy.health -= 1
                    hit_enemy = True
                    break
            if not hit_enemy:
                remaining_projectiles.append(projectile)

        self.projectiles = remaining_projectiles
        surviving_enemies = [enemy for enemy in self.enemies if enemy.health > 0]
        self.score += len(self.enemies) - len(surviving_enemies)
        self.enemies = surviving_enemies

        player_rect = pygame.Rect(self.player.x, self.player.y, self.player.width, self.player.height)
        remaining_enemies: list[Enemy] = []
        for enemy in self.enemies:
            enemy_rect = pygame.Rect(enemy.x, enemy.y, enemy.width, enemy.height)
            if player_rect.colliderect(enemy_rect):
                self.player.lives -= 1
            else:
                remaining_enemies.append(enemy)

        self.enemies = remaining_enemies
        if self.player.lives <= 0:
            self.finish_game(False)

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
            boss_health = self.boss.health if self.boss is not None else None
            self.ui.draw_hud(self.score, self.player.lives, self.current_wave, boss_health)
        else:
            self.ui.draw_result(self.state == self.VICTORY)
        pygame.display.flip()
