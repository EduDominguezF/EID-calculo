import math
import os

import pygame

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
        ruta_sonido = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "sound",
            "sound_001.wav",
        )
        self.sonido = pygame.mixer.Sound(ruta_sonido)
        self.sonido.set_volume(0.1)
        self.sonido.play()
        self.posicion_x, self.posicion_y = trayectoria.posicion(0)
        self.tiempo_anterior = self.tiempo
        self.posicion_anterior_x = self.posicion_x
        self.posicion_anterior_y = self.posicion_y

    def actualizar(self, tiempo_delta: float) -> None:
        self.tiempo_anterior = self.tiempo
        self.posicion_anterior_x = self.posicion_x
        self.posicion_anterior_y = self.posicion_y
        tiempo_siguiente = self.tiempo + tiempo_delta
        if isinstance(self.trayectoria, Elipse) and self.trayectoria.velocidad_angular > 0:
            duracion = 2 * math.pi / self.trayectoria.velocidad_angular
            tiempo_siguiente = min(tiempo_siguiente, duracion)
        self.tiempo = tiempo_siguiente
        self.posicion_x, self.posicion_y = self.trayectoria.posicion(self.tiempo)

    def puntos_recorridos(
        self,
        ancho: int | None = None,
    ) -> list[tuple[float, float]]:
        tiempo_inicio = self.tiempo_anterior
        tiempo_fin = self.tiempo
        if isinstance(self.trayectoria, Parabola) and ancho is not None:
            velocidad_x = self.trayectoria.direccion * self.trayectoria.velocidad_x
            if velocidad_x == 0:
                return []
            tiempos_borde = (
                (-self.radio - self.trayectoria.x0) / velocidad_x,
                (ancho + self.radio - self.trayectoria.x0) / velocidad_x,
            )
            tiempo_inicio = max(tiempo_inicio, min(tiempos_borde))
            tiempo_fin = min(tiempo_fin, max(tiempos_borde))
            if tiempo_inicio > tiempo_fin:
                return []

        inicio = (self.posicion_anterior_x, self.posicion_anterior_y)
        fin = (self.posicion_x, self.posicion_y)
        if tiempo_inicio == self.tiempo_anterior and tiempo_fin == self.tiempo:
            punto_inicio = inicio
            punto_fin = fin
        else:
            punto_inicio = self.trayectoria.posicion(tiempo_inicio)
            punto_fin = self.trayectoria.posicion(tiempo_fin)
        if tiempo_fin <= tiempo_inicio or isinstance(self.trayectoria, Recta):
            return [punto_inicio, punto_fin]

        puntos = [punto_inicio]
        desviacion_maxima = 0.05
        longitud_maxima = 4.0
        profundidad_maxima = 20
        angulo_maximo = math.pi / 64

        def subdividir(
            tiempo_inicio: float,
            punto_inicio: tuple[float, float],
            tiempo_fin: float,
            punto_fin: tuple[float, float],
            profundidad: int,
        ) -> None:
            tiempo_medio = (tiempo_inicio + tiempo_fin) / 2
            punto_medio = self.trayectoria.posicion(tiempo_medio)
            punto_medio_segmento = (
                (punto_inicio[0] + punto_fin[0]) / 2,
                (punto_inicio[1] + punto_fin[1]) / 2,
            )
            desviacion = math.hypot(
                punto_medio[0] - punto_medio_segmento[0],
                punto_medio[1] - punto_medio_segmento[1],
            )
            longitud = math.hypot(
                punto_fin[0] - punto_inicio[0],
                punto_fin[1] - punto_inicio[1],
            )
            angulo_excesivo = (
                isinstance(self.trayectoria, Elipse)
                and abs(self.trayectoria.velocidad_angular)
                * (tiempo_fin - tiempo_inicio)
                > angulo_maximo
            )

            if profundidad < profundidad_maxima and (
                desviacion > desviacion_maxima
                or longitud > longitud_maxima
                or angulo_excesivo
            ):
                subdividir(
                    tiempo_inicio,
                    punto_inicio,
                    tiempo_medio,
                    punto_medio,
                    profundidad + 1,
                )
                subdividir(
                    tiempo_medio,
                    punto_medio,
                    tiempo_fin,
                    punto_fin,
                    profundidad + 1,
                )
            else:
                puntos.append(punto_fin)

        subdividir(
            tiempo_inicio,
            punto_inicio,
            tiempo_fin,
            punto_fin,
            0,
        )
        return puntos

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
