import pandas as pd
import os

#VARIABLES GLOBALES

cat_1 = ['ABARROTES','BEBESTIBLES', 'CONFITERIA', 'DESECHABLES', 'EPP', 'MATERIALES DE LIMPIEZA', 'ART ESCRITORIO', 'ART KIOSCO']
cat_2 = ['AVES', 'CECINAS','CERDO ','FRIZADOS', 'FRUTA Y VERDURA', 'HUEVOS Y LACTEOS', 'PANADERIA', 'PESCADOS Y MARISCOS','VACUNO','PRE-ELABORADOS','PLATOS PREPARADOS','X']

#FUNCIONES

def data_frame(df, dcl):
    dlc = dcl[['SEMANA','COD. PRODUCTO', 'DESCRIPCION PRODUCTO','CANT. TOTAL', 'CENTRO', 'MES']]
    dlc = dlc.rename(columns={'CANT. TOTAL': 'RECTIFICACION'})
    df = df[['SEMANA','COD. PRODUCTO', 'DESCRIPCION PRODUCTO', 'RECTIFICACION', 'CENTRO', 'MES']]
    df = pd.concat([df,dlc])
    df.sort_values('DESCRIPCION PRODUCTO', inplace=True)
    df.dropna(subset=['RECTIFICACION'], inplace=True)
    
    return df
def compra_local():
    archivos = ["C:\\Users\\joshi\\Desktop\\EKLIPSE\\Consolidado\\Planillas\\Consolidado3\\Compra local COLBUN.xlsx", "C:\\Users\\joshi\\Desktop\\EKLIPSE\\Consolidado\\Planillas\\Consolidado3\\Compra local INCA.xlsx", "C:\\Users\\joshi\\Desktop\\EKLIPSE\\Consolidado\\Planillas\\Consolidado3\\Compra local LUCES.xlsx", "C:\\Users\\joshi\\Desktop\\EKLIPSE\\Consolidado\\Planillas\\Consolidado3\\Compra local PUCOBRE.xlsx","C:\\Users\\joshi\\Desktop\\EKLIPSE\\Consolidado\\Planillas\\Consolidado3\\Compra local RIO BLANCO.xlsx", "C:\\Users\\joshi\\Desktop\\EKLIPSE\\Consolidado\\Planillas\\Consolidado3\\Compra local ROCAS.xlsx" ]
    centros = []
    name_centro = []
    dfs = []
    for archivo in archivos:
        df = pd.read_excel(archivo,dtype={'COD. PRODUCTO': str}, sheet_name='PRODUCTOS')
        df = df[['FAMILIA', 'COD. PRODUCTO', 'DESCRIPCION PRODUCTO', 'UNIDAD', 'Lu', 'Ma', 'Mi', 'Ju', 'Vi', 'Sa', 'CANT. TOTAL', 'CENTRO', 'SEMANA','MES']]
        df['FAMILIA'] = df['FAMILIA'].fillna('X')
        df['COD. PRODUCTO'] = df['COD. PRODUCTO'].fillna('X')
        df['CANT. TOTAL'].astype(float)
        df = df[df['CANT. TOTAL'] != 0]
        df.dropna(subset=['CANT. TOTAL'], inplace=True)
        
        dfs.append(df)

        unico = df['CENTRO'].unique()
        valores_sin_corchetes = ', '.join(unico)
        name_centro.append(valores_sin_corchetes)

    dlc = pd.concat(dfs)
    dff = dlc.sort_values(by=['FAMILIA','DESCRIPCION PRODUCTO'])
    for i in range(len(name_centro)):
        dc = dff[dff['CENTRO'] == name_centro[i]]
        dc = dc[['FAMILIA', 'COD. PRODUCTO', 'DESCRIPCION PRODUCTO', 'UNIDAD', 'Lu', 'Ma', 'Mi', 'Ju', 'Vi', 'Sa', 'CANT. TOTAL']]
        centros.append(dc)
    return centros, name_centro, dlc
def bodega(df_final,name_centro):
    centros = []
    for i in range(len(name_centro)):
        dc = df_final[['FAMILIA','COD. PRODUCTO', 'DESCRIPCION PRODUCTO','UNIDAD','CATEGORIA',name_centro[i]]].dropna()
        dc = dc[dc[name_centro[i]] != 0]
        if name_centro[i] != 'TOLOLO' and name_centro[i] != 'PACHON':
            dc = dc[dc['FAMILIA'] != 'FRUTA Y VERDURA']
        centros.append(dc)
    
    with pd.ExcelWriter("C:\\Users\\joshi\\Desktop\\EKLIPSE\\Consolidado\\Planillas\\Consolidado3\\0_BODEGA.xlsx") as writer:
        for i in range(len(centros)):
            centros[i].to_excel(writer, sheet_name=name_centro[i], index=False)
    print("---> Archivo de BODEGA creado.")
def modelado(df, centros, name_centro, n_centros, dlc):
    df['FAMILIA'] = df['FAMILIA'].fillna('X')
    df['COD. PRODUCTO'] = df['COD. PRODUCTO'].fillna('X') 
    d_data = data_frame(df, dlc)
    df = df.pivot_table(index=['FAMILIA','COD. PRODUCTO','DESCRIPCION PRODUCTO','UNIDAD','CATEGORIA'],columns='CENTRO',values='RECTIFICACION').reset_index()
    s_a = df[df['CATEGORIA'] != 'PRODUCTOS'].reset_index(drop=True)

    df = df.sort_values(by=['FAMILIA','DESCRIPCION PRODUCTO'])
    g1 = df[df['FAMILIA'].isin(cat_1)]
    g2 = df[df['FAMILIA'].isin(cat_2)]
    df = pd.concat([g1,g2]).reset_index(drop=True)

    g1 = s_a[s_a['FAMILIA'].isin(cat_1)]
    g2 = s_a[s_a['FAMILIA'].isin(cat_2)]

    s_a = pd.concat([g1,g2]).reset_index(drop=True)

    df['TOTAL'] = df.sum(axis=1)
    with pd.ExcelWriter("C:\\Users\\joshi\\Desktop\\EKLIPSE\\Consolidado\\Planillas\\Consolidado3\\0_CONSOLIDADO.xlsx") as writer:    
        df.to_excel(writer, sheet_name='Detalle Consolidado', index=False)
        s_a.to_excel(writer, sheet_name='Pendientes Aprobacion', index=False)
        d_data.to_excel(writer, sheet_name='Modelado Estadistico', index=False)
        for i in range(len(centros)):
            centros[i].to_excel(writer, sheet_name=('C.L '+name_centro[i]), index=False)
    print("---> Archivo de CONSOLIDADO creado.")
    bodega(df, n_centros)

def modelado_semanal(df, Tipo_Categoria): 
    df = df[['FAMILIA', 'COD. PRODUCTO', 'DESCRIPCION PRODUCTO', 'UNIDAD', 'RECTIFICACION', 'CENTRO', 'SEMANA', 'MES']]
    df.dropna(subset=['RECTIFICACION'], inplace=True) 
    df['RECTIFICACION'].astype(float)
    df = df[df['RECTIFICACION'] != 0]
    df['CATEGORIA'] = Tipo_Categoria
    return df

def modelado_mensual(df, Tipo_Categoria):
    df = df[['FAMILIA', 'COD. PRODUCTO', 'DESCRIPCION PRODUCTO', 'UNIDAD',df.columns[5], 'CENTRO', 'MES']]
    df['SEMANA'] = df[df.columns[4]].name
    df = df.rename(columns={df[df.columns[4]].name: 'RECTIFICACION'})
    df.dropna(subset=['RECTIFICACION'], inplace=True) 
    df['RECTIFICACION'].astype(float)
    df = df[df['RECTIFICACION'] != 0]
    df['CATEGORIA'] = Tipo_Categoria
    return df
'''    
def exportar(df):
    print("----- EXPORTANDO DATOS -----")
    try:
        print("Ingrese la ruta de la carpeta a guardar el archivo: ")
        ruta = input()
        print("Ingrese el nombre del archivo: ")
        nombre = input() + ".xlsx"
        archivo = os.path.join(ruta, nombre)
        with pd.ExcelWriter(archivo) as writer:
            df.to_excel(writer, sheet_name='CONSOLIDADO', index=False)
        print("---> Archivo exportado exitosamente.")
    except Exception as e:
        print("---> Ocurrió un error al exportar el archivo:", str(e))

def buscar_archivo():
    dfs = ["C:\\Users\\joshi\\Desktop\\EKLIPSE\\Consolidado\\Planillas\\Consolidado3\\Solicitud semanal COLBUN.xlsx","C:\\Users\\joshi\\Desktop\\EKLIPSE\\Consolidado\\Planillas\\Consolidado3\\Solicitud semanal INCA.xlsx", "C:\\Users\\joshi\\Desktop\\EKLIPSE\\Consolidado\\Planillas\\Consolidado3\\Solicitud semanal LUCES.xlsx","C:\\Users\\joshi\\Desktop\\EKLIPSE\\Consolidado\\Planillas\\Consolidado3\\Solicitud semanal PACHON.xlsx", "C:\\Users\\joshi\\Desktop\\EKLIPSE\\Consolidado\\Planillas\\Consolidado3\\Solicitud semanal PUCOBRE.xlsx", "C:\\Users\\joshi\\Desktop\\EKLIPSE\\Consolidado\\Planillas\\Consolidado3\\Solicitud semanal RIO BLANCO.xlsx", "C:\\Users\\joshi\\Desktop\\EKLIPSE\\Consolidado\\Planillas\\Consolidado3\\Solicitud semanal ROCAS.xlsx", "C:\\Users\\joshi\\Desktop\\EKLIPSE\\Consolidado\\Planillas\\Consolidado3\\Solicitud semanal TOLOLO.xlsx" ]
    dfs = []
    print("----- CARGAR ARCHIVO -----")
    print("Ingrese la cantidad de archivos a cargar: ")
    cantidad = int(input())
    for i in range(cantidad):
        print("Ingrese la ruta del archivo Excel: ")
        ruta = input()
        try:
            dfs.append(ruta)
            print("---> Archivo cargado exitosamente.")
        except FileNotFoundError:
            print("---> No se encontró el archivo.")
            return None
        except Exception as e:
            print("---> Ocurrió un error al cargar el archivo:", str(e))
            return None
    return dfs
'''
def menu():
    while True:
        print("----- MENÚ ------\n1.Consolidado Mensual\n2.Consolidado Semanal\n3.Reposiciones\n4.Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            n_centros = []
            dfs = []
            df = ["C:\\Users\\joshi\\Desktop\\EKLIPSE\\Consolidado\\Planillas\\Consolidado3\\Solicitud mensual LUCES.xlsx"]
            print("----- % MODELANDO DATOS % -----")
            for archivo in df:
                try:
                    df_producto = pd.read_excel(archivo,dtype={'COD. PRODUCTO': str}, sheet_name='PRODUCTOS')
                    df_producto = modelado_mensual(df_producto, 'PRODUCTOS')
                    dfs.append(df_producto)

                    df_especial = pd.read_excel(archivo,dtype={'COD. PRODUCTO': str}, sheet_name='ESPECIALES')
                    df_especial = modelado_mensual(df_especial, 'ESPECIALES')
                    dfs.append(df_especial)

                    unico_centro = df_producto['CENTRO'].unique()
                    print(unico_centro)
                    valores_sin_corchetes = ', '.join(unico_centro)
                    print(valores_sin_corchetes)
                    n_centros.append(valores_sin_corchetes)
                    print(n_centros)

                    print("---> Datos modelados exitosamente.")
                except Exception as e:
                    print("---> Ocurrió un error al leer el archivo:", str(e))
                
            df_final = pd.concat(dfs)
            centros, name_centro, dlc = compra_local()
            modelado(df_final, centros, name_centro, n_centros, dlc)  
        
        elif opcion == "2":
            n_centros = []
            dfs = []
            df = ["C:\\Users\\joshi\\Desktop\\EKLIPSE\\Consolidado\\Planillas\\Consolidado3\\Solicitud semanal COLBUN.xlsx","C:\\Users\\joshi\\Desktop\\EKLIPSE\\Consolidado\\Planillas\\Consolidado3\\Solicitud semanal INCA.xlsx", "C:\\Users\\joshi\\Desktop\\EKLIPSE\\Consolidado\\Planillas\\Consolidado3\\Solicitud semanal LUCES.xlsx","C:\\Users\\joshi\\Desktop\\EKLIPSE\\Consolidado\\Planillas\\Consolidado3\\Solicitud semanal PACHON.xlsx", "C:\\Users\\joshi\\Desktop\\EKLIPSE\\Consolidado\\Planillas\\Consolidado3\\Solicitud semanal PUCOBRE.xlsx", "C:\\Users\\joshi\\Desktop\\EKLIPSE\\Consolidado\\Planillas\\Consolidado3\\Solicitud semanal RIO BLANCO.xlsx", "C:\\Users\\joshi\\Desktop\\EKLIPSE\\Consolidado\\Planillas\\Consolidado3\\Solicitud semanal ROCAS.xlsx", "C:\\Users\\joshi\\Desktop\\EKLIPSE\\Consolidado\\Planillas\\Consolidado3\\Solicitud semanal TOLOLO.xlsx" ]
            print("----- % MODELANDO DATOS % -----")
            for archivo in df:
                try:
                    df_producto = pd.read_excel(archivo,dtype={'COD. PRODUCTO': str}, sheet_name='PRODUCTOS')
                    
                    df_producto = modelado_semanal(df_producto, 'PRODUCTOS')
                    dfs.append(df_producto)

                    unico_centro = df_producto['CENTRO'].unique()
                    valores_sin_corchetes = ', '.join(unico_centro)
                    n_centros.append(valores_sin_corchetes)
    
                    df_especial = pd.read_excel(archivo,dtype={'COD. PRODUCTO': str}, sheet_name='ESPECIALES')
                    df_especial = modelado_semanal(df_especial, 'ESPECIALES')
                    dfs.append(df_especial)
                except Exception as e:
                    print("---> Ocurrió un error al leer el archivo:", str(e))
            print("---> Datos modelados exitosamente.")
            df_final = pd.concat(dfs)
            centros, name_centro, dlc = compra_local()
            modelado(df_final, centros, name_centro, n_centros, dlc)            
        elif opcion == "4":
            print("Saliendo del programa...")
            break
        else:
            print("Opción inválida. Por favor, seleccione una opción válida.")

menu()
