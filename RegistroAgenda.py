from datetime import datetime
from DatosActividad import  DocCSV
from DatosActividad import ActividadesUsuario

import csv
def RegistrarAgenda():
    print("Bienvenido a la gestión de actividades de USleepWell!")
    print("Por favor, ingresa los siguientes datos para registrar una nueva actividad.")
    nombre_actividad = input("Nombre de la actividad: ")
    fecha_actividad = input("Fecha de la actividad (DD/MM/AAAA): ")
    hora_actividad = input("Hora de la actividad (HH:MM): ")
    duracion_actividad = input("Duración de la actividad (en minutos): ")

    print("Actividad registrada exitosamente!")
    print(f"Nombre: {nombre_actividad}")
    print(f"Fecha: {fecha_actividad}")
    print(f"Hora: {hora_actividad}")
    print(f"Duración: {duracion_actividad} minutos")

    
    actividad = ActividadesUsuario(nombre_actividad, fecha_actividad, hora_actividad, duracion_actividad)
    doc = DocCSV("ActividadesUsuario.csv", ["Actividad", "Fecha", "Hora", "Duración (min)"])
    doc.guardar_fila(actividad.obtener_datos_csv())
RegistrarAgenda()
