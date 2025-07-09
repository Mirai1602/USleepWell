"""
Autor: Mayrin Tellez
Fecha: 2025-06-26
Descripcion: Este es el archivo para el registro del usuario. Aqui se definen las funciones
"""

import random
import csv

def GenerarID():
    return random.randint(1000, 9999)
def RegistrarUsuario():
     print("-"*40)
     print("Bienvenido al registro de USleepWell!")
     print("-"*40)
     nombre = input("Por favor, ingresa tu nombre: ")
     apellido = input("Por favor, ingresa tu apellido: ")
     Nacimiento = input("Por favor, ingresa tu fecha de nacimiento (DD/MM/AAAA): ")
     email = input("Por favor, ingresa tu correo electronico: ")
     ValidarDatos(nombre, apellido, Nacimiento, email)
     print(f"Nombre: {nombre}, Apellido: {apellido}, Fecha de Nacimiento: {Nacimiento}, Email: {email}")
     id = GenerarID() #Genera un ID aleatorio
     print(f" Tu ID de usuario es: {id}")
     print("Registro exitoso!")


def GuardarDatos(nombre, apellido, Nacimiento, email, id, Archivo='DatosUsuarios.csv'):
    usuario = (nombre, apellido, Nacimiento, email, id)
    Datos = [usuario[0], usuario[1], usuario[2], usuario[3], usuario[4]] #Lista de los datos en orden
    with open(Archivo, 'a', newline= '' ,encoding='utf-8') as file:
        # Abre el archivo en modo append ('a') para agregar datos sin sobrescribir
        # Si el archivo no existe, se creara automaticamente
        # 'utf-8' es una codificacion comon que maneja caracteres especiales, quiero evitar que la enie no sirva
        writer = csv.writer(file) #esto funciona por la libreria csv
        writer.writerow(Datos) #Aqui esto lo va a imprimir en filitas bien bonitas
        file.seek(0) #Verifica que no existe el archivo, si no existe lo crea
        if file.tell() == 0:
            writer.writerow(usuario)

        writer.writerow(Datos)

    print("Se guardaron tus datos!")
 #Llama a la funcion de validar datos
     

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
print("Registro exitoso!")

RegistrarUsuario()
