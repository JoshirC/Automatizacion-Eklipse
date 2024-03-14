import os
import flet as ft
import pandas as pd

from estilo_excel import aplicar_estilo_excel
from assets.modals import modal_error, modal_correcto, modal_inicial

class Unificar(ft.Container):
    """
    Clase que representa la interfaz para unificar archivos consolidados y de compra local.

    Attributes:
        directorio (ft.Text): Campo de texto para almacenar la ruta del directorio.
        txt_salida (ft.Text): Campo de texto para el nombre del archivo de salida.
        txt_consolidado (ft.TextField): Campo de entrada para la ruta de los archivos consolidados.
        txt_compra_local (ft.TextField): Campo de entrada para la ruta de los archivos de compra local.
        txt_nombre_archivo (ft.TextField): Campo de entrada para el nombre del archivo de salida o la ruta de un archivo existente.
    Methods:
        __init__: Constructor de la clase.
        create_unificar: Método para crear la vista de unificación de archivos.
        unificar: Método para unificar los archivos consolidados y de compra local.
        dataFrame: Método para crear DataFrames a partir de los archivos consolidados y de compra local.
        creacion_archivo: Método para crear un archivo con los DataFrames unificados.
        es_ruta: Método para verificar si el texto es una ruta existente.
    """
    directorio = ft.Text("")
    txt_salida = ft.Text("")
    txt_consolidado = ft.TextField(label="Ingrese la ruta de los archivos consolidados", multiline=True, bgcolor=ft.colors.WHITE)
    txt_compra_local = ft.TextField(label="Ingrese la ruta de los archivos de compra local", multiline=True, bgcolor=ft.colors.WHITE)
    txt_nombre_archivo = ft.TextField(label="Ingrese el nombre del archivo a crear o la ruta de un archivo existente", multiline=False, bgcolor=ft.colors.WHITE)
    def __init__(self):
        """
        Inicializa una instancia de la clase Unificar.

        Returns:
            None
        """
        super().__init__(
            width=750, 
            height=600,
            padding=10,
            bgcolor=ft.colors.WHITE,
            content= self.create_unificar(modal_inicial)
        )
    def create_unificar(self, modal):
         """
        Crea la interfaz de usuario para unificar archivos consolidados y de compra local.

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
                     ft.Text("UNIFICAR", size=30, weight=ft.FontWeight.W_900), #Titulo
                     modal
                 ],alignment =ft.MainAxisAlignment.SPACE_BETWEEN),
             ),
             ft.Container(
                    width=695,
                    height=130,
                    bgcolor="#ee440f",
                    border_radius=12,
                    alignment=ft.alignment.center,
                    padding=15,
                    content=ft.Column([
                        ft.Text("Unificar Archivos Consolidado", size=15, color=ft.colors.WHITE),
                        ft.Container(
                            width=680,
                            height=100,
                            border_radius=12,
                            padding=5,
                            content= self.txt_consolidado
                            ),
                        ]),
             ),
             ft.Container(
                    width=695,
                    height=130,
                    bgcolor="#ee440f",
                    border_radius=12,
                    alignment=ft.alignment.center,
                    padding=15,
                    content=ft.Column([
                        ft.Text("Unificar Archivos Compra Local", size=15, color=ft.colors.WHITE),
                        ft.Container(
                            width=680,
                            height=100,
                            border_radius=12,
                            padding=5,
                            content= self.txt_compra_local
                            ),
                        ]),
             ),
             ft.Container(
                    width=695,
                    height=130,
                    bgcolor="#ee440f",
                    border_radius=12,
                    alignment=ft.alignment.center,
                    padding=15,
                    content=ft.Column([
                        ft.Text("Archivo de Salida", size=15, color=ft.colors.WHITE),
                        ft.Container(
                            width=680,
                            height=100,
                            border_radius=12,
                            padding=5,
                            content= self.txt_nombre_archivo
                            ),
                        ]),
             ),
             ft.ElevatedButton(
                content= ft.Container(
                    width=650,
                    height=50,
                    alignment=ft.alignment.center,
                    content=ft.Text("Unificar Consolidados", color=ft.colors.WHITE, size=20),
                ),
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                bgcolor='#FF8412',
                on_click=self.unificar
            ),
         ])
    def unificar(self, button):
        """
        Unifica los archivos consolidados y de compra local.

        Args:
            button: Botón que activa la unificación de los archivos.

        Returns:
            None
        """
        try:
            txt_archivos_consolidados = self.txt_consolidado.value
            txt_archivos_compra_local = self.txt_compra_local.value
            self.txt_salida.value = self.txt_nombre_archivo.value
            self.txt_salida.value = self.txt_salida.value.replace('"', '')
            lista_archivos_consolidados = txt_archivos_consolidados.splitlines()
            lista_archivos_consolidados = [archivo.replace('"', '') for archivo in lista_archivos_consolidados]
            lista_archivos_compra_local = txt_archivos_compra_local.splitlines()
            lista_archivos_compra_local = [archivo.replace('"', '') for archivo in lista_archivos_compra_local]

            self.dataFrame(lista_archivos_consolidados, lista_archivos_compra_local)
            self.txt_consolidado.value = ""
            self.txt_compra_local.value = ""
            self.txt_nombre_archivo.value = ""
            self.content = self.create_unificar(modal_correcto)
            self.update()
        except:
            self.content = self.create_unificar(modal_error)
            self.update()

    def dataFrame(self, archivo_consolidado, archivo_compra_local):
        """
        Crea DataFrames a partir de los archivos consolidados y de compra local.

        Args:
            archivo_consolidado (list): Lista de rutas de archivos consolidados.
            archivo_compra_local (list): Lista de rutas de archivos de compra local.

        Returns:
            None
        """
        dfc = []
        dfcl = []
        if len(archivo_consolidado) != 0:
            for i in range(len(archivo_consolidado)):
                df = pd.read_excel(archivo_consolidado[i],dtype={'COD. PRODUCTO': str}, sheet_name='Modelado Estadistico')
                dfc.append(df)
                self.directorio.value = os.path.dirname(archivo_consolidado[i]) 
            df_consolidado = pd.concat(dfc)               
        else:
            df_consolidado = pd.DataFrame()
        if len(archivo_compra_local) != 0:
            for i in range(len(archivo_compra_local)):
                df = pd.read_excel(archivo_compra_local[i],dtype={'COD. PRODUCTO': str}, sheet_name='Modelado Estadistico')
                dfcl.append(df)
                self.directorio.value = os.path.dirname(archivo_compra_local[i])
            df_compra_local = pd.concat(dfcl)
        else:
            df_compra_local = pd.DataFrame()
        
        self.creacion_archivo(df_consolidado, df_compra_local)

    def creacion_archivo(self, df_consolidado, df_compra_local):
        """
        Crea un archivo con los DataFrames unificados.

        Args:
            df_consolidado (pd.DataFrame): DataFrame de los archivos consolidados.
            df_compra_local (pd.DataFrame): DataFrame de los archivos de compra local.

        Returns:
            None
        """
        if self.es_ruta(self.txt_salida.value):
            df_co = pd.read_excel(self.txt_salida.value,dtype={'COD. PRODUCTO': str}, sheet_name='MD Bodega')
            df_cl = pd.read_excel(self.txt_salida.value,dtype={'COD. PRODUCTO': str}, sheet_name='MD Compra Local')
            df_co = df_co[df_co['RECTIFICADO'] != 0]
            df_cl = df_cl[df_cl['RECTIFICADO'] != 0]

            df_consolidado = pd.concat([df_co, df_consolidado])
            df_compra_local = pd.concat([df_cl, df_compra_local])

            nombre_archivo = self.txt_salida.value
        else:
            ruta = self.directorio.value
            nombre = self.txt_salida.value
            nombre_archivo = ruta + '\\' + nombre + '.xlsx'

        with pd.ExcelWriter(nombre_archivo) as writer:
            df_consolidado.to_excel(writer, sheet_name='MD Bodega', index=False)
            df_compra_local.to_excel(writer, sheet_name='MD Compra Local', index=False)

        aplicar_estilo_excel(nombre_archivo)
    def es_ruta(self,texto):
        """
        Verifica si el texto es una ruta existente.

        Args:
            texto (str): Texto que se va a verificar como ruta.

        Returns:
            bool: True si el texto es una ruta existente, False en caso contrario.
        """
        return os.path.exists(texto)
