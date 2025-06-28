"""
Author: Mayrin Tellez
Date: 2025-06-26
Description: This is the file for the first entry menu of the program. Which describes the opcions
that the user has to choose from.
"""
from Registro import RegistrarUsuario #Importamos la funcion de registro de usuario
def MenuPrincipal():
    print("-"*40)
    print("Bienvenido a USleepWell!")
    print("-"*40)
    print("Opcion 1: Registrarte")
    print("Opcion 2: Iniciar sesión") #Aqui van las funciones de inicio de sesion
    print("Opcion 3: Registrar tu agenda") #Aqui van las funciones de Gestion de actividades
    print("Opcion 4: Ver tu rutina de sueño") # aqui van las funciones de la rutina de sueño
    print("Opcion 5: Salir del programa")
    opcion = 0 #Variable para controlar el menu

    #While para controlar el menu 
    while opcion != 5:
        MenuPrincipal()
        try:
            opcion = int(input("Selecciona una opcion: "))
        except ValueError: #Try error para el ususario no ponga otra cosa
            print("Por favor, ingresa una opcion válida.")
        continue
        if opcion == 1:
            RegistrarUsuario() #Aqui van las funciones de registro de usuario
        if opcion == 2:
            InicioSesion() #Aqui van las funciones de inicio de sesion
        if opcion == 3:
            RegistrarAgenda() #Aqui van las funciones de gestion de actividades
        if opcion == 4:
            VerRutina() #Aqui van las funciones de la rutina de sueño
        if opcion == 5:
            print("Gracias por usar USleepWell. ¡Hasta luego!")
