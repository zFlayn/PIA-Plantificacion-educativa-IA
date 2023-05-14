import os
import csv
import heapq
import timeit

# Directorio que contiene los archivos CSV
carpeta = 'D:/Users/kaka1/Downloads/PIA/instancias/test'

# Lista para almacenar las variables
variables = []

# Diccionario para almacenar las relaciones de precedencia
relaciones_precedencia = {}

calificaciones_subtemas = {
    1: 70,
    2: 70
}

velocidad_promedio = 1  # Valor de velocidad promedio deseado

# Definir una estructura de datos para almacenar los estados
class Estado:
    def __init__(self, actividades_seleccionadas, calificaciones_actuales, tiempo_acumulado):
        self.actividades_seleccionadas = actividades_seleccionadas
        self.calificaciones_actuales = calificaciones_actuales
        self.tiempo_acumulado = tiempo_acumulado

    def obtener_costo(self, duracion_actividad):
        return self.tiempo_acumulado + duracion_actividad / velocidad_promedio  # Considerar la duración de la actividad

    def obtener_heuristica(self):
        heuristica = 0
        for subtema, calificacion_minima in calificaciones_subtemas.items():
            calificacion_actual = self.calificaciones_actuales[subtema]
            if calificacion_actual < calificacion_minima:
                progreso_restante = calificacion_minima - calificacion_actual
                tiempo_restante = progreso_restante / velocidad_promedio
                heuristica += tiempo_restante
        return heuristica

# Iterar sobre los archivos en la carpeta
for archivo in os.listdir(carpeta):
    if archivo.endswith('.csv'):  # Filtrar solo archivos CSV
        ruta_archivo = os.path.join(carpeta, archivo)
        
        # Leer el archivo CSV
        with open(ruta_archivo, 'r') as archivo_csv:
            lector_csv = csv.reader(archivo_csv, delimiter=',')
            
            for fila in lector_csv:
                if not any(fila):
                    # La fila está vacía, salta al siguiente archivo
                    break
                
                # Procesar las variables de cada fila según sea necesario
                Subtema = fila[0].strip()
                Num_Actividad = int(fila[1].strip())
                Duracion = int(fila[2].strip())
                Valor = int(fila[3].strip())
                Obligatoria = int(fila[6].strip())
                Requerimiento1 = int(fila[5].strip())
                Requerimiento2 = int(fila[4].strip())
                
                # Resto del código para procesar las variables y relaciones de precedencia
                variables.append((Subtema, Num_Actividad, Duracion, Valor, Obligatoria, Requerimiento1, Requerimiento2))
                if Subtema == '2': 
                    print(variables)
                    break 
                
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
    if Obligatoria > 0:
        print(f'La actividad {Num_Actividad} es obligatoria.')

        if Requerimiento1:
            print(f'Requiere la actividad {Requerimiento1} antes de ser seleccionada.')

        if Requerimiento2:
            print(f'Requiere la actividad {Requerimiento2} antes de ser seleccionada.')


# Ejecutar el algoritmo A*
def algoritmo_a_estrella():
    # Estado inicial sin actividades seleccionadas
    estados_visitados = set()
    estado_inicial = Estado([], {1: 0, 2: 0}, 0)
    cola_prioridad = [(estado_inicial.obtener_heuristica(), estado_inicial)]
    heapq.heapify(cola_prioridad)

    while cola_prioridad:
        _, estado_actual = heapq.heappop(cola_prioridad)
        actividades_seleccionadas = tuple(sorted(estado_actual.actividades_seleccionadas))

        if actividades_seleccionadas in estados_visitados:
            continue

        estados_visitados.add(actividades_seleccionadas)

        if all(calificacion >= calificaciones_subtemas[subtema] for subtema, calificacion in estado_actual.calificaciones_actuales.items()):
            # Se alcanzó la calificación mínima en cada subtema
            print("¡Solución encontrada!")
            actividades_solucion = []
            for actividad in estado_actual.actividades_seleccionadas:
                actividades_solucion.append(actividad)
                print(actividad)
            print("Tiempo total necesario:", estado_actual.tiempo_acumulado)
            return actividades_solucion


        for siguiente_actividad in obtener_actividades_siguientes(estado_actual.actividades_seleccionadas):
            duracion_actividad = siguiente_actividad[2]  # Duración de la siguiente actividad
            calificaciones_actuales = dict(estado_actual.calificaciones_actuales)  # Copia de las calificaciones actuales
            tiempo_acumulado = estado_actual.obtener_costo(duracion_actividad)  # Tiempo acumulado hasta el momento

            # Verificar si se cumplen los requisitos de precedencia
            if siguiente_actividad[5] not in estado_actual.actividades_seleccionadas:
                continue

            # Actualizar las calificaciones y el tiempo acumulado
            subtema = siguiente_actividad[0]
            calificaciones_actuales[subtema] += siguiente_actividad[3]  # Sumar el valor de la actividad al subtema correspondiente

            nuevo_estado = Estado(estado_actual.actividades_seleccionadas + [siguiente_actividad],
                                  calificaciones_actuales, tiempo_acumulado)

            costo = nuevo_estado.obtener_costo(duracion_actividad)
            heuristica = nuevo_estado.obtener_heuristica()
            heapq.heappush(cola_prioridad, (costo + heuristica, nuevo_estado))

    print("No se encontró solución")

def obtener_actividades_siguientes(actividades_seleccionadas):
    actividades_siguientes = []
    for actividad in variables:
        if (
            actividad[1] not in actividades_seleccionadas and
            all(requerimiento in actividades_seleccionadas for requerimiento in relaciones_precedencia.get(actividad[1], [])) and
            (actividad[4] == 0 or (actividad[4] > 0 and actividad[5] in actividades_seleccionadas)) and
            (actividad[6] == 0 or (actividad[6] > 0 and actividad[6] in actividades_seleccionadas))
        ):
            actividades_siguientes.append(actividad)
    return actividades_siguientes

# Ejecutar el algoritmo A*
algoritmo_a_estrella()

# Medir el tiempo de ejecución
tiempo_ejecucion = timeit.timeit(algoritmo_a_estrella, number=1)

print("Tiempo de ejecución:", tiempo_ejecucion, "segundos")
