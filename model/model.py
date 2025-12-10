from itertools import combinations
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
            if r1 is None or r2 is None:
                continue
            if l.difficolta == "facile":
                fattore = 1
            elif l.difficolta == "media":
                fattore = 1.5
            else:
                fattore = 2
            peso = float(l.distanza) * fattore
            self.G.add_edge(r1, r2, peso=peso)

    def get_edges_weight_min_max(self):
        """
        Restituisce min e max peso degli archi nel grafo
        :return: il peso minimo degli archi nel grafo
        :return: il peso massimo degli archi nel grafo
        """
        pesi = []
        if self.G.number_of_edges() == 0: #verifichiamo che il grafo abbia gli archi
            return None
        for u,v, data in self.G.edges(data=True):
            peso = data['peso']
            pesi.append(peso)
        min_peso = min(pesi)
        max_peso = max(pesi)
        return min_peso, max_peso

    def count_edges_by_threshold(self, soglia):
        """
        Conta il numero di archi con peso < soglia e > soglia
        :param soglia: soglia da considerare nel conteggio degli archi
        :return minori: archi con peso < soglia
        :return maggiori: archi con peso > soglia
        """
        minori = 0
        maggiori = 0
        if self.G.number_of_edges() == 0:
            return 0,0
        for u,v, data in self.G.edges(data=True):
            peso = data['peso']
            if peso < soglia:
                minori += 1
            if peso > soglia:
                maggiori +=1
        return minori, maggiori

    """Implementare la parte di ricerca del cammino minimo"""
    def find_cammino_nx(self, soglia):
        # grafo che contiene solo gli archi che hanno il peso > soglia
        grafo_filtrato = nx.Graph()
        for u, v, data in self.G.edges(data=True):
            if data['peso'] > soglia:
                grafo_filtrato.add_edge(u,v,peso =data['peso'])
        if grafo_filtrato.number_of_edges() == 0:
            return []

        min_cammino = [] #cammino minimo
        min_peso = float('inf') #peso totale minimo, inizializzano a infinito o un numero molto grande
        for nodo_partenza in grafo_filtrato.nodes():
            for nodo_arrivo in grafo_filtrato.nodes():
                if nodo_partenza == nodo_arrivo:
                    continue
                try:
                    path = nx.shortest_path(grafo_filtrato, nodo_partenza, nodo_arrivo, weight ='peso')
                    if len(path) < 3:
                        continue
                    peso_totale = nx.shortest_path_length(grafo_filtrato, nodo_partenza, nodo_arrivo, weight = 'peso')
                    if peso_totale < min_peso:
                        min_peso = peso_totale
                        min_cammino = path
                except nx.NetworkXNoPath:  #mi dice che se il cammino tra i due nodi  non ce
                    continue # si passa alla coppia di nodi successiva
        return min_cammino

    def find_cammino_ric(self, soglia):
        grafo_filtrato = nx.Graph()
        for u, v, data in self.G.edges(data=True):
            if data['peso'] > soglia:
                grafo_filtrato.add_edge(u, v, peso=data['peso'])
        if grafo_filtrato.number_of_edges() == 0:
            return []
        miglior_cammino = None
        miglior_peso = float('inf')
        for nodo_partenza in grafo_filtrato.nodes():
            cammino, peso = self.dfs(nodo_partenza, {nodo_partenza}, [nodo_partenza], 0, grafo_filtrato)
            if cammino is not None and peso < miglior_peso:
                miglior_peso = peso
                miglior_cammino = cammino

        def dfs(self, nodo, visited, cammino, peso, grafo_filtrato):  # questa fz ci restituisce la tupla del miglior cammino (cammino, peso), esplorando tutti i cammini semplici
            #se ha almeno due archi lo considero
            if len(cammino) >= 3: #quindi se la lista dei nodi è maggiore o uguale di tre
                miglior_cammino = cammino.copy() #mi fa una copia della lista di nodi, così che anche dopo il backtracking mi rimane
                peso_m = peso
            else:
                miglior_cammino = None
                peso_m = float('inf')
            for vicino in grafo_filtrato.neighbors(nodo):
                if vicino not in visited:
                    peso_arco = grafo_filtrato[nodo][vicino]['peso']
                    visited.add(vicino)
                    cammino.append(vicino)

                    sub_cammino, sub_peso = self.dfs(vicino, visited, cammino, peso+peso_arco, grafo_filtrato)
                    if sub_cammino is not None and sub_peso < peso_m:
                        peso_m = sub_peso
                        miglior_cammino = sub_cammino
                    cammino.pop()
                    visited.remove(vicino)
            return miglior_cammino, peso_m







