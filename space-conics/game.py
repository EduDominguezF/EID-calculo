import pygame

from boss import Jefe
from enemies import Enemigo
from player import Jugador
from projectiles import Proyectil
from settings import (
    ALTO_VENTANA,
    ANCHO_VENTANA,
    CUADROS_POR_SEGUNDO,
    COLOR_FONDO,
    TITULO,
)
from ui import Interfaz
from waves import GestorOleadas


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
        self.gestionar_colisiones()
        if not self.enemigos and self.jefe is None:
            if self.gestor_oleadas.hay_mas_oleadas():
                self.gestor_oleadas.avanzar_oleada()
                self.enemigos = self.gestor_oleadas.generar_enemigos()
            else:
                self.jefe = Jefe(420, 40)
        self._actualizar_jefe()

    def _actualizar_jugador(self) -> None:
        teclas = pygame.key.get_pressed()
        direccion_x = int(teclas[pygame.K_RIGHT] or teclas[pygame.K_d]) - int(
            teclas[pygame.K_LEFT] or teclas[pygame.K_a]
        )
        direccion_y = int(teclas[pygame.K_DOWN] or teclas[pygame.K_s]) - int(
            teclas[pygame.K_UP] or teclas[pygame.K_w]
        )
        self.jugador.moverse(direccion_x, direccion_y)
        self.jugador.posicion_x = max(
            0,
            min(self.jugador.posicion_x, ANCHO_VENTANA - self.jugador.ancho),
        )
        self.jugador.posicion_y = max(
            0,
            min(self.jugador.posicion_y, ALTO_VENTANA - self.jugador.alto),
        )

    def _actualizar_proyectiles(self) -> None:
        for proyectil in self.proyectiles:
            proyectil.actualizar()
        self.proyectiles = [
            proyectil
            for proyectil in self.proyectiles
            if not (
                proyectil.posicion_x + proyectil.radio < 0
                or proyectil.posicion_x - proyectil.radio > ANCHO_VENTANA
                or proyectil.posicion_y + proyectil.radio < 0
                or proyectil.posicion_y - proyectil.radio > ALTO_VENTANA
            )
        ]

        for proyectil in self.proyectiles_enemigos:
            proyectil.actualizar()
        self.proyectiles_enemigos = [
            proyectil
            for proyectil in self.proyectiles_enemigos
            if not (
                proyectil.posicion_x + proyectil.radio < 0
                or proyectil.posicion_x - proyectil.radio > ANCHO_VENTANA
                or proyectil.posicion_y + proyectil.radio < 0
                or proyectil.posicion_y - proyectil.radio > ALTO_VENTANA
            )
        ]

    def _actualizar_enemigos(self) -> None:
        for enemigo in self.enemigos:
            enemigo.actualizar(self.tiempo_delta)
        self.enemigos = [
            enemigo
            for enemigo in self.enemigos
            if not (
                enemigo.posicion_x + enemigo.ancho < 0
                or enemigo.posicion_x > ANCHO_VENTANA
                or enemigo.posicion_y + enemigo.alto < 0
                or enemigo.posicion_y > ALTO_VENTANA
            )
        ]

    def _actualizar_jefe(self) -> None:
        if self.jefe is None:
            return
        nuevo_proyectil = self.jefe.actualizar(self.tiempo_delta)
        if nuevo_proyectil:
            self.proyectiles_enemigos.append(nuevo_proyectil)
        
        self.jefe.posicion_x = max(
            0,
            min(self.jefe.posicion_x, ANCHO_VENTANA - self.jefe.ancho),
        )
        self.jefe.posicion_y = max(
            0,
            min(self.jefe.posicion_y, ALTO_VENTANA - self.jefe.alto),
        )

    def gestionar_colisiones(self) -> None:
        # 1. Colisiones de proyectiles del jugador con enemigos comunes
        proyectiles_restantes: list[Proyectil] = []
        for proyectil in self.proyectiles:
            impacto = False
            for enemigo in self.enemigos:
                punto_x = max(
                    enemigo.posicion_x,
                    min(proyectil.posicion_x, enemigo.posicion_x + enemigo.ancho),
                )
                punto_y = max(
                    enemigo.posicion_y,
                    min(proyectil.posicion_y, enemigo.posicion_y + enemigo.alto),
                )
                distancia_x = proyectil.posicion_x - punto_x
                distancia_y = proyectil.posicion_y - punto_y
                if (
                    distancia_x * distancia_x + distancia_y * distancia_y
                    <= proyectil.radio * proyectil.radio
                ):
                    enemigo.vida -= 1
                    impacto = True
                    break
            if not impacto:
                proyectiles_restantes.append(proyectil)
        
        self.proyectiles = proyectiles_restantes

        # 2. Colisiones de proyectiles del jugador con el jefe
        if self.jefe is not None:
            rect_jefe = pygame.Rect(self.jefe.posicion_x, self.jefe.posicion_y, self.jefe.ancho, self.jefe.alto)
            proyectiles_restantes_jefe = []
            
            for proyectil in self.proyectiles:
                rect_proyectil = pygame.Rect(proyectil.posicion_x - proyectil.radio, proyectil.posicion_y - proyectil.radio, proyectil.radio*2, proyectil.radio*2)
                if rect_jefe.colliderect(rect_proyectil):
                    self.jefe.vida -= 1
                else:
                    proyectiles_restantes_jefe.append(proyectil)
            
            self.proyectiles = proyectiles_restantes_jefe
            
            if self.jefe.vida <= 0:
                self.finalizar_partida(True)

        # 3. Definir rectángulo del jugador para las siguientes colisiones
        rect_jugador = pygame.Rect(
            self.jugador.posicion_x,
            self.jugador.posicion_y,
            self.jugador.ancho,
            self.jugador.alto,
        )

        # 4. Colisiones de proyectiles enemigos con el jugador
        proyectiles_enemigos_restantes = []
        for proyectil in self.proyectiles_enemigos:
            rect_proyectil = pygame.Rect(proyectil.posicion_x - proyectil.radio, proyectil.posicion_y - proyectil.radio, proyectil.radio*2, proyectil.radio*2)
            if rect_jugador.colliderect(rect_proyectil):
                self.jugador.vidas -= 1
            else:
                proyectiles_enemigos_restantes.append(proyectil)
        self.proyectiles_enemigos = proyectiles_enemigos_restantes

        # 5. Colisiones de enemigos (cuerpo a cuerpo) con el jugador y eliminación de enemigos muertos
        enemigos_restantes = []
        enemigos_muertos_ahora = 0
        for enemigo in self.enemigos:
            if enemigo.vida <= 0:
                enemigos_muertos_ahora += 1
                continue
                
            rect_enemigo = pygame.Rect(
                enemigo.posicion_x,
                enemigo.posicion_y,
                enemigo.ancho,
                enemigo.alto,
            )
            if rect_jugador.colliderect(rect_enemigo):
                self.jugador.vidas -= 1
            else:
                enemigos_restantes.append(enemigo)

        self.puntaje += enemigos_muertos_ahora
        self.enemigos = enemigos_restantes

        # 6. Comprobar si el jugador ha muerto
        if self.jugador.vidas <= 0:
            self.finalizar_partida(False)

    def iniciar_partida(self) -> None:
        self.tiempo_transcurrido = 0.0
        self.jugador = Jugador(ANCHO_VENTANA // 2 - 20, ALTO_VENTANA - 70)
        self.proyectiles = []
        self.proyectiles_enemigos = []
        self.jefe = None
        self.puntaje = 0
        self.gestor_oleadas = GestorOleadas()
        self.enemigos = [Enemigo(200, 50, 1), Enemigo(480, 50, 2), Enemigo(760, 50, 3)]
        self.estado = self.JUGANDO

    def finalizar_partida(self, victoria: bool) -> None:
        self.estado = self.VICTORIA if victoria else self.DERROTA

    def dibujar(self) -> None:
        self.pantalla.fill(COLOR_FONDO)
        if self.estado == self.MENU:
            self.interfaz.dibujar_menu()
        elif self.estado == self.JUGANDO:
            self.interfaz.dibujar_partida(
                self.jugador,
                self.proyectiles + self.proyectiles_enemigos,
                self.enemigos,
                self.jefe,
                self.tiempo_transcurrido,
                self.puntaje,
                self.gestor_oleadas.oleada_actual,
            )
        else:
            self.interfaz.dibujar_resultado(self.estado == self.VICTORIA)
        pygame.display.flip()