from dataclasses import dataclass, asdict
import json, os

ROOMS_FILE = 'data/rooms.json'


@dataclass
class Quarto:
    numero: int
    tipo: str
    preco_noite: float
    ocupado: bool = False


class QuartosRepo:
    def __init__(self):
        self._rooms = {}
        os.makedirs('data', exist_ok=True)
        self.load()

    def add(self, numero, tipo, preco):
        q = Quarto(numero, tipo, preco)
        self._rooms[q.numero] = q
        self.save()
        return q

    def list_all(self):
        return list(self._rooms.values())

    def remove(self, numero):
        if numero in self._rooms:
            del self._rooms[numero]
            self.save()

    def save(self):
        with open(ROOMS_FILE, 'w', encoding='utf-8') as f:
            json.dump([asdict(r) for r in self._rooms.values()], f, indent=2)

    def load(self):
        if os.path.exists(ROOMS_FILE):
            with open(ROOMS_FILE, encoding='utf-8') as f:
                for item in json.load(f):
                    q = Quarto(**item)
                    self._rooms[q.numero] = q
