import networkx as nx
from database.dao import DAO

class Model:
    def __init__(self):
        """Definire le strutture dati utili"""
        self.G = nx.Graph()
        self._lista_rifugi = []
        self._lista_sentieri = []
        self.idMappa = {}



    def build_weighted_graph(self, year: int):
        """
        Costruisce il grafo pesato dei rifugi considerando solo le connessioni con campo `anno` <= year passato
        come argomento.
        Il peso del grafo è dato dal prodotto "distanza * fattore_difficolta"
        """
        self.G.clear()
        self._lista_rifugi = DAO.leggiRifugio(year)
        self.idMappa = {r.id: r for r in self._lista_rifugi}
        self.G.add_nodes_from(self._lista_rifugi)
        self._lista_sentieri = DAO.leggiSentieri(year)
        for l in self._lista_sentieri:
            r1 = self.idMappa[l.id_rifugio1]
            r2 = self.idMappa[l.id_rifugio2]
            self.G.add_edge(r1, r2, peso=l.peso)

    def get_edges_weight_min_max(self):
        """
        Restituisce min e max peso degli archi nel grafo
        :return: il peso minimo degli archi nel grafo
        :return: il peso massimo degli archi nel grafo
        """
        # TODO

    def count_edges_by_threshold(self, soglia):
        """
        Conta il numero di archi con peso < soglia e > soglia
        :param soglia: soglia da considerare nel conteggio degli archi
        :return minori: archi con peso < soglia
        :return maggiori: archi con peso > soglia
        """
        # TODO

    """Implementare la parte di ricerca del cammino minimo"""
    # TODO
