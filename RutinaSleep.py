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