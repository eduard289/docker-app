import streamlit as st

st.set_page_config(page_title="Docker Docente", page_icon="🐳", layout="centered")

st.title("🐳 Docker Docente")
st.markdown("### Aprende a construir y entender contenedores")

# --- SECCIÓN 1: GENERADOR DE DOCKERFILES ---
st.header("1. Generador de Dockerfiles")
st.write("Configura tu proyecto y observa cómo se construye la receta.")

lenguaje = st.selectbox("¿Qué entorno utilizas?", ["Python", "Node.js", "Nginx"])
puerto = st.number_input("Puerto a exponer", min_value=1, value=8501)

if lenguaje == "Python":
    dockerfile_code = f"FROM python:3.10-slim\nWORKDIR /app\nCOPY requirements.txt .\nRUN pip install -r requirements.txt\nCOPY . .\nEXPOSE {puerto}\nCMD [\"python\", \"app.py\"]"
elif lenguaje == "Node.js":
    dockerfile_code = f"FROM node:18-alpine\nWORKDIR /app\nCOPY package*.json ./\nRUN npm install\nCOPY . .\nEXPOSE {puerto}\nCMD [\"npm\", \"start\"]"
else:
    dockerfile_code = f"FROM nginx:alpine\nCOPY ./public /usr/share/nginx/html\nEXPOSE {puerto}\nCMD [\"nginx\", \"-g\", \"daemon off;\"]"

st.code(dockerfile_code, language="dockerfile")

st.divider()

# --- SECCIÓN 2: TRADUCTOR DE COMANDOS ---
st.header("2. Traductor de `docker run`")
comando = st.text_input("Pega aquí un comando:", value="docker run -d -p 8080:80 --name servidor nginx")

if comando.startswith("docker run"):
    partes = comando.split()
    for i, p in enumerate(partes):
        if p == "-d": st.info("`-d`: Modo desatendido (segundo plano).")
        elif p == "-p": st.info(f"`-p {partes[i+1]}`: Mapeo de puertos (PC:Contenedor).")
        elif p == "--name": st.info(f"`--name {partes[i+1]}`: Nombre personalizado.")
        elif p == "-v": st.info(f"`-v {partes[i+1]}`: Volumen (Carpeta compartida).")
