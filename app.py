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
# --- SECCIÓN 3: DOCKER COMPOSE Y EXPLICACIONES ---
st.divider()
st.header("3. Generador de Docker Compose")
st.write("¿Tienes varios contenedores (ej. una Web y una Base de Datos)? Orquístalos con `docker-compose.yml`.")

stack = st.selectbox("Elige tu Stack (Conjunto de tecnologías):", ["Python + Redis (Caché rápida)", "Node.js + PostgreSQL (Base de datos relacional)"])

if stack == "Python + Redis (Caché rápida)":
    compose_code = """version: '3.8'
services:
  web:
    build: .
    ports:
      - "8000:8000"
    depends_on:
      - cache
  
  cache:
    image: redis:alpine
    ports:
      - "6379:6379"
"""
    st.code(compose_code, language="yaml")
    
    with st.expander("📖 ¿Qué hace exactamente este archivo? (Haz clic para leer)"):
        st.markdown("""
        * **`version: '3.8'`**: Indica la versión del formato de Compose.
        * **`services:`**: Aquí definimos las "máquinas" que vamos a encender. En este caso son dos: `web` y `cache`.
        * **`build: .`**: Le dice al servicio `web` que busque el `Dockerfile` en esta misma carpeta y construya la imagen.
        * **`depends_on:`**: Crea un orden de encendido. Le dice a Docker: *"No arranques la web hasta que la caché de Redis esté lista"*.
        * **`image: redis:alpine`**: El servicio `cache` no necesita un Dockerfile propio, simplemente descarga la imagen oficial de Redis ya hecha de internet.
        """)

elif stack == "Node.js + PostgreSQL (Base de datos relacional)":
    compose_code = """version: '3.8'
services:
  api:
    build: .
    ports:
      - "3000:3000"
    environment:
      - DB_HOST=db
      - DB_USER=usuario
      - DB_PASS=secreta
    depends_on:
      - db

  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_USER=usuario
      - POSTGRES_PASSWORD=secreta
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
"""
    st.code(compose_code, language="yaml")
    
    with st.expander("📖 ¿Qué hace exactamente este archivo? (Haz clic para leer)"):
        st.markdown("""
        * **`environment:`**: Inyecta variables de entorno (como contraseñas) de forma segura en los contenedores. Fíjate que la `api` se conecta a la base de datos usando `DB_HOST=db` (el nombre del servicio funciona como una dirección IP interna mágica en Docker).
        * **`volumes:`**: Al final del archivo se crea un volumen llamado `postgres_data`. Esto es vital: si apagas el contenedor de PostgreSQL, los datos de tus usuarios **no se borrarán**, quedarán guardados en ese volumen para la próxima vez que lo enciendas.
        """)

st.success("🚀 **Tip para tu vídeo:** Muestra cómo al desplegar un `docker-compose.yml`, todos los servicios se conectan automáticamente a la misma red interna de Docker, lo que garantiza seguridad y privacidad entre ellos.")
