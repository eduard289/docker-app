import streamlit as st
import time

st.set_page_config(page_title="Docker Demo", page_icon="🐳", layout="centered")

st.title("🐳 Docker Demo")
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
        
    # --- BOTÓN DE SIMULACIÓN DINÁMICO ---
    if st.button("🚀 Simular Ejecución"):
        with st.spinner("Hablando con el motor de Docker..."):
            time.sleep(1.5) # Pausa dramática para el vídeo
            
            # Intentamos extraer el puerto local para hacerlo más realista
            puerto_mostrar = "80" # Puerto por defecto si no encuentra otro
            if "-p" in partes:
                idx = partes.index("-p")
                if idx + 1 < len(partes):
                    # Extrae el '8080' de '8080:80'
                    puerto_mostrar = partes[idx+1].split(":")[0]

            # El f-string inyecta el comando exacto que has pegado
            st.code(f"""
$ {comando}
Unable to find image locally...
Pulling from library...
a2abf6c4d29d: Pull complete
b3117d2fc40a: Pull complete
Digest: sha256:b4b7...
Status: Downloaded newer image
8f1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7q8r9s0t

✅ ¡Éxito! Contenedor ejecutándose en segundo plano.
🌐 Ejecución en: http://localhost:{puerto_mostrar}
            """, language="bash")
            
            st.balloons()
            st.success("Compilación comandos en terminal.")

# --- SECCIÓN 3: DOCKER COMPOSE Y EXPLICACIONES ---
st.divider()
st.header("3. Generador de Docker Compose")
st.write("¿Tienes varios contenedores? Orquestalos con `docker-compose.yml`.")

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
    
    with st.expander("📖 ¿Qué hace exactamente este archivo?"):
        st.markdown("""
        * **`services:`**: Define las máquinas virtuales que se encenderán juntas: `web` y `cache`.
        * **`depends_on:`**: Asegura que la caché de Redis se inicie antes que la aplicación web.
        * **`image: redis:alpine`**: Descarga una imagen oficial y ligera de Redis sin necesidad de un Dockerfile propio.
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
    depends_on:
      - db

  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_PASSWORD=secreta
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
"""
    st.code(compose_code, language="yaml")
    
    with st.expander("📖 ¿Qué hace exactamente este archivo?"):
        st.markdown("""
        * **`environment:`**: Configura variables de entorno como contraseñas de forma segura.
        * **`volumes:`**: Crea persistencia de datos. Si el contenedor se apaga, la base de datos no se borra.
        * **Red Interna:** Docker crea automáticamente una red privada donde la `api` puede hablar con la `db` usando solo su nombre.
        """)

# --- FOOTER PERSONALIZADO ---
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: grey;'>Diseñado por Jose Luis Asenjo</div>", 
    unsafe_allow_html=True
)
