from dataclasses import dataclass, asdict
import json, os
from datetime import datetime

RES_FILE = 'data/reservas.json'


@dataclass
class Reserva:
    id: int
    cliente_id: int
    quarto_numero: int
    checkin: str
    checkout: str


class ReservasRepo:
    def __init__(self):
        self._reservas = {}
        self._next_id = 1
        os.makedirs('data', exist_ok=True)
        self.load()

    def create(self, cliente_id, quarto_numero, checkin, checkout):
        d1 = datetime.fromisoformat(checkin)
        d2 = datetime.fromisoformat(checkout)
        if d2 <= d1:
            raise ValueError('Checkout must be after checkin')
        r = Reserva(self._next_id, cliente_id, quarto_numero, checkin, checkout)
        self._reservas[r.id] = r
        self._next_id += 1
        self.save()
        return r

    def list_all(self):
        return list(self._reservas.values())

    def cancel(self, rid):
        if rid in self._reservas:
            del self._reservas[rid]
            self.save()

    def save(self):
        with open(RES_FILE, 'w', encoding='utf-8') as f:
            json.dump([asdict(r) for r in self._reservas.values()], f, indent=2)

    def load(self):
        if os.path.exists(RES_FILE):
            with open(RES_FILE, encoding='utf-8') as f:
                for item in json.load(f):
                    r = Reserva(**item)
                    self._reservas[r.id] = r
                    self._next_id = max(self._next_id, r.id + 1)
