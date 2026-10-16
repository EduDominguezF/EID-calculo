# Space Conics: videojuego con secciones cónicas y funciones trigonométricas

Videojuego de naves desarrollado para el EID 1. La nave del jugador ataca con trayectorias definidas por rectas, parábolas y secciones cónicas, y los enemigos se mueven con funciones trigonométricas (movimiento sinusoidal).

## Integrantes

| Integrante | Rol | Archivos |
|---|---|---|
| Eduardo Dominguez | Base del proyecto, estructura, bucle principal e integración | `main.py`, `settings.py`, `game.py`, `ui.py`, `README.md` |
| Alessandro Budini | Nave principal y sus 3 tipos de acciones | `player.py`, `projectiles.py`, `conics.py` |
| Javier Poblete | Enemigos, oleadas y jefe | `enemies.py`, `waves.py`, `boss.py` |

## Responsabilidades

### Eduardo Dominguez: base e integración
- Crear la estructura de carpetas y el repositorio.
- Definir las constantes globales en `settings.py` (tamaño de ventana, FPS, colores, velocidades, vidas).
- Programar el bucle principal del juego, los estados (menú, jugando, victoria, derrota) y el reloj.
- Implementar los límites de mapa para la nave, los proyectiles y los enemigos.
- Gestionar las colisiones entre proyectiles y enemigos, y entre enemigos y nave.
- Dibujar el HUD: vidas, puntaje, oleada actual y vida del jefe.
- Integrar los módulos de Alessandro y Javier y revisar que el código final no tenga comentarios.

### Alessandro Budini: nave principal
- Clase `Jugador` con movimiento horizontal y vertical.
- Acción 1: disparo en línea recta (ecuación de la recta).
- Acción 2: disparo parabólico (ecuación de la parábola).
- Acción 3: disparo con sección cónica (circunferencia, elipse o hipérbola) parametrizada con `math.sin` y `math.cos`.
- Clases de proyectiles en `projectiles.py` y las ecuaciones en `conics.py`.

### Javier Poblete: enemigos, oleadas y jefe
- 3 tipos de enemigos con movimiento sinusoidal, sin colisión entre ellos.
- Sistema de 3 oleadas con dificultad creciente en `waves.py`.
- Jefe final con vida, patrón de movimiento y ataque propios en `boss.py`.
- Aparición con `random` y eliminación de enemigos al salir del mapa.

## Requisitos

Librerías permitidas (únicas que se pueden usar):

- `pygame`
- `random`
- `math`

Librerías prohibidas:

- `numpy`
- `scipy`
- `sympy`

## Instalación y ejecución

```
pip install pygame
python main.py
```

## Controles

| Tecla | Acción |
|---|---|
| Flechas | Mover la nave |
| Z (mantener) | Disparo en línea recta, sin límite |
| X | Disparo parabólico (cooldown 0.8 s) |
| C | Disparo elíptico (cooldown 2.5 s) |
| ESC | Salir |

## Estructura del proyecto

```
space-conics/
├── main.py
├── settings.py
├── game.py
├── ui.py
├── player.py
├── projectiles.py
├── conics.py
├── enemies.py
├── waves.py
├── boss.py
└── README.md
```

## Organización del código

Se conserva la estructura de archivos actual con responsabilidades separadas:

- `main.py` inicia la aplicación con `iniciar_aplicacion`.
- `game.py` coordina el ciclo del juego, los estados, la entrada, las actualizaciones y las colisiones mediante `Juego`.
- `ui.py` contiene la presentación y el dibujado mediante `Interfaz`; recibe entidades y no controla las reglas de la partida.
- `settings.py` centraliza la configuración con nombres en español.
- Los demás módulos contienen los datos y el comportamiento de `Jugador`, `Proyectil`, `Conica`, `Enemigo`, `Oleada`, `GestorOleadas` y `Jefe`, sin depender de Pygame para dibujarse.

Los nombres propios del lenguaje y de Pygame, como `__init__`, `pygame.draw` y las constantes de teclas, conservan su forma original para respetar sus interfaces.

## Reglas de entrega

- Código sin comentarios.
- Defensa en video explicando el código y las matemáticas aplicadas.
- Juego funcionando.
