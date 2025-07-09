from datetime import datetime, timedelta
from DatosActividad import  DocCSV
from DatosActividad import ActividadesUsuario
from collections import defaultdict
#Esa bendita libreria esta buena para agrupar las actividades y crea intervalos como diccionarios
import csv
import csv

def EliminarActividad(id):
    print("\n🗑️ Menú de eliminación de actividades")
    fecha_objetivo = input("Ingresa la fecha exacta de la actividad que deseas eliminar (DD/MM/AAAA): ").strip()

    actividades = []
    with open("ActividadesUsuario.csv", mode='r', encoding='utf-8') as f:
        reader = csv.reader(f)
        encabezado = next(reader)
        for fila in reader:
            if fila[0] == str(id) and fila[3] == fecha_objetivo:
                actividades.append(fila)

    if not actividades:
        print(f"📭 No se encontraron actividades para {fecha_objetivo}.")
        return

    print(f"\n📋 Actividades registradas para {fecha_objetivo}:")
    for i, act in enumerate(actividades):
        print(f"{i + 1}. {act[2]} a las {act[4]} ({act[5]} min)")

    try:
        index = int(input("¿Cuál actividad deseas eliminar? (Número): ")) - 1
        if index < 0 or index >= len(actividades):
            print("❌ Número fuera de rango.")
            return
        actividad_eliminada = actividades[index]
    except ValueError:
        print("❌ Entrada inválida.")
        return

    with open("ActividadesUsuario.csv", mode='r', encoding='utf-8') as f:
        contenido = list(csv.reader(f))

    with open("ActividadesUsuario.csv", mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(encabezado)
        for fila in contenido[1:]:
            if fila != actividad_eliminada:
                writer.writerow(fila)

    print(f"✅ Actividad '{actividad_eliminada[2]}' eliminada exitosamente.")



import csv
from RegistroAgenda import EliminarActividad  # Asegúrate de que no cause recursión circular

def EditarActividad(id):
    print("\n📝 Menú de edición de actividades")
    print("*" * 50)
    fecha_objetivo = input("Ingresa la fecha exacta de la actividad que deseas editar (DD/MM/AAAA): ").strip()

    actividades = []
    with open("ActividadesUsuario.csv", mode='r', encoding="utf-8") as f:
        reader = csv.reader(f)
        encabezado = next(reader)
        for fila in reader:
            if fila[0] == str(id) and fila[3] == fecha_objetivo:
                actividades.append(fila)

    if not actividades:
        print(f"📭 No se encontraron actividades para {fecha_objetivo}.")
        return

    print(f"\n📋 Actividades registradas para {fecha_objetivo}:")
    for i, act in enumerate(actividades):
        print(f"{i + 1}. {act[2]} a las {act[4]} ({act[5]} min)")

    try:
        index = int(input("¿Cuál actividad deseas editar? (Número): ")) - 1
        if index < 0 or index >= len(actividades):
            print("❌ Número fuera de rango.")
            return
        seleccion = actividades[index]
    except ValueError:
        print("❌ Entrada inválida.")
        return

    campos = ["Actividad", "Fecha", "Hora", "Duración (min)"]
    campo_a_indice = {0: 2, 1: 3, 2: 4, 3: 5}

    print("\nPuedes editar cualquiera de los siguientes campos:")
    for i, campo in enumerate(campos):
        print(f"{i}. {campo}")

    try:
        campo_index = int(input("¿Qué campo deseas editar? (0-3): "))
        if campo_index not in campo_a_indice:
            print("❌ Opción fuera de rango.")
            return
        nuevo_valor = input(f"Ingrese el nuevo valor para {campos[campo_index]}: ").strip()
        if nuevo_valor:
            seleccion[campo_a_indice[campo_index]] = nuevo_valor
    except ValueError:
        print("❌ Entrada inválida.")
        return

    # Reescribir el archivo con la actividad editada
    with open("ActividadesUsuario.csv", mode='r', encoding="utf-8") as f:
        contenido = list(csv.reader(f))

    with open("ActividadesUsuario.csv", mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(encabezado)
        for fila in contenido[1:]:
            if fila == actividades[index]:
                writer.writerow(seleccion)
            else:
                writer.writerow(fila)

    print("✅ Tu actividad ha sido editada con éxito.")

    opcion2 = input("¿Deseas editar otra actividad? (s/n): ").strip().lower()
    if opcion2 == 's':
        EditarActividad(id)

    opcion3 = input("¿Deseas eliminar alguna actividad? (s/n): ").strip().lower()
    if opcion3 == 's':
        EliminarActividad(id)

#Estructura de la funcioon editar actividad


def RegistrarAgenda(id):
    SemanaUsuario = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo"]
    doc = DocCSV("ActividadesUsuario.csv", ["id", "Hora de levantarse (HH:MM)","Actividad", "Fecha", "Hora", "Duración (min)"]) #Encabezados del csv
    print("Bienvenido a la gestión de actividades de USleepWell!")
    print("Aqui registraremos tus actividades del dia a dia para crear una rutina")
    print("Piensa en todas las actividades que haces por cada dia de la semana, asi planificaremos tu rutina!")
    for dia in SemanaUsuario:
        print(f"Registra las actividades y rutina para  {dia}:")
        Hora_levantar = input(f"¿A qué hora te levantas los {dia}? (HH:MM): ")
        while True:
           print("Por favor, ingresa los siguientes datos para registrar una nueva actividad.")
           nombre_actividad = input("Nombre de la actividad: ")
           fecha_actividad = input("Fecha de la actividad (DD/MM/AAAA): ")
           hora_actividad = input("Hora de la actividad (HH:MM): ")
           duracion_actividad = input("Duración de la actividad (en minutos): ")

           objeto = ActividadesUsuario(id, Hora_levantar, nombre_actividad, fecha_actividad, hora_actividad, duracion_actividad)
        
           doc.guardar_fila(objeto.obtener_datos_csv())

           print("Actividad registrada exitosamente!")
           print("Detalles de la actividad:")
           print(f"Hora a la que te levantas: {Hora_levantar}")
           print(f"Nombre: {nombre_actividad}")
           print(f"Fecha: {fecha_actividad}")
           print(f"Hora: {hora_actividad}")
           print(f"Duración: {duracion_actividad} minutos")
          #Adicion para saber si el user quiere regitrar otra actividad
    
           other = input("¿Deseas registrar otra actividad? (s/n): ").strip().lower() 
          #convierte a minusculas para evitarnos validaciones
           if other != 's':   
             print("Registro terminado. ¡Gracias por usar USleepWell!")
             break
        if dia == "Domingo":
           OpcionEditar = input("¿Deseas editar alguna actividad registrada? (s/n): ").strip().lower()
           if OpcionEditar == 's':
               EditarActividad()
        if dia == "Domingo":
            OpcionEliminar = input("¿Deseas eliminar alguna actividad registrada? (s/n): ").strip().lower()
            if OpcionEliminar == 's':
                EliminarActividad()

def ConsultaAgenda(): #Se encarga de ver los huecos para determinar las siestas, pero las siestas no se calcula aqui
     LapsoDisponibles = []
     ActPorFecha = defaultdict(list)  # Usamos defaultdict para agrupar actividades por fecha, toma list como primer valor para no tener que estar validando
     with open("ActividadesUsuario.csv", encoding='utf-8') as f:
         reader = csv.reader(f)
         encabezado = next(reader)  #Salta encabezado
         for fila in reader: 
             ActPorFecha[fila[2]].append(fila)
      # Agrupa actividades por fecha, creando una clave si aun no existe como si fuera un diccionario
             for fecha, actividades in ActPorFecha.items():
                 #Forma de manejar los elementos en un diccionario
                 actividades = [a for a in actividades if a[4].strip()]  # Filtra filas con hora válida
                 actividades.sort(key=lambda x: datetime.strptime(x[4], "%H:%M"))
                 #Se ordenan de la mas tardia a la mas temprana
                 actual = datetime.strptime("11:00", "%H:%M")  # Hora de inicio del día, para que solo nos cuente las horas libres apratir de ahi
                 FinDia= datetime.strptime("16:00" , "%H:%M")  # Hora de fin del día, para que solo nos cuente las horas libres hasta ahi
                 #Solo le puse esas horas porque son las mas recomendadas para siestas, y solo esas me interesan
                 for act in actividades:
                     inicioAct = datetime.strptime(act[3], "%H:%M")  # Convierte la hora de la actividad a tipo date. Basicamente, pasa todos los datos del cvs a sus tipos
                     duracion = timedelta(minutes=int(act[4]))  # Convierte la duración a un objeto timedelta, que es un intervalo de tiempo con el timpo de la actividad registrada
                     if inicioAct > actual:
                         lapso = (inicioAct - actual).total_seconds() / 60  # Calcula el lapso libre en minutos
                         if lapso >= 20: #Si mi lapso de tiempo registrado es mayor o igual a 20, porque eso debe de durar en general una siesta
                             LapsoDisponibles.append((fecha, actual.strftime("%H:%M"), inicioAct.strftime("%H:%M"), lapso))  # Guarda la fecha, hora de inicio y fin de la siesta, y el lapso libre
                     actual= max(actual, inicioAct + duracion)  # Actualiza la hora actual al final de la actividad
             if actual < FinDia:  # Si la hora actual es menor que la hora de fin del día
                 lapso= (FinDia - actual).total_seconds() / 60  # Calcula el lapso libre hasta el fin del día
                 if lapso >= 20:  # Si el lapso libre es mayor o igual a 20 minutos
                        LapsoDisponibles.append((fecha, actual.strftime("%H:%M"), FinDia.strftime("%H:%M"), lapso))  # Guarda el lapso libre hasta el fin del día
                        #Para que luego lo podamos leer, lo agrega a esa lista temporal
     return LapsoDisponibles  # Retorna la lista de lapsos disponibles para siestas
if __name__ == "__main__":
    # Esta parte se ejecuta si el script se ejecuta directamente
    print("Bienvenido al sistema de gestión de actividades de USleepWell!")
if __name__ == "__main__":
    RegistrarAgenda()
