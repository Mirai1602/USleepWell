import streamlit as st
import csv
import os
import random
import datetime
import pandas as pd


usuarios_doc = "usuarios.csv"
actividades_doc = "actividades.csv"
sueño_doc = "sueño.csv"

# ----------------------------- Guardar datos -----------------------------
def cargar_datos(nombre_archivo):
    return pd.read_csv(nombre_archivo) if os.path.exists(nombre_archivo) else pd.DataFrame()

def guardar_datos(df, nombre_archivo):
    df.to_csv(nombre_archivo, index=False)

usuario = cargar_datos(usuarios_doc)
actividades = cargar_datos(actividades_doc)
sueño = cargar_datos(sueño_doc)

# ------------------------- Cálculo de edad -------------------------
def calcular_edad(fecha_nacimiento):
    hoy = datetime.date.today()
    return hoy.year - fecha_nacimiento.year - ((hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day))

# ------------------------- Generar ID único -------------------------
def generar_id_unico():
    import random
    return random.randint(1000, 9999)

# ------------------------- Cargar datos -------------------------

if "pagina" not in st.session_state:
    st.session_state.pagina = "inicio"
if "usuario_id" not in st.session_state:
    st.session_state.usuario_id = None

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
    ]
}

# ----------------------------- PÁGINAS -----------------------------
def pagina_inicio():
    st.title("🌙 Bienvenido a SleepWell")
    st.markdown("Una forma inteligente de mejorar tu descanso")

    opcion = st.radio("", ["Iniciar sesión", "Registrarse"])

    if opcion == "Iniciar sesión":
        st.subheader("🔑 Iniciar sesión")
        user_id = st.text_input("Ingresa tu ID de usuario")
        if st.button("Entrar"):
            if not usuario.empty and int(user_id) in usuario["id"].values:
                st.session_state.usuario_id = int(user_id)
                st.success("Inicio de sesión exitoso")
                st.session_state.pagina = "principal"
            else:
                st.error("ID no encontrado")

    elif opcion == "Registrarse":
        st.subheader("📝 Crear cuenta")
        nombre = st.text_input("Nombre", placeholder="Ingresa tu nombre")
        apellido = st.text_input("Apellido", placeholder="Ingresa tu apellido")
        gmail = st.text_input("Correo electrónico", placeholder="Ingresa tu correo electrónico")
        fecha_nac = st.date_input(
            "Fecha de nacimiento",
            min_value=datetime.date(1900, 1, 1),
            max_value=datetime.date.today(),
            value=datetime.date(2000, 1, 1)
        )
        trastorno = st.selectbox("¿Padeces algún trastorno del sueño?", ["Ninguno", "Insomnio", "Apnea", "Narcolepsia", "Sonambulismo", "Sindrome de piernas inquietas", "Terrores nocturnos", "Parálisis del sueño", "Trastorno del ritmo circadiano", "Hipersomnia idiopática"])

        if st.button("Crear cuenta"):
            nuevo_id = generar_id_unico()
            edad = calcular_edad(fecha_nac)
            nuevo_usuario = pd.DataFrame([{
                "id": nuevo_id,
                "nombre": nombre,
                "apellido": apellido,
                "gmail": gmail,
                "fecha_nacimiento": fecha_nac,
                "edad": edad,
                "trastorno": trastorno
            }])
            guardar_datos(nuevo_usuario, usuarios_doc)
            st.success(f"Cuenta creada exitosamente. Tu ID es: {nuevo_id}. Guárdalo para iniciar sesión.")

# ----------------------------- Sugerir siesta -----------------------------

def sugerir_siestas(actividades_user, ciclos_faltantes):
    if actividades_user.empty or "fecha" not in actividades_user.columns:
        st.info("No hay actividades registradas hoy. Puedes tomar una siesta entre 13:00 y 16:00 si lo deseas.")
        return

    hoy = pd.to_datetime(datetime.date.today())
    actividades_user["fecha"] = pd.to_datetime(actividades_user["fecha"], errors="coerce")
    actividades_hoy = actividades_user[actividades_user["fecha"] == hoy]

    if actividades_hoy.empty:
        st.info("No tienes actividades programadas hoy. Considera tomar una siesta entre 13:00 y 16:00.")
        return

    st.subheader("🕒 Sugerencias de siestas")
    actividades_hoy = actividades_hoy.sort_values("inicio")

    actividades_hoy["inicio"] = pd.to_datetime(actividades_hoy["inicio"], format="%H:%M:%S", errors="coerce")
    actividades_hoy["fin"] = pd.to_datetime(actividades_hoy["fin"], format="%H:%M:%S", errors="coerce")

    huecos = []
    for i in range(len(actividades_hoy) - 1):
        fin_actual = actividades_hoy.iloc[i]["fin"]
        inicio_siguiente = actividades_hoy.iloc[i+1]["inicio"]
        duracion = (inicio_siguiente - fin_actual).total_seconds() / 60
        if duracion >= 30:
            huecos.append((fin_actual.time(), inicio_siguiente.time()))

    if huecos:
        st.success("Aquí tienes algunos espacios disponibles para una siesta de 30 a 90 minutos:")
        for inicio, fin in huecos[:ciclos_faltantes]:
            st.markdown(f"- 💤 {inicio.strftime('%H:%M')} a {fin.strftime('%H:%M')}")
    else:
        st.warning("No hay espacios disponibles hoy para sugerir siestas entre tus actividades.")

# ----------------------------- PÁGINA PRINCIPAL -----------------------------

def pagina_principal():
    usuario_id = st.session_state.usuario_id

    menu = st.sidebar.radio("Menú", ["Registrar Actividad", "Registrar Sueño", "Calendario y Recomendaciones", "Ver actividades"])

    user_info = usuario[usuario["id"] == st.session_state.usuario_id].iloc[0]
    nombre = user_info["nombre"]
    trastorno = user_info["trastorno"]

    st.title(f"🌙 Hola, {nombre}")
    st.markdown("---")

    if menu == "Registrar Actividad":
        st.header("📅 Añadir actividad diaria")
        fecha = st.date_input("Fecha")
        actividad = st.text_input("Actividad")
        inicio = st.slider(
            "Hora de inicio de la actividad",
            min_value=datetime.time(0, 0),
            max_value=datetime.time(23, 59),
            value=datetime.time(22, 0),
            step=datetime.timedelta(minutes=1)
            )
        fin = st.slider(
            "Hora de fin de la actividad",
            min_value=datetime.time(0, 0),
            max_value=datetime.time(23, 59),
            value=datetime.time(22, 0),
            step=datetime.timedelta(minutes=1)
            )

        if st.button("Guardar actividad"):
            nueva = pd.DataFrame([{
                "id": st.session_state.usuario_id,
                "fecha": fecha,
                "actividad": actividad,
                "inicio": inicio,
                "fin": fin
            }])
            actividades_actualizadas = pd.concat([actividades, nueva], ignore_index=True)
            guardar_datos(actividades_actualizadas, actividades_doc)
            st.success("Actividad guardada correctamente")

    elif menu == "Registrar Sueño":
        st.header("🛌 Registrar horas de sueño")
        fecha = st.date_input("Fecha de sueño")
        dormir = st.slider(
            "Hora en que dormiste",
            min_value=datetime.time(0, 0),
            max_value=datetime.time(23, 59),
            value=datetime.time(22, 0),
            step=datetime.timedelta(minutes=1)
            )
        despertar = st.slider(
            "Hora en que despertaste",
            min_value=datetime.time(0, 0),
            max_value=datetime.time(23, 59),
            value=datetime.time(22, 0),
            step=datetime.timedelta(minutes=1)
            )

        if st.button("Guardar sueño"):
            nuevo = pd.DataFrame([{
                "id": st.session_state.usuario_id,
                "fecha": fecha,
                "dormir": dormir,
                "despertar": despertar
            }])
            sueño_actualizado = pd.concat([sueño, nuevo], ignore_index=True)
            guardar_datos(sueño_actualizado, sueño_doc)
            st.success("Sueño registrado correctamente")

    elif menu == "Ver actividades":
        st.header("📊 Actividades registradas")
        if "id" in actividades.columns:
            act_user = actividades[actividades["id"] == st.session_state.usuario_id]

            if not act_user.empty:
                act_user['fecha'] = pd.to_datetime(act_user['fecha'], errors='coerce')
                act_user = act_user.sort_values('fecha')
                st.dataframe(act_user)
            else:
                st.info("Aún no has registrado actividades.")
        else:
            st.info("No hay actividades registradas.")

    elif menu == "Calendario y Recomendaciones":
        st.header("📆 Historial y ciclos de sueño")

        if "id" in sueño.columns:
            sueño_user = sueño[sueño["id"] == st.session_state.usuario_id]
        else:
            sueño_user = pd.DataFrame()

        if sueño_user.empty:
            st.info("Aún no has registrado tus horas de sueño.")
        else:
            st.subheader("📄 Historial de sueño")
            historial = []
        
            ciclos_dormidos = 0
            for _, row in sueño_user.iterrows():
                fecha = row["fecha"]
                dormir = datetime.datetime.strptime(row['dormir'], "%H:%M:%S")
                despertar = datetime.datetime.strptime(row['despertar'], "%H:%M:%S")

                if despertar < dormir:
                    despertar += datetime.timedelta(days=1)
                duracion = (despertar - dormir).total_seconds() / 60
                ciclos = int(duracion // 90)
                ciclos_dormidos += ciclos
                historial.append({
                    "fecha": fecha,
                    "dormir": dormir.strftime("%H:%M:%S"),
                    "despertar": despertar.strftime("%H:%M:%S"),
                    "duracion": f"{int(duracion // 60)} horas {int(duracion % 60)} minutos",
                    "ciclos": ciclos
                })
            
            df_historial = pd.DataFrame(historial)
            df_historial['fecha'] = pd.to_datetime(df_historial['fecha'], errors='coerce')
            df_historial = df_historial.sort_values('fecha', ascending=False)
            st.dataframe(df_historial)

            if df_historial.empty:
                st.info("No hay registros de sueño.")
            else:
                st.success(f"Has dormido un total de {ciclos_dormidos} ciclos de sueño (90 minutos cada uno).")

            st.header("🌀 Ciclos de sueño")
            completados = min(ciclos_dormidos, 7)
            faltantes = max(0, 7 - completados)
            st.metric("Ciclos completados", f"{completados}/7")
            st.progress(completados / 7)

            if ciclos_dormidos < 7:
                st.warning("No completaste los ciclos ideales. Se recomiendan siestas de 90 minutos.")
                actividades_user = actividades[actividades["id"] == usuario_id] if "id" in actividades.columns else pd.DataFrame()
                sugerir_siestas(actividades_user, faltantes)

        st.header("💡 Recomendaciones")
        recomendaciones = recomendaciones_generales.copy()

        user_info = usuario[usuario["id"] == st.session_state.usuario_id].iloc[0]
        trastorno = user_info["trastorno"]

        if trastorno.lower() in recomendaciones_trastornos:
            recomendaciones += recomendaciones_trastornos[trastorno.lower()]

        recomendaciones_mostrar = random.sample(recomendaciones, 5)
        for rec in recomendaciones_mostrar:
            st.markdown(f"- {rec}")

# ----------------------------- CARGAR PÁGINAS -----------------------------

if st.session_state.pagina == "inicio":
    pagina_inicio()
elif st.session_state.pagina == "principal":
    pagina_principal()