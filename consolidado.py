import flet as ft
import pandas as pd

class Consolidado(ft.Container):
    cadena_texto_semanal = ft.Text("")
    cadena_texto_local = ft.Text("")

    txt_consolidado = ft.TextField(label="Ingrese la ruta de los archivos", multiline=True, bgcolor=ft.colors.WHITE)
    txt_compra_local = ft.TextField(label="Ingrese la ruta de los archivos", multiline=True, bgcolor=ft.colors.WHITE,)

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
                                    height=350,
                                    #bgcolor=ft.colors.WHITE,
                                    border_radius=12,
                                    padding=5,
                                    content= self.txt_consolidado
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
                                    height=350,
                                    #bgcolor=ft.colors.WHITE,
                                    border_radius=12,
                                    padding=5,
                                    content= self.txt_compra_local
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
                            on_click=self.txt
                        )
            ])
        )
    def txt(self, button):
            self.cadena_texto_semanal.value = self.txt_consolidado.value
            self.cadena_texto_local.value = self.txt_compra_local.value
            self.separar_caracteres()
            self.txt_consolidado.value = ""
            self.txt_compra_local.value = ""

            self.update()
    def separar_caracteres(self):
        print(self.cadena_texto_semanal.value)
        df_semanal = pd.DataFrame(self.cadena_texto_semanal.value)
        print(df_semanal)
        