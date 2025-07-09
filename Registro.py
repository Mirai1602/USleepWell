"""
Autor: Mayrin Tellez
Fecha: 2025-06-26
Descripcion: Este es el archivo para el registro del usuario. Aqui se definen las funciones
"""
import os
import random
import csv
from datetime import datetime
from MenUsuario import MenUsuario


def GenerarID(existentes):
    while True:
        # Genera un ID aleatorio entre 1000 y 9999
        # Si el ID ya existe, genera uno nuevo
        id = random.randint(1000, 9999)
        if id not in existentes:
            return id
        
def GenerarIDsExistentes(archivo):
    if not os.path.exists(archivo):
        return set()
    with open(archivo, 'r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        return {int(row['id']) for row in reader if 'id' in row}
    
def ValidarEmail(email):
    # Verifica si el email tiene un formato valido
    if '@' in email and '.' in email:
        return True
    else:
        print("El correo electronico no es valido. Por favor, ingresa un correo valido.")
        return False
    
def ValidarFechaNacimiento(fecha):
    try:
        # Verifica si la fecha tiene un formato valido
        datetime.strptime(fecha, '%d/%m/%Y')
        return True
    except ValueError:
        print("La fecha de nacimiento no es valida. Por favor, ingresa una fecha en el formato DD/MM/AAAA.")
        return False

def ValidarDatos(nombre, apellido, Nacimiento, email): #Usa el operador not porque son cadenas, para validarlas
    while not nombre or not apellido or not Nacimiento or not email:
        print("Todos los campos son obligatorios. Por favor, completa todos los datos, para tu registro.")
        if not nombre:
            nombre = input("Por favor, ingresa tu nombre: ")
        if not apellido:
            apellido = input("Por favor, ingresa tu apellido: ")
        if not Nacimiento:
            Nacimiento = input("Por favor, ingresa tu fecha de nacimiento (DD/MM/AAAA): ")
        if not email:
            email = input("Por favor, ingresa tu correo electronico: ")
    return nombre, apellido, Nacimiento, email
def GuardarDatos(nombre, apellido, Nacimiento, email, id, Archivo='DatosUsuarios.csv'):
    usuario = ["id","nombre", "apellido", "Nacimiento", "email"]
    Datos = [id, nombre, apellido, Nacimiento, email] #Lista de los datos en orden
    with open(Archivo, 'a', newline= '' ,encoding='utf-8') as file:
        # Abre el archivo en modo append ('a') para agregar datos sin sobrescribir
        # Si el archivo no existe, se creara automaticamente
        # 'utf-8' es una codificacion comon que maneja caracteres especiales, quiero evitar que la enie no sirva
        writer = csv.writer(file) #esto funciona por la libreria csv
        #writer.writerow(Datos) #Aqui esto lo va a imprimir en filitas bien bonitas
        file.seek(0) #Verifica que no existe el archivo, si no existe lo crea
        if file.tell() == 0:
            writer.writerow(usuario)

        writer.writerow(Datos)
    print("Se guardaron tus datos!")
 
def RegistrarUsuario():
     print("-"*40)
     print("Bienvenido al registro de USleepWell!")
     print("-"*40)
     nombre = input("Por favor, ingresa tu nombre: ")
     apellido = input("Por favor, ingresa tu apellido: ")
     Nacimiento = input("Por favor, ingresa tu fecha de nacimiento (DD/MM/AAAA): ")
     email = input("Por favor, ingresa tu correo electronico: ")
     idsExistenetes= GenerarIDsExistentes('DatosUsuarios.csv') #Genera los IDs existentes del archivo
     id= GenerarID(idsExistenetes) #Genera un ID aleatorio que no exista en el archivo
     ValidarDatos(nombre, apellido, Nacimiento, email)
     print(f"Nombre: {nombre}, Apellido: {apellido}, Fecha de Nacimiento: {Nacimiento}, Email: {email}")
     print(f" Tu ID de usuario es: {id}")
     print("Registro exitoso!")
     GuardarDatos(nombre, apellido, Nacimiento, email, id) #Guarda los datos en el archivo
     MenUsuario(str(id), nombre)
if __name__ == "__main__":
    #RegistrarUsuario()
    pass