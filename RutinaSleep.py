from RegistroAgenda import ConsultaAgenda
from datetime import datetime, timedelta
import csv

def FiltroDeLapsos(lapsos):
    SurgeSiesta = []
    for fecha, inicio, fin, _ in lapsos:
        try:
            h_inicio = datetime.strptime(inicio, '%H:%M')
            h_fin = datetime.strptime(fin, '%H:%M')
            duracion = (h_fin - h_inicio).seconds / 60
            if 13 <= h_inicio.hour < 16 and duracion >= 20:
                SurgeSiesta.append((fecha, inicio, fin))
        except ValueError:
            continue
    return SurgeSiesta


def HorarioSleep(id_usuario, ciclos=5):
    recomendaciones = []

    try:
        with open("ActividadesUsuario.csv", encoding="UTF-8") as f:
            reader = csv.reader(f)
            encabezado = next(reader)  # Salta el encabezado

            for fila in reader:
                if fila[0] != str(id_usuario):
                    continue  # Solo procesa actividades del usuario actual

                horaLevantarse = fila[1].strip()  # Hora de levantarse
                dia = fila[3].strip()             # Fecha de la actividad

                try:
                    horaDespertar = datetime.strptime(horaLevantarse, "%H:%M")
                    duracionSleep = timedelta(minutes=90 * ciclos)
                    horaDormir = horaDespertar - duracionSleep

                    recomendaciones.append({
                        "dia": dia,
                        "levantarse": horaDespertar.strftime("%H:%M"),
                        "dormir_ideal": horaDormir.strftime("%H:%M"),
                        "ciclos": ciclos
                    })
                except ValueError:
                    print(f"❌ Formato de hora inválido en el registro: {horaLevantarse}")

    except FileNotFoundError:
        print("❌ No se encontró el archivo de actividades.")
        return []

    return recomendaciones

# Solo para pruebas directas
if __name__ == "__main__":
    lapsos = ConsultaAgenda()
    recomendaciones = FiltroDeLapsos(lapsos)
    print("\n🛌 Recomendaciones de siesta:")
    for fecha, ini, fin in recomendaciones:
        print(f"📅 {fecha}: Siesta posible entre {ini} y {fin}")

    print("\n🌙 Recomendaciones de sueño nocturno:")
    for r in HorarioSleep():
        print(f"{r['dia']}: Dormir idealmente a las {r['dormir_ideal']} para levantarse a las {r['levantarse']}")