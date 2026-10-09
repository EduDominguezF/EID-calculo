class Proyectil:
    def __init__(
        self,
        posicion_x: int,
        posicion_y: int,
        velocidad: int,
        radio: int = 5,
        color: tuple[int, int, int] = (255, 220, 100),
    ) -> None:
        self.posicion_x = posicion_x
        self.posicion_y = posicion_y
        self.velocidad = velocidad
        self.radio = radio
        self.color = color

    def actualizar(self) -> None:
        self.posicion_y -= self.velocidad
