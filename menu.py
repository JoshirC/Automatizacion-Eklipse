import flet as ft
from consolidado import Consolidado
from mensual import Mensual
from reposiciones import Reposiciones
from compra_local import CompraLocal
from bodega import Bodega

class Menu(ft.Container):
    def __init__(self):
        self.main_content = ft.Container(
            width=750, 
            height=600,
            padding=10,
           #bgcolor=ft.colors.BLUE
            content=ft.Column([
                ft.Text("Bienvenido a EKLIPSE", size=30, weight=ft.FontWeight.W_900, selectable=True), #Titulo
                ft.Container(
                    content=ft.Image(src=f"/images/Concurso Fotografico Ganadores.jpg", width=700, height=400,border_radius=50)
                ),
                ft.Text("Creado por Joshir Contreras S ")
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
                    padding=15,
                    content=ft.Column([
                        ft.Image(src=f"/images/logo_eklipse.png", width=220, height=200),
                        ft.ElevatedButton(
                            content= ft.Container(
                                width=200,
                                height=50,
                                alignment=ft.alignment.center,
                                content=ft.Text("RECTIFICACIÓN", color=ft.colors.BLACK, size=15),
                            ),
                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                            on_click=self.show_consolidado
                        ),
                        ft.ElevatedButton(
                            content= ft.Container(
                                width=200,
                                height=50,
                                alignment=ft.alignment.center,
                                content=ft.Text("MENSUAL", color=ft.colors.BLACK, size=15),
                            ),
                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                            on_click=self.show_mensual
                        ),
                        ft.ElevatedButton(
                            content= ft.Container(
                                width=200,
                                height=50,
                                alignment=ft.alignment.center,
                                content=ft.Text("COMPRA LOCAL", color=ft.colors.BLACK, size=15),
                            ),
                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                            on_click=self.show_compra_local
                        ),
                        ft.ElevatedButton(
                            content= ft.Container(
                                width=200,
                                height=50,
                                alignment=ft.alignment.center,
                                content=ft.Text("BODEGA", color=ft.colors.BLACK, size=15),
                            ),
                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                            on_click=self.show_bodega
                        ),
                        ft.ElevatedButton(
                            content= ft.Container(
                                width=200,
                                height=50,
                                alignment=ft.alignment.center,
                                content=ft.Text("REPOSICIONES", color=ft.colors.BLACK, size=15),
                            ),
                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                            on_click=self.show_reposiciones
                        )
                    ])
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
