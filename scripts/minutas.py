import pandas as pd 

ruta_archivo = 'C:\\Users\\joshi\\Desktop\\EKLIPSE\\MINUTAS\\Solicitud de abastecimiento V3.xlsx'
salida = 'C:\\Users\\joshi\\Desktop\\EKLIPSE\\MINUTAS\\EJMMM.xlsx'
recetas = pd.read_excel(ruta_archivo, sheet_name='Recetas')
contratos = pd.read_excel(ruta_archivo, sheet_name='Contrato')
print("Ingresa el servicio que deseas consultar: ")
servicio = input()

def guardar_archivo(receta, archivo):
    with pd.ExcelWriter(archivo) as writer:
        receta.to_excel(writer, sheet_name='EJEMPLO_1', index=False)
    print("---> Archivo exportado exitosamente.")

def final(recetas, contratos, tipo):
    print("Ingrese la receta: ")
    receta = input()
    receta_existente = recetas[recetas['RECETA'] == receta]
    if not receta_existente.empty:
        print("Ingrese la cantidad:")
        cantidad = input()
        receta_existente['CONTRATO'] = contratos
        receta_existente['CANTIDAD'] = cantidad
        print("Ingrese la fecha: ")
        fecha = input()
        receta_existente['FECHA'] = fecha
        receta_existente['TOTAL'] = float(cantidad) * receta_existente[tipo]
        print(receta_existente)
        guardar_archivo(receta_existente, salida)
    else:
        print("La receta no existe.")
def generar_tabla(recetas, tipo, contrato):
    if tipo == "CANT. GRANEL":
        recetas = recetas[['SERVICIO', 'RECETA','INGREDIENTES','CANT. GRANEL']]
        print(recetas)
        final(recetas, contrato, tipo)
    elif tipo == "CANT. TRANSPORTADO":
        recetas = recetas[['SERVICIO', 'RECETA','INGREDIENTES','CANT. TRANSPORTADO']]
        print(recetas)
        final(recetas, contrato, tipo)

def separar_tipo(df, servicio, contratos):
    print("Ingrese el contrato:")
    contrato = input()

    if contrato == "SML":
        c_s = contratos[(contratos['Contrato'] == 'SML') & (contratos['Servicio'] == servicio)]
        print(c_s)
        tipo = c_s['Tipo'].values[0]
        print(tipo)
        generar_tabla(df, tipo, contrato)
        
    elif contrato == "PUCOBRE":
        c_s = contratos[(contratos['Contrato'] == 'PUCOBRE') & (contratos['Servicio'] == servicio)]
        print(c_s)
        tipo = c_s['Tipo'].values[0]
        print(tipo)
        generar_tabla(df, tipo, contrato)
    else:
        print("El contrato no existe.")

if servicio == "ALMUERZO":
    r_a = recetas[recetas['SERVICIO'] == 'ALMUERZO']
    print(r_a)
    separar_tipo(r_a, servicio, contratos)
elif servicio == "POSTRE":
    r_s = recetas[recetas['SERVICIO'] == 'POSTRE']
    print(r_s)
    separar_tipo(r_s, servicio, contratos)
else:
    print("El servicio no existe.")


    