import pandas as pd

#VARIABLES GLOBALES

cat_1 = ['ABARROTES','BEBESTIBLES', 'CONFITERIA', 'DESECHABLES', 'EPP', 'MATERIALES DE LIMPIEZA', 'ART ESCRITORIO', 'ART KIOSCO']
cat_2 = ['AVES', 'CECINAS','CERDO','FRIZADOS', 'FRUTA Y VERDURA', 'HUEVOS Y LACTEOS', 'PANADERIA', 'PESCADOS Y MARISCOS','VACUNO','PRE-ELABORADOS','PLATOS PREPARADOS','X']

#FUNCIONES

'''
Función que permite modelar los datos obtenidos de los archivos de excel, para luego obtener estadisticas sobre estos mismos.

'''
def data_frame(df):
    df = df[['SEMANA','COD. PRODUCTO', 'DESCRIPCION PRODUCTO', 'RECTIFICACION', 'CENTRO', 'MES', 'CATEGORIA', "SALIDA"]]
    df.sort_values('DESCRIPCION PRODUCTO', inplace=True)
    df.dropna(subset=['RECTIFICACION'], inplace=True)
    
    return df
'''
Función que permite leer los archivos de compra local y los transforma según el modelo indicado.

'''
def compra_local():
    archivos = ["C:\\Users\\joshi\\Desktop\\EKLIPSE\\Consolidado\\Marzo\\Semana 1\\Compra local - Colbun.xlsx","C:\\Users\\joshi\\Desktop\\EKLIPSE\\Consolidado\\Marzo\\Semana 1\\Compra local - Cerro Negro.xlsx","C:\\Users\\joshi\\Desktop\\EKLIPSE\\Consolidado\\Marzo\\Semana 1\\Compra local - Inca de Oro.xlsx","C:\\Users\\joshi\\Desktop\\EKLIPSE\\Consolidado\\Marzo\\Semana 1\\Compra local - Pucobre.xlsx","C:\\Users\\joshi\\Desktop\\EKLIPSE\\Consolidado\\Marzo\\Semana 1\\Compra local - Rio Blanco.xlsx","C:\\Users\\joshi\\Desktop\\EKLIPSE\\Consolidado\\Marzo\\Semana 1\\Compra local - Rocas.xlsx","C:\\Users\\joshi\\Desktop\\EKLIPSE\\Consolidado\\Marzo\\Semana 1\\Compra local - Chacabuco.xlsx"]
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

        unico_centro = df['CENTRO'].unique()
        valores_sin_corchetes = ', '.join(unico_centro)
        name_centro.append(valores_sin_corchetes)

        dfs.append(df)

        

    dlc = pd.concat(dfs)
    dff = dlc.sort_values(by=['FAMILIA','DESCRIPCION PRODUCTO'])
    dl_c = dlc[['SEMANA','COD. PRODUCTO', 'DESCRIPCION PRODUCTO','CANT. TOTAL', 'CENTRO', 'MES']]
    print(dl_c)
    dl_c = dlc.rename(columns={'CANT. TOTAL': 'RECTIFICACION'})
    dl_c["CATEGORIA"] = "NN"
    dl_c["SALIDA"] = "LOCAL"
    dl_c = data_frame(dl_c)
    for i in range(len(name_centro)):
        dc = dff[dff['CENTRO'] == name_centro[i]]
        dc = dc[['FAMILIA', 'COD. PRODUCTO', 'DESCRIPCION PRODUCTO', 'UNIDAD', 'Lu', 'Ma', 'Mi', 'Ju', 'Vi', 'Sa', 'CANT. TOTAL']]
        centros.append(dc)
    with pd.ExcelWriter("C:\\Users\\joshi\\Desktop\\EKLIPSE\\Consolidado\\Marzo\\Semana 1\\0_COMPRA_LOCAL.xlsx") as writer:
        for i in range(len(centros)):
            centros[i].to_excel(writer, sheet_name=name_centro[i], index=False)
        dl_c.to_excel(writer, sheet_name='Modelado Estadistico', index=False)    
    #return centros, name_centro, dlc
'''
Función que permite modelar los datos para procesar las solicitudes de envio en bodega.

'''
def bodega():
    df = pd.read_excel("C:\\Users\\joshi\\Desktop\\EKLIPSE\\Consolidado\\Marzo\\Semana 1\\0_CONSOLIDADO.xlsx", sheet_name='Detalle Consolidado')
    n_columnas = len(df.columns)
    n_columnas = n_columnas - 1

    with pd.ExcelWriter("C:\\Users\\joshi\\Desktop\\EKLIPSE\\Consolidado\\Marzo\\Semana 1\\0_BODEGA.xlsx") as writer:
        for i in range(5,n_columnas):
            df_final = df[['FAMILIA','COD. PRODUCTO', 'DESCRIPCION PRODUCTO','UNIDAD',df.columns[i]]].dropna()
            df_final.to_excel(writer, sheet_name=df.columns[i], index=False)
    print("---> Archivo de BODEGA creado.")
    '''
        centros = []
    for i in range(len(name_centro)):
        dc = df_final[['FAMILIA','COD. PRODUCTO', 'DESCRIPCION PRODUCTO','UNIDAD','CATEGORIA',name_centro[i]]].dropna()
        dc = dc[dc[name_centro[i]] != 0]
        if name_centro[i] != 'TOLOLO' and name_centro[i] != 'PACHON':
            dc = dc[dc['FAMILIA'] != 'FRUTA Y VERDURA']
        centros.append(dc)
    
    with pd.ExcelWriter("C:\\Users\\joshi\\Desktop\\EKLIPSE\\Consolidado\\Marzo\\Semana 1\\0_BODEGA.xlsx") as writer:
        for i in range(len(centros)):
            centros[i].to_excel(writer, sheet_name=name_centro[i], index=False)
    print("---> Archivo de BODEGA creado.")
    '''
    
'''
Función que permite modelar los datos para procesar las solicitudes de reposicion.

'''
def modelado_reposicion(df, n_centros):
    centros = []
    df['FAMILIA'] = df['FAMILIA'].fillna('X')
    df['COD. PRODUCTO'] = df['COD. PRODUCTO'].fillna('X')
    dn = df[['SEMANA', 'COD. PRODUCTO', 'DESCRIPCION PRODUCTO', 'CANTIDAD', 'CENTRO', 'MES']]
    dn = dn.rename(columns={'CANTIDAD': 'RECTIFICACION'})
    dn = dn.dropna(subset=['RECTIFICACION'])
    dn = dn.sort_values(by=['DESCRIPCION PRODUCTO'])

    df = df.pivot_table(index=['FAMILIA','COD. PRODUCTO','DESCRIPCION PRODUCTO','UNIDAD'],columns='CENTRO',values='CANTIDAD').reset_index()
    df = df.sort_values(by=['FAMILIA','DESCRIPCION PRODUCTO'])

    df_T = df.drop(columns=['FAMILIA', 'COD. PRODUCTO', 'DESCRIPCION PRODUCTO', 'UNIDAD'])
    df["TOTAL"] = df_T.sum(axis=1)

    with pd.ExcelWriter("C:\\Users\\joshi\\Desktop\\EKLIPSE\\Consolidado\\Planillas\\Consolidado3\\1_REPOSICIONES.xlsx") as writer:
        df.to_excel(writer, sheet_name='Detalle Consolidado', index=False)
        dn.to_excel(writer, sheet_name='Modelado Estadistico', index=False)

    for i in range(len(n_centros)):
        dc = df[['FAMILIA','COD. PRODUCTO', 'DESCRIPCION PRODUCTO','UNIDAD',n_centros[i]]].dropna()
        dc = dc[dc[n_centros[i]] != 0]
        centros.append(dc)
    with pd.ExcelWriter("C:\\Users\\joshi\\Desktop\\EKLIPSE\\Consolidado\\Planillas\\Consolidado3\\1_BODEGA.xlsx") as writer:
        for i in range(len(centros)):
            centros[i].to_excel(writer, sheet_name=n_centros[i], index=False)
'''
Función que permite modelar los datos para procesar las solicitudes de compra.

'''
def modelado(df, n_centros):
    df['FAMILIA'] = df['FAMILIA'].fillna('X')
    df['COD. PRODUCTO'] = df['COD. PRODUCTO'].fillna('X') 
    df["SALIDA"] = "BODEGA"
    d_data = data_frame(df)
    df = df.pivot_table(index=['FAMILIA','COD. PRODUCTO','DESCRIPCION PRODUCTO','UNIDAD','CATEGORIA'],columns='CENTRO',values='RECTIFICACION').reset_index()
    s_a = df[df['CATEGORIA'] != 'PRODUCTOS'].reset_index(drop=True)

    df = df.sort_values(by=['FAMILIA','DESCRIPCION PRODUCTO'])
    g1 = df[df['FAMILIA'].isin(cat_1)]
    g2 = df[df['FAMILIA'].isin(cat_2)]
    df = pd.concat([g1,g2]).reset_index(drop=True)

    g1 = s_a[s_a['FAMILIA'].isin(cat_1)]
    g2 = s_a[s_a['FAMILIA'].isin(cat_2)]

    s_a = pd.concat([g1,g2]).reset_index(drop=True)
    #La funcion sum no omite los strings, por lo que se debe eliminar las columnas que no son numericas
    df_T = df.drop(columns=['FAMILIA', 'COD. PRODUCTO', 'DESCRIPCION PRODUCTO', 'UNIDAD', 'CATEGORIA'])
    df["TOTAL"] = df_T.sum(axis=1)

    with pd.ExcelWriter("C:\\Users\\joshi\\Desktop\\EKLIPSE\\Consolidado\\Marzo\\Semana 1\\0_CONSOLIDADO.xlsx") as writer:    
        df.to_excel(writer, sheet_name='Detalle Consolidado', index=False)
        s_a.to_excel(writer, sheet_name='Pendientes Aprobacion', index=False)
        d_data.to_excel(writer, sheet_name='Modelado Estadistico', index=False)
    print("---> Archivo de CONSOLIDADO creado.")
'''
Función que permite leer los archivos de compra local y los transforma según el modelo indicado.

'''
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
Función principal que administra el script y carga los archivos según la opción solicitada.

'''
def menu():
    while True:
        print("----- MENÚ ------\n1.Consolidado Mensual\n2.Consolidado Semanal\n3.Reposiciones\n4.Compra Local\n5.Bodega\n6.Salir\n-----------------")
        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            n_centros = []
            dfs = []
            df = ["C:\\Users\\joshi\\Desktop\\EKLIPSE\\Consolidado\\Marzo\\Semana 1\\Solicitud Mensual - Colbun.xlsx","C:\\Users\\joshi\\Desktop\\EKLIPSE\\Consolidado\\Marzo\\Semana 1\\Solicitud Mensual - Cerro Negro.xlsx","C:\\Users\\joshi\\Desktop\\EKLIPSE\\Consolidado\\Marzo\\Semana 1\\Solicitud Mensual - Chacabuco.xlsx","C:\\Users\\joshi\\Desktop\\EKLIPSE\\Consolidado\\Marzo\\Semana 1\\Solicitud Mensual - Inca de Oro.xlsx","C:\\Users\\joshi\\Desktop\\EKLIPSE\\Consolidado\\Marzo\\Semana 1\\Solicitud Mensual - Pachon.xlsx","C:\\Users\\joshi\\Desktop\\EKLIPSE\\Consolidado\\Marzo\\Semana 1\\Solicitud Mensual - Pucobre.xlsx","C:\\Users\\joshi\\Desktop\\EKLIPSE\\Consolidado\\Marzo\\Semana 1\\Solicitud Mensual - Rio Blanco.xlsx","C:\\Users\\joshi\\Desktop\\EKLIPSE\\Consolidado\\Marzo\\Semana 1\\Solicitud Mensual - Rocas.xlsx","C:\\Users\\joshi\\Desktop\\EKLIPSE\\Consolidado\\Marzo\\Semana 1\\Solicitud Mensual - Tololo.xlsx"]
            print("----- % MODELANDO DATOS % -----")
            for archivo in df:
                try:
                    print(archivo)
                    df_producto = pd.read_excel(archivo,dtype={'COD. PRODUCTO': str}, sheet_name='PRODUCTOS')
                    df_producto = modelado_mensual(df_producto, 'PRODUCTOS')
                    dfs.append(df_producto)

                    df_especial = pd.read_excel(archivo,dtype={'COD. PRODUCTO': str}, sheet_name='ESPECIALES')
                    df_especial = modelado_mensual(df_especial, 'ESPECIALES')
                    dfs.append(df_especial)

                    unico_centro = df_producto['CENTRO'].unique()
                    valores_sin_corchetes = ', '.join(unico_centro)
                    n_centros.append(valores_sin_corchetes)

                    print("---> Datos modelados exitosamente.")
                except Exception as e:
                    print("---> Ocurrió un error al leer el archivo:", str(e))
                
            df_final = pd.concat(dfs)
            #centros, name_centro, dlc = compra_local()
            modelado(df_final, n_centros)  
        elif opcion == "2":
            n_centros = []
            dfs = []
            df = ["C:\\Users\\joshi\\Desktop\\EKLIPSE\\Consolidado\\Archivos Base\\26 - 03 feb\\Solicitud semanal RIO BLANCO.xlsx","C:\\Users\\joshi\\Desktop\\EKLIPSE\\Consolidado\\Archivos Base\\26 - 03 feb\\Solicitud semanal CHACABUCO.xlsx","C:\\Users\\joshi\\Desktop\\EKLIPSE\\Consolidado\\Archivos Base\\26 - 03 feb\\Solicitud semanal COLBUN.xlsx","C:\\Users\\joshi\\Desktop\\EKLIPSE\\Consolidado\\Archivos Base\\26 - 03 feb\\Solicitud semanal INCA.xlsx","C:\\Users\\joshi\\Desktop\\EKLIPSE\\Consolidado\\Archivos Base\\26 - 03 feb\\Solicitud semanal LUCES.xlsx","C:\\Users\\joshi\\Desktop\\EKLIPSE\\Consolidado\\Archivos Base\\26 - 03 feb\\Solicitud semanal PACHON.xlsx","C:\\Users\\joshi\\Desktop\\EKLIPSE\\Consolidado\\Archivos Base\\26 - 03 feb\\Solicitud semanal PUCOBRE.xlsx","C:\\Users\\joshi\\Desktop\\EKLIPSE\\Consolidado\\Archivos Base\\26 - 03 feb\\Solicitud semanal ROCAS.xlsx","C:\\Users\\joshi\\Desktop\\EKLIPSE\\Consolidado\\Archivos Base\\26 - 03 feb\\Solicitud semanal TOLOLO.xlsx"]
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
            #centros, name_centro, dlc = compra_local()
            modelado(df_final, n_centros)     
        elif opcion == "3":
            n_centros = []
            dfs = []
            df = ["C:\\Users\\joshi\\Desktop\\EKLIPSE\\Consolidado\\Planillas\\Consolidado3\\EJM Reposiciones COLBUN.xlsx","C:\\Users\\joshi\\Desktop\\EKLIPSE\\Consolidado\\Planillas\\Consolidado3\\EJM Reposiciones LUCES.xlsx"]
            print("----- % MODELANDO DATOS % -----")
            for archivo in df:
                try:
                    df_producto = pd.read_excel(archivo,dtype={'COD. PRODUCTO': str}, sheet_name='PRODUCTOS')
                    df_producto = df_producto[['FAMILIA', 'COD. PRODUCTO', 'DESCRIPCION PRODUCTO', 'UNIDAD', 'CANTIDAD', 'CENTRO', 'SEMANA', 'MES']]
                    dfs.append(df_producto)

                    unico_centro = df_producto['CENTRO'].unique()
                    valores_sin_corchetes = ', '.join(unico_centro)
                    n_centros.append(valores_sin_corchetes)
    
                except Exception as e:
                    print("---> Ocurrió un error al leer el archivo:", str(e))
            print("---> Datos modelados exitosamente.")
            df_final = pd.concat(dfs)
            modelado_reposicion(df_final, n_centros)  
        
        elif opcion == "4":
            compra_local()
        elif opcion == "5":
            bodega()
        elif opcion == "6":
            print("Saliendo del programa...")
            break
        else:
            print("Opción inválida. Por favor, seleccione una opción válida.")
menu()
