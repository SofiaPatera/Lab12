import flet as ft
from UI.alert import AlertManager

class View:
    def __init__(self, page: ft.Page):
        # Page
        self.page = page
        self.page.title = "Lab12"
        self.page.horizontal_alignment = "center"
        self.page.theme_mode = ft.ThemeMode.DARK

        # Alert
        self.alert = AlertManager(page)

        # Controller
        self.controller = None

    def show_alert(self, messaggio):
        self.alert.show_alert(messaggio)

    def set_controller(self, controller):
        self.controller = controller

    def update(self):
        self.page.update()

    def load_interface(self):
        """ Crea e aggiunge gli elementi di UI alla pagina e la aggiorna. """
        # Intestazione
        self.txt_titolo = ft.Text(value="Gestione Sentieri di Montagna", size=38, weight=ft.FontWeight.BOLD)

        # Riga 1
        self.txt_anno = ft.TextField(label="Anno (1950-2024)", width=200)
        pulsante_crea_grafo = ft.ElevatedButton(
            text="Crea Grafo",
            on_click=self.controller.handle_grafo if self.controller else None,
            width=200
        )
        row1 = ft.Row([self.txt_anno, pulsante_crea_grafo], alignment=ft.MainAxisAlignment.CENTER)
        self.lista_visualizzazione_1 = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=False)

        # Riga 2
        self.txt_soglia = ft.TextField(label="Soglia Peso", width=200)
        self.pulsante_conta_archi = ft.ElevatedButton("Conta Archi", width=200,
                                                 on_click=self.controller.handle_conta_archi if self.controller else None)
        row2 = ft.Row([self.txt_soglia, self.pulsante_conta_archi], alignment=ft.MainAxisAlignment.CENTER)
        self.lista_visualizzazione_2 = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=False)

        # Riga 3: Implementare la parte di ricerca del cammino minimo
        self.lista_visualizzazione_3 = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=False)
        pulsante_cammino_minimo = ft.ElevatedButton(text  = "Cammino Minimo",
                                                    on_click = self.controller.handle_cammino_minimo if self.controller else None)
        row3= ft.Row([pulsante_cammino_minimo], alignment=ft.MainAxisAlignment.CENTER)

        # --- Toggle Tema ---
        self.toggle_cambia_tema = ft.Switch(label="Tema scuro", value=True, on_change=self.cambia_tema)

        # --- Layout della pagina ---
        self.page.add(
            self.toggle_cambia_tema,

            # Sezione 1
            self.txt_titolo,
            ft.Divider(),

            row1,
            self.lista_visualizzazione_1,
            ft.Divider(),

            row2,
            self.lista_visualizzazione_2,
            ft.Divider(),

            # Implementare la parte di ricerca del cammino minimo
            row3,
            self.lista_visualizzazione_3,


        )

        self.page.scroll = "adaptive"
        self.page.update()

    def cambia_tema(self, e):
        """ Cambia tema scuro/chiaro """
        self.page.theme_mode = ft.ThemeMode.DARK if self.toggle_cambia_tema.value else ft.ThemeMode.LIGHT
        self.toggle_cambia_tema.label = "Tema scuro" if self.toggle_cambia_tema.value else "Tema chiaro"
        self.page.update()
