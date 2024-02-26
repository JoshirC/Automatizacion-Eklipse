import os
import flet as ft
import pandas as pd
from assets.modals import modal_error, modal_correcto, modal_inicial

class Mensual(ft.Container):
    directorio = ft.Text("")
    txt_salida = ft.Text("")
    txt_mensual = ft.TextField(label="Ingrese la ruta de los archivos", multiline=True, bgcolor=ft.colors.WHITE)
    txt_nombre_archivo = ft.TextField(label="Ingrese el nombre del archivo a crear", multiline=False, bgcolor=ft.colors.WHITE)
    def __init__(self):
        super().__init__(
            width=750, 
            height=600,
            padding=10, 
            bgcolor=ft.colors.WHITE,
            content= self.create_mensual(modal_inicial)
        )
    def create_mensual(self, modal):
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
        dfs = []
        for i in range(len(archivo)):
        #LECTURA DE ARCHIVOS EN HOJA DE PRODUCTOS
            df_productos = pd.read_excel(archivo[i],dtype={'COD. PRODUCTO': str} ,sheet_name='PRODUCTOS')
        #MODELADO DE DATAFRAME
            df_productos = df_productos[['FAMILIA', 'COD. PRODUCTO', 'DESCRIPCION PRODUCTO', 'UNIDAD',df_productos.columns[5], 'CENTRO', 'MES']]
            df_productos['SEMANA'] = df_productos[df_productos.columns[4]].name
            df_productos = df_productos.rename(columns={df_productos[df_productos.columns[4]].name: 'RECTIFICACION'})
            df_productos['RECTIFICACION'].astype(float)
            df_productos['CATEGORIA'] = "PRODUCTO"
            df_productos = df_productos.dropna(subset=['RECTIFICACION'])

            dfs.append(df_productos)
        #LECTURA DE ARCHIVOS EN HOJA ESPECIALES
            df_especiales = pd.read_excel(archivo[i],dtype={'COD. PRODUCTO': str}, sheet_name='ESPECIALES')
        #MODELADO DE DATAFRAME
            df_especiales = df_especiales[['FAMILIA', 'COD. PRODUCTO', 'DESCRIPCION PRODUCTO', 'UNIDAD',df_especiales.columns[5], 'CENTRO', 'MES']]
            df_especiales['SEMANA'] = df_especiales[df_especiales.columns[4]].name
            df_especiales = df_especiales.rename(columns={df_especiales[df_especiales.columns[4]].name: 'RECTIFICACION'})
            df_especiales['RECTIFICACION'].astype(float)
            df_especiales['CATEGORIA'] = "ESPECIAL"
            df_especiales = df_especiales.dropna(subset=['RECTIFICACION'])
            dfs.append(df_especiales)
        #NOMBRE DE LA RUTA DE LOS ARCHIVOS
            self.directorio.value = os.path.dirname(archivo[i])
        df = pd.concat(dfs)
        print('------> LECTURA DE ARCHIVOS <------')
        self.modelado(df)

    def modelado(self,df):
    #VARIABLES GLOBALES
        cat_1 = ['ABARROTES','BEBESTIBLES', 'CONFITERIA', 'DESECHABLES', 'EPP', 'MATERIALES DE LIMPIEZA', 'ART ESCRITORIO', 'ART KIOSCO']
        cat_2 = ['AVES', 'CECINAS','CERDO','FRIZADOS', 'FRUTA Y VERDURA', 'HUEVOS Y LACTEOS', 'PANADERIA', 'PESCADOS Y MARISCOS','VACUNO','PRE-ELABORADOS','PLATOS PREPARADOS','X']

    #MODELADO DE DATAFRAME
        df['FAMILIA'] = df['FAMILIA'].fillna('X')
        df['COD. PRODUCTO'] = df['COD. PRODUCTO'].fillna('X')
        df['SALIDA'] = "BODEGA"

    #MODELADO DE DATAFRAME PARA DETALLE ESTADISTICO
        df_data = self.dataFrameEstadistico(df)

    #TRANSFORMACION DE COLUMNAS
        df = df.pivot_table(index=['FAMILIA','COD. PRODUCTO','DESCRIPCION PRODUCTO','UNIDAD','CATEGORIA'],columns='CENTRO',values='RECTIFICACION').reset_index()
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
        df_total = df.drop(columns=['FAMILIA','COD. PRODUCTO','DESCRIPCION PRODUCTO','UNIDAD','CATEGORIA'])
        df['TOTAL'] = df_total.sum(axis=1)

    #CREACION DE ARCHIVO
        print('------> MODELADO DE ARCHIVO <------')
        self.creacion_archivo(df,df_data,df_aprobacion)
        
    def dataFrameEstadistico(self,df):
        df = df[['SEMANA','COD. PRODUCTO', 'DESCRIPCION PRODUCTO', 'RECTIFICACION', 'CENTRO', 'MES', 'CATEGORIA', "SALIDA"]]
        df.sort_values('DESCRIPCION PRODUCTO', inplace=True)
        df.dropna(subset=['RECTIFICACION'], inplace=True)
        print('------> MODELADO ESTADISTICO <------')
        return df
    
    def creacion_archivo(self,df,df_data,df_aprobacion):
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
