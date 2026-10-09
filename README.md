# NutriGuajira - Sistema de Valoracion Nutricional

NutriGuajira es una aplicacion web desarrollada en Django y Django REST Framework para la gestion, seguimiento y diagnostico nutricional de pacientes. El sistema permite registrar datos clinicos, generar valoraciones con el calculo automatico de IMC, crear recomendaciones mediante la API de Groq y almacenar datos de forma local cuando no hay conexion a internet para sincronizarlos posteriormente con el servidor.

## Requisitos previos

- Python 3.10 o superior
- Pip (gestor de paquetes de Python)
- Git

## Instalacion y configuracion local

1. Clonar el repositorio:
   git clone https://github.com/Male0523/nutriresuelve.git
   cd nutriresuelve

2. Crear y activar el entorno virtual:
   python3 -m venv venv
   source venv/bin/activate

3. Instalar dependencias:
   pip install -r requirements.txt

4. Configurar el archivo de entorno:
   Crear un archivo `.env` en la raiz del proyecto con la siguiente estructura:

   SECRET_KEY=clave_secreta_django
   DEBUG=True
   GROQ_API_KEY=api_key_de_groq

5. Aplicar migraciones e iniciar el servidor:
   python manage.py migrate
   python manage.py runserver

El servidor iniciara en http://127.0.0.1:8000/

## Funcionalidades principales

- Gestion de Pacientes: Registro de datos personales, representantes legales, antecedentes de salud y alergias.
- Valoracion Nutricional: Calculo automatico de indice de masa corporal y diagnostico segun el nivel socioeconomico y de actividad.
- Integracion con Groq: Generacion automatica de planes alimenticios basados en el perfil del paciente.
- Soporte Offline: Intercepcion de formularios mediante JavaScript (offline-sync.js) cuando falla la red o el servidor esta caido. Los datos se guardan en el localStorage del navegador y se envian al backend en cuanto se restablece la conexion.
- API REST: Endpoints construidos con Django REST Framework para la exposicion de los datos en formato JSON.

## Estructura del proyecto

- apps/: Contiene los modulos de pacientes, valoracion, seguimiento y recomendaciones.
- core/: Configuracion principal de Django, rutas globales y WSGI/ASGI.
- static/: Archivos CSS, JavaScript de sincronizacion offline (offline-sync.js) y Service Worker.
- templates/: Plantillas HTML estructuradas con Bootstrap 5.