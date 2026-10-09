class Oleada:
    def __init__(self, numero: int, cantidad_enemigos: int) -> None:
        self.numero = numero
        self.cantidad_enemigos = cantidad_enemigos

    def generar_apariciones(self) -> list[dict[str, int]]:
        return [
            {"posicion_x": 50 + indice * 70, "posicion_y": 50}
            for indice in range(self.cantidad_enemigos)
        ]


class GestorOleadas:
    def __init__(self) -> None:
        self.oleada_actual = 1

    def avanzar_oleada(self) -> None:
        self.oleada_actual += 1

    def obtener_oleada_actual(self) -> Oleada:
        return Oleada(self.oleada_actual, self.oleada_actual * 3)
