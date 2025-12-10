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
            return None
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
        #il percorso deve contenere almeno 2 archi
        if grafo_filtrato.number_of_edges() < 2:
            return []

        minimo_cammino = None #cammino minimo
        min_peso = float('inf') #peso totale minimo, inizializzano a infinito o un numero molto grande
        nodi = list(grafo_filtrato.nodes) #lista dei nodi del grafo
        nodo_partenza = nodi[0] #fisso il nodo di partenza
        for nodo_arrivo in nodi[1:]:
                try:
                    path = nx.shortest_path(grafo_filtrato, nodo_partenza, nodo_arrivo, weight ='peso')
                except nx.NetworkXNoPath:  #mi dice che se il cammino tra i due nodi  non ce
                    continue # si passa alla coppia di nodi successiva

                #calcolo il peso totale del cammino che abbiamo trovato
                totale_weight = 0
                for p in range(len(path)-1): # -1 perchè dobbiamo prendere gli indici dei nodi che partono da 0
                    nodo1 = path[p]
                    nodo2 = path[p+1]
                    edge_weight = grafo_filtrato[nodo1][nodo2]['peso'] #prendiamo il peso dell'arco tra questi due nodi
                    totale_weight += edge_weight #somma di tutti i pesi degli archi nel cammino

                #controllo se il cammino ha almeno 3 nodi (che implica due archi)
                if len(path) >= 3 and totale_weight < min_peso:
                    #se il peso tot è < di quello trovato => si aggiorna
                        min_peso = totale_weight
                        minimo_cammino = path[:]

        return minimo_cammino if minimo_cammino is not None else []

    def find_cammino_ric(self, soglia):
        grafo_filtrato = nx.Graph()
        for u, v, data in self.G.edges(data=True):
            if data['peso'] > soglia:
                grafo_filtrato.add_edge(u, v, peso=data['peso'])
        if grafo_filtrato.number_of_edges() < 2:
            return []

        def dfs(path, visited, weight):  # questa fz ci restituisce la tupla del miglior cammino (cammino, peso), esplorando tutti i cammini semplici
            #iniziliazziamo
            miglior_cammino = None
            miglior_peso = float('inf')
            #se ha almeno due archi lo considero
            if len(path) >= 3: #quindi se la lista dei nodi è maggiore o uguale di tre
                miglior_peso = weight
                miglior_cammino = path[:] #mi fa una copia della lista di nodi, così che anche dopo il backtracking mi rimane
            #guardo i nodi vicini a l'ultimo nodo preso
            ultimo_nodo = path[-1]
            for n in grafo_filtrato.neighbors(ultimo_nodo):
                if n not in visited:
                    edge_w = grafo_filtrato[ultimo_nodo][n]['peso']

                    visited.add(n) #aggiungo a quelli visitati quello appena visto
                    path.append(n)

                    candidati_path, candidati_weight = dfs(path, visited, weight+ edge_w)

                    if candidati_weight and candidati_weight < miglior_peso: # se quella appena selezionata è migliore di quella che gia ho
                        miglior_cammino = candidati_path
                        miglior_peso = candidati_weight

                    #rimuovo le aggiunte di prima, prima di riprovare altri vicini
                    path.pop()
                    visited.remove(n)

            return miglior_cammino, miglior_peso #ritorno la miglior soluzione trovata

        lista_migliori_path = None
        miglio_peso_globale = float('inf')
        nodo_partenza = list(grafo_filtrato.nodes)[0]
        cammino, peso = dfs([nodo_partenza], {nodo_partenza}, 0)

        if cammino is not None and peso < miglio_peso_globale:
                miglio_peso_globale = peso
                lista_migliori_path = cammino
        return lista_migliori_path if lista_migliori_path is not None else []







