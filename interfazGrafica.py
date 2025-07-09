import streamlit as st
import json
import os
import random
from datetime import date, datetime
import pandas as pd
import csv
from DatosUsuario import Usuario

# ----------------------------- INICIAR SESIÓN PÁGINA -----------------------------
if "pagina" not in st.session_state:
    st.session_state.pagina = "inicio"
if "usuario_actual" not in st.session_state:
    st.session_state.usuario_actual = None

# ----------------------------- RECOMENDACIONES -----------------------------
recomendaciones_generales = [
    "Evita el uso de pantallas al menos 1 hora antes de dormir.",
    "Mantén una rutina constante para acostarte y levantarte.",
    "Haz ejercicio regularmente, pero no justo antes de dormir.",
    "Evita consumir cafeína en la tarde o noche.",
    "Mantén tu habitación oscura, silenciosa y fresca."
]

recomendaciones_trastornos = {
    "insomnio": [
        "Prueba con ejercicios de respiración antes de dormir.",
        "Evita las siestas prolongadas durante el día.",
        "Practica meditación o técnicas de relajación.",
        "Evita comer en grandes cantidades antes de dormir.",
        "Consulta con un especialista si los síntomas persisten."
    ],
    "apnea": [
        "Evita dormir boca arriba.",
        "Mantén un peso saludable.",
        "Evita alcohol y sedantes.",
        "Consulta sobre el uso de CPAP.",
        "Acude a un especialista del sueño."
    ],
    "narcolepsia": [
        "Evita cafeína, alcohol y tabaco.",
        "Establece una rutina de sueño relajante.",
        "Haz ejercicio moderado durante el día.",
        "Aplica masajes o baños tibios en las piernas antes de acostarte.",
        "Consulta si necesitas suplementos de hierro o dopaminérgicos."
    ],
    "sonambulismo": [
        "Mantén un ambiente seguro para evitar accidentes.",
        "Evita el estrés y la privación de sueño.",
        "Mantén una rutina nocturna calmada.",
        "Evita el consumo de alcohol y drogas.",
        "Consulta con un especialista si los episodios son frecuentes."
    ],
    "sindrome de piernas inquietas": [
        "Evita cafeína y alcohol.",
        "Mantén una rutina de sueño regular.",
        "Haz ejercicios suaves como estiramientos o yoga.",
        "Aplica calor o frío en las piernas antes de dormir.",
        "Consulta si necesitas suplementos de hierro o magnesio."
    ],
    "terrores nocturnos": [
        "Mantén un ambiente seguro y cómodo para dormir.",
        "Evita el estrés y la privación de sueño.",
        "Practica técnicas de relajación antes de acostarte.",
        "Evita el consumo de alcohol y drogas.",
        "Consulta con un especialista si los episodios son frecuentes."
    ],
    "parálisis del sueño": [
        "Mantén una rutina de sueño regular.",
        "Evita dormir boca arriba.",
        "Practica técnicas de relajación antes de acostarte.",
        "Reduce el estrés y la ansiedad con meditación o journaling.",
        "Consulta con un especialista si los episodios son frecuentes."
    ],
    "trastorno del ritmo circadiano": [
        "Ajusta gradualmente tus horarios antes de un viaje o cambio de turno.",
        "Evita la exposición a luz brillante por la noche.",
        "Usa cortinas opacas para bloquear la luz.",
        "Consulta sobre el uso de melatonina.",
        "Manten horarios regulares incluso los fines de semana."
    ],
    "hipersomnia idiopática": [
        "Mantén una rutina de sueño estricta.",
        "Evita comidas pesadas y alcohol por la noche.",
        "Haz ejercicio moderado durante el día.",
        "Consulta si necesitas medicamentos para regular el sueño.",
        "Practica técnicas de relajación para reducir la somnolencia."
    ]
}

# ----------------------------- CALCULAR SIESTAS -----------------------------
def sugerir_siestas(df_acts, ciclos_faltantes):
    if ciclos_faltantes <= 0:
        st.info("¡Felicidades! No necesitas siestas adicionales hoy.")
        return
    
    # Definir rango razonable para siestas
    hora_min = pd.to_datetime("07:00:00")
    hora_max = pd.to_datetime("18:00:00")

    # Filtrar actividades del día actual
    hoy = pd.Timestamp.today().normalize()
    acts_hoy = df_acts[df_acts['fecha'] == hoy]
    if acts_hoy.empty:
        # Si no hay actividades, sugerir siesta en cualquier momento razonable
        st.info("No tienes actividades registradas hoy. Puedes tomar una siesta cuando lo desees, preferiblemente entre 13:00 y 16:00.")
        return

    # Ordenar actividades por hora de inicio
    acts_hoy = acts_hoy.sort_values('inicio')
    sugerencias = []
    # Convertir horas a datetime para comparar
    acts_hoy['inicio_dt'] = pd.to_datetime(acts_hoy['inicio'], format="%H:%M:%S")
    acts_hoy['fin_dt'] = pd.to_datetime(acts_hoy['fin'], format="%H:%M:%S")

    # Buscar huecos entre actividades
    for i in range(len(acts_hoy) - 1):
        fin_actual = acts_hoy.iloc[i]['fin_dt']
        inicio_siguiente = acts_hoy.iloc[i+1]['inicio_dt']
            # Sugerir siesta de 30 minutos justo después de la actividad actual
        posible_inicio = max(fin_actual + pd.Timedelta(minutes=1), hora_min)
        posible_fin = posible_inicio + pd.Timedelta(minutes=30)
        while posible_fin <= min(inicio_siguiente, hora_max):
            if (inicio_siguiente - posible_inicio).total_seconds() / 60 >= 30:
                sugerencias.append((posible_inicio, posible_fin))
                if len(sugerencias) >= ciclos_faltantes:
                    break
            posible_inicio += pd.Timedelta(minutes=1)
            posible_fin = posible_inicio + pd.Timedelta(minutes=30)
        if len(sugerencias) >= ciclos_faltantes:
            break

    # También considerar antes de la primera actividad y después de la última
    primer_inicio = acts_hoy.iloc[0]['inicio_dt']
    siesta_fin = primer_inicio - pd.Timedelta(minutes=1)
    siesta_inicio = siesta_fin - pd.Timedelta(minutes=30)
    if (primer_inicio - hora_min).total_seconds() / 60 >= 30 and hora_min <= siesta_inicio <= hora_max and hora_min <= siesta_fin <= hora_max:
        sugerencias.insert(0, (siesta_inicio, siesta_fin))

    #Después de la última actividad
    ultimo_fin = acts_hoy.iloc[-1]['fin_dt']
    siesta_inicio = ultimo_fin + pd.Timedelta(minutes=30)
    siesta_fin = siesta_inicio + pd.Timedelta(minutes=30)
    if (hora_max - ultimo_fin).total_seconds() / 60 >= 30 and hora_min <= siesta_inicio <= hora_max and hora_min <= siesta_fin <= hora_max:
        sugerencias.append((siesta_inicio, siesta_fin))

    # Limitar sugerencias a los ciclos faltantes
    sugerencias = sugerencias[:ciclos_faltantes]

    if sugerencias:
        st.info("Te sugerimos tomar siestas en los siguientes horarios:")
        for inicio, fin in sugerencias:
            st.markdown(f"- De {inicio.strftime('%H:%M')} a {fin.strtime('%H:%M')}")
    else:
        st.warning("No hay espacios disponibles hoy para sugerir una siesta sin interferir con tus actividades.")


# ----------------------------- INTERFACES -----------------------------

def GenerarID(existentes):
    id = random.randint(1000, 9999)
    if id not in existentes:
                return id

def GenerarIDsExistentes(archivo):
    if not os.path.exists(archivo):
        return set()
    with open(archivo, 'r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        return {int(row['id']) for row in reader if 'id' in row}
    
def GuardarDatos(archivo, datos):
    with open(archivo, "w", newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=["ID", "Nombre", "Apellido", "Gmail", "Trastorno", "Edad"])
        writer.writeheader()
        for nombre, info in datos.items():
            writer.writerow({
                "ID": info["id"],
                "Nombre": nombre.split()[0],
                "Apellido": nombre.split()[1] if len(nombre.split()) > 1 else "",
                "Gmail": info["gmail"],
                "Trastorno": info["trastorno"],
                "Edad": info["edad"]
            })

def pagina_inicio():
    st.title("🌙 Bienvenido a SleepWell")
    st.markdown("Una forma inteligente de mejorar tu descanso")

    opcion = st.radio("¿Qué deseas hacer?", ["Iniciar sesión", "Registrarse"], horizontal=True)
    st.write("")

# ----------------------------- INICIAR SESIÓN / REGISTRARSE -----------------------------

    if opcion == "Iniciar sesión":
        st.subheader("🔑 Iniciar sesión")

        archivo = "DatosUsuarios.csv"

        if not os.path.exists(archivo):
            st.error("No hay usuarios registrados. Por favor, regístrate primero.")
        else:
            id_usuario = st.text_input("ID de usuario", placeholder="Ingresa tu ID de usuario")

            if st.button("Entrar"):
                if not id_usuario:
                    st.error("Por favor, ingresa tu ID de usuario.")
                elif not id_usuario.isdigit():
                    st.error("El ID de usuario debe ser un número.")
                else:
                    with open(archivo, "r", newline='', encoding='utf-8') as file:
                        reader = csv.DictReader(file)
                        usuario_encontrado = False

                        for row in reader:
                            if row["ID"] == id_usuario:
                                st.session_state.usuario_actual = row["Nombre"]
                                st.session_state.pagina = "principal"
                                st.success(f"Bienvenido, {st.session_state.usuario_actual}!")
                                usuario_encontrado = True
                                break

                        if not usuario_encontrado:
                            st.error("ID de usuario no encontrado. Por favor, verifica tu ID.")

        if "usuario_actual" in st.session_state and st.session_state.usuario_actual:
            st.success(f"Ya has iniciado sesión como {st.session_state.usuario_actual}.")

        st.write("¿No tienes una cuenta? Regístrate para empezar a usar SleepWell.")

    elif opcion == "Registrarse":
        st.subheader("📝 Crear cuenta")
        nuevo_usuario_nombre = st.text_input("Nombre", placeholder="¿Cómo te llamas?")
        nuevo_usuario_apellido = st.text_input("Apellido", placeholder="¿Cuál es tu apellido?")
        nuevo_usuario = f"{nuevo_usuario_nombre} {nuevo_usuario_apellido}".strip()

        gmail_usuario = st.text_input("Correo electrónico", placeholder="Ingresa tu correo electrónico")
        
        fecha_nacimiento = st.date_input(
        "Fecha de nacimiento",
        min_value=date(1900, 1, 1),
        max_value=date.today()
        )
        hoy = date.today()
        edad = hoy.year - fecha_nacimiento.year - ((hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day))

        trastorno = st.selectbox("¿Padeces algún trastorno del sueño?", ["Ninguno", "Insomnio", "Apnea", "Narcolepsia", "Sonambulismo", "Sindrome de piernas inquietas", "Terrores nocturnos", "Parálisis del sueño", "Trastorno del ritmo circadiano", "Hipersomnia idiopática"])

        if st.button("Crear cuenta"):
            if not nuevo_usuario or not gmail_usuario or not trastorno or not edad:
                st.error("Todos los campos son obligatorios")
            if not gmail_usuario.endswith("@gmail.com"):
                    st.error("El correo electrónico debe ser de Gmail")
            if nuevo_usuario in Usuario:
                st.error("El usuario ya existe")
            else:
                id_usuario = GenerarID()
                Usuario[nuevo_usuario] = {"id": id_usuario, "gmail":gmail_usuario, "trastorno": trastorno, "edad": edad}
                GuardarDatos("DatosUsuarios.csv", Usuario)
                st.session_state.usuario_actual = nuevo_usuario
                st.session_state.pagina = "principal"
                st.success(f"Cuenta creada con éxito. Bienvenido, {nuevo_usuario}!")

def pagina_principal():
    usuario = st.session_state.usuario_actual
    st.title(f"🌙 Hola, {usuario}")
    st.markdown("---")

    menu = st.sidebar.radio("Menú", ["Registrar Actividad", "Registrar Sueño", "Calendario y Recomendaciones"])

    if menu == "Registrar Actividad":
        st.header("📅 Añadir actividad diaria")
        fecha = st.date_input("Fecha")
        actividad = st.text_input("Actividad", placeholder="Ejemplo: Estudiar, Hacer ejercicio, Leer")
        inicio = st.time_input("Hora de inicio")
        fin = st.time_input("Hora de fin")

        if st.button("Guardar actividad"):
            if not actividad or not inicio or not fin:
                st.error("Todos los campos son obligatorios")
            else:
                actividades.setdefault(usuario, []).append({"fecha": str(fecha), "actividad": actividad, "inicio": str(inicio), "fin": str(fin)})
                guardar_datos(ACTIVITIES_FILE, actividades)
                st.success("Actividad guardada correctamente")

    elif menu == "Registrar Sueño":
        st.header("🛌 Registrar horas de sueño")
        fecha = st.date_input("Fecha de sueño")
        dormir = st.time_input("Hora en que dormiste")
        despertar = st.time_input("Hora en que despertaste")

        if st.button("Guardar sueño"):
            sueños.setdefault(usuario, []).append({"fecha": str(fecha), "dormir": str(dormir), "despertar": str(despertar)})
            guardar_datos(SLEEP_FILE, sueños)
            st.success("Sueño registrado correctamente")

    elif menu == "Calendario y Recomendaciones":
        st.header("📆 Bienvenido a la gestión de actividades de USleepWell!")

        df_acts = pd.DataFrame(actividades.get(usuario, []))
        df_acts['fecha'] = pd.to_datetime(df_acts['fecha'])
        df_acts = df_acts.sort_values('fecha')
        st.dataframe(df_acts)

        st.header("📊 Ciclos de sueño")
        df_sueños = pd.DataFrame(sueños.get(usuario, []))
        ciclos_dormidos = 0
        if not df_sueños.empty:
            for _, row in df_sueños.iterrows():
                t1 = datetime.datetime.strptime(row['dormir'], "%H:%M:%S")
                t2 = datetime.datetime.strptime(row['despertar'], "%H:%M:%S")
                #calcula cuánto se durmió
                if t2 < t1:
                    t2 += datetime.timedelta(days=1)
                duracion = (t2 - t1).total_seconds() / 60 #calcula la diferencia de horas, lo convierte a segundos y finalmente a minutos
                ciclos_dormidos += int(duracion // 90) #toma el total de minutos y lo divide por 90 para obtener los ciclos completos

        st.bar_chart(pd.DataFrame({"Ciclos": [ciclos_dormidos, 7 - ciclos_dormidos]}, index=["Completados", "Faltantes"]))

        if ciclos_dormidos < 7:
            st.warning("No completaste los ciclos de sueño ideales. Aquí tienes algunas sugerencias de siesta:")
            # Sugerencias de siesta
            sugerir_siestas(df_acts, 7 - ciclos_dormidos)

        st.header("💡 Recomendaciones")
        trastorno = usuarios[usuario].get("trastorno")
        if trastorno in recomendaciones_trastornos:
            recomendaciones += recomendaciones_trastornos[trastorno]

        recomendaciones_mostrar = random.sample(recomendaciones, 5)
        for rec in recomendaciones_mostrar:
            st.markdown(f"- {rec}")

# ----------------------------- RENDER -----------------------------

if st.session_state.pagina == "inicio":
    pagina_inicio()
elif st.session_state.pagina == "principal":
    pagina_principal()
    recomendaciones = recomendaciones_generales.copy()