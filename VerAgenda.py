import csv
import os

def MostrarActividades(archivo="ActividadesUsuario.csv", id=None):
    print("\n📅 Tus actividades programadas:")
    print("-" * 40)

    if not os.path.exists(archivo):
        print("❌ No se encontró el archivo de actividades.")
        return

    actividades_encontradas = False

    with open(archivo, "r", newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if id is None or row.get("id") == str(id):
                actividad = row.get("Actividad", "Sin nombre")
                hora = row.get("Hora", "Sin hora")
                fecha = row.get("Fecha", "Sin fecha")
                duracion = row.get("Duración (min)", "?")
                print(f"📆 {fecha} | 🕒 {hora} - {actividad} ({duracion} min)")
                actividades_encontradas = True

    if not actividades_encontradas:
        print("📭 No tienes actividades registradas.")
