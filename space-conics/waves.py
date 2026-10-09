class Wave:
    def __init__(self, number: int, enemy_count: int) -> None:
        self.number = number
        self.enemy_count = enemy_count

    def spawn(self) -> list[dict]:
        return [{"x": 50 + i * 70, "y": 50} for i in range(self.enemy_count)]


class WaveManager:
    def __init__(self) -> None:
        self.current_wave = 1

    def next_wave(self) -> None:
        self.current_wave += 1

    def get_current_wave(self) -> Wave:
        return Wave(self.current_wave, self.current_wave * 3)
