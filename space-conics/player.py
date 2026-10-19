from conics import Elipse, Parabola, Recta
from projectiles import Proyectil
from settings import (
    ALTURA_PARABOLA,
    COLOR_BASICA,
    COLOR_CONICA,
    COLOR_PARABOLICA,
    COOLDOWN_CONICA,
    COOLDOWN_PARABOLICA,
    DANIO_MUNICION,
    DISTANCIA_VERTICE_PARABOLA,
    SEMIEJE_A_ELIPSE,
    SEMIEJE_B_ELIPSE,
    TIEMPO_INVULNERABLE,
    VELOCIDAD_ANGULAR_ELIPSE,
    VELOCIDAD_HORIZONTAL_PARABOLA,
    VELOCIDAD_JUGADOR,
    VELOCIDAD_PROYECTIL_BASICO,
    VIDA_JUGADOR,
)


class Jugador:
    def __init__(self, posicion_x: int, posicion_y: int) -> None:
        self.posicion_x = posicion_x
        self.posicion_y = posicion_y
        self.ancho = 40
        self.alto = 40
        self.velocidad = VELOCIDAD_JUGADOR
        self.vida_maxima = VIDA_JUGADOR
        self.vida = VIDA_JUGADOR
        self.direccion = 1
        self.espera_parabolica = 0.0
        self.espera_conica = 0.0
        self.invulnerable = 0.0

    def moverse(self, direccion_x: int, direccion_y: int) -> None:
        self.posicion_x += direccion_x * self.velocidad
        self.posicion_y += direccion_y * self.velocidad
        if direccion_x != 0:
            self.direccion = direccion_x

    def actualizar_tiempos(self, tiempo_delta: float) -> None:
        self.espera_parabolica = max(0.0, self.espera_parabolica - tiempo_delta)
        self.espera_conica = max(0.0, self.espera_conica - tiempo_delta)
        self.invulnerable = max(0.0, self.invulnerable - tiempo_delta)

    def recibir_danio(self, danio: int) -> None:
        if self.invulnerable > 0:
            return
        self.vida -= danio
        self.invulnerable = TIEMPO_INVULNERABLE

    def punta(self) -> tuple[float, float]:
        return self.posicion_x + self.ancho / 2, self.posicion_y

    def disparar_basica(self) -> Proyectil | None:
        x, y = self.punta()
        return Proyectil(
            Recta(x, y, 0, -VELOCIDAD_PROYECTIL_BASICO),
            "basica",
            DANIO_MUNICION["basica"],
            5,
            COLOR_BASICA,
        )

    def disparar_parabolica(self) -> Proyectil | None:
        if self.espera_parabolica > 0:
            return None
        self.espera_parabolica = COOLDOWN_PARABOLICA
        x, y = self.punta()
        return Proyectil(
            Parabola(
                x,
                y,
                self.direccion,
                ALTURA_PARABOLA,
                DISTANCIA_VERTICE_PARABOLA,
                VELOCIDAD_HORIZONTAL_PARABOLA,
            ),
            "parabolica",
            DANIO_MUNICION["parabolica"],
            8,
            COLOR_PARABOLICA,
        )

    def disparar_conica(self) -> Proyectil | None:
        if self.espera_conica > 0:
            return None
        self.espera_conica = COOLDOWN_CONICA
        x, y = self.punta()
        return Proyectil(
            Elipse(
                x,
                y,
                SEMIEJE_A_ELIPSE,
                SEMIEJE_B_ELIPSE,
                VELOCIDAD_ANGULAR_ELIPSE,
            ),
            "conica",
            DANIO_MUNICION["conica"],
            11,
            COLOR_CONICA,
        )
