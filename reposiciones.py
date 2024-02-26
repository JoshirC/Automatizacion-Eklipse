import os
import flet as ft
import pandas as pd

from  assets.modals import modal_error, modal_correcto, modal_inicial
class Reposiciones(ft.Container):
    directorio = ft.Text("")
    txt_salida = ft.Text("")
    txt_reposiciones = ft.TextField(label="Ingrese la ruta de los archivos", multiline=True, bgcolor=ft.colors.WHITE)
    txt_nombre_archivo = ft.TextField(label="Ingrese el nombre del archivo a crear", multiline=False, bgcolor=ft.colors.WHITE)
    def __init__(self):
        super().__init__(
            width=750, 
            height=600,
            padding=10, 
            content= self.create_reposiciones(modal_inicial)
        )
    def create_reposiciones(self, modal):
        return ft.Column([
            ft.Row([
                    ft.Text("REPOSICIONES", size=30, weight=ft.FontWeight.W_900, selectable=True), #Titulo
                    modal
                ],alignment =ft.MainAxisAlignment.SPACE_AROUND),
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
                    width=200,
                    height=50,
                    alignment=ft.alignment.center,
                    content=ft.Text("Generar Reposiciones", color=ft.colors.BLACK, size=15),
                ),
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                bgcolor="#FF8412",
                on_click=self.generar_reposiciones
            )
        ])
    def generar_reposiciones(self, button):
        try:
            txt_archivos = self.txt_reposiciones.value
            self.txt_salida.value = self.txt_nombre_archivo.value
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
        dfs = []
        for i in range(len(archivo)):
        #LECTURA DE ARCHIVOS EN HOJA DE PRODUCTOS
            df_reposicion = pd.read_excel(archivo[i],dtype={'COD. PRODUCTO': str} ,sheet_name="PRODUCTOS", header=4)
        #MODELADO DEL DATAFRAME
            df_reposicion = df_reposicion[['FAMILIA', 'COD. PRODUCTO', 'DESCRIPCION PRODUCTO', 'UNIDAD', 'CANTIDAD', 'CENTRO', 'FECHA']]
            dfs.append(df_reposicion)
        #NOMBRE DE LA RUTA DE ARCHIVOS
            self.directorio.value = os.path.dirname(archivo[i])

        df = pd.concat(dfs)
        print('------> LECTURA DE ARCHIVOS <------')
        self.modelado(df)

    def modelado(self, df):
    #MODELADO DE DATAFRAME REPOSICIONES
        df['FAMILIA'] = df['FAMILIA'].fillna('X')
        df['COD. PRODUCTO'] = df['COD. PRODUCTO'].fillna('X')
        df['ESTATUS'] = 'SOLICITADO'
        df['FECHA'].rename('FECHA SOLICITUD')
        df['FECHA DESPACHO'] = ''
        df['COMENTARIOS'] = pd.Series(dtype=object)
        df.dropna(subset=['CANTIDAD'], inplace=True)
        
        self.creacion_archivo(df)

    def creacion_archivo(self, df):
        ruta = self.directorio.value
        print(ruta)
        nombre = self.txt_salida.value
        print(nombre)
        nombre_archivo = ruta + '\\' + nombre + '.xlsx'

        with pd.ExcelWriter(nombre_archivo) as writer:
            df.to_excel(writer, sheet_name='REPOSICIONES', index=False)

