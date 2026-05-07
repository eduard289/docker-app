# docker-app
# Docker Demo: Laboratorio Interactivo de Primitivas y Orquestación de Contenedores

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_svg)](https://docker-app.streamlit.app/)
[![Docker](https://img.shields.io/badge/Docker-Enabled-blue?logo=docker)](https://www.docker.com/)
[![Python](https://img.shields.io/badge/Python-3.10+-yellow?logo=python)](https://www.python.org/)

## 1. Descripción Técnica
**Docker Demo** es una plataforma educativa de arquitectura abierta diseñada para la disección y generación de manifiestos en entornos de contenedores. El objetivo principal del proyecto es cerrar la brecha entre la ejecución imperativa de comandos y la comprensión declarativa de la infraestructura, permitiendo a desarrolladores y administradores de sistemas visualizar la lógica subyacente del motor de Docker.

La herramienta aborda tres pilares fundamentales del ecosistema nativo de la nube: el empaquetado de artefactos, la gestión de ciclos de vida de contenedores y la orquestación de microservicios interdependientes.

---

## 2. Funcionalidades de Análisis

### A. Ingeniería de Construcción (Dockerfile Generator)
Implementa una lógica de generación de imágenes basada en la optimización de capas (*layer caching*). La herramienta permite configurar entornos para Python, Node.js y Nginx, aplicando principios de:
* **Inmutabilidad:** Definición de directorios de trabajo constantes (`WORKDIR`).
* **Eficiencia de Capas:** Estrategia de copia selectiva de dependencias (`requirements.txt`, `package.json`) previa a la inyección del código fuente para minimizar los tiempos de compilación.
* **Exposición de Puertos:** Documentación explícita de interfaces de red mediante la directiva `EXPOSE`.

### B. Análisis Sintáctico y Simulación (`docker run`)
Módulo dedicado al parsing de instrucciones de terminal. Desglosa parámetros críticos de ejecución, tales como:
* **Modo Detached (`-d`):** Aislamiento de procesos en segundo plano.
* **Mapeo de Puertos (`-p`):** Configuración de *port forwarding* entre el host y el espacio de nombres del contenedor.
* **Persistencia de Datos (`-v`):** Implementación de *bind mounts* para la sincronización de volúmenes en tiempo real.
* **Simulador Dinámico:** Emulación del flujo de eventos del *Docker Daemon*, incluyendo el reporte de *image pulling* y hashes de identificación de contenedor.

### C. Orquestación de Microservicios (Docker Compose)
Generación de manifiestos YAML para la gestión de topologías complejas. Se enfoca en:
* **Resolución de DNS Interno:** Comunicación entre servicios mediante nombres de host locales.
* **Dependencias de Arranque:** Control de flujo mediante `depends_on`.
* **Persistencia Gestionada:** Definición de volúmenes compartidos para sistemas de bases de datos (PostgreSQL, Redis).

---

## 3. Arquitectura del Proyecto

El software ha sido desarrollado bajo un paradigma de micro-aplicación utilizando el stack **Streamlit**, lo que garantiza una interfaz reactiva sin sobrecarga de estado en el servidor.

```text
.
├── app.py              # Lógica principal y motor de procesamiento de texto
├── requirements.txt    # Dependencias del entorno (Streamlit, etc.)
└── Dockerfile          # Instrucciones para la autocontenerización del proyecto

## 4. Despliegue e Instalación
Requisitos previos
Docker Engine instalado.

Python 3.10+ (para ejecución local sin contenedor).
