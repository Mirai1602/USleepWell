from datetime import datetime
from DatosActividad import  DocCSV
from DatosActividad import ActividadesUsuario

import csv
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

