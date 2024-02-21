import flet as ft
from consolidado import Consolidado
from mensual import Mensual
from reposiciones import Reposiciones
from compra_local import CompraLocal
from bodega import Bodega

class Menu(ft.Container):
    def __init__(self):
        self.main_content = Consolidado()  # Inicialmente mostrar la vista de Consolidado
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
                        ft.Image(src=f"https://cdn.discordapp.com/attachments/602383815486210058/1209131285423853569/Logo-Eklipse-02-1.png?ex=65e5ce43&is=65d35943&hm=3acb8be947925f9a7bbaec9e27b8bfd7294bf1584f1f7bb7f91bcd5791772e9d&", width=220, height=200),
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
