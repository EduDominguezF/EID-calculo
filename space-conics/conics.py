class Conica:
    def __init__(
        self,
        posicion_x: int,
        posicion_y: int,
        radio: int,
        color: tuple[int, int, int],
    ) -> None:
        self.posicion_x = posicion_x
        self.posicion_y = posicion_y
        self.radio = radio
        self.color = color
