import pygame
import math

from settings import *

def Load_Image(sFile,transp = False):
    try: image = pygame.image.load(sFile)
    except pygame.error as message:
        raise SystemExit(message)
    image = image.convert()
    if transp:
       color = image.get_at((0,0))
       image.set_colorkey(color,pygame.RLEACCEL)
    return image


class Enemigo:
    def __init__(self, posicion_x: int, posicion_y: int, tipo: int = 1) -> None:
        self.posicion_x = posicion_x
        self.posicion_y = posicion_y
        self.x_inicial = posicion_x
        self.tipo = tipo
        self.tiempo = 0
        if tipo == 1:
            self.vida = 1
            self.amplitud = 40
            self.frecuencia = 0.04
            self.imagen = Load_Image("enemies/m1.png", True)
        elif tipo == 2:
            self.vida = 2
            self.amplitud = 80
            self.frecuencia = 0.06
            self.imagen = Load_Image("enemies/m2.png", True)
        else:
            self.vida = 3
            self.amplitud = 120
            self.frecuencia = 0.08
            self.imagen = Load_Image("enemies/m3.png", True)
        self.ancho = self.imagen.get_width() 
        self.alto = self.imagen.get_height()
    

    def actualizar(self, tiempo_delta: float) -> None:
        self.tiempo += tiempo_delta * 60

        self.posicion_y += VELOCIDAD_ENEMIGO
        self.posicion_x = self.x_inicial + self.amplitud * math.sin(
            self.frecuencia * self.tiempo
        )