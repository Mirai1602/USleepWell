from datetime import datetime, timedelta
from DatosActividad import  DocCSV
from DatosActividad import ActividadesUsuario
from collections import defaultdict
#Esa bendita libreria esta buena para agrupar las actividades y crea intervalos como diccionarios
import csv
def EliminarActividad():
    print("\n Menú de eliminación de actividades")
    fecha_objetivo = input("Ingresa la fecha exacta de la actividad que deseas eliminar (DD/MM/AAAA): ").strip()

    actividades = []
    with open("ActividadesUsuario.csv", mode='r', encoding='utf-8') as f:
        reader = csv.reader(f)
        encabezado = next(reader)
        for fila in reader:
            if fila[2] == fecha_objetivo:
                actividades.append(fila)
    if not actividades:
        print(f" No se encontraron actividades para {fecha_objetivo}.")
        return
    print(f"\nActividades registradas para {fecha_objetivo}:")
    for i, act in enumerate(actividades):
        print(f"{i + 1}. {act[1]} a las {act[3]} ({act[4]} min)")

    try:
        index = int(input("¿Cuál actividad deseas eliminar? (Número): ")) - 1
        if index < 0 or index >= len(actividades):
            print(" Número fuera de rango.")
            return
        actividad_eliminada = actividades.pop(index)
    except ValueError:
        print(" Entrada inválida.")
        return

    with open("ActividadesUsuario.csv", mode='r', encoding='utf-8') as f:
        contenido = list(csv.reader(f))

    # Reescribir el archivo sin la actividad eliminada
    with open("ActividadesUsuario.csv", mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(encabezado)
        if len(contenido) <= 1:
            print(" El archivo CSV no tiene actividades registradas para eliminar.")
            return
        for fila in contenido[1:]:
            if fila != actividad_eliminada:
                writer.writerow(fila)
    
    print(f" Actividad '{actividad_eliminada[1]}' eliminada exitosamente.")

def EditarActividad():
   print("Hola, Bienvenido al menu de edición de actividades.")
   print("*"*50)
   FechaOpcion= input("Ingresa la fecha exacta de la actividad que deseas editar (DD/MM/AAAA): ").strip().capitalize()
   ActSecundaria = []
   with open("ActividadesUsuario.csv", mode = 'r' , encoding = "UTF-8") as f: 
      reader = csv.reader(f) 
      encabezado = next(reader)  # Leer el encabezado
      for fila in reader:
         if fila[2] == FechaOpcion:  # Verificar si la fecha coincide con el día seleccionado dependiendo del dia que le pongamos 
            ActSecundaria.append(fila)  # Agregar la fila a la lista si coincide
      print(f"Estas son las actividades del dia: {FechaOpcion}")
      for i, acti in enumerate(ActSecundaria):  #Controlo la actividad que e va mostrando, la recorro i es el num de actividad
         print(f"{i+1}. {acti[1]} a la(s) {acti[3]} que dura {acti[4]} minutos")  
         #Va a mostrar todas las actividades del dia que le ponga, y las tuquea en acti
      try:
            index = int(input("¿Cuál actividad deseas editar? (Ingresa el numero): ")) - 1 #Pide el numero de actividad que quiere editar
            Seleccion = ActSecundaria[index]  #Selecciona la actividad que el usuario quiere editar
      except ValueError:
            print("Por favor, ingresa un número válido.")
            return
      campos = ["Hora de levantarse (HH:MM)", "Actividad", "fecha", "Hora", "Duracion (min)"]
      print("Puedes editar cualquiera de los siguientes datos (Iniciando desde el 0):")
      for i, campo in enumerate(campos): #La quite el uno para que las opciones coincidancon el numero ingresado
          print(f"{i}. {campo}")
      try:
          # Pide el campo que quiere editar
          index2 = int(input("¿Qué campo deseas editar? (0-4): "))
          if index2 == 0: 
              nuevoValor = input(f"Nuevo nombre {Seleccion[1]}: ").strip() or Seleccion[1] 
              Seleccion[1] = nuevoValor  # Actualiza el nombre de la actividad
              #Si no se escribe nada, se deja el valor que ya tiene
          if index2==1:
              nuevoValor = input(f"Nuevo fecha {Seleccion[2]}: ").strip() or Seleccion[2]
              Seleccion[2] = nuevoValor  # Actualiza la fecha de la actividad
          if index2==2:
              nuevoValor = input(f"Nueva hora {Seleccion[3]}:").strip() or Seleccion[3]
              Seleccion[3] = nuevoValor  # Actualiza la hora de la actividad
          if index2 ==3:
              nuevoValor = input(f"Nueva duracion de la actividad {Seleccion[4]}: ").strip() or Seleccion[4]
              Seleccion[4] = nuevoValor  # Actualiza la duración de la actividad
      except ValueError:
          print("Por favor, ingresa un número válido de opcion de los campos.")
          return
      #Leemos el contenido
      with open("ActividadesUsuario.csv", mode = 'r', encoding="UTF-8") as f:
          cont = list(csv.reader(f))  # Lee el contenido del archivo CSV lo convierto a lista 
      #Escribimos en el conteido en el CSV
      with open("ActividadesUsuario.csv", mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(encabezado)
        if len(contenido) <= 1:
            print(" El archivo CSV no tiene actividades registradas para eliminar.")
            return
        for fila in contenido[1:]:
            if fila != actividad_eliminada:
                writer.writerow(fila)

      print("Tu actividad ha sido editada!")
      opcion2= input("¿Deseas editar otra actividad? (s/n): ").strip().lower()
      if opcion2 == 's':
          EditarActividad()
      opcion3 = input("¿Deseas eliminar alguna actividad? (s/n): ").strip().lower()
      if opcion3 == 's':
          EliminarActividad()

      #Estructura de eliminar actividad


def RegistrarAgenda():
    SemanaUsuario = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo"]
    doc = DocCSV("ActividadesUsuario.csv", ["Hora de levantarse (HH:MM)","Actividad", "Fecha", "Hora", "Duración (min)"]) #Encabezados del csv
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

           objeto = ActividadesUsuario(Hora_levantar, nombre_actividad, fecha_actividad, hora_actividad, duracion_actividad)
        
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
                 actividades.sort(key=lambda x: datetime.strptime(x[3], "%H:%M"))  # Ordena actividades por hora. Convierte texto a tipo date
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
    RegistrarAgenda() 