import os
import flet as ft
import pandas as pd

class Bodega(ft.Container):
    txt_bodega = ft.TextField(label="Ingrese la ruta del consolidado", multiline=False, bgcolor=ft.colors.WHITE)
    txt_nombre_archivo = ft.TextField(label="Ingrese el nombre del archivo a crear", multiline=False, bgcolor=ft.colors.WHITE,)

    def __init__(self):
        super().__init__(
            width=750, 
            height=600,
            padding=10, 
            bgcolor=ft.colors.WHITE,
            content=ft.Column([
                ft.Text("BODEGA", size=30, weight=ft.FontWeight.W_900, selectable=True), #Titulo
                ft.Container(
                    width=695,
                    height=250,
                    bgcolor="#D9D9D9",
                    border_radius=12,
                    alignment=ft.alignment.center,
                    padding=15,
                    content=ft.Column([
                        ft.Text("Consolidado a Bodega", size=20),
                        ft.Container(
                            width=680,
                            height=180,
                            border_radius=12,
                            padding=5,
                            content= self.txt_bodega
                            ),
                        ]),
                ),
                ft.Container(
                    width=695,
                    height=150,
                    bgcolor="#D9D9D9",
                    border_radius=12,
                    padding=15,
                    alignment=ft.alignment.center,
                    content=ft.Column([
                        ft.Text("Archivo Bodega", size=20),
                        ft.Container(
                            width=680,
                            height=80,
                            border_radius=12,
                            padding=5,
                            content=self.txt_nombre_archivo
                        ),
                    ]),
                ),
                ft.ElevatedButton(
                    content= ft.Container(
                        width=650,
                        height=50,
                        alignment=ft.alignment.center,
                        content=ft.Text("Generar archivo Bodega", color=ft.colors.WHITE, size=20),
                    ),
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                    bgcolor='#FF8412',
                    on_click=self.generar_bodega
                ),
            ])
        )
    def generar_bodega(self, button):
        try:
        #MODIFICACION DE RUTA
            txt_ruta = self.txt_bodega.value
            txt_ruta = txt_ruta.replace('"', '')
        #MODIFICACION DE NOMBRE ARCHIVO
            self.txt_salida = self.txt_nombre_archivo.value
        #LLAMADO A FUNCION
            self.dataFrame(txt_ruta)
            self.txt_bodega.value = ""
            self.txt_nombre_archivo.value = ""
            self.update()
        except:
            print("Error al generar archivo")
    def dataFrame(self, txt_ruta):
    #LECTURA DE ARCHIVO EN HOJA DETALLE CONSOLIDADO
        df = pd.read_excel(txt_ruta, sheet_name="Detalle Consolidado")
    #CALCULO DE COLUMNAS
        n_columnas = len(df.columns)
        n_columnas = n_columnas - 1
    #CREACION DE RUTA Y NOMBRE ARCHIVO
        ruta = os.path.dirname(txt_ruta)
        nombre = self.txt_nombre_archivo.value
        nombre_archivo = ruta + "\\" + nombre + ".xlsx"
    #EXPORTACION DE ARCHIVO
        with pd.ExcelWriter(nombre_archivo) as writer:
            for i in range(5, n_columnas):
                df_final = df[['FAMILIA','COD. PRODUCTO', 'DESCRIPCION PRODUCTO','UNIDAD',df.columns[i]]].dropna()
                df_final.to_excel(writer, sheet_name= df.columns[i], index=False)

    