

import pygame


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
        self.vida = vida
        self.imagen = Load_Image("boss/big.png", True)
        self.ancho = self.imagen.get_width() 
        self.alto = self.imagen.get_height()

    def actualizar(self) -> None:
        self.posicion_x += 1
