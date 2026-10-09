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
        self.ancho = 120
        self.alto = 80

    def actualizar(self) -> None:
        self.posicion_x += 1
