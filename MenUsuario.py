from RegistroAgenda import RegistrarAgenda
from VerAgenda import MostrarActividades
from RutinaSleep import HorarioSleep

def MenUsuario(id, nombre_usuario):
    while True:
        print("\n" + "=" * 50)
        print(f"👤 Bienvenido, {nombre_usuario} (ID: {id})")
        print("Selecciona una opción:")
        print("1. Registrar actividad")
        print("2. Mostrar agenda")
        print("3. Editar actividad")
        print("4. Eliminar actividad")
        print("5. Recomendaciones de siesta")
        print("6. Recomendaciones de sueño nocturno")
        print("0. Cerrar sesión")
        opcion = input("Opción: ").strip()

        if opcion == "1":
            RegistrarAgenda(id)
        elif opcion == "2":
            MostrarActividades(id=id)
        elif opcion == "3":
            EditarActividad(id)
        elif opcion == "4":
            EliminarActividad(id)
        elif opcion == "5":
            lapsos = ConsultaAgenda()
            siestas = FiltroDeLapsos(lapsos)
            print("\n🛌 Recomendaciones de siesta:")
            if siestas:
                for fecha, ini, fin in siestas:
                    print(f"📅 {fecha}: Siesta posible entre {ini} y {fin}")
            else:
                print("📭 No se encontraron lapsos ideales para siesta.")
        elif opcion == "6":
            recomendaciones = HorarioSleep(id)
            print("\n🌙 Recomendaciones de sueño nocturno:")
            if recomendaciones:
                for r in recomendaciones:
                    print(f"{r['dia']}: Dormir idealmente a las {r['dormir_ideal']} para levantarse a las {r['levantarse']}")
            else:
                print("📭 No se encontraron datos suficientes para calcular recomendaciones.")
        elif opcion == "0":
            print("👋 Cerrando sesión. ¡Hasta pronto!")
            break
        else:
            print("❌ Opción inválida. Intenta de nuevo.")
