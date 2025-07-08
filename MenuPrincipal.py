"""
Author: Mayrin Tellez
Date: 2025-06-26
Description: This is the file for the first entry menu of the program. Which describes the opcions
that the user has to choose from.
"""
from Registro import RegistrarUsuario
from InicioSesion import IniciarSesion
from MenUsuario import MenUsuario

def MenuPrincipal():
    while True:
        print("\n" + "=" * 40)
        print("🌙 Bienvenido a USleepWell")
        print("=" * 40)
        print("1. Registrar nuevo usuario")
        print("2. Iniciar sesión")
        print("3. Salir")
        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            RegistrarUsuario()
        elif opcion == "2":
            usuario = IniciarSesion()
            if usuario:
                MenUsuario(usuario["ID"], usuario["Nombre"])
        elif opcion == "3":
            print("👋 ¡Hasta luego!")
            break
        else:
            print("❌ Opción inválida. Intenta de nuevo.")

MenuPrincipal()