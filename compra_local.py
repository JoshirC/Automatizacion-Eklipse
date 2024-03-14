import os
import flet as ft
import pandas as pd

from estilo_excel import aplicar_estilo_excel
from  assets.modals import modal_error, modal_correcto, modal_inicial

class CompraLocal(ft.Container):
    """
    Clase para la creación de la vista de Compra Local.

    Attributes:
        directorio (ft.Text): Directorio de archivos.
        txt_salida (ft.Text): Texto de salida.
        txt_compra_local (ft.TextField): Campo de texto para ingresar la ruta de los archivos a consolidar.
        txt_nombre_archivo (ft.TextField): Campo de texto para ingresar el nombre del archivo a crear.
    Methods:
        __init__: Constructor de la clase.
        create_compra_local: Método para crear la vista de Compra Local.
        txt: Método para generar el consolidado.
        dataFrame: Método para crear el DataFrame de consolidado.
        modelado: Método para el modelado de los datos.
        creacion_archivo: Método para la creación del archivo de consolidado.
    """
    directorio = ft.Text("")
    txt_salida = ft.Text("")
    txt_compra_local = ft.TextField(label="Ingrese la ruta de los archivos a consolidar", multiline=True, bgcolor=ft.colors.WHITE)
    txt_nombre_archivo = ft.TextField(label="Ingrese el nombre del archivo a crear", multiline=False, bgcolor=ft.colors.WHITE) 
    
    def __init__(self):
        """
        Constructor de la clase CompraLocal.

        Crea una instancia de CompraLocal con un contenido inicial.
        """
        super().__init__(
            width=750, 
            height=600,
            padding=10, 
            bgcolor=ft.colors.WHITE,
            content=self.create_compra_local(modal_inicial)
        )
    
    def create_compra_local(self, modal):
        """
        Método para crear la vista de Compra Local.

        Args:
            modal: Modal a ser incluido en la vista.

        Returns:
            ft.Column: Contenedor de la vista Compra Local.
        """
        return ft.Column([
            ft.Container(
                width=700,
                height=40,
                content=ft.Row([
                    ft.Text("COMPRA LOCAL", size=30, weight=ft.FontWeight.W_900, selectable=True), #Titulo
                    modal
                ],alignment =ft.MainAxisAlignment.SPACE_BETWEEN),
            ),
            ft.Container( #Contenedor para archivo compra local
                width=695,
                height=250,
                bgcolor="#D9D9D9",
                border_radius=12,
                alignment=ft.alignment.center,
                padding=15,
                content=ft.Column([
                    ft.Text("Consolidado Compra Local", size=20),
                    ft.Container( #Contenedor para mostrar archivos cargados (scroll ?)
                        width=680,
                        height=180,
                        #bgcolor=ft.colors.WHITE,
                        border_radius=12,
                        padding=5,
                        content= self.txt_compra_local
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
                    ft.Text("Archivo Salida Compra Local", size=20),
                    ft.Container(
                        width=680,
                        height=80,
                        border_radius=12,
                        padding=5,
                        content=self.txt_nombre_archivo
                    ),
                ]),
            ),
            ft.ElevatedButton( #Boton para generar el consolidado
                content= ft.Container(
                    width=650,
                    height=50,
                    alignment=ft.alignment.center,
                    content=ft.Text("Generar Consolidado Compra Local", color=ft.colors.WHITE, size=20),
                ),
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                bgcolor="#FF8412",
                on_click=self.generar_compra_local
            )
        ])
    
    def generar_compra_local(self, button):
        """
        Método para generar el archivo de Compra Local.

        Args:
            button: Botón que activa la generación del archivo.

        Raises:
            Exception: Si ocurre algún error durante la generación del archivo.
        """
        try:
            txt_archivos = self.txt_compra_local.value
            self.txt_salida.value = self.txt_nombre_archivo.value
            lista_archivos = txt_archivos.splitlines()
            lista_archivos = [archivo.replace('"', '') for archivo in lista_archivos]

            self.dataFrame(lista_archivos)

            self.content = self.create_compra_local(modal_correcto)
            self.txt_compra_local.value = ""
            self.txt_nombre_archivo.value = ""
            self.update()
        except Exception as e:
            self.content = self.create_compra_local(modal_error)
            self.update()
    
    def dataFrame(self, archivo):
        """
        Método para crear el DataFrame de Compra Local.

        Args:
            archivo (list): Lista de rutas de archivos a procesar.
        """
        dfs = []
        name_centros = []
        
        for i in range(len(archivo)):
            # LECTURA DE ARCHIVO EN HOJA DE PRODUCTOS
            df_producto = pd.read_excel(archivo[i],dtype={'COD. PRODUCTO': str}, sheet_name='PRODUCTOS')
        
            # MODELADO DE DATAFRAME
            df_producto = df_producto[['FAMILIA', 'COD. PRODUCTO', 'DESCRIPCION PRODUCTO', 'UNIDAD', 'PRECIO $', 'Lu', 'Ma', 'Mi', 'Ju', 'Vi', 'Sa', 'CANT. TOTAL', 'CENTRO', 'CODIGO', 'SEMANA','MES']]
            df_producto['FAMILIA'] = df_producto['FAMILIA'].fillna('X')
            df_producto['COD. PRODUCTO'] = df_producto['COD. PRODUCTO'].fillna('X')
            df_producto['UNIDAD'] = df_producto['UNIDAD'].fillna('X')
            df_producto['PRECIO $'] = df_producto['PRECIO $'].fillna(0)
            df_producto['CAN. TOTAL'] = df_producto['CANT. TOTAL'].astype(float)
            df_producto = df_producto[df_producto['CANT. TOTAL'] != 0]

            # CAPTURA DE CENTROS
            unico_centro = df_producto['CENTRO'].unique()
            valor = ', '.join(unico_centro)
            name_centros.append(valor)

            # AGRUPACION DE DATAFRAME
            dfs.append(df_producto)

            # NOMBRE DE LA RUTA DE ARCHIVOS
            self.directorio.value = os.path.dirname(archivo[i])

        # CONCATENACION DE DATAFRAMES 
        df = pd.concat(dfs)
        print('------> LECTURA DE ARCHIVOS <------')
        self.modelado(df, name_centros)

    def modelado(self, df, name_centros):
        """
        Método para el modelado de Compra Local.

        Args:
            df: DataFrame principal.
            name_centros (list): Lista de nombres de centros.
        """
        centros = [] 
        df_compra_local = df.sort_values(by=['FAMILIA', 'DESCRIPCION PRODUCTO'])

        # MODELADO ESTADISTICO
        df_estadistico = df_compra_local[['SEMANA','COD. PRODUCTO', 'DESCRIPCION PRODUCTO','CANT. TOTAL', 'CENTRO', 'CODIGO', 'MES']]
        df_estadistico = df_estadistico.rename(columns={'CANT. TOTAL': 'RECTIFICACION'})
        df_estadistico['CATEGORIA'] = "PRODUCTOS CL"
        df_estadistico['SALIDA'] = "LOCAL"

        df_estadistico = self.dataFrameEstadistico(df_estadistico)

        # AGRUPACION POR CENTRO
        for i in range(len(name_centros)):
            df_centro = df_compra_local[df_compra_local['CENTRO'] == name_centros[i]]
            df_centro = df_centro[['FAMILIA', 'COD. PRODUCTO', 'DESCRIPCION PRODUCTO', 'UNIDAD', 'Lu', 'Ma', 'Mi', 'Ju', 'Vi', 'Sa', 'CANT. TOTAL']]
            centros.append(df_centro)
        print('------> MODELADO DE ARCHIVO <------')
        self.creacion_archivo(df_estadistico, centros, name_centros)

    def dataFrameEstadistico(self, df):
        """
        Método para crear el DataFrame estadístico de Compra Local.

        Args:
            df: DataFrame principal.

        Returns:
            DataFrame: DataFrame estadístico.
        """
        df = df[['SEMANA','COD. PRODUCTO', 'DESCRIPCION PRODUCTO', 'RECTIFICACION', 'CENTRO', 'CODIGO', 'MES', 'CATEGORIA', "SALIDA"]]
        df.sort_values('DESCRIPCION PRODUCTO', inplace=True)
        df.dropna(subset=['RECTIFICACION'], inplace=True)
        print('------> MODELADO ESTADISTICO <------')
        return df
    
    def creacion_archivo(self, df_estadistico, centros, name_centro):
        """
        Método para la creación del archivo de Compra Local.

        Args:
            df_estadistico: DataFrame estadístico.
            centros (list): Lista de DataFrames de centros.
            name_centro (list): Lista de nombres de centros.
        """
        print('------> CREACION DE ARCHIVO <------')

        # CREACION DE RUTA Y NOMBRE ARCHIVO
        ruta = self.directorio.value
        nombre = self.txt_salida.value
        nombre_archivo = ruta + '\\' + nombre + '.xlsx'

        # EXPORTACION DE ARCHIVO
        with pd.ExcelWriter(nombre_archivo) as writer:
            df_estadistico.to_excel(writer, sheet_name='Modelado Estadistico', index=False)
            for i in range(len(centros)):
                centros[i].to_excel(writer, sheet_name=name_centro[i], index=False)

        # APLICACION DE ESTILO SEGUN LA CLASE ESTILO_EXCEL
        aplicar_estilo_excel(nombre_archivo)