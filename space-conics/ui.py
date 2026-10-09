import pygame

from boss import Jefe
from enemies import Enemigo
from player import Jugador
from projectiles import Proyectil
from settings import COLOR_ENEMIGO, COLOR_JUGADOR, FUENTE


class Interfaz:
    def __init__(self, pantalla: pygame.Surface) -> None:
        self.pantalla = pantalla
        self.fuente_titulo = pygame.font.SysFont(FUENTE, 48)
        self.fuente_mensaje = pygame.font.SysFont(FUENTE, 26)
        self.fuente_pequena = pygame.font.SysFont(FUENTE, 20)

    def dibujar_texto_centrado(
        self,
        texto: str,
        fuente: pygame.font.Font,
        color: tuple[int, int, int],
        posicion_y: int,
    ) -> None:
        texto_renderizado = fuente.render(texto, True, color)
        rect_texto = texto_renderizado.get_rect(
            center=(self.pantalla.get_width() // 2, posicion_y)
        )
        self.pantalla.blit(texto_renderizado, rect_texto)

    def dibujar_menu(self) -> None:
        self.dibujar_texto_centrado(
            "SPACE CONICS",
            self.fuente_titulo,
            (100, 200, 255),
            190,
        )
        self.dibujar_texto_centrado(
            "Presiona ENTER o ESPACIO para comenzar",
            self.fuente_mensaje,
            (255, 255, 255),
            280,
        )
        self.dibujar_texto_centrado(
            "ESC para salir",
            self.fuente_pequena,
            (180, 180, 180),
            325,
        )

    def dibujar_partida(
        self,
        jugador: Jugador,
        proyectiles: list[Proyectil],
        enemigos: list[Enemigo],
        jefe: Jefe | None,
        tiempo_transcurrido: float,
        puntaje: int,
        oleada: int,
    ) -> None:
        pygame.draw.rect(
            self.pantalla,
            COLOR_JUGADOR,
            (jugador.posicion_x, jugador.posicion_y, jugador.ancho, jugador.alto),
        )
        for proyectil in proyectiles:
            pygame.draw.circle(
                self.pantalla,
                proyectil.color,
                (proyectil.posicion_x, proyectil.posicion_y),
                proyectil.radio,
            )
        for enemigo in enemigos:
            pygame.draw.rect(
                self.pantalla,
                COLOR_ENEMIGO,
                (enemigo.posicion_x, enemigo.posicion_y, enemigo.ancho, enemigo.alto),
            )
        if jefe is not None:
            pygame.draw.rect(
                self.pantalla,
                (220, 50, 50),
                (jefe.posicion_x, jefe.posicion_y, jefe.ancho, jefe.alto),
            )

        self.dibujar_texto_centrado(
            f"Tiempo: {tiempo_transcurrido:.1f} s",
            self.fuente_mensaje,
            (180, 180, 180),
            285,
        )
        self.dibujar_hud(puntaje, jugador.vidas, oleada, jefe.vida if jefe else None)

    def dibujar_hud(
        self,
        puntaje: int,
        vidas: int,
        oleada: int,
        vida_jefe: int | None = None,
    ) -> None:
        textos = (
            f"Puntaje: {puntaje}",
            f"Vidas: {vidas}",
            f"Oleada: {oleada}",
        )
        for indice, texto in enumerate(textos):
            texto_renderizado = self.fuente_pequena.render(texto, True, (255, 255, 255))
            self.pantalla.blit(texto_renderizado, (20, 20 + indice * 25))

        if vida_jefe is not None:
            texto_jefe = self.fuente_pequena.render(
                f"Vida del jefe: {max(0, vida_jefe)}",
                True,
                (255, 150, 150),
            )
            rect_jefe = texto_jefe.get_rect(
                center=(self.pantalla.get_width() // 2, 30)
            )
            self.pantalla.blit(texto_jefe, rect_jefe)

    def dibujar_resultado(self, victoria: bool) -> None:
        texto_titulo = "VICTORIA" if victoria else "DERROTA"
        color_titulo = (100, 255, 140) if victoria else (255, 100, 100)
        self.dibujar_texto_centrado(
            texto_titulo,
            self.fuente_titulo,
            color_titulo,
            220,
        )
        self.dibujar_texto_centrado(
            "ENTER o ESPACIO para volver al menu",
            self.fuente_mensaje,
            (255, 255, 255),
            285,
        )
        self.dibujar_texto_centrado(
            "ESC para salir",
            self.fuente_pequena,
            (180, 180, 180),
            325,
        )
