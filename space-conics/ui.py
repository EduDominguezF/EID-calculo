import math
import random

import pygame

from boss import Jefe
from enemies import Enemigo
from player import Jugador
from projectiles import Proyectil
from settings import (
    COLOR_BASICA,
    COLOR_CONICA,
    COLOR_FONDO,
    COLOR_JUGADOR,
    COLOR_PARABOLICA,
    FUENTE,
)


class Interfaz:
    def __init__(self, pantalla: pygame.Surface) -> None:
        self.pantalla = pantalla
        self.fuente_titulo = pygame.font.SysFont(FUENTE, 48)
        self.fuente_mensaje = pygame.font.SysFont(FUENTE, 26)
        self.fuente_pequena = pygame.font.SysFont(FUENTE, 20)
        self.estrellas = self.crear_estrellas()
        self.tiempo_fondo = 0.0
        self.fondo_fijo = self.crear_fondo_fijo()

    def crear_fondo_fijo(self) -> pygame.Surface:
        ancho = self.pantalla.get_width()
        alto = self.pantalla.get_height()
        fondo = pygame.Surface((ancho, alto), 0, 24)
        fondo.fill(COLOR_FONDO)
        nebulosas = (
            ((ancho * 0.8, alto * 0.3), 220, (90, 40, 140)),
            ((ancho * 0.15, alto * 0.75), 180, (30, 60, 130)),
            ((ancho * 0.45, alto * 0.05), 140, (120, 40, 90)),
        )
        for centro, radio_maximo, color in nebulosas:
            capa = pygame.Surface((ancho, alto), pygame.SRCALPHA)
            for radio in range(radio_maximo, 0, -6):
                opacidad = int(110 * (1 - radio / radio_maximo) ** 1.5)
                pygame.draw.circle(capa, (*color, opacidad), centro, radio)
            fondo.blit(capa, (0, 0))
        centro_planeta = (ancho * 0.88, alto * 0.62)
        pygame.draw.circle(fondo, (60, 45, 100), centro_planeta, 34)
        pygame.draw.circle(fondo, (85, 65, 130), (centro_planeta[0] - 7, centro_planeta[1] - 7), 25)
        pygame.draw.ellipse(fondo, (140, 120, 180), (centro_planeta[0] - 58, centro_planeta[1] - 8, 116, 16), 2)
        return fondo

    def crear_estrellas(self) -> list[dict]:
        ancho = self.pantalla.get_width()
        alto = self.pantalla.get_height()
        capas = (
            (90, 20, 1, 110),
            (45, 45, 2, 170),
            (18, 90, 3, 240),
        )
        estrellas = []
        for cantidad, velocidad, radio, brillo in capas:
            for _ in range(cantidad):
                estrellas.append(
                    {
                        "x": random.uniform(0, ancho),
                        "y": random.uniform(0, alto),
                        "velocidad": velocidad,
                        "radio": radio,
                        "brillo": brillo,
                        "fase": random.uniform(0, 2 * math.pi),
                    }
                )
        return estrellas

    def dibujar_fondo(self, tiempo_delta: float) -> None:
        ancho = self.pantalla.get_width()
        alto = self.pantalla.get_height()
        self.tiempo_fondo += tiempo_delta
        self.pantalla.blit(self.fondo_fijo, (0, 0))
        for estrella in self.estrellas:
            estrella["y"] += estrella["velocidad"] * tiempo_delta
            if estrella["y"] > alto:
                estrella["y"] = 0
                estrella["x"] = random.uniform(0, ancho)
            parpadeo = 0.75 + 0.25 * math.sin(3 * self.tiempo_fondo + estrella["fase"])
            brillo = int(estrella["brillo"] * parpadeo)
            pygame.draw.circle(
                self.pantalla,
                (brillo, brillo, min(255, brillo + 30)),
                (estrella["x"], estrella["y"]),
                estrella["radio"],
            )

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

    def dibujar_texto(
        self,
        texto: str,
        color: tuple[int, int, int],
        posicion: tuple[int, int],
    ) -> None:
        self.pantalla.blit(self.fuente_pequena.render(texto, True, color), posicion)

    def dibujar_barra(
        self,
        x: float,
        y: float,
        ancho: float,
        valor: int,
        maximo: int,
        color: tuple[int, int, int],
    ) -> None:
        proporcion = max(0, valor) / maximo
        pygame.draw.rect(self.pantalla, (60, 60, 60), (x, y, ancho, 6))
        pygame.draw.rect(self.pantalla, color, (x, y, ancho * proporcion, 6))

    def dibujar_menu(self) -> None:
        self.dibujar_texto_centrado(
            "SPACE CONICS",
            self.fuente_titulo,
            (100, 200, 255),
            150,
        )
        self.dibujar_texto_centrado(
            "Presiona ENTER o ESPACIO para comenzar",
            self.fuente_mensaje,
            (255, 255, 255),
            230,
        )
        controles = (
            ("Flechas: mover la nave", (200, 200, 200)),
            ("Z: disparo recto (sin limite)", COLOR_BASICA),
            ("X: disparo parabolico (cooldown)", COLOR_PARABOLICA),
            ("C: disparo eliptico (cooldown)", COLOR_CONICA),
            ("ESC para salir", (180, 180, 180)),
        )
        for indice, (texto, color) in enumerate(controles):
            self.dibujar_texto_centrado(
                texto, self.fuente_pequena, color, 290 + indice * 30
            )

    def dibujar_jugador(self, jugador: Jugador) -> None:
        if jugador.invulnerable > 0 and int(jugador.invulnerable * 10) % 2 == 0:
            return
        x = jugador.posicion_x
        y = jugador.posicion_y
        puntos = (
            (x + jugador.ancho / 2, y),
            (x + jugador.ancho, y + jugador.alto),
            (x + jugador.ancho / 2, y + jugador.alto * 0.75),
            (x, y + jugador.alto),
        )
        pygame.draw.polygon(self.pantalla, COLOR_JUGADOR, puntos)

    def dibujar_enemigo(self, enemigo: Enemigo) -> None:
        self.pantalla.blit(enemigo.imagen, (enemigo.posicion_x, enemigo.posicion_y))
        self.dibujar_barra(
            enemigo.posicion_x,
            enemigo.posicion_y - 8,
            enemigo.ancho,
            enemigo.vida,
            enemigo.vida_maxima,
            (255, 90, 90),
        )

    def dibujar_partida(
        self,
        jugador: Jugador,
        proyectiles: list[Proyectil],
        enemigos: list[Enemigo],
        jefe: Jefe | None,
        tiempo_transcurrido: float,
        puntaje: int,
        oleada: str,
    ) -> None:
        for enemigo in enemigos:
            self.dibujar_enemigo(enemigo)
        if jefe is not None:
            self.dibujar_enemigo(jefe)
        for proyectil in proyectiles:
            pygame.draw.circle(
                self.pantalla,
                proyectil.color,
                (proyectil.posicion_x, proyectil.posicion_y),
                proyectil.radio,
            )
        self.dibujar_jugador(jugador)
        self.dibujar_hud(jugador, puntaje, oleada, tiempo_transcurrido, jefe)

    def dibujar_hud(
        self,
        jugador: Jugador,
        puntaje: int,
        oleada: str,
        tiempo_transcurrido: float,
        jefe: Jefe | None,
    ) -> None:
        ancho_pantalla = self.pantalla.get_width()
        alto_pantalla = self.pantalla.get_height()
        self.dibujar_texto(f"Vida: {max(0, jugador.vida)}/{jugador.vida_maxima}", (255, 255, 255), (20, 12))
        self.dibujar_barra(20, 38, 150, jugador.vida, jugador.vida_maxima, (90, 220, 120))
        self.dibujar_texto(f"Puntaje: {puntaje}", (255, 255, 255), (20, 50))
        self.dibujar_texto(oleada, (255, 255, 255), (ancho_pantalla - 170, 12))
        self.dibujar_texto(f"Tiempo: {tiempo_transcurrido:.1f} s", (180, 180, 180), (ancho_pantalla - 170, 37))

        municiones = (
            ("Z Recta", 0.0, COLOR_BASICA),
            ("X Parabola", jugador.espera_parabolica, COLOR_PARABOLICA),
            ("C Elipse", jugador.espera_conica, COLOR_CONICA),
        )
        for indice, (nombre, espera, color) in enumerate(municiones):
            estado = "LISTA" if espera <= 0 else f"{espera:.1f} s"
            self.dibujar_texto(
                f"{nombre}: {estado}",
                color if espera <= 0 else (120, 120, 120),
                (20 + indice * 190, alto_pantalla - 30),
            )

        if jefe is not None:
            self.dibujar_texto_centrado(
                f"Jefe: {max(0, jefe.vida)}/{jefe.vida_maxima}",
                self.fuente_pequena,
                (255, 150, 150),
                22,
            )

    def dibujar_resultado(self, victoria: bool, puntaje: int) -> None:
        texto_titulo = "VICTORIA" if victoria else "DERROTA"
        color_titulo = (100, 255, 140) if victoria else (255, 100, 100)
        self.dibujar_texto_centrado(
            texto_titulo,
            self.fuente_titulo,
            color_titulo,
            200,
        )
        self.dibujar_texto_centrado(
            f"Puntaje: {puntaje}",
            self.fuente_mensaje,
            (255, 255, 255),
            250,
        )
        self.dibujar_texto_centrado(
            "ENTER o ESPACIO para volver al menu",
            self.fuente_mensaje,
            (255, 255, 255),
            295,
        )
        self.dibujar_texto_centrado(
            "ESC para salir",
            self.fuente_pequena,
            (180, 180, 180),
            335,
        )
