import random

from enemies import Enemigo
from settings import ANCHO_VENTANA

COMPOSICION_OLEADAS = {
    1: [1, 1, 1, 1],
    2: [1, 1, 1, 2, 2, 2],
    3: [1, 1, 2, 2, 3, 3, 3],
}

ESCOLTA_JEFE = [1, 2]


def generar_grupo(tipos: list[int]) -> list[Enemigo]:
    enemigos = []
    ancho_franja = ANCHO_VENTANA / len(tipos)
    orden = tipos[:]
    random.shuffle(orden)
    for indice, tipo in enumerate(orden):
        posicion_x = random.uniform(
            indice * ancho_franja,
            (indice + 1) * ancho_franja - 80,
        )
        direccion = random.choice((-1, 1))
        enemigos.append(Enemigo(posicion_x, tipo, direccion))
    return enemigos


class Oleada:
    def __init__(self, numero: int) -> None:
        self.numero = numero
        self.tipos = COMPOSICION_OLEADAS[numero]

    def generar_enemigos(self) -> list[Enemigo]:
        return generar_grupo(self.tipos)


class GestorOleadas:
    def __init__(self) -> None:
        self.oleada_actual = 1

    def avanzar_oleada(self) -> None:
        self.oleada_actual += 1

    def hay_mas_oleadas(self) -> bool:
        return self.oleada_actual < len(COMPOSICION_OLEADAS)

    def generar_enemigos(self) -> list[Enemigo]:
        return self.obtener_oleada_actual().generar_enemigos()

    def generar_escolta_jefe(self) -> list[Enemigo]:
        return generar_grupo(ESCOLTA_JEFE)

    def obtener_oleada_actual(self) -> Oleada:
        return Oleada(self.oleada_actual)
