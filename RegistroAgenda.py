from datetime import datetime
from DatosActividad import  DocCSV
from DatosActividad import ActividadesUsuario
import csv
def EditarActividad():
   print("Hola, Bienvenido al menu de edición de actividades.")
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
      with open("ActividadesUsuario.csv", mode = 'w', newline='', encoding="UTF-8") as f:
          writer = csv.writer(f)
          writer.writerow(encabezado)
          for fila in cont[1:]: #Slide notation: Del uno en adelante, para no incluir el encabezado
              if fila[2] != FechaOpcion:
                  writer.writerow(fila)  # Escribe las filas que no coinciden con el día
          for fila in ActSecundaria:
             writer.writerow(fila)  #Guarda la actividad o mas bien la escribe si la fecha coincide 

      print("Tu actividad ha sido editada!")
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

RegistrarAgenda()

