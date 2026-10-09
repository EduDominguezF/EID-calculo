from settings import VELOCIDAD_JUGADOR, VIDAS_INICIALES


class Jugador:
    def __init__(self, posicion_x: int, posicion_y: int) -> None:
        self.posicion_x = posicion_x
        self.posicion_y = posicion_y
        self.ancho = 40
        self.alto = 40
        self.velocidad = VELOCIDAD_JUGADOR
        self.vidas = VIDAS_INICIALES

    def moverse(self, direccion_x: int, direccion_y: int) -> None:
        self.posicion_x += direccion_x * self.velocidad
        self.posicion_y += direccion_y * self.velocidad
