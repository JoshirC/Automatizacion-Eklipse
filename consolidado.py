import flet as ft
import pandas as pd

class Consolidado(ft.Container):
    def __init__(self):
        super().__init__(
            width=750, 
            height=600,
            padding=10, 
            bgcolor=ft.colors.WHITE,
            content=ft.Column([
                ft.Text("CONSOLIDADO", size=30, weight=ft.FontWeight.W_900, selectable=True), #Titulo
                ft.Container( #Contenedor para el contenido
                    width=695,
                    height=420,
                    alignment=ft.alignment.center,
                    content= ft.Row([
                        ft.Container( #Contenedor para archivo semanal
                            width=342,
                            height=420,
                            bgcolor="#D9D9D9",
                            border_radius=12,
                            alignment=ft.alignment.center,
                            padding=15,
                            content=ft.Column([
                                ft.Text("Rectificado Semanal", size=20),
                                ft.Container( #Contenedor para mostrar archivos cargados (scroll ?)
                                    width=300,
                                    height=290,
                                    #bgcolor=ft.colors.WHITE,
                                    border_radius=12
                                ),
                                ft.Container(
                                    content=ft.Icon("ADD", size=30, color=ft.colors.WHITE),
                                    padding=10,
                                    alignment=ft.alignment.center,
                                    bgcolor='#FF8412',
                                    width=50,
                                    height=50,
                                    border_radius=100,
                                    on_click=lambda e: print("Clickable with Ink clicked!"),
                                 ),
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                         ),
                        ft.Container( #Contenedor para archivo local
                            width=342,
                            height=420,
                            bgcolor="#D9D9D9",
                            border_radius=12,
                            padding=15,
                            content=ft.Column([
                                ft.Text("Compra Local", size=20),
                                ft.Container(
                                    width=300,
                                    height=290,
                                    #bgcolor=ft.colors.WHITE,
                                    border_radius=12
                                ),
                                ft.Container(
                                    content=ft.Icon("ADD", size=30, color=ft.colors.WHITE),
                                    padding=10,
                                    alignment=ft.alignment.center,
                                    bgcolor='#FF8412',
                                    width=50,
                                    height=50,
                                    border_radius=100,
                                    on_click=lambda e: print("Clickable with Ink clicked!"),
                                ),
                            ],alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        )
                    ]),
                ),
                ft.ElevatedButton( #Boton para generar el consolidado
                            content= ft.Container(
                                width=650,
                                height=50,
                                alignment=ft.alignment.center,
                                content=ft.Text("Generar Consolidado", color=ft.colors.WHITE, size=20),
                            ),
                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                            bgcolor='#FF8412',
                            #on_click=self.show_mensual
                        )
            ])
        )