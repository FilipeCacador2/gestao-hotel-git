from dataclasses import dataclass, asdict
import json, os

CLIENTS_FILE = 'data/clients.json'


@dataclass
class Cliente:
    id: int
    nome: str
    telefone: str
    email: str


class ClientesRepo:
    def __init__(self):
        self._clientes = {}
        self._next_id = 1
        os.makedirs('data', exist_ok=True)
        self.load()

    def add(self, nome, telefone, email):
        c = Cliente(self._next_id, nome, telefone, email)
        self._clientes[c.id] = c
        self._next_id += 1
        self.save()
        return c

    def list_all(self):
        return list(self._clientes.values())

    def remove(self, cid):
        if cid in self._clientes:
            del self._clientes[cid]
            self.save()

    def save(self):
        with open(CLIENTS_FILE, 'w', encoding='utf-8') as f:
            json.dump(
                [asdict(c) for c in self._clientes.values()],
                f,
                ensure_ascii=False,
                indent=2,
            )

    def load(self):
        if os.path.exists(CLIENTS_FILE):
            with open(CLIENTS_FILE, encoding='utf-8') as f:
                for item in json.load(f):
                    c = Cliente(**item)
                    self._clientes[c.id] = c
                    self._next_id = max(self._next_id, c.id + 1)
