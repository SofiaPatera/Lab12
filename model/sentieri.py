from dataclasses import dataclass
import datetime

@dataclass
class Sentieri:
    id: int
    id_rifugio1: int
    id_rifugio2: int
    distanza: float
    difficolta: str
    durata: datetime.time
    anno: int
    peso : float

    def __str__(self):
        return f"{self.id}"