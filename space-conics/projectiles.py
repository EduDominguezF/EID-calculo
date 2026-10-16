from conics import Elipse, Parabola, Recta


class Proyectil:
    def __init__(
        self,
        trayectoria: Recta | Parabola | Elipse,
        tipo: str,
        danio: int,
        radio: int,
        color: tuple[int, int, int],
    ) -> None:
        self.trayectoria = trayectoria
        self.tipo = tipo
        self.danio = danio
        self.radio = radio
        self.color = color
        self.tiempo = 0.0
        self.posicion_x, self.posicion_y = trayectoria.posicion(0)

    def actualizar(self, tiempo_delta: float) -> None:
        self.tiempo += tiempo_delta
        self.posicion_x, self.posicion_y = self.trayectoria.posicion(self.tiempo)

    def fuera_de_pantalla(self, ancho: int, alto: int) -> bool:
        return (
            self.posicion_x + self.radio < 0
            or self.posicion_x - self.radio > ancho
            or self.posicion_y + self.radio < 0
            or self.posicion_y - self.radio > alto
        )

    def terminado(self, ancho: int, alto: int) -> bool:
        if isinstance(self.trayectoria, Elipse):
            return self.trayectoria.terminada(self.tiempo)
        return self.fuera_de_pantalla(ancho, alto)
