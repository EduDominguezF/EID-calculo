import math

from conics import Recta
from enemies import Enemigo
from projectiles import Proyectil
from settings import (
    COLOR_PROYECTIL_JEFE,
    DANIO_A_JUGADOR,
    VELOCIDAD_PROYECTIL_JEFE,
)

PARAMETROS_JEFE = {
    "A": 35,
    "B": 0.010,
    "C": math.pi / 4,
    "D": 60,
    "velocidad": 110,
    "vida": 40,
    "imagen": "boss/big.png",
}


class Jefe(Enemigo):
    def __init__(self, posicion_x: float) -> None:
        super().__init__(posicion_x, "jefe", 1, PARAMETROS_JEFE)
        self.tiempo_ataque = 0.0
        self.intervalo_ataque = 1.3

    def actualizar(self, tiempo_delta: float) -> Proyectil | None:
        super().actualizar(tiempo_delta)
        if self.entrando:
            return None
        self.tiempo_ataque += tiempo_delta
        if self.tiempo_ataque < self.intervalo_ataque:
            return None
        self.tiempo_ataque = 0.0
        return Proyectil(
            Recta(
                self.posicion_x + self.ancho / 2,
                self.posicion_y + self.alto,
                0,
                VELOCIDAD_PROYECTIL_JEFE,
            ),
            "jefe",
            DANIO_A_JUGADOR["jefe"],
            7,
            COLOR_PROYECTIL_JEFE,
        )
