from dataclasses import dataclass

@dataclass
class Rifugio:
    id: int
    nome: str
    localita: str
    altitudine: int
    capienza: int
    aperto: str

    def __str__(self):
        return self.nome

    def __hash__(self):
        return hash(self.id)
