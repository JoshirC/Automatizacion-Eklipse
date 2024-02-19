import flet as ft

from consolidado import Consolidado

opcion = Consolidado()

class Menu(ft.Container):
    def __init__(self):
        super().__init__(
            width=1000,
            height=600,
            #bgcolor=ft.colors.BLACK,
            content= ft.Row([ft.Container(
                            width=250,
                            height=600,
                            bgcolor=ft.colors.ORANGE,
                            padding=15,
                            content=ft.Column(
                                [   
                                    ft.Image(src=f"https://cdn.discordapp.com/attachments/602383815486210058/1209131285423853569/Logo-Eklipse-02-1.png?ex=65e5ce43&is=65d35943&hm=3acb8be947925f9a7bbaec9e27b8bfd7294bf1584f1f7bb7f91bcd5791772e9d&", width=220, height=250),
                                    ft.ElevatedButton(
                                        content= ft.Container(
                                            width=200,
                                            height=50,
                                            alignment=ft.alignment.center,
                                            content=ft.Text("CONSOLIDADO", color=ft.colors.BLACK, size=15),
                                        ),
                                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                                        on_click=on_click_consolidado()
                                    ),
                                    ft.ElevatedButton(
                                        content= ft.Container(
                                            width=200,
                                            height=50,
                                            alignment=ft.alignment.center,
                                            content=ft.Text("MENSUAL", color=ft.colors.BLACK, size=15),
                                        ),
                                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                                        #on_click=self.on_click_mensual()
                                    ),
                                    ft.ElevatedButton(
                                        content= ft.Container(
                                            width=200,
                                            height=50,
                                            alignment=ft.alignment.center,
                                            content=ft.Text("REPOSICIONES", color=ft.colors.BLACK, size=15),
                                        ),
                                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                                        #on_click=self.on_click_reposiciones()
                                    )
                                ],
                                alignment=ft.MainAxisAlignment.START
                            )
                        ), 
                      ft.Container(
                            width=730,
                            height=600,
                            content=opcion
                      )])
        )
        def on_click_consolidado(e):
            opcion = Consolidado()
            self.update()

