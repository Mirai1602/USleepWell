from RegistroAgenda import RegistrarAgenda, ConsultaAgenda, EditarActividad, EliminarActividad
from VerAgenda import MostrarActividades
from RutinaSleep import HorarioSleep, FiltroDeLapsos

def MenUsuario(id, nombre):
    while True:
        print("\n" + "=" * 50)
        print(f"👤 Bienvenido, {nombre} (ID: {id})")
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
            recomendaciones = HorarioSleep()
            print("\n🌙 Recomendaciones de sueño nocturno:")
            if recomendaciones:
                for rec in recomendaciones:
                    print(f"📅 {rec['fecha']} — 🛌 Dormir ideal: {rec['dormir_ideal']} | 🕒 Levantarse: {rec['levantarse']} | 🌀 Ciclos: {rec['ciclos']}")
            else:
                print("📭 No se encontraron datos suficientes para calcular recomendaciones.")

        else:
            print("❌ Opción inválida. Intenta de nuevo.")
