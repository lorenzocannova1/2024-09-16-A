import flet as ft
from UI.view import View
from model.modello import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view: View = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

        self.maxLat = None
        self.minLat = None
        self.maxLng = None
        self.minLng = None
        self.formaSelezionata = None

    def MaxMinLatLng(self):
        res1 = self._model.getMaxMinLat()
        for r in res1:
            self.minLat = r[0]
            self.maxLat = r[1]
        res2 = self._model.getMaxMinLng()
        for r in res2:
            self.minLng = r[0]
            self.maxLng = r[1]

    def handle_graph(self, e):
        try:
            lat = float(self._view.txt_latitude.value)
            long = float(self._view.txt_longitude.value)
        except ValueError:
            self._view.txt_result1.controls.clear()
            self._view.txt_result1.controls.append(
                ft.Text(f"Il valore della latitudine e della longitudine inserita devono essere numeri (anche decimali)"))
            self._view.update_page()
            return

        if float(self._view.txt_latitude.value) < self.minLat or float(self._view.txt_latitude.value) > self.maxLat:
            self._view.txt_result1.controls.clear()
            self._view.txt_result1.controls.append(ft.Text(f"Il valore della latitudine deve essere compreso tra {self.minLat} e {self.maxLat}"))
            self._view.update_page()
            return

        if float(self._view.txt_longitude.value) < self.minLng or float(self._view.txt_longitude.value) > self.maxLng:
            self._view.txt_result1.controls.clear()
            self._view.txt_result1.controls.append(
                ft.Text(f"Il valore della longitudine deve essere compreso tra {self.minLng} e {self.maxLng}"))
            self._view.update_page()
            return

        if self.formaSelezionata == None:
            self._view.txt_result1.controls.clear()
            self._view.txt_result1.controls.append(
                ft.Text(f"Seleziona una forma prima di procedere con la creazione del grafo"))
            self._view.update_page()
            return

        self._view.txt_result1.controls.clear()
        self._model.creaGrafo(self._view.txt_latitude.value, self._view.txt_longitude.value, self.formaSelezionata)
        nNodi, nArchi = self._model.infoGrafo()
        self._view.txt_result1.controls.clear()
        self._view.txt_result1.controls.append(ft.Text(f"Numero di vertici {nNodi}"))
        self._view.txt_result1.controls.append(ft.Text(f"Numero di vertici {nArchi}"))
        self._view.btn_path.disabled = False
        self._view.update_page()

        res1, res2 = self._model.dettagliGrafo()
        self._view.txt_result1.controls.append(ft.Text(f"I cinque nodi di grado maggiore sono: "))
        for r in res1:
            self._view.txt_result1.controls.append(ft.Text(f"{r[0]} -> degree {r[1]}"))

        self._view.txt_result1.controls.append(ft.Text(f"I cinque archi di peso maggiore sono: "))
        for r in res2:
            self._view.txt_result1.controls.append(ft.Text(f"{r[0]} <-> {r[1]} | peso = {r[2]}"))

        self._view.update_page()



    def riempi_ddshape(self):
        forme = self._model.getAllForme()
        for forma in forme:
            self._view.ddshape.options.append(ft.dropdown.Option(data=forma, text= forma, on_click=self.pickForma))
        self._view.update_page()

    def pickForma(self, e):
        self.formaSelezionata = e.control.data
        print(self.formaSelezionata)

    def handle_path(self, e):

        self._view.txt_result2.controls.clear()
        path, punteggio = self._model.cammino_ottimo()
        self._view.txt_result2.controls.append(ft.Text(f"Il punteggio del percorso ottimo è {punteggio}"))
        self._view.txt_result2.controls.append(ft.Text(f"Il percorso ottimo è costituito da {len(path)} nodi:"))
        for p in path:
            self._view.txt_result2.controls.append(ft.Text(f"{p} | densità = {p.Population / p.Area}"))

        self._view.update_page()


