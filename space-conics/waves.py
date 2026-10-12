import random

from settings import *
from enemies import Enemigo


class Oleada:
    def __init__(self, numero: int, cantidad_enemigos: int) -> None:
        self.numero = numero
        self.cantidad_enemigos = cantidad_enemigos

    def generar_apariciones(self) -> list[dict[str, int]]:
        return [
            {
                "posicion_x": random.randint(120, ANCHO_VENTANA - 150),
                "posicion_y": -30,
            }
            for _ in range(self.cantidad_enemigos)
        ]


class GestorOleadas:
    def __init__(self) -> None:
        self.oleada_actual = 1

    def avanzar_oleada(self) -> None:
        self.oleada_actual += 1

    def hay_mas_oleadas(self) -> bool:
        return self.oleada_actual < 3

    def generar_enemigos(self) -> list[Enemigo]:
        enemigos = []
        for aparicion in self.obtener_oleada_actual().generar_apariciones():
            enemigos.append(
                Enemigo(aparicion["posicion_x"], aparicion["posicion_y"], self.oleada_actual)
            )
        return enemigos

    def obtener_oleada_actual(self) -> Oleada:
        return Oleada(self.oleada_actual, self.oleada_actual * 3)
