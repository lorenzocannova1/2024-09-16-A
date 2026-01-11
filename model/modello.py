import copy

from database.DAO import DAO
import networkx as nx
from model.state import State
import geopy.distance as distance

class Model:
    def __init__(self):
        self.grafo = nx.Graph()

    def getMaxMinLat(self):
        return DAO.getMaxMinLat()

    def getMaxMinLng(self):
        return DAO.getMaxMinLng()

    def getAllForme(self):
        return DAO.getAllForme()

    def creaGrafo(self,lat, lng, forma):
        self.grafo.clear()
        nodi = DAO.getAllNodi(lat, lng, forma)
        self.grafo.add_nodes_from(nodi)

        vicini = DAO.getAllVicini()

        for i in nodi:
            for j in nodi:
                if (i.id,j.id) in vicini or (j.id,i.id) in vicini:
                    peso1 = self.calcolaPeso(i, forma)
                    peso2 = self.calcolaPeso(j, forma)
                    pesoTot = peso1 + peso2
                    self.grafo.add_edge(i, j, weight=pesoTot)

    def calcolaPeso(self, nodo, forma):
        peso = DAO.getCalcolaPeso(nodo.id, forma)[0]
        return peso

    def infoGrafo(self):
        return len(self.grafo.nodes), len(self.grafo.edges)

    def dettagliGrafo(self):
        res1 = []
        for nodo in self.grafo.nodes:
            grado = nx.degree(self.grafo,nodo)
            res1.append( (nodo,grado) )

        res1.sort(key = lambda x: x[1], reverse = True)

        res2 = []
        for arco in self.grafo.edges(data=True):
            res2.append( (arco[0],arco[1],arco[2]['weight']) )

        res2.sort(key = lambda x: x[2], reverse = True)

        return res1[0:5], res2[0:5]

    def cammino_ottimo(self):
        self._cammino_ottimo = []
        self._punteggio_ottimo = 0.0

        for nodo in self.grafo.nodes():
            self._calcola_cammino_ricorsivo([nodo], self._calcola_successivi(nodo))
        return self._cammino_ottimo, self._punteggio_ottimo

    def _calcola_cammino_ricorsivo(self, parziale: list[State], successivi: list[State]):
        if len(successivi) == 0:
            score = self._calcola_score(parziale)
            if score > self._punteggio_ottimo:
                self._punteggio_ottimo = score
                self._cammino_ottimo = copy.deepcopy(parziale)
        else:
            for nodo in successivi:
                # aggiungo il nodo in parziale ed aggiorno le occorrenze del mese corrispondente
                parziale.append(nodo)
                # nuovi successivi
                nuovi_successivi = self._calcola_successivi(nodo)
                # ricorsione
                self._calcola_cammino_ricorsivo(parziale, nuovi_successivi)
                parziale.pop()

    def _calcola_successivi(self, nodo: State) -> list[State]:
        """
        Calcola il sottoinsieme dei successivi ad un nodo
        """
        successivi = self.grafo.neighbors(nodo)
        successivi_ammissibili = []
        for s in successivi:
            if (s.Population/s.Area) > (nodo.Population/nodo.Area):
                successivi_ammissibili.append(s)
        return successivi_ammissibili

    def _calcola_score(self, cammino: list[State]) -> float:
        """
        Funzione che calcola il punteggio di un cammino.
        """
        score = 0
        for i in range(0, len(cammino)-1):
            peso = self.grafo.get_edge_data(cammino[i], cammino[i+1])["weight"]
            distanza = cammino[i].distance_HV(cammino[i+1])
            score += peso/distanza
        return score