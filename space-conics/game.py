import pygame

from boss import Jefe
from enemies import Enemigo
from player import Jugador
from projectiles import Proyectil
from settings import (
    ALTO_VENTANA,
    ANCHO_VENTANA,
    CUADROS_POR_SEGUNDO,
    DANIO_A_JUGADOR,
    TITULO,
)
from ui import Interfaz
from waves import GestorOleadas

PUNTOS_POR_TIPO = {1: 10, 2: 20, 3: 30, "jefe": 200}


def colision_rectangulos(
    ax: float, ay: float, aw: float, ah: float,
    bx: float, by: float, bw: float, bh: float,
) -> bool:
    return ax < bx + bw and bx < ax + aw and ay < by + bh and by < ay + ah


def colision_circulo_rectangulo(
    cx: float, cy: float, radio: float,
    rx: float, ry: float, rw: float, rh: float,
) -> bool:
    punto_x = max(rx, min(cx, rx + rw))
    punto_y = max(ry, min(cy, ry + rh))
    distancia_x = cx - punto_x
    distancia_y = cy - punto_y
    return distancia_x * distancia_x + distancia_y * distancia_y <= radio * radio


def proyectil_toca(proyectil: Proyectil, entidad: Enemigo | Jugador) -> bool:
    return colision_circulo_rectangulo(
        proyectil.posicion_x,
        proyectil.posicion_y,
        proyectil.radio,
        entidad.posicion_x,
        entidad.posicion_y,
        entidad.ancho,
        entidad.alto,
    )


def entidades_se_tocan(a: Enemigo | Jugador, b: Enemigo | Jugador) -> bool:
    return colision_rectangulos(
        a.posicion_x, a.posicion_y, a.ancho, a.alto,
        b.posicion_x, b.posicion_y, b.ancho, b.alto,
    )


class Juego:
    MENU = "menu"
    JUGANDO = "jugando"
    VICTORIA = "victoria"
    DERROTA = "derrota"

    def __init__(self) -> None:
        pygame.init()
        self.pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
        pygame.display.set_caption(TITULO)
        self.reloj = pygame.time.Clock()
        self.interfaz = Interfaz(self.pantalla)
        self.en_ejecucion = True
        self.estado = self.MENU
        self.tiempo_transcurrido = 0.0
        self.tiempo_delta = 0.0
        self.jugador = Jugador(ANCHO_VENTANA // 2 - 20, ALTO_VENTANA - 70)
        self.proyectiles: list[Proyectil] = []
        self.proyectiles_enemigos: list[Proyectil] = []
        self.enemigos: list[Enemigo] = []
        self.jefe: Jefe | None = None
        self.puntaje = 0
        self.gestor_oleadas = GestorOleadas()

    def ejecutar(self) -> None:
        try:
            while self.en_ejecucion:
                self.tiempo_delta = self.reloj.tick(CUADROS_POR_SEGUNDO) / 1000
                self.procesar_eventos()
                self.actualizar()
                self.dibujar()
        finally:
            pygame.quit()

    def procesar_eventos(self) -> None:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.en_ejecucion = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    self.en_ejecucion = False
                elif self.estado == self.MENU and evento.key in (
                    pygame.K_RETURN,
                    pygame.K_SPACE,
                ):
                    self.iniciar_partida()
                elif self.estado in (self.VICTORIA, self.DERROTA) and evento.key in (
                    pygame.K_RETURN,
                    pygame.K_SPACE,
                ):
                    self.estado = self.MENU

    def actualizar(self) -> None:
        if self.estado != self.JUGANDO:
            return

        self.tiempo_transcurrido += self.tiempo_delta
        self._actualizar_jugador()
        self._actualizar_proyectiles()
        self._actualizar_enemigos()
        self._actualizar_jefe()
        self.evitar_choques_entre_enemigos()
        self.gestionar_colisiones()
        if self.estado != self.JUGANDO:
            return
        if not self.enemigos and self.jefe is None:
            if self.gestor_oleadas.hay_mas_oleadas():
                self.gestor_oleadas.avanzar_oleada()
                self.enemigos = self.gestor_oleadas.generar_enemigos()
            else:
                self.jefe = Jefe(ANCHO_VENTANA / 2 - 97)
                self.enemigos = self.gestor_oleadas.generar_escolta_jefe()

    def _actualizar_jugador(self) -> None:
        teclas = pygame.key.get_pressed()
        direccion_x = int(teclas[pygame.K_RIGHT]) - int(teclas[pygame.K_LEFT])
        direccion_y = int(teclas[pygame.K_DOWN]) - int(teclas[pygame.K_UP])
        self.jugador.moverse(direccion_x, direccion_y)
        self.jugador.posicion_x = max(
            0,
            min(self.jugador.posicion_x, ANCHO_VENTANA - self.jugador.ancho),
        )
        self.jugador.posicion_y = max(
            0,
            min(self.jugador.posicion_y, ALTO_VENTANA - self.jugador.alto),
        )

        self.jugador.actualizar_tiempos(self.tiempo_delta)
        disparos = []
        if teclas[pygame.K_z]:
            disparos.append(self.jugador.disparar_basica())
        if teclas[pygame.K_x]:
            disparos.append(self.jugador.disparar_parabolica())
        if teclas[pygame.K_c]:
            disparos.append(self.jugador.disparar_conica())
        self.proyectiles += [disparo for disparo in disparos if disparo is not None]

    def _actualizar_proyectiles(self) -> None:
        for proyectil in self.proyectiles + self.proyectiles_enemigos:
            proyectil.actualizar(self.tiempo_delta)
        self.proyectiles = [
            proyectil
            for proyectil in self.proyectiles
            if not proyectil.terminado(ANCHO_VENTANA, ALTO_VENTANA)
        ]
        self.proyectiles_enemigos = [
            proyectil
            for proyectil in self.proyectiles_enemigos
            if not proyectil.terminado(ANCHO_VENTANA, ALTO_VENTANA)
        ]

    def _actualizar_enemigos(self) -> None:
        for enemigo in self.enemigos:
            enemigo.actualizar(self.tiempo_delta)

    def _actualizar_jefe(self) -> None:
        if self.jefe is None:
            return
        nuevo_proyectil = self.jefe.actualizar(self.tiempo_delta)
        if nuevo_proyectil is not None:
            self.proyectiles_enemigos.append(nuevo_proyectil)

    def todos_los_enemigos(self) -> list[Enemigo]:
        if self.jefe is None:
            return self.enemigos
        return self.enemigos + [self.jefe]

    def evitar_choques_entre_enemigos(self) -> None:
        activos = [e for e in self.todos_los_enemigos() if not e.entrando]
        for i in range(len(activos)):
            for j in range(i + 1, len(activos)):
                a = activos[i]
                b = activos[j]
                if not entidades_se_tocan(a, b):
                    continue
                velocidad_relativa = a.direccion * a.velocidad - b.direccion * b.velocidad
                if (a.posicion_x - b.posicion_x) * velocidad_relativa < 0:
                    a.direccion *= -1
                    b.direccion *= -1

    def gestionar_colisiones(self) -> None:
        proyectiles_restantes: list[Proyectil] = []
        for proyectil in self.proyectiles:
            impacto = False
            for enemigo in self.todos_los_enemigos():
                if proyectil_toca(proyectil, enemigo):
                    enemigo.vida -= proyectil.danio
                    impacto = True
                    break
            if not impacto:
                proyectiles_restantes.append(proyectil)
        self.proyectiles = proyectiles_restantes

        enemigos_vivos = []
        for enemigo in self.enemigos:
            if enemigo.vida <= 0:
                self.puntaje += PUNTOS_POR_TIPO[enemigo.tipo]
            else:
                enemigos_vivos.append(enemigo)
        self.enemigos = enemigos_vivos

        if self.jefe is not None and self.jefe.vida <= 0:
            self.puntaje += PUNTOS_POR_TIPO["jefe"]
            self.finalizar_partida(True)
            return

        proyectiles_enemigos_restantes = []
        for proyectil in self.proyectiles_enemigos:
            if proyectil_toca(proyectil, self.jugador):
                self.jugador.recibir_danio(proyectil.danio)
            else:
                proyectiles_enemigos_restantes.append(proyectil)
        self.proyectiles_enemigos = proyectiles_enemigos_restantes

        for enemigo in self.todos_los_enemigos():
            if entidades_se_tocan(self.jugador, enemigo):
                self.jugador.recibir_danio(DANIO_A_JUGADOR[enemigo.tipo])

        if self.jugador.vida <= 0:
            self.finalizar_partida(False)

    def iniciar_partida(self) -> None:
        self.tiempo_transcurrido = 0.0
        self.jugador = Jugador(ANCHO_VENTANA // 2 - 20, ALTO_VENTANA - 70)
        self.proyectiles = []
        self.proyectiles_enemigos = []
        self.jefe = None
        self.puntaje = 0
        self.gestor_oleadas = GestorOleadas()
        self.enemigos = self.gestor_oleadas.generar_enemigos()
        self.estado = self.JUGANDO

    def finalizar_partida(self, victoria: bool) -> None:
        self.estado = self.VICTORIA if victoria else self.DERROTA

    def dibujar(self) -> None:
        self.interfaz.dibujar_fondo(self.tiempo_delta)
        if self.estado == self.MENU:
            self.interfaz.dibujar_menu()
        elif self.estado == self.JUGANDO:
            texto_oleada = (
                "Jefe final"
                if self.jefe is not None
                else f"Oleada {self.gestor_oleadas.oleada_actual}"
            )
            self.interfaz.dibujar_partida(
                self.jugador,
                self.proyectiles + self.proyectiles_enemigos,
                self.enemigos,
                self.jefe,
                self.tiempo_transcurrido,
                self.puntaje,
                texto_oleada,
            )
        else:
            self.interfaz.dibujar_resultado(self.estado == self.VICTORIA, self.puntaje)
        pygame.display.flip()
