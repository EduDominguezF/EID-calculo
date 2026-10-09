class Enemigo:
    def __init__(self, posicion_x: int, posicion_y: int, vida: int = 1) -> None:
        self.posicion_x = posicion_x
        self.posicion_y = posicion_y
        self.vida = vida
        self.ancho = 30
        self.alto = 30

    def actualizar(self) -> None:
        self.posicion_y += 1
