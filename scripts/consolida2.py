import pandas as pd
import os

#VARIABLES GLOBALES

cat_1 = ['ABARROTES','BEBESTIBLES', 'CONFITERIA', 'DESECHABLES', 'EPP', 'MATERIALES DE LIMPIEZA', 'ART ESCRITORIO', 'ART KIOSCO']
cat_2 = ['AVES', 'CECINAS','CERDO ','FRIZADOS', 'FRUTA Y VERDURA', 'HUEVOS Y LACTEOS', 'PANADERIA', 'PESCADOS Y MARISCOS','VACUNO','PRE-ELABORADOS','PLATOS PREPARADOS','X']
aguas = ['08854','09065','49615','00142','00152','00153','08855','08938','09007','1325','1326','1327','1328','00154','00155']

def compra_local():
    archivos = ["C:\\Users\\joshi\\Desktop\\EKLIPSE\\Consolidado\\Planillas\\Consolidado3\\Compra local COLBUN.xlsx", "C:\\Users\\joshi\\Desktop\\EKLIPSE\\Consolidado\\Planillas\\Consolidado3\\Compra local INCA.xlsx", "C:\\Users\\joshi\\Desktop\\EKLIPSE\\Consolidado\\Planillas\\Consolidado3\\Compra local LUCES.xlsx", "C:\\Users\\joshi\\Desktop\\EKLIPSE\\Consolidado\\Planillas\\Consolidado3\\Compra local PUCOBRE.xlsx","C:\\Users\\joshi\\Desktop\\EKLIPSE\\Consolidado\\Planillas\\Consolidado3\\Compra local RIO BLANCO.xlsx", "C:\\Users\\joshi\\Desktop\\EKLIPSE\\Consolidado\\Planillas\\Consolidado3\\Compra local ROCAS.xlsx" ]
    centros = []
    name_centro = []
    dfs = []
    for archivo in archivos:
        df = pd.read_excel(archivo,dtype={'COD. PRODUCTO': str}, sheet_name='PRODUCTOS')
        df = df[['FAMILIA', 'COD. PRODUCTO', 'DESCRIPCION PRODUCTO', 'UNIDAD', 'Lu', 'Ma', 'Mi', 'Ju', 'Vi', 'Sa', 'CANT. TOTAL', 'CENTRO', 'SEMANA']]
        df['FAMILIA'] = df['FAMILIA'].fillna('X')
        df['COD. PRODUCTO'] = df['COD. PRODUCTO'].fillna('X')
        df['CANT. TOTAL'].astype(float)
        df = df[df['CANT. TOTAL'] != 0]
        
        dfs.append(df)

        unico = df['CENTRO'].unique()
        valores_sin_corchetes = ', '.join(unico)
        name_centro.append(valores_sin_corchetes)

    dff = pd.concat(dfs)
    dff = dff.sort_values(by=['FAMILIA','DESCRIPCION PRODUCTO'])
    for i in range(len(name_centro)):
        dc = dff[dff['CENTRO'] == name_centro[i]]
        dc = dc[['FAMILIA', 'COD. PRODUCTO', 'DESCRIPCION PRODUCTO', 'UNIDAD', 'Lu', 'Ma', 'Mi', 'Ju', 'Vi', 'Sa', 'CANT. TOTAL']]
        centros.append(dc)
    return centros, name_centro
def bodega(df_final,name_centro):
    centros = []
    for i in range(len(name_centro)):
        dc = df_final[['FAMILIA','COD. PRODUCTO', 'DESCRIPCION PRODUCTO','UNIDAD','SITUACION',name_centro[i]]].dropna()
        dc = dc[dc[name_centro[i]] != 0]
        if name_centro[i] != 'TOLOLO' and name_centro[i] != 'PACHON':
            dc = dc[dc['FAMILIA'] != 'FRUTA Y VERDURA']
        centros.append(dc)
    
    with pd.ExcelWriter("C:\\Users\\joshi\\Desktop\\EKLIPSE\\Consolidado\\Planillas\\Consolidado3\\0_BODEGA.xlsx") as writer:
        for i in range(len(centros)):
            centros[i].to_excel(writer, sheet_name=name_centro[i], index=False)
    print("---> Archivo de BODEGA creado.")
def modelado(df, centros, name_centro, n_centros):
    df['FAMILIA'] = df['FAMILIA'].fillna('X')
    df['COD. PRODUCTO'] = df['COD. PRODUCTO'].fillna('X')   
    df = df.pivot_table(index=['FAMILIA','COD. PRODUCTO','DESCRIPCION PRODUCTO','UNIDAD','SITUACION'],columns='CENTRO',values='RECTIFICACION').reset_index()
    s_a = df[df['SITUACION'] != 'APROBADO'].reset_index(drop=True)

    df = df.sort_values(by=['FAMILIA','DESCRIPCION PRODUCTO'])
    g1 = df[df['FAMILIA'].isin(cat_1)]
    g2 = df[df['FAMILIA'].isin(cat_2)]
    df = pd.concat([g1,g2]).reset_index(drop=True)

    g1 = s_a[s_a['FAMILIA'].isin(cat_1)]
    g2 = s_a[s_a['FAMILIA'].isin(cat_2)]

    s_a = pd.concat([g1,g2]).reset_index(drop=True)

    df['TOTAL'] = df.sum(axis=1)
    with pd.ExcelWriter("C:\\Users\\joshi\\Desktop\\EKLIPSE\\Consolidado\\Planillas\\Consolidado3\\0_RECTIFICADO.xlsx") as writer:    
        df.to_excel(writer, sheet_name='Detalle Rectificado', index=False)
        s_a.to_excel(writer, sheet_name='Pendientes Aprobacion', index=False)
        for i in range(len(centros)):
            centros[i].to_excel(writer, sheet_name=name_centro[i], index=False)
    print("---> Archivo de CONSOLIDADO creado.")
    bodega(df, n_centros)

def modelado_semanal(df, Tipo_Categoria): 
    df = df[['FAMILIA', 'COD. PRODUCTO', 'DESCRIPCION PRODUCTO', 'UNIDAD', 'RECTIFICACION', 'CENTRO', 'SEMANA']]
    df.dropna(subset=['RECTIFICACION'], inplace=True) 
    df['RECTIFICACION'].astype(float)
    df = df[df['RECTIFICACION'] != 0]
    df['CATEGORIA'] = Tipo_Categoria
    if Tipo_Categoria == 'PRODUCTOS':
        df['SITUACION'] = 'APROBADO'
    else:
        df['SITUACION'] = '--------'
    return df

#def modelado_mensual(df, Tipo_Categoria):
#    try:
#        df = df.drop(['Unnamed: 0'], axis=1) 
#        df = df.dropna(subset=['CENTRO']) 
#        df = df.melt(id_vars=['FAMILIA', 'COD. PRODUCTO', 'DESCRIPCION PRODUCTO', 'UNIDAD', 'PRECIO $', 'CENTRO'], 
#                    value_vars=['Semana 1', 'Semana 2', 'Semana 3', 'Semana 4', 'Semana 5'], 
#                    var_name='SEMANA', 
#                    value_name='CANTIDAD')
#        df = df[['SEMANA', 'FAMILIA', 'COD. PRODUCTO', 'DESCRIPCION PRODUCTO', 'UNIDAD', 'PRECIO $', 'CENTRO', 'CANTIDAD']]
#        df.dropna(subset=['CANTIDAD'], inplace=True) 
#        df['CANTIDAD'] = df['CANTIDAD'].astype(int)
#        df = df[df['CANTIDAD'] != 0]

#        df['CATEGORIA'] = Tipo_Categoria

#        if Tipo_Categoria == 'PRODUCTOS':
#            df['SITUACION'] = 'APROBADO'
#        else:
#            df['SITUACION'] = '--------'
#
#       return df
#    except Exception as e:
#        print("---> Ocurrió un error al modelar el archivo:", str(e))
#        return None
    
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
        return None
def buscar_archivo():
    dfs = ["C:\\Users\\joshi\\Desktop\\EKLIPSE\\Consolidado\\Planillas\\Consolidado3\\Solicitud semanal COLBUN.xlsx","C:\\Users\\joshi\\Desktop\\EKLIPSE\\Consolidado\\Planillas\\Consolidado3\\Solicitud semanal INCA.xlsx", "C:\\Users\\joshi\\Desktop\\EKLIPSE\\Consolidado\\Planillas\\Consolidado3\\Solicitud semanal LUCES.xlsx","C:\\Users\\joshi\\Desktop\\EKLIPSE\\Consolidado\\Planillas\\Consolidado3\\Solicitud semanal PACHON.xlsx", "C:\\Users\\joshi\\Desktop\\EKLIPSE\\Consolidado\\Planillas\\Consolidado3\\Solicitud semanal PUCOBRE.xlsx", "C:\\Users\\joshi\\Desktop\\EKLIPSE\\Consolidado\\Planillas\\Consolidado3\\Solicitud semanal RIO BLANCO.xlsx", "C:\\Users\\joshi\\Desktop\\EKLIPSE\\Consolidado\\Planillas\\Consolidado3\\Solicitud semanal ROCAS.xlsx", "C:\\Users\\joshi\\Desktop\\EKLIPSE\\Consolidado\\Planillas\\Consolidado3\\Solicitud semanal TOLOLO.xlsx" ]
    #dfs = []
    #print("----- CARGAR ARCHIVO -----")
    #print("Ingrese la cantidad de archivos a cargar: ")
    #cantidad = int(input())
    #for i in range(cantidad):
    #    print("Ingrese la ruta del archivo Excel: ")
    #    ruta = input()
    #    try:
    #        dfs.append(ruta)
    #        print("---> Archivo cargado exitosamente.")
    #    except FileNotFoundError:
    #        print("---> No se encontró el archivo.")
    #        return None
    #    except Exception as e:
    #        print("---> Ocurrió un error al cargar el archivo:", str(e))
    #        return None
    return dfs
def menu():
    while True:
        print("----- MENÚ ------\n1.Consolidado Mensual\n2.Consolidado Semanal\n3.Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            dfs = []
            df = buscar_archivo()
            print("----- % MODELANDO DATOS % -----")
            for archivo in df:
                try:
                    df_producto = pd.read_excel(archivo,dtype={'COD. PRODUCTO': str}, sheet_name='PRODUCTOS')
                    #df_producto = modelado_mensual(df_producto, 'PRODUCTOS')
                    dfs.append(df_producto)

                    df_especial = pd.read_excel(archivo,dtype={'COD. PRODUCTO': str}, sheet_name='ESPECIALES')
                    #df_especial = modelado_mensual(df_especial, 'ESPECIALES')
                    dfs.append(df_especial)

                    df_final = pd.concat(dfs)
                    print("---> Datos modelados exitosamente.")
                    exportar(df_final)

                except Exception as e:
                    print("---> Ocurrió un error al leer el archivo:", str(e))
                
                # Falta agregar los implementos
        elif opcion == "2":
            n_centros = []
            dfs = []
            df = buscar_archivo()
            print("----- % MODELANDO DATOS % -----")
            for archivo in df:
                try:
                    df_producto = pd.read_excel(archivo,dtype={'COD. PRODUCTO': str}, sheet_name='PRODUCTOS')
                    
                    df_producto = modelado_semanal(df_producto, 'PRODUCTOS')
                    dfs.append(df_producto)

                    unico_familia = df_producto['FAMILIA'].unique()
                    #print(unico_familia)

                    unico_centro = df_producto['CENTRO'].unique()
                    valores_sin_corchetes = ', '.join(unico_centro)
                    n_centros.append(valores_sin_corchetes)
    
                    df_especial = pd.read_excel(archivo,dtype={'COD. PRODUCTO': str}, sheet_name='ESPECIALES')
                    df_especial = modelado_semanal(df_especial, 'ESPECIALES')
                    dfs.append(df_especial)

                    #df_implemento = pd.read_excel(archivo,dtype={'COD. PRODUCTO': str}, sheet_name='IMPLEMENTOS')
                    #df_implemento = modelado_semanal(df_implemento, 'IMPLEMENTOS')
                    #dfs.append(df_implemento)
                    
                    #exportar(df_final)
                except Exception as e:
                    print("---> Ocurrió un error al leer el archivo:", str(e))
            print("---> Datos modelados exitosamente.")
            df_final = pd.concat(dfs)
            centros, name_centro = compra_local()
            modelado(df_final, centros, name_centro, n_centros)            
        elif opcion == "3":
            print("Saliendo del programa...")
            break
        else:
            print("Opción inválida. Por favor, seleccione una opción válida.")

menu()
