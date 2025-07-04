import streamlit as st
import json
import os
import random
import datetime
import pandas as pd
import matplotlib.pyplot as plt

# Archivos de almacenamiento local
USERS_FILE = "usuarios.json"
ACTIVITIES_FILE = "actividades.json"
SLEEP_FILE = "sueño.json"

# ----------------------------- DATOS DEL USUARIO -----------------------------
def cargar_datos(nombre_archivo):
    if os.path.exists(nombre_archivo):
        with open(nombre_archivo, "r") as f:
            return json.load(f)
    return {}

def guardar_datos(nombre_archivo, datos):
    with open(nombre_archivo, "w") as f:
        json.dump(datos, f, indent=4)

usuarios = cargar_datos(USERS_FILE)
actividades = cargar_datos(ACTIVITIES_FILE)
sueños = cargar_datos(SLEEP_FILE)

# ----------------------------- INICIAR SESIÓN -----------------------------
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

#------------------------------ CALCULAR SIESTAS -----------------------------
def sugerir_siestas(df_acts, ciclos_faltantes):
    if ciclos_faltantes <= 0:
        st.info("¡Felicidades! No necesitas siestas adicionales hoy.")
        return

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
        hueco = (inicio_siguiente - fin_actual).total_seconds() / 60
        if hueco >= 30:
            # Sugerir siesta media hora después de terminar la actividad actual
            sugerencias.append(fin_actual + pd.Timedelta(minutes=30))
            if len(sugerencias) >= ciclos_faltantes:
                break

    # También considerar antes de la primera actividad y después de la última
    primer_inicio = acts_hoy.iloc[0]['inicio_dt']
    if (primer_inicio - pd.to_datetime("07:00:00")).total_seconds() / 60 >= 30:
        sugerencias.insert(0, primer_inicio - pd.Timedelta(minutes=30))
    ultimo_fin = acts_hoy.iloc[-1]['fin_dt']
    if (pd.to_datetime("22:00:00") - ultimo_fin).total_seconds() / 60 >= 30:
        sugerencias.append(ultimo_fin + pd.Timedelta(minutes=30))

    # Limitar sugerencias a los ciclos faltantes
    sugerencias = sugerencias[:ciclos_faltantes]

    if sugerencias:
        st.info("Te sugerimos tomar siestas en los siguientes horarios:")
        for s in sugerencias:
            st.markdown(f"- {s.strftime('%H:%M')}")
    else:
        st.warning("No hay espacios disponibles hoy para sugerir una siesta sin interferir con tus actividades.")


# ----------------------------- INTERFACES -----------------------------
def pagina_inicio():
    st.title("😴 Bienvenido a SleepWell")
    st.markdown("Una forma inteligente de mejorar tu descanso")

    opcion = st.radio("", ["Iniciar sesión", "Registrarse"])

    if opcion == "Iniciar sesión":
        usuario = st.text_input("Usuario")
        contraseña = st.text_input("Contraseña", type="password")
        if st.button("Entrar"):
            if usuario in usuarios and usuarios[usuario]["contraseña"] == contraseña:
                st.session_state.usuario_actual = usuario
                st.success("Inicio de sesión exitoso")
                st.session_state.pagina = "principal"
            else:
                st.error("Usuario o contraseña incorrectos")

    elif opcion == "Registrarse":
        nuevo_usuario = st.text_input("Nuevo usuario")
        nueva_contraseña = st.text_input("Contraseña", type="password")
        trastorno = st.selectbox("¿Padeces algún trastorno del sueño?", ["Ninguno", "Insomnio", "Apnea", "Narcolepsia", "Sonambulismo", "Sindrome de piernas inquietas", "Terrores nocturnos", "Parálisis del sueño", "Trastorno del ritmo circadiano", "Hipersomnia idiopática"])
        edad = st.slider("Edad", 10, 100, 25)
        if st.button("Crear cuenta"):
            if nuevo_usuario in usuarios:
                st.error("El usuario ya existe")
            else:
                usuarios[nuevo_usuario] = {"contraseña": nueva_contraseña, "trastorno": trastorno, "edad": edad}
                guardar_datos(USERS_FILE, usuarios)
                st.success("Cuenta creada con éxito, ahora inicia sesión") 


def pagina_principal():
    usuario = st.session_state.usuario_actual
    st.title(f"🌙 Hola, {usuario}")
    st.markdown("---")

    menu = st.sidebar.radio("Menú", ["Registrar Actividad", "Registrar Sueño", "Calendario y Recomendaciones"])

    if menu == "Registrar Actividad":
        st.header("📅 Añadir actividad diaria")
        fecha = st.date_input("Fecha")
        actividad = st.text_input("Actividad")
        inicio = st.time_input("Hora de inicio")
        fin = st.time_input("Hora de fin")

        if st.button("Guardar actividad"):
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
        st.header("📆 Vista semanal de actividades")

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
                if t2 < t1:
                    t2 += datetime.timedelta(days=1)
                duracion = (t2 - t1).total_seconds() / 60
                ciclos_dormidos += int(duracion // 90)

        st.bar_chart(pd.DataFrame({"Ciclos": [ciclos_dormidos, 7 - ciclos_dormidos]}, index=["Completados", "Faltantes"]))

        if ciclos_dormidos < 7:
            st.warning("No completaste los ciclos de sueño ideales. Aquí tienes algunas sugerencias de siesta:")
            # Sugerencias de siesta
            sugerir_siestas(df_acts, 7 - ciclos_dormidos)

        st.header("💡 Recomendaciones")
        recomendaciones = recomendaciones_generales.copy()
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