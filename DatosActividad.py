import os 
import csv
class NombreActividad: #Vamos a tratar a cada parametro como una clase u objeto
    def __init__(self, nombre_actividad):
        self.nombre_actividad = nombre_actividad
class FechaActividad:
    def __init__(self, fecha_actividad):
        self.fecha_actividad = fecha_actividad

class HoraActividad:
    def __init__(self, hora_actividad): #Cada uno es objeto
        self.hora_actividad = hora_actividad

class DuracionActividad:
    def __init__(self, duracion_actividad):
        self.duracion_actividad = duracion_actividad
class ActividadesUsuario: #Esta clase reune los objetos anteriores
    def __init__(self, nombre_actividad, fecha_actividad, hora_actividad, duracion_actividad):
        self.nombre_actividad = NombreActividad(nombre_actividad) #Estan bien repetitivo los nombre
        #pero es para que se entienda que son objetos y me da miedo cambiarlo jaajaj
        self.fecha_actividad = FechaActividad(fecha_actividad)
        self.hora_actividad = HoraActividad(hora_actividad)
        self.duracion_actividad = DuracionActividad(duracion_actividad) #Mala practica pero aja
class DocCSV: 
    def __init__(self, file, encabezado):
        self.file = file
        self.CrearCSV() #Creo el csv al iniciar la clase
        self.encabezado = encabezado

    def CrearCSV(self):
        if not os.path.exists(self.file):
            with open(self.file, mode='w', newline='', encoding= "UTF-8") as f:
                writer = csv.writer(f)
                writer.writerow(self.encabezado)
               
    def guardar_fila(self, datos):
        with open(self.file, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(datos) #Guarda la nueva actividad en una fila en el CSV 

