from RegistrarAgenda import RegistrarAgenda
from VerAgenda import MostrarActividades
from Recomendaciones import VerRecomendaciones
from Alarma import ProgramarAlarma

def MenuUsuario(id, nombre):
    while True:
        print(f"\n👤 Menú de {nombre}")
        print("-" * 40)
        print("1. Registrar actividad")
        print("2. Ver mi agenda")
        print("3. Programar alarma")
        print("4. Ver recomendaciones")
        print("5. Cerrar sesión")
        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            RegistrarAgenda(id)
        elif opcion == "2":
            MostrarActividades(id)
        elif opcion == "3":
            ProgramarAlarma(id)
        elif opcion == "4":
            VerRecomendaciones(id)
        elif opcion == "5":
            print("🔒 Sesión cerrada.")
            break
        else:
            print("❌ Opción inválida.")
