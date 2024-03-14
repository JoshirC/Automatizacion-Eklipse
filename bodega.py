import os
import flet as ft
import pandas as pd

from estilo_excel import aplicar_estilo_excel
from assets.modals import modal_error, modal_correcto, modal_inicial
class Bodega(ft.Container):
    """
    Clase que representa la interfaz para generar archivos de consolidado a bodega.

    Attributes:
        txt_bodega (ft.TextField): Campo de entrada para la ruta del archivo de consolidado.
        txt_nombre_archivo (ft.TextField): Campo de entrada para el nombre del archivo de salida.
    Methods:
        __init__: Constructor de la clase.
        create_bodega: Método para crear la vista de generación de archivo de consolidado a bodega.
        generar_bodega: Método para generar el archivo de consolidado a bodega.
        dataFrame: Método para crear el DataFrame de consolidado a bodega.
    """
    txt_bodega = ft.TextField(label="Ingrese la ruta del consolidado", multiline=False, bgcolor=ft.colors.WHITE)
    txt_nombre_archivo = ft.TextField(label="Ingrese el nombre del archivo a crear", multiline=False, bgcolor=ft.colors.WHITE,)

    def __init__(self):
        """
        Inicializa una instancia de la clase Bodega.

        Returns:
            None
        """
        super().__init__(
            width=750, 
            height=600,
            padding=10, 
            bgcolor=ft.colors.WHITE,
            content= self.create_bodega(modal_inicial)
        )
    def create_bodega(self, modal):
        """
        Crea la interfaz de usuario para generar archivos de consolidado a bodega.

        Args:
            modal: Modal que se muestra junto al título.

        Returns:
            ft.Column: Columna que contiene la interfaz de usuario.
        """
        return ft.Column([
            ft.Container(
                width=700,
                height=40,
                content=ft.Row([
                    ft.Text("BODEGA", size=30, weight=ft.FontWeight.W_900, selectable=True), #Titulo
                    modal
                ],alignment =ft.MainAxisAlignment.SPACE_BETWEEN),
            ),
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
                    ft.Text("Archivo Salida Bodega", size=20),
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
    def generar_bodega(self, button):
        """
        Genera el archivo de consolidado a bodega.

        Args:
            button: Botón que activa la generación del archivo.

        Returns:
            None
        """
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
            self.content = self.create_bodega(modal_correcto)
            self.update()
        except:
            self.content = self.create_bodega(modal_error)
            self.update()
    def dataFrame(self, txt_ruta):
        """
        Genera un DataFrame a partir del archivo de consolidado.

        Args:
            txt_ruta (str): Ruta del archivo de consolidado.

        Returns:
            None
        """
    #LECTURA DE ARCHIVO EN HOJA DETALLE CONSOLIDADO
        df = pd.read_excel(txt_ruta, dtype={'COD. PRODUCTO': str},sheet_name="Detalle Consolidado")
    #CALCULO DE COLUMNAS
        n_columnas = len(df.columns)
        n_columnas = n_columnas - 1
    #CREACION DE RUTA Y NOMBRE ARCHIVO
        ruta = os.path.dirname(txt_ruta)
        nombre = self.txt_nombre_archivo.value
        nombre_archivo = ruta + "\\" + nombre + ".xlsx"
    #EXPORTACION DE ARCHIVO
        with pd.ExcelWriter(nombre_archivo) as writer:
            for i in range(6, n_columnas):
                df_final = df[['FAMILIA','COD. PRODUCTO', 'DESCRIPCION PRODUCTO','UNIDAD',df.columns[i]]].dropna()
                df_final.to_excel(writer, sheet_name= df.columns[i], index=False)

        aplicar_estilo_excel(nombre_archivo)