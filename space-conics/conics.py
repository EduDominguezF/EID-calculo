import math


class Recta:
    def __init__(
        self,
        posicion_x: float,
        posicion_y: float,
        velocidad_x: float,
        velocidad_y: float,
    ) -> None:
        self.x0 = posicion_x
        self.y0 = posicion_y
        self.velocidad_x = velocidad_x
        self.velocidad_y = velocidad_y

    def posicion(self, tiempo: float) -> tuple[float, float]:
        x = self.x0 + self.velocidad_x * tiempo
        y = self.y0 + self.velocidad_y * tiempo
        return x, y

    def terminada(self, tiempo: float) -> bool:
        return False


class Parabola:
    def __init__(
        self,
        posicion_x: float,
        posicion_y: float,
        direccion: int,
        altura: float,
        distancia: float,
        velocidad_x: float,
    ) -> None:
        self.x0 = posicion_x
        self.direccion = direccion
        self.h = posicion_x + direccion * distancia
        self.k = posicion_y - altura
        self.p = distancia * distancia / (4 * altura)
        self.velocidad_x = velocidad_x

    def y(self, x: float) -> float:
        return self.k + (x - self.h) ** 2 / (4 * self.p)

    def posicion(self, tiempo: float) -> tuple[float, float]:
        x = self.x0 + self.direccion * self.velocidad_x * tiempo
        return x, self.y(x)

    def terminada(self, tiempo: float) -> bool:
        return False


class Elipse:
    def __init__(
        self,
        posicion_x: float,
        posicion_y: float,
        a: float,
        b: float,
        velocidad_angular: float,
    ) -> None:
        self.h = posicion_x
        self.k = posicion_y - b
        self.a = a
        self.b = b
        self.velocidad_angular = velocidad_angular
        self.angulo_inicial = math.pi / 2

    def posicion(self, tiempo: float) -> tuple[float, float]:
        angulo = self.angulo_inicial + self.velocidad_angular * tiempo
        x = self.h + self.a * math.cos(angulo)
        y = self.k + self.b * math.sin(angulo)
        return x, y

    def terminada(self, tiempo: float) -> bool:
        return self.velocidad_angular * tiempo >= 2 * math.pi
