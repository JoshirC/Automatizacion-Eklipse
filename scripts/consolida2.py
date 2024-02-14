import pandas as pd

#VARIABLES GLOBALES

cat_1 = ['ABARROTES','BEBESTIBLES', 'CONFITERIA', 'DESECHABLES', 'EPP', 'MATERIALES DE LIMPIEZA', 'ART ESCRITORIO', 'ART KIOSCO']
cat_2 = ['AVES', 'CECINAS','CERDO ','FRIZADOS', 'FRUTA Y VERDURA', 'HUEVOS Y LACTEOS', 'PANADERIA', 'PESCADOS Y MARISCOS','VACUNO','PRE-ELABORADOS','PLATOS PREPARADOS','X']

#FUNCIONES

def data_frame(df, dcl):
    dlc = dcl[['SEMANA','COD. PRODUCTO', 'DESCRIPCION PRODUCTO','CANT. TOTAL', 'CENTRO', 'MES']]
    dlc['SALIDA'] = "LOCAL"
    dlc = dlc.rename(columns={'CANT. TOTAL': 'RECTIFICACION'})
    df = df[['SEMANA','COD. PRODUCTO', 'DESCRIPCION PRODUCTO', 'RECTIFICACION', 'CENTRO', 'MES']]
    df['SALIDA'] = "BODEGA"
    df = pd.concat([df,dlc])
    df.sort_values('DESCRIPCION PRODUCTO', inplace=True)
    df.dropna(subset=['RECTIFICACION'], inplace=True)
    
    return df
def compra_local():
    archivos = ["C:\\Users\\joshi\\Desktop\\EKLIPSE\\Consolidado\\Archivos Base\\26 - 03 feb\\Compra Local RIO BLANCO.xlsx","C:\\Users\\joshi\\Desktop\\EKLIPSE\\Consolidado\\Archivos Base\\26 - 03 feb\\Compra Local CHACABUCO.xlsx","C:\\Users\\joshi\\Desktop\\EKLIPSE\\Consolidado\\Archivos Base\\26 - 03 feb\\Compra Local COLBUN.xlsx","C:\\Users\\joshi\\Desktop\\EKLIPSE\\Consolidado\\Archivos Base\\26 - 03 feb\\Compra Local INCA.xlsx","C:\\Users\\joshi\\Desktop\\EKLIPSE\\Consolidado\\Archivos Base\\26 - 03 feb\\Compra Local LUCES.xlsx","C:\\Users\\joshi\\Desktop\\EKLIPSE\\Consolidado\\Archivos Base\\26 - 03 feb\\Compra Local PUCOBRE.xlsx","C:\\Users\\joshi\\Desktop\\EKLIPSE\\Consolidado\\Archivos Base\\26 - 03 feb\\Compra Local ROCAS.xlsx"]
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
    
    with pd.ExcelWriter("C:\\Users\\joshi\\Desktop\\EKLIPSE\\Consolidado\\Archivos Base\\26 - 03 feb\\0_BODEGA.xlsx") as writer:
        for i in range(len(centros)):
            centros[i].to_excel(writer, sheet_name=name_centro[i], index=False)
    print("---> Archivo de BODEGA creado.")
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
    #La funcion sum no omite los strings, por lo que se debe eliminar las columnas que no son numericas
    df_T = df.drop(columns=['FAMILIA', 'COD. PRODUCTO', 'DESCRIPCION PRODUCTO', 'UNIDAD', 'CATEGORIA'])
    df["TOTAL"] = df_T.sum(axis=1)

    with pd.ExcelWriter("C:\\Users\\joshi\\Desktop\\EKLIPSE\\Consolidado\\Archivos Base\\26 - 03 feb\\0_CONSOLIDADO.xlsx") as writer:    
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
def menu():
    while True:
        print("----- MENÚ ------\n1.Consolidado Mensual\n2.Consolidado Semanal\n3.Reposiciones\n4.Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            n_centros = []
            dfs = []
            df = ["C:\\Users\\joshi\\Desktop\\EKLIPSE\\Consolidado\\Planillas\\Consolidado3\\EJM Solicitud mensual LUCES.xlsx"]
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
            centros, name_centro, dlc = compra_local()
            modelado(df_final, centros, name_centro, n_centros, dlc)     
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
            print("Saliendo del programa...")
            break
        else:
            print("Opción inválida. Por favor, seleccione una opción válida.")

menu()
