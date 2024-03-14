import os
import flet as ft
import pandas as pd

from estilo_excel import aplicar_estilo_excel
from  assets.modals import modal_error, modal_correcto, modal_inicial
class Reposiciones(ft.Container):
    """
    Clase para la gestión de reposiciones.

    Attributes:
        directorio (ft.Text): Campo de texto para la ruta del directorio.
        txt_salida (ft.Text): Campo de texto para el nombre del archivo de salida.
        txt_reposiciones (ft.TextField): Campo de texto para la ruta de los archivos de reposiciones.
        txt_nombre_archivo (ft.TextField): Campo de texto para el nombre del archivo a crear o la ruta de un archivo existente.

    Methods:
        __init__: Constructor de la clase.
        create_reposiciones: Método para crear la vista de gestión de reposiciones.
        generar_reposiciones: Método para generar las reposiciones.
        dataFrame: Método para crear el DataFrame de reposiciones.
        modelado: Método para el modelado de los datos de reposiciones.
        creacion_archivo: Método para la creación del archivo de reposiciones.
        es_ruta: Método para verificar si el texto es una ruta de archivo existente.
        parse_fecha: Método para parsear una fecha al formato de pandas.
    """
    directorio = ft.Text("")
    txt_salida = ft.Text("")
    txt_reposiciones = ft.TextField(label="Ingrese la ruta de los archivos", multiline=True, bgcolor=ft.colors.WHITE)
    txt_nombre_archivo = ft.TextField(label="Ingrese el nombre del archivo a crear o la ruta de un archivo existente", multiline=False, bgcolor=ft.colors.WHITE)
    def __init__(self):
        """
        Constructor de la clase Reposiciones.

        Inicializa la clase con un contenedor de especificaciones predeterminadas y contenido generado por
        el método create_reposiciones, utilizando un modal inicial.
        """
        super().__init__(
            width=750, 
            height=600,
            padding=10, 
            content= self.create_reposiciones(modal_inicial)
        )
    def create_reposiciones(self, modal):
        """
        Método para crear la vista de gestión de reposiciones.

        Args:
            modal: Modal a mostrar junto con el título.

        Returns:
            ft.Column: Columna con el contenido de la vista de gestión de reposiciones.
        """
        return ft.Column([
            ft.Container(
                width=700,
                height=40,
                content=ft.Row([
                    ft.Text("REPOSICIONES", size=30, weight=ft.FontWeight.W_900, selectable=True), #Titulo
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
                    ft.Text("Modelado Reposiciones", size=20),
                    ft.Container(
                        width=680,
                        height=180,
                        border_radius=12,
                        padding=5,
                        content=self.txt_reposiciones
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
                    ft.Text("Archivo Salida Reposiciones", size=20),
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
                content=ft.Container(
                    width=650,
                    height=50,
                    alignment=ft.alignment.center,
                    content=ft.Text("Generar Reposiciones", color=ft.colors.WHITE, size=20),
                ),
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                bgcolor="#FF8412",
                on_click=self.generar_reposiciones
            )
        ])
    def generar_reposiciones(self, button):
        """
        Método para generar las reposiciones.

        Lee los archivos ingresados, crea un DataFrame consolidado y genera el archivo de salida.

        Args:
            button: Botón de generación de reposiciones.
        """
        try:
            txt_archivos = self.txt_reposiciones.value
            self.txt_salida.value = self.txt_nombre_archivo.value
            self.txt_salida.value = self.txt_salida.value.replace('"', '')
            lista_archivos = txt_archivos.splitlines()
            lista_archivos = [archivo.replace('"', '') for archivo in lista_archivos]

            self.dataFrame(lista_archivos)

            self.content = self.create_reposiciones(modal_correcto)
            self.txt_nombre_archivo.value = ""
            self.txt_reposiciones.value = ""
            self.update()
        except Exception as e:
            print(e)
            self.content = self.create_reposiciones(modal_error)
            self.update()
    
    def dataFrame(self, archivo):
        """
        Método para crear el DataFrame de reposiciones.

        Lee los archivos de reposiciones ingresados, realiza el modelado de los datos y los concatena en un DataFrame de reposiciones.

        Args:
            archivo (list): Lista de rutas de los archivos de reposiciones.
        """
        dfs = []
        for i in range(len(archivo)):
        #LECTURA DE ARCHIVOS EN HOJA DE PRODUCTOS
            df_reposicion = pd.read_excel(archivo[i],dtype={'COD. PRODUCTO': str} ,sheet_name="PRODUCTOS", header=8, date_format='%d/%m/%Y', parse_dates=['FECHA'])
        #MODELADO DEL DATAFRAME
            df_reposicion = df_reposicion[['FAMILIA', 'COD. PRODUCTO', 'DESCRIPCION PRODUCTO', 'UNIDAD', 'CANTIDAD', 'CENTRO', 'FECHA', 'OBSERVACIONES CC']]
            dfs.append(df_reposicion)
        #NOMBRE DE LA RUTA DE ARCHIVOS
            self.directorio.value = os.path.dirname(archivo[i])

        df = pd.concat(dfs)
        print('------> LECTURA DE ARCHIVOS <------')
        self.modelado(df)

    def modelado(self, df):
        """
        Método para el modelado de los datos de reposiciones.

        Realiza el modelado de los datos del DataFrame de reposiciones.

        Args:
            df (DataFrame): DataFrame de reposiciones.
        """
        #MODELADO DE DATAFRAME REPOSICIONES
        df['FAMILIA'] = df['FAMILIA'].fillna('X')
        df['COD. PRODUCTO'] = df['COD. PRODUCTO'].fillna('X')
        df['ESTATUS'] = 'SOLICITADO'
        df['FECHA'].rename('FECHA SOLICITUD')
        df['FECHA DESPACHO'] = ''
        df['COMENTARIOS'] = pd.Series(dtype=object)
        df.dropna(subset=['CANTIDAD'], inplace=True)
        df = df[df['CANTIDAD'] != 0]
        
        self.creacion_archivo(df)

    def creacion_archivo(self, df):
        """
        Método para la creación del archivo de reposiciones.

        Crea el archivo de reposiciones a partir del DataFrame de reposiciones.

        Args:
            df (DataFrame): DataFrame de reposiciones.
        """
        if df.empty:
            print("No hay datos para escribir en el archivo.")
            return

        if self.es_ruta(self.txt_salida.value):
            if os.path.exists(self.txt_salida.value):
                df_anterior = pd.read_excel(self.txt_salida.value, sheet_name='Guia de Estatus', date_format='%d/%m/%Y', parse_dates=['FECHA'])
                df = pd.concat([df_anterior, df])
            nombre_archivo = self.txt_salida.value
        else:   
            ruta = self.directorio.value
            nombre = self.txt_salida.value
            nombre_archivo = os.path.join(ruta, nombre + '.xlsx')
        with pd.ExcelWriter(nombre_archivo) as writer:
            print('------> CREACION DE ARCHIVO <------')
            df.to_excel(writer, sheet_name='Guia de Estatus', index=False)
        aplicar_estilo_excel(nombre_archivo)
    def es_ruta(self, texto):
        """
        Método para verificar si el texto es una ruta de archivo existente.

        Args:
            texto (str): Texto a verificar.

        Returns:
            bool: True si es una ruta de archivo existente, False de lo contrario.
        """
        return os.path.exists(texto) and texto.endswith('.xlsx')
    def parse_fecha(self,fecha):
        """
        Método para parsear una fecha al formato de pandas.

        Args:
            fecha (str): Fecha en formato de texto.

        Returns:
            datetime: Fecha parseada en formato de pandas.
        """
        return pd.to_datetime(fecha, format='%d/%m/%Y')
