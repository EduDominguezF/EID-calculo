
import math
import pygame
from projectiles import Proyectil


def Load_Image(sFile,transp = False):
    try: image = pygame.image.load(sFile)
    except pygame.error as message:
        raise SystemExit(message)
    image = image.convert()
    if transp:
       color = image.get_at((0,0))
       image.set_colorkey(color,pygame.RLEACCEL)
    return image

class Jefe:
    def __init__(
        self,
        posicion_x: int,
        posicion_y: int,
        vida: int = 20,
    ) -> None:
        self.posicion_x = posicion_x
        self.posicion_y = posicion_y
        self.x_inicial = posicion_x
        self.vida = vida
        self.imagen = Load_Image("boss/big.png", True)
        self.ancho = self.imagen.get_width() 
        self.alto = self.imagen.get_height()
        self.tiempo = 0
        self.tiempo_disparo = 0
        self.tiempo_ataque = 0

    def actualizar(self, tiempo_delta: float) -> Proyectil | None:
        self.tiempo += tiempo_delta * 60
        self.posicion_x = self.x_inicial + 250 * math.sin(0.03 * self.tiempo)
        self.tiempo_ataque += tiempo_delta * 60
        if self.tiempo_ataque >= 80:  # Dispara aprox cada 80 "ticks"
            self.tiempo_ataque = 0
            # Retornamos un proyectil rojo.
            # Nota: La velocidad es negativa para que vaya hacia abajo, ya que
            # en projectiles.py la 'velocidad' se resta a 'posicion_y'.
            return Proyectil(
                posicion_x=int(self.posicion_x + self.ancho / 2),
                posicion_y=self.posicion_y + self.alto,
                velocidad=-6,
                color=(255, 50, 50)
            )
        return None