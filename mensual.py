import os
import flet as ft
import pandas as pd

from estilo_excel import aplicar_estilo_excel
from assets.modals import modal_error, modal_correcto, modal_inicial

class Mensual(ft.Container):
    """
    Clase para la creación de la vista de Mensual.

    Atributes:
        directorio (ft.Text): Representa el directorio.
        txt_salida (ft.Text): Representa el texto de salida.
        txt_mensual (ft.TextField): Campo de texto para ingresar la ruta de los archivos a consolidar.
        txt_nombre_archivo (ft.TextField): Campo de texto para ingresar el nombre del archivo a crear.
    Métodos:
        __init__: Constructor de la clase.
        create_mensual: Método para crear la vista de Mensual.
        generar_mensual: Método para generar el archivo Mensual.
        dataFrame: Método para crear el DataFrame de Mensual.
        modelado: Método para el modelado de Mensual.
        creacion_archivo: Método para la creación del archivo Mensual.
    """
    directorio = ft.Text("")
    txt_salida = ft.Text("")
    txt_mensual = ft.TextField(label="Ingrese la ruta de los archivos a consolidar", multiline=True, bgcolor=ft.colors.WHITE)
    txt_nombre_archivo = ft.TextField(label="Ingrese el nombre del archivo a crear", multiline=False, bgcolor=ft.colors.WHITE)
    
    def __init__(self):
        """
        Constructor de la clase Mensual.
        Crea una instancia de Mensual con un contenido inicial.
        """
        super().__init__(
            width=750, 
            height=600,
            padding=10, 
            bgcolor=ft.colors.WHITE,
            content= self.create_mensual(modal_inicial)
        )
    
    def create_mensual(self, modal):
        """
        Método para crear la vista de Mensual.
        Args:
            modal: Modal a ser incluido en la vista.
        Returns:
            ft.Column: Contenedor de la vista Mensual.
        """
        return ft.Column([
            ft.Container(
                width=700,
                height=40,
                content=ft.Row([
                    ft.Text("MENSUAL", size=30, weight=ft.FontWeight.W_900, selectable=True), #Titulo
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
                    ft.Text("Consolidado Mensual", size=20),
                    ft.Container(
                        width=680,
                        height=180,
                        border_radius=12,
                        padding=5,
                        content= self.txt_mensual
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
                    ft.Text("Archivo Salida Mensual", size=20),
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
                    content=ft.Text("Generar Consolidado Mensual", color=ft.colors.WHITE, size=20),
                ),
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                bgcolor='#FF8412',
                on_click=self.generar_mensual
            ),
        ])
    
    def generar_mensual(self, button):
        """
            Método para generar el archivo Mensual.
            Args:
                button: Botón que activa la generación del archivo.
            Raises:
                Exception: Si ocurre algún error durante la generación del archivo.
        """
        try:
            txt_archivos = self.txt_mensual.value
            self.txt_salida.value = self.txt_nombre_archivo.value
            lista_archivos = txt_archivos.splitlines()
            lista_archivos = [archivo.replace('"', '') for archivo in lista_archivos]

            self.dataFrame(lista_archivos)
            self.txt_mensual.value = ""
            self.txt_nombre_archivo.value = ""
            self.content = self.create_mensual(modal_correcto)
            self.update()
        except:
            self.content = self.create_mensual(modal_error)
            self.update()
    
    def dataFrame(self, archivo):
        """
            Método para crear el DataFrame de Mensual.
            Args:
                archivo (list): Lista de rutas de archivos a procesar.
        """
        dfs = []
        dfx = []
        for i in range(len(archivo)):
            #LECTURA DE ARCHIVOS EN HOJA DE PRODUCTOS
            df_productos = pd.read_excel(archivo[i],dtype={'COD. PRODUCTO': str} ,sheet_name='PRODUCTOS')
            dfx.append(df_productos)
            #MODELADO DE DATAFRAME
            df_productos = df_productos[['FAMILIA', 'COD. PRODUCTO', 'DESCRIPCION PRODUCTO', 'UNIDAD',df_productos.columns[5],'PRECIO $','CENTRO','CODIGO', 'MES']]
            df_productos['SEMANA'] = df_productos[df_productos.columns[4]].name
            df_productos = df_productos.rename(columns={df_productos[df_productos.columns[4]].name: 'RECTIFICACION'})
            df_productos['RECTIFICACION'].astype(float)
            df_productos['CATEGORIA'] = "PRODUCTO"
            df_productos = df_productos.dropna(subset=['RECTIFICACION'])
            df_productos = df_productos[df_productos['RECTIFICACION'] != 0]


            dfs.append(df_productos)
            #LECTURA DE ARCHIVOS EN HOJA ESPECIALES
            df_especiales = pd.read_excel(archivo[i],dtype={'COD. PRODUCTO': str}, sheet_name='ESPECIALES')
            dfx.append(df_especiales)
            #MODELADO DE DATAFRAME
            df_especiales = df_especiales[['FAMILIA', 'COD. PRODUCTO', 'DESCRIPCION PRODUCTO', 'UNIDAD',df_especiales.columns[5],'PRECIO $', 'CENTRO','CODIGO', 'MES']]
            df_especiales['SEMANA'] = df_especiales[df_especiales.columns[4]].name
            df_especiales = df_especiales.rename(columns={df_especiales[df_especiales.columns[4]].name: 'RECTIFICACION'})
            df_especiales['RECTIFICACION'].astype(float)
            df_especiales['CATEGORIA'] = "ESPECIAL"
            df_especiales = df_especiales.dropna(subset=['RECTIFICACION'])
            df_especiales = df_especiales[df_especiales['RECTIFICACION'] != 0]
            dfs.append(df_especiales)
            #NOMBRE DE LA RUTA DE LOS ARCHIVOS
            self.directorio.value = os.path.dirname(archivo[i])
            #LECTURA DE ARCHIVO CALENDARIO
            df_calendario = pd.read_excel(archivo[i], sheet_name='PORTADA', header=15)

        df = pd.concat(dfs)
        df2 = pd.concat(dfx)
        print('------> LECTURA DE ARCHIVOS <------')
        self.modelado(df,df2, df_calendario)

    def modelado(self,df,df2,df_calendario):
        """
            Método para el modelado de Mensual.
            Args:
                df: DataFrame principal.
                df2: DataFrame secundario.
                df_calendario: DataFrame para el calendario.
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

        df2['FAMILIA'] = df2['FAMILIA'].fillna('X')
        df2['COD. PRODUCTO'] = df2['COD. PRODUCTO'].fillna('X')
        df2['UNIDAD'] = df2['UNIDAD'].fillna('X')
        df2['PRECIO $'] = df2['PRECIO $'].fillna(0)
        df['SALIDA'] = "BODEGA"

        #MODELADO DE DATAFRAME PARA DETALLE ESTADISTICO
        df_data = self.dataFrameEstadistico(df, df_calendario)
        df_data_2 = self.dataFrameCostos(df2, df_calendario)

        #TRANSFORMACION DE COLUMNAS
        df = df.pivot_table(index=['FAMILIA','COD. PRODUCTO','DESCRIPCION PRODUCTO','UNIDAD','CATEGORIA','PRECIO $'],columns='CENTRO',values='RECTIFICACION').reset_index()
        df_aprobacion = df[df['CATEGORIA'] != 'PRODUCTO'].reset_index(drop=True)

        #ORDEN DEL DATAFRAME
        df = df.sort_values(by=['FAMILIA','DESCRIPCION PRODUCTO'])
        grupo1 = df[df['FAMILIA'].isin(cat_1)]
        grupo2 = df[df['FAMILIA'].isin(cat_2)]
        df = pd.concat([grupo1,grupo2]).reset_index(drop=True)

        grupo1 = df_aprobacion[df_aprobacion['FAMILIA'].isin(cat_1)]
        grupo2 = df_aprobacion[df_aprobacion['FAMILIA'].isin(cat_2)]

        df_aprobacion = pd.concat([grupo1,grupo2]).reset_index(drop=True)

        #VARIABLE TOTAL
        df_total = df.drop(columns=['FAMILIA','COD. PRODUCTO','DESCRIPCION PRODUCTO','UNIDAD','CATEGORIA', 'PRECIO $'])
        df['TOTAL'] = df_total.sum(axis=1)

        #CREACION DE ARCHIVO
        print('------> MODELADO DE ARCHIVO <------')
        self.creacion_archivo(df,df_data, df_data_2,df_aprobacion)
    
    def dataFrameCostos(self,df,df_calendario):
        """
            Método para crear el DataFrame de costos Mensual.
            Args:
                df: DataFrame principal.
                df_calendario: DataFrame para el calendario.
        """
        df = df[['COD. PRODUCTO', 'DESCRIPCION PRODUCTO', 'Semana 1', 'Semana 2', 'Semana 3', 'Semana 4', 'Semana 5','PRECIO $' ,'CENTRO', 'CODIGO', 'MES']]
        df = df.melt(id_vars=['COD. PRODUCTO', 'DESCRIPCION PRODUCTO', 'PRECIO $', 'CENTRO', 'CODIGO', 'MES'],
             value_vars=['Semana 1', 'Semana 2', 'Semana 3', 'Semana 4', 'Semana 5'],
             var_name='SEMANA',
             value_name='CANTIDAD')
        df.dropna(subset=['CANTIDAD'], inplace=True)
        print(df)
        df = df[df['CANTIDAD'] != 0.0]
        df['PRECIO TOTAL'] = df['CANTIDAD'] * df['PRECIO $']
        df=df[['SEMANA','COD. PRODUCTO', 'DESCRIPCION PRODUCTO','CANTIDAD', 'CENTRO', 'CODIGO', 'MES', 'PRECIO $', 'PRECIO TOTAL']]
        # Crear un diccionario que mapee los valores de 'SEMANA' a las correspondientes columnas de df_calendario
        mapeo_semanas = {
        'Semana 1': df_calendario['N° Semana 1'].iloc[0],
        'Semana 2': df_calendario['N° Semana 2'].iloc[0],
        'Semana 3': df_calendario['N° Semana 3'].iloc[0],
        'Semana 4': df_calendario['N° Semana 4'].iloc[0],
        'Semana 5': df_calendario['N° Semana 5'].iloc[0]
        }

        # Mapear los valores de 'SEMANA' utilizando el diccionario
        df['SEMANA'] = df['SEMANA'].map(mapeo_semanas)

        print(df)   
        return df
    
    def dataFrameEstadistico(self,df, df_calendario):
        """
            Método para crear el DataFrame estadístico de Mensual.
            Args:
                df: DataFrame principal.
                df_calendario: DataFrame para el calendario.
        """
        df = df[['SEMANA','COD. PRODUCTO', 'DESCRIPCION PRODUCTO', 'RECTIFICACION','PRECIO $', 'CENTRO','CODIGO', 'MES', 'CATEGORIA', "SALIDA"]]
        df.sort_values('DESCRIPCION PRODUCTO', inplace=True)
        df.dropna(subset=['RECTIFICACION'], inplace=True)
        df['SEMANA'] = df_calendario['N° Semana 1'].iloc[0]
        print('------> MODELADO ESTADISTICO <------')
        return df
    
    def creacion_archivo(self,df,df_data,df_data_2,df_aprobacion):
        """
            Método para la creación del archivo Mensual.
            Args:
                df: DataFrame principal.
                df_data: DataFrame de datos.
                df_data_2: DataFrame de datos secundario.
                df_aprobacion: DataFrame de aprobación.
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
            df_data_2.to_excel(writer, sheet_name='Modelado Costos Mensual', index=False)

        # APLICACION DE ESTILO AL ARCHIVO EXCEL DE LA CLASE ESTILO_EXCEL
        aplicar_estilo_excel(nombre_archivo)