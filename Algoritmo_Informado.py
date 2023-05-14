import os
import csv
import time

# Directorio que contiene los archivos CSV
carpeta = 'D:/Users/kaka1/Downloads/PIA Inteligencia Artificial/instancias'

# Lista para almacenar las variables
variables = []

# Diccionario para almacenar las relaciones de precedencia
relaciones_precedencia = {}

start_time = time.time()

# Iterar sobre los archivos en la carpeta
for archivo in os.listdir(carpeta):
    if archivo.endswith('.csv'):  # Filtrar solo archivos CSV
        ruta_archivo = os.path.join(carpeta, archivo)
        
        # Leer el archivo CSV
        with open(ruta_archivo, 'r') as archivo_csv:
            lector_csv = csv.reader(archivo_csv, delimiter=',')
            
            # Iterar sobre las filas del archivo CSV
            for fila in lector_csv:
                # Procesar las variables de cada fila según sea necesario
                Subtema =        fila[2]  
                Num_Actividad =  fila[3]  
                Duracion=        fila[4] 
                Valor =          fila[5]  
                Obligatoria =    fila[7]  
                Requerimiento1 = fila[8]
                Requerimiento2 = fila[9]
                # Agregar las variables a la lista
                variables.append((Subtema, Num_Actividad, Duracion, Valor, Obligatoria, Requerimiento1, Requerimiento2))
                # Agregar las relaciones de precedencia al diccionario
                if Requerimiento1 not in relaciones_precedencia:
                    relaciones_precedencia[Requerimiento1] = []
                relaciones_precedencia[Requerimiento1].append(Num_Actividad)

# Imprimir las variables
for Subtema, Num_Actividad, Duracion, Valor, Obligatoria, Requerimiento1, Requerimiento2 in variables:
    print(f'Subtema: {Subtema}, Num_Actividad: {Num_Actividad}, Duracion: {Duracion}, Valor: {Valor}, Obligatoria: {Obligatoria}, Requerimiento1: {Requerimiento1}, Requerimiento2: {Requerimiento2}')

# Imprimir las relaciones de precedencia
print("Relaciones de Precedencia:")
for actividad, requerimientos in relaciones_precedencia.items():
    print(f'Actividad: {actividad}, Requerimientos: {requerimientos}')  


# Restricciones de precedencia o habilitamiento
for Subtema, Num_Actividad, Duracion, Valor, Obligatoria, Requerimiento1, Requerimiento2 in variables:
    print(f'Subtema: {Subtema}, Num_Actividad: {Num_Actividad}')
    
    # Restricción de puntaje mínimo y máximo
    kmin = 10  # Valor mínimo requerido
    kmax = 50  # Valor máximo permitido
    
    if int(Valor) < kmin:
        print(f'El puntaje de la actividad es menor al valor mínimo requerido: {Valor} < {kmin}')
    
    if int(Valor) > kmax:
        print(f'El puntaje de la actividad es mayor al valor máximo permitido: {Valor} > {kmax}')
    
    if int(Obligatoria) > 1:
        print(f'La actividad {Num_Actividad} es obligatoria.')
        if Requerimiento1:
                print(f'Requiere la actividad {Requerimiento1} antes de ser seleccionada.')
            
        if Requerimiento2:
                print(f'Requiere la actividad {Requerimiento2} antes de ser seleccionada.')

end_time = time.time()
print(f"Tiempo de compilación: {end_time - start_time} segundos")