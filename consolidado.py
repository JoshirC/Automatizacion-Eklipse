from io import StringIO
import os
import flet as ft
import pandas as pd

from estilo_excel import aplicar_estilo_excel
from assets.modals import modal_error, modal_correcto, modal_inicial
class Consolidado(ft.Container):
    """
    Clase para la creación de la vista de consolidado.

    Attributes:
        directorio (ft.Text): Campo de texto para la ruta del directorio.
        txt_salida (ft.Text): Campo de texto para el nombre del archivo de salida.
        txt_consolidado (ft.TextField): Campo de texto para la ruta de los archivos a consolidar.
        txt_nombre_archivo (ft.TextField): Campo de texto para el nombre del archivo a crear.
    Methods:
        __init__: Constructor de la clase.
        create_consolidado: Método para crear la vista de consolidado.
        txt: Método para generar el consolidado.
        dataFrame: Método para crear el DataFrame de consolidado.
        modelado: Método para el modelado de los datos.
        dataFrameEstadistico: Método para el modelado estadístico del DataFrame.
        creacion_archivo: Método para la creación del archivo de consolidado.
    """
    directorio = ft.Text("")
    txt_salida = ft.Text("")
    txt_consolidado = ft.TextField(label="Ingrese la ruta de los archivos a consolidar", multiline=True, bgcolor=ft.colors.WHITE)
    txt_nombre_archivo = ft.TextField(label="Ingrese el nombre del archivo a crear", multiline=False, bgcolor=ft.colors.WHITE,)

    def __init__(self):
        """
        Constructor de la clase Consolidado.

        Inicializa la clase con un contenedor de especificaciones predeterminadas y contenido generado por
        el método create_consolidado, utilizando un modal inicial.
        """
        super().__init__(
            width=750, 
            height=600,
            padding=10, 
            bgcolor=ft.colors.WHITE,
            content= self.create_consolidado(modal_inicial)
        )
    def create_consolidado(self, modal):
        """
        Método para crear la vista de consolidado.

        Args:
            modal: Modal a mostrar junto con el título.

        Returns:
            ft.Column: Columna con el contenido de la vista de consolidado.
        """
        return ft.Column([
            ft.Container(
                width=700,
                height=40,
                content=ft.Row([
                    ft.Text("RECTIFICACIÓN", size=30, weight=ft.FontWeight.W_900, selectable=True), #Titulo
                    modal
                ],alignment =ft.MainAxisAlignment.SPACE_BETWEEN),
            ),
            ft.Container( #Contenedor para archivo semanal
                width=695,
                height=250,
                bgcolor="#D9D9D9",
                border_radius=12,
                alignment=ft.alignment.center,
                padding=15,
                content=ft.Column([
                    ft.Text("Rectificado Semanal", size=20),
                    ft.Container( #Contenedor para mostrar archivos cargados (scroll ?)
                        width=680,
                        height=180,
                        #bgcolor=ft.colors.WHITE,
                        border_radius=12,
                        padding=5,
                        content= self.txt_consolidado
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
                    ft.Text("Archivo Salida Consolidado", size=20),
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
                        content=ft.Text("Generar Consolidado", color=ft.colors.WHITE, size=20),
                        ),
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                        bgcolor='#FF8412',
                        on_click=self.txt
                )
        ])
    def txt(self, button):
            """
            Método para generar el consolidado.

            Lee los archivos ingresados, crea un DataFrame consolidado y genera el archivo de salida.

            Args:
                button: Botón de generación de consolidado.
            """
            try:
                txt_archivos = self.txt_consolidado.value
                self.txt_salida.value = self.txt_nombre_archivo.value
                lista_archivos = txt_archivos.splitlines()
                lista_archivos = [archivo.replace('"', '') for archivo in lista_archivos]
                
                self.dataFrame(lista_archivos)
                self.txt_consolidado.value = ""
                self.txt_nombre_archivo.value = ""
                self.content = self.create_consolidado(modal_correcto)
                self.update()
            except:
                self.content = self.create_consolidado(modal_error)
                self.update()
    def dataFrame(self,archivo):
        """
        Método para crear el DataFrame de consolidado.

        Lee los archivos ingresados, realiza el modelado de los datos y los concatena en un DataFrame consolidado.

        Args:
            archivo (list): Lista de rutas de los archivos a consolidar.
        """
        dfs = []
        for i in range(len(archivo)):
        #LECTURA DE ARCHIVO EN HOJA PRODUCTOS
            df_producto = pd.read_excel(archivo[i], dtype={'COD. PRODUCTO': str}, sheet_name='PRODUCTOS')
        #MODELADO DE DATAFRAME
            df_producto = df_producto[['FAMILIA', 'COD. PRODUCTO', 'DESCRIPCION PRODUCTO', 'UNIDAD', 'RECTIFICACION','PRECIO $', 'CENTRO', 'SEMANA', 'MES', 'CODIGO']]
            df_producto['CATEGORIA'] = "PRODUCTO"
            df_producto['RECTIFICACION'].astype(float)
            df_producto = df_producto.dropna(subset=['RECTIFICACION'])
            df_producto = df_producto[df_producto['RECTIFICACION'] != 0]

            dfs.append(df_producto)
        #LECTURA DE ARCHIVO EN HOJA ESPECIALES
            df_especiales = pd.read_excel(archivo[i], dtype={'COD. PRODUCTO': str}, sheet_name='ESPECIALES')
        #MODELADO DE DATAFRAME
            df_especiales = df_especiales[['FAMILIA', 'COD. PRODUCTO', 'DESCRIPCION PRODUCTO', 'UNIDAD', 'RECTIFICACION','PRECIO $', 'CENTRO', 'SEMANA', 'MES','CODIGO']]
            df_especiales['CATEGORIA'] = "ESPECIAL"
            df_especiales['RECTIFICACION'].astype(float)
            df_especiales = df_especiales.dropna(subset=['RECTIFICACION'])
            df_especiales = df_especiales[df_especiales['RECTIFICACION'] != 0]
            dfs.append(df_especiales)

        #NOMBRE DE LA RUTA DE LOS ARCHIVOS
            self.directorio.value = os.path.dirname(archivo[i])
        df = pd.concat(dfs)
        print('------> LECTURA DE ARCHIVOS <------')
        self.modelado(df)

    def modelado(self,df):
        """
        Método para el modelado de los datos.

        Realiza el modelado de los datos del DataFrame de consolidado.

        Args:
            df (DataFrame): DataFrame de consolidado.
        """
        #VARIABLES GLOBALES

        """

        cat_1: Lista de categorías de productos secos.
        cat_2: Lista de categorías de productos congelados.
        
        """
        cat_1 = ['ABARROTES','CONFITERIA','BEBESTIBLES','DESECHABLES','EPP','FRUTAS Y VERDURAS','MATERIALES ASEO Y EPP','OTROS NON FOOD','QUÍMICOS']
        cat_2 = ['AVES','CECINAS','CERDO','LÁCTEOS Y HUEVOS''PANADERIA','PANADERÍA Y PASTELERÍA','PESCADOS Y MARISCOS','CECINAS Y EMBUTIDOS','CERDOS','VACUNO','HUEVOS Y LACTEOS','X']

        #MODELADO DE DATAFRAME
        df['FAMILIA'] = df['FAMILIA'].fillna('X')
        df['COD. PRODUCTO'] = df['COD. PRODUCTO'].fillna('X')
        df['UNIDAD'] = df['UNIDAD'].fillna('X')
        df['PRECIO $'] = df['PRECIO $'].fillna(0)
        df['SALIDA'] = "BODEGA"

        #MODELADO DE DATAFRAME PARA DETALLE ESTADISTICO
        df_data = self.dataFrameEstadistico(df)

        #TRANSFORMACION DE COLUMNAS
        df_1 = df.pivot_table(index=['FAMILIA','COD. PRODUCTO','DESCRIPCION PRODUCTO','UNIDAD','CATEGORIA','PRECIO $'],columns='CENTRO',values='RECTIFICACION').reset_index()
        df_aprobacion = df_1[df_1['CATEGORIA'] != 'PRODUCTO']
        #ORDEN DEL DATAFRAME
        df_2 = df_1.sort_values(by=['FAMILIA','DESCRIPCION PRODUCTO'])
        grupo1 = df_2[df_2['FAMILIA'].isin(cat_1)]
        grupo2 = df_2[df_2['FAMILIA'].isin(cat_2)]

        df = pd.concat([grupo1,grupo2]).reset_index(drop=True)

        grupo1 = df_aprobacion[df_aprobacion['FAMILIA'].isin(cat_1)]
        grupo2 = df_aprobacion[df_aprobacion['FAMILIA'].isin(cat_2)]

        df_aprobacion = pd.concat([grupo1,grupo2]).reset_index(drop=True)

        #VARIABLE TOTAL
        df_total = df.drop(columns=['FAMILIA','COD. PRODUCTO','DESCRIPCION PRODUCTO','UNIDAD','CATEGORIA','PRECIO $'])
        df['TOTAL'] = df_total.sum(axis=1)

        #CREACION DE ARCHIVO
        print('------> MODELADO DE ARCHIVO <------')
        self.creacion_archivo(df,df_data,df_aprobacion)
        
    def dataFrameEstadistico(self,df):
        """
        Método para crear el DataFrame estadístico de Rectificaciones.

        Args:
            df: DataFrame principal.

        Returns:
            DataFrame: DataFrame estadístico.
        """
        df = df[['SEMANA','COD. PRODUCTO', 'DESCRIPCION PRODUCTO', 'RECTIFICACION','PRECIO $', 'CENTRO','CODIGO', 'MES', 'CATEGORIA', "SALIDA"]]
        df.sort_values('DESCRIPCION PRODUCTO', inplace=True)
        df.dropna(subset=['RECTIFICACION'], inplace=True)
        print('------> MODELADO ESTADISTICO <------')
        return df
    
    def creacion_archivo(self,df,df_data,df_aprobacion):
        """
        Método para la creación del archivo de Rectificacion.

        Args:
            df: DataFrame principal.
            df_data: DataFrame estadístico.
            df_aprobacion: DataFrame de pendientes aprobación.
        """
        print('------> CREACION DE ARCHIVO <------')
        #CREACION DE RUTA Y NOMBRE DE ARCHIVO
        ruta = self.directorio.value
        nombre = self.txt_salida.value
        nombre_archivo = ruta + '\\' + nombre + '.xlsx'
        #EXPORTACION DE ARCHIVO
        with pd.ExcelWriter(nombre_archivo) as writer:
            df.to_excel(writer, sheet_name='Detalle Consolidado', index=False)
            df_aprobacion.to_excel(writer, sheet_name='Pendientes Aprobación', index=False)
            df_data.to_excel(writer, sheet_name='Modelado Estadistico', index=False)
        aplicar_estilo_excel(nombre_archivo)