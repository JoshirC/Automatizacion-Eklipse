import flet as ft
from consolidado import Consolidado
from mensual import Mensual
from reposiciones import Reposiciones
from compra_local import CompraLocal
from bodega import Bodega
from unificar import Unificar

class Menu(ft.Container):
    def __init__(self):
        self.main_content = ft.Container(
            width=750, 
            height=600,
            padding=10,
           #bgcolor=ft.colors.BLUE
            content=ft.Column([
                ft.Container(
                    content=ft.Image(src=f"/fondo.jpg", width=700, height=400)
                ),
                ft.Text("Bienvenido a EKLIPSE", size=60, weight=ft.FontWeight.W_900, selectable=True), #Titulo
                ft.Row([
                    ft.Icon(ft.icons.COPYRIGHT_SHARP, size=15, color=ft.colors.BLACK),
                    ft.Text("2024 - Desarrollado por Joshir", size=12, color=ft.colors.BLACK),
                    ft.Icon(ft.icons.EMAIL_OUTLINED, size=15, color=ft.colors.BLACK),
                    ft.Text("joshir.contreras@gmail.com", size=12, color=ft.colors.BLACK),
                ]),
            ])

        )  # Inicialmente mostrara la informacion de la APP
        super().__init__(
            width=1000,
            height=600,
            content=self.create_row(self.main_content)
        )
    def create_row(self, main_content):
         return ft.Row([
            ft.Container(
                    width=250,
                    height=600,
                    bgcolor='#FF8412',
                    padding=20,
                    #alignment=ft.alignment.center,
                    content=ft.Column([
                        ft.Image(src=f"/logo_eklipse.png", width=220, height=150),
                        ft.ElevatedButton(
                            content= ft.Container(
                                width=250,
                                height=45,
                                alignment=ft.alignment.center,
                                content=ft.Text("RECTIFICACIÓN", color=ft.colors.BLACK, size=15),
                            ),
                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                            on_click=self.show_consolidado
                        ),
                        ft.ElevatedButton(
                            content= ft.Container(
                                width=200,
                                height=45,
                                alignment=ft.alignment.center,
                                content=ft.Text("MENSUAL", color=ft.colors.BLACK, size=15),
                            ),
                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                            on_click=self.show_mensual
                        ),
                        ft.ElevatedButton(
                            content= ft.Container(
                                width=200,
                                height=45,
                                alignment=ft.alignment.center,
                                content=ft.Text("COMPRA LOCAL", color=ft.colors.BLACK, size=15),
                            ),
                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                            on_click=self.show_compra_local
                        ),
                        ft.ElevatedButton(
                            content= ft.Container(
                                width=200,
                                height=45,
                                alignment=ft.alignment.center,
                                content=ft.Text("BODEGA", color=ft.colors.BLACK, size=15),
                            ),
                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                            on_click=self.show_bodega
                        ),
                        ft.ElevatedButton(
                            content= ft.Container(
                                width=200,
                                height=45,
                                alignment=ft.alignment.center,
                                content=ft.Text("REPOSICIONES", color=ft.colors.BLACK, size=15),
                            ),
                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                            on_click=self.show_reposiciones
                        ),
                        ft.ElevatedButton(
                            content= ft.Container(
                                width=200,
                                height=45,
                                alignment=ft.alignment.center,
                                content=ft.Text("UNIFICAR", color=ft.colors.WHITE, size=15),
                            ),
                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                            bgcolor='#FB4308',
                            on_click=self.show_unificar
                        ),
                    ], alignment=ft.MainAxisAlignment.START),
                ),
                main_content # Inicialmente mostrar la vista de Consolidado
            ])

    def show_consolidado(self, button):
        self.main_content = Consolidado()
        self.content = self.create_row(self.main_content)
        self.update()

    def show_mensual(self, button):
        self.main_content = Mensual()
        self.content = self.create_row(self.main_content)
        self.update()

    def show_reposiciones(self, button):
        self.main_content = Reposiciones()
        self.content = self.create_row(self.main_content)
        self.update()
    def show_compra_local(self, button):
        self.main_content = CompraLocal()
        self.content = self.create_row(self.main_content)
        self.update()
    def show_bodega(self, button):
        self.main_content = Bodega()
        self.content = self.create_row(self.main_content)
        self.update()
    def show_unificar(self,buton):
        self.main_content = Unificar()
        self.content = self.create_row(self.main_content)
        self.update()