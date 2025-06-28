#Tiene su propia clase porque se van a guardar en disco
import csv
import Registro
class Usuario:
    def __init__(self, nombre, apellido, nacimiento, email, id):
        self.nombre = nombre
        self.apellido = apellido
        self.nacimiento = nacimiento
        self.email = email
        self.id = id