import csv
import os

def IniciarSesion(archivo= "DatosUsuarios.csv"):
    print("*" *40)
    print("Inicio de sesion en USleepWell")
    print("*" *40)
    
    if not os.path.exists(archivo):
        print("No hay usuarios registrados aun.")
        return None # No hay sesiones activas
    
    id_usuario = input("Por favor, ingresa tu ID de usuario: ")
    if not id_usuario.isdigit():
        print("El ID debe ser un numero.")
        return None
    with open(archivo, "r", newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            print({list(row.keys())})
            if row['id'] == id_usuario:
                print(f"Bienvenido, {row['nombre']} {row['apellido']}!")
                return row
    print("ID de usuario no encontrado. Por favor, verifica tu ID e intenta nuevamente.")
    return None # No se encontro el usuario
# Llamada a la funcion para iniciar sesion
