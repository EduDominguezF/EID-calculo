import math

import pygame

from settings import ANCHO_VENTANA, VELOCIDAD_ENTRADA_ENEMIGO


def cargar_imagen(archivo: str, transparente: bool = False) -> pygame.Surface:
    try:
        imagen = pygame.image.load(archivo)
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
        self.posicion_x = max(0, min(posicion_x, ANCHO_VENTANA - self.ancho))
        self.posicion_y = -self.alto
        self.entrando = True

    def f(self, x: float) -> float:
        return self.A * math.sin(self.B * x + self.C) + self.D

    def actualizar(self, tiempo_delta: float) -> None:
        if self.entrando:
            self.posicion_y += VELOCIDAD_ENTRADA_ENEMIGO * tiempo_delta
            if self.posicion_y >= self.f(self.posicion_x):
                self.posicion_y = self.f(self.posicion_x)
                self.entrando = False
            return

        self.posicion_x += self.direccion * self.velocidad * tiempo_delta
        if self.posicion_x <= 0:
            self.posicion_x = 0
            self.direccion = 1
        elif self.posicion_x >= ANCHO_VENTANA - self.ancho:
            self.posicion_x = ANCHO_VENTANA - self.ancho
            self.direccion = -1
        self.posicion_y = self.f(self.posicion_x)
