<<<<<<< HEAD
from RegistroAgenda import ConsultaAgenda
from datetime import datetime, timedelta #Recuerden que el timedenta permite tratar las fechas como objetos
import csv

def FiltroDeLapsos(lapsos): #para retomar los lapsos de las siestas que se definen en la otra funcion
    SurgeSiesta=[]
    for fecha, inicio, fin in lapsos:
        h_inicio = datetime.strptime(inicio, '%H:%M:%S')
        h_fin = datetime.strptime(fin, '%H:%M:%S')
        duracion = (h_fin - h_inicio).seconds / 60
        if 13 <= h_inicio.hour < 16 and duracion >= 20:
            SurgeSiesta.append((fecha, inicio, fin))
lapsos= ConsultaAgenda()
recomendaciones = FiltroDeLapsos(lapsos)
print("\n Recomendaciones de siesta:")
for fecha, ini, fin in recomendaciones:
    print(f" {fecha}: Siesta posible entre {ini} y {fin}")
def HorarioSleep(ciclos=5):
    #Por defecto dejamos que ciclos sean 5 = 7.5 horas de sueño
    recomendaciones = []
    #Ahora vamos a leer la hora en que el ususario se levanta por dia
    with open("ActividadesUsuario.csv", encoding="UTF-8")as f:
        reader = csv.reader(f)
        encabezado = next(reader) #Ya sabemos la sentencia que necesita para el encabezado
        for fila in reader:
            horaLevantarse = fila[0].strip()
            dia= fila[2].strip()
            try:
                horaDespertar= datetime.strptime(horaLevantarse, "%H:%M")
                duracionSleep = timedelta(minutes=90 * ciclos)
                horaDormir = horaDespertar - duracionSleep
                recomendaciones.append({
                        "dia": dia, #Lo naranja son las palablas claves en el diccionario
                        "levantarse": horaDespertar.strftime("%H:%M"),
                        "dormir_ideal": horaDormir.strftime("%H:%M"),
                        "ciclos": ciclos
                    })
            except:
                print(f" Formato de hora inválido en el registro: {horaLevantarse}")
=======
from RegistroAgenda import ConsultaAgenda
from datetime import datetime, timedelta #Recuerden que el timedenta permite tratar las fechas como objetos
import csv
from collections import defaultdict

def FiltroDeLapsos(lapsos): #para retomar los lapsos de las siestas que se definen en la otra funcion
    SurgeSiesta=[]
    for fecha, inicio, fin, _ in lapsos:
        h_inicio = datetime.strptime(inicio, '%H:%M')
        h_fin = datetime.strptime(fin, '%H:%M')
        duracion = (h_fin - h_inicio).seconds / 60
        if 13 <= h_inicio.hour < 16 and duracion >= 20:
            SurgeSiesta.append((fecha, inicio, fin))
    return SurgeSiesta
lapsos= ConsultaAgenda()
recomendaciones = FiltroDeLapsos(lapsos)
print("\n Recomendaciones de siesta:")
for fecha, ini, fin in recomendaciones:
    print(f" {fecha}: Siesta posible entre {ini} y {fin}")


def HorarioSleep(ciclos=5):
    recomendaciones = []
    fechas_registradas = set()

    with open("ActividadesUsuario.csv", encoding="UTF-8") as f:
        reader = csv.reader(f)
        next(reader)

        for fila in reader:
            try:
                fecha = fila[3].strip()
                hora_levantarse = fila[1].strip()

                # Mostramos valor crudo para inspección
                print(f"🔍 DEBUG — {fecha} | Hora original: {repr(hora_levantarse)}")

                # Limpieza de caracteres ocultos
                hora_limpia = hora_levantarse.replace("\ufeff", "").replace("\n", "").replace("\r", "").strip()

                if fecha not in fechas_registradas:
                    hora_despertar = datetime.strptime(hora_limpia, "%H:%M")
                    duracion_sleep = timedelta(minutes=90 * ciclos)
                    hora_dormir = hora_despertar - duracion_sleep

                    recomendaciones.append({
                        "fecha": fecha,
                        "levantarse": hora_despertar.strftime("%H:%M"),
                        "dormir_ideal": hora_dormir.strftime("%H:%M"),
                        "ciclos": ciclos
                    })

                    fechas_registradas.add(fecha)

            except ValueError as e:
                print(f"❌ ERROR al convertir '{repr(hora_levantarse)}' en {fecha} → {e}")

    return recomendaciones
if __name__ == "__main__":
    recomendaciones = HorarioSleep()
    print("\n🌙 Recomendaciones de sueño nocturno:")
    if recomendaciones:
        for rec in recomendaciones:
            print(f"📅 {rec['fecha']} — 🛌 Dormir ideal: {rec['dormir_ideal']} | 🕒 Levantarse: {rec['levantarse']} | 🌀 Ciclos: {rec['ciclos']}")
    else:
        print("📭 No se encontraron datos suficientes para calcular recomendaciones.")
>>>>>>> Ale
