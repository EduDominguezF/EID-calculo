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


def distancia_punto_segmento_cuadrada(
    px: float,
    py: float,
    x1: float,
    y1: float,
    x2: float,
    y2: float,
) -> float:
    vector_x = x2 - x1
    vector_y = y2 - y1
    longitud_cuadrada = vector_x * vector_x + vector_y * vector_y
    if longitud_cuadrada == 0:
        return (px - x1) ** 2 + (py - y1) ** 2
    proporcion = max(
        0.0,
        min(1.0, ((px - x1) * vector_x + (py - y1) * vector_y) / longitud_cuadrada),
    )
    punto_x = x1 + proporcion * vector_x
    punto_y = y1 + proporcion * vector_y
    return (px - punto_x) ** 2 + (py - punto_y) ** 2


def segmentos_se_intersectan(
    ax: float,
    ay: float,
    bx: float,
    by: float,
    cx: float,
    cy: float,
    dx: float,
    dy: float,
) -> bool:
    def orientacion(
        x1: float, y1: float, x2: float, y2: float, x3: float, y3: float
    ) -> float:
        return (x2 - x1) * (y3 - y1) - (y2 - y1) * (x3 - x1)

    def en_segmento(
        x1: float, y1: float, x2: float, y2: float, x: float, y: float
    ) -> bool:
        return (
            min(x1, x2) <= x <= max(x1, x2)
            and min(y1, y2) <= y <= max(y1, y2)
        )

    o1 = orientacion(ax, ay, bx, by, cx, cy)
    o2 = orientacion(ax, ay, bx, by, dx, dy)
    o3 = orientacion(cx, cy, dx, dy, ax, ay)
    o4 = orientacion(cx, cy, dx, dy, bx, by)
    if o1 * o2 < 0 and o3 * o4 < 0:
        return True
    return (
        (o1 == 0 and en_segmento(ax, ay, bx, by, cx, cy))
        or (o2 == 0 and en_segmento(ax, ay, bx, by, dx, dy))
        or (o3 == 0 and en_segmento(cx, cy, dx, dy, ax, ay))
        or (o4 == 0 and en_segmento(cx, cy, dx, dy, bx, by))
    )


def segmento_toca_rectangulo(
    x1: float,
    y1: float,
    x2: float,
    y2: float,
    radio: float,
    entidad: Enemigo | Jugador,
) -> bool:
    izquierda = entidad.posicion_x
    arriba = entidad.posicion_y
    derecha = izquierda + entidad.ancho
    abajo = arriba + entidad.alto

    def distancia_punto_rectangulo_cuadrada(x: float, y: float) -> float:
        dx = max(izquierda - x, 0.0, x - derecha)
        dy = max(arriba - y, 0.0, y - abajo)
        return dx * dx + dy * dy

    if (
        distancia_punto_rectangulo_cuadrada(x1, y1) == 0
        or distancia_punto_rectangulo_cuadrada(x2, y2) == 0
    ):
        return True

    bordes = (
        (izquierda, arriba, derecha, arriba),
        (derecha, arriba, derecha, abajo),
        (derecha, abajo, izquierda, abajo),
        (izquierda, abajo, izquierda, arriba),
    )
    distancia_minima = min(
        distancia_punto_rectangulo_cuadrada(x1, y1),
        distancia_punto_rectangulo_cuadrada(x2, y2),
    )
    for ex1, ey1, ex2, ey2 in bordes:
        if segmentos_se_intersectan(x1, y1, x2, y2, ex1, ey1, ex2, ey2):
            return True
        distancia_minima = min(
            distancia_minima,
            distancia_punto_segmento_cuadrada(x1, y1, ex1, ey1, ex2, ey2),
            distancia_punto_segmento_cuadrada(x2, y2, ex1, ey1, ex2, ey2),
            distancia_punto_segmento_cuadrada(ex1, ey1, x1, y1, x2, y2),
            distancia_punto_segmento_cuadrada(ex2, ey2, x1, y1, x2, y2),
        )
    return distancia_minima <= radio * radio


def proyectil_recorrido_toca(
    proyectil: Proyectil,
    entidad: Enemigo | Jugador,
    puntos: list[tuple[float, float]] | None = None,
) -> bool:
    if puntos is None:
        puntos = proyectil.puntos_recorridos(ANCHO_VENTANA)
    if len(puntos) == 1:
        return colision_circulo_rectangulo(
            puntos[0][0],
            puntos[0][1],
            proyectil.radio,
            entidad.posicion_x,
            entidad.posicion_y,
            entidad.ancho,
            entidad.alto,
        )
    return any(
        segmento_toca_rectangulo(
            punto_inicio[0],
            punto_inicio[1],
            punto_fin[0],
            punto_fin[1],
            proyectil.radio,
            entidad,
        )
        for punto_inicio, punto_fin in zip(puntos, puntos[1:])
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
        self.aparicion_pendiente = None

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
        if self.interfaz.aviso_activo():
            return
        if self.aparicion_pendiente == "oleada":
            self.enemigos = self.gestor_oleadas.generar_enemigos()
            self.aparicion_pendiente = None
        elif self.aparicion_pendiente == "jefe":
            self.jefe = Jefe(ANCHO_VENTANA / 2 - 97)
            self.enemigos = self.gestor_oleadas.generar_escolta_jefe()
            self.aparicion_pendiente = None
        elif not self.enemigos and self.jefe is None:
            if self.gestor_oleadas.hay_mas_oleadas():
                self.gestor_oleadas.avanzar_oleada()
                self.interfaz.mostrar_aviso(f"OLEADA {self.gestor_oleadas.oleada_actual}")
                self.aparicion_pendiente = "oleada"
            else:
                self.interfaz.mostrar_aviso("JEFE FINAL")
                self.aparicion_pendiente = "jefe"

        elif not self.enemigos and self.jefe is None:
                if self.gestor_oleadas.hay_mas_oleadas():
                    self.gestor_oleadas.avanzar_oleada()
                    self.interfaz.mostrar_aviso(f"OLEADA {self.gestor_oleadas.oleada_actual}")
                    self.aparicion_pendiente = "oleada"
                else:
                    self.interfaz.mostrar_aviso("JEFE FINAL")
                    self.aparicion_pendiente = "jefe"

                        
           

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
            puntos = proyectil.puntos_recorridos(ANCHO_VENTANA)
            for enemigo in self.todos_los_enemigos():
                if enemigo.vida > 0 and proyectil_recorrido_toca(
                    proyectil, enemigo, puntos
                ):
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
                self.interfaz.crear_explosion(
                    enemigo.posicion_x + enemigo.ancho / 2,
                    enemigo.posicion_y + enemigo.alto / 2,
                )
            else:
                enemigos_vivos.append(enemigo)
        self.enemigos = enemigos_vivos

        jefe_derrotado = self.jefe is not None and self.jefe.vida <= 0
        if jefe_derrotado:
            self.puntaje += PUNTOS_POR_TIPO["jefe"]

        proyectiles_enemigos_restantes = []
        for proyectil in self.proyectiles_enemigos:
            puntos = proyectil.puntos_recorridos(ANCHO_VENTANA)
            if proyectil_recorrido_toca(proyectil, self.jugador, puntos):
                self.jugador.recibir_danio(proyectil.danio)
            else:
                proyectiles_enemigos_restantes.append(proyectil)
        self.proyectiles_enemigos = proyectiles_enemigos_restantes

        for enemigo in self.todos_los_enemigos():
            if enemigo.vida > 0 and entidades_se_tocan(self.jugador, enemigo):
                self.jugador.recibir_danio(DANIO_A_JUGADOR[enemigo.tipo])

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

        if self.jugador.vida <= 0:
            self.finalizar_partida(False)
        elif jefe_derrotado:
            self.finalizar_partida(True)

    def iniciar_partida(self) -> None:
        self.tiempo_transcurrido = 0.0
        self.jugador = Jugador(ANCHO_VENTANA // 2 - 20, ALTO_VENTANA - 70)
        self.proyectiles = []
        self.proyectiles_enemigos = []
        self.jefe = None
        self.puntaje = 0
        self.gestor_oleadas = GestorOleadas()
        self.enemigos = []
        self.aparicion_pendiente = "oleada"
        self.interfaz.mostrar_aviso(f"OLEADA {self.gestor_oleadas.oleada_actual}")
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
                if self.jefe is not None or self.aparicion_pendiente == "jefe"
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
