import math
import os

import pygame

from settings import ANCHO_VENTANA


def cargar_imagen(archivo: str, transparente: bool = False) -> pygame.Surface:
    try:
        ruta = os.path.join(os.path.dirname(os.path.abspath(__file__)), archivo)
        imagen = pygame.image.load(ruta)
    except pygame.error as mensaje:
        raise SystemExit(mensaje)
    imagen = imagen.convert()
    if transparente:
        color = imagen.get_at((0, 0))
        imagen.set_colorkey(color, pygame.RLEACCEL)
    return imagen


TIPOS_ENEMIGO = {
    1: {
        "A": 30,
        "B": 0.020,
        "C": 0,
        "D": 110,
        "velocidad": 120,
        "vida": 3,
        "imagen": "enemies/m1.png",
    },
    2: {
        "A": 50,
        "B": 0.015,
        "C": math.pi / 2,
        "D": 180,
        "velocidad": 160,
        "vida": 6,
        "imagen": "enemies/m2.png",
    },
    3: {
        "A": 70,
        "B": 0.025,
        "C": math.pi,
        "D": 250,
        "velocidad": 200,
        "vida": 9,
        "imagen": "enemies/m3.png",
    },
}


class Enemigo:
    def __init__(
        self,
        posicion_x: float,
        tipo: int,
        direccion: int,
        parametros: dict | None = None,
    ) -> None:
        datos = parametros if parametros is not None else TIPOS_ENEMIGO[tipo]
        self.tipo = tipo
        self.A = datos["A"]
        self.B = datos["B"]
        self.C = datos["C"]
        self.D = datos["D"]
        self.velocidad = datos["velocidad"]
        self.vida = datos["vida"]
        self.vida_maxima = datos["vida"]
        self.imagen = cargar_imagen(datos["imagen"], True)
        self.ancho = self.imagen.get_width()
        self.alto = self.imagen.get_height()
        self.direccion = direccion
        self.posicion_x_objetivo_entrada = max(
            0,
            min(posicion_x, ANCHO_VENTANA - self.ancho),
        )
        self.posicion_x = (
            0 if direccion > 0 else ANCHO_VENTANA - self.ancho
        )
        self.posicion_y = self.f(self.posicion_x)
        self.entrando = self.posicion_x != self.posicion_x_objetivo_entrada

    def f(self, x: float) -> float:
        return self.A * math.sin(self.B * x + self.C) + self.D

    def actualizar(self, tiempo_delta: float) -> None:
        if self.entrando:
            posicion_siguiente = (
                self.posicion_x + self.direccion * self.velocidad * tiempo_delta
            )
            if self.direccion > 0:
                self.posicion_x = min(
                    posicion_siguiente,
                    self.posicion_x_objetivo_entrada,
                )
                self.entrando = (
                    self.posicion_x < self.posicion_x_objetivo_entrada
                )
            else:
                self.posicion_x = max(
                    posicion_siguiente,
                    self.posicion_x_objetivo_entrada,
                )
                self.entrando = (
                    self.posicion_x > self.posicion_x_objetivo_entrada
                )
            self.posicion_y = self.f(self.posicion_x)
            return

        self.posicion_x += self.direccion * self.velocidad * tiempo_delta
        if self.posicion_x <= 0:
            self.posicion_x = 0
            self.direccion = 1
        elif self.posicion_x >= ANCHO_VENTANA - self.ancho:
            self.posicion_x = ANCHO_VENTANA - self.ancho
            self.direccion = -1
        self.posicion_y = self.f(self.posicion_x)
