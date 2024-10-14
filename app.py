import streamlit as st
import requests
import json
import re

# Título de la aplicación
st.title("Generador de Bestseller de No Ficción para Amazon")

# Descripción de la aplicación
st.write("""
Esta aplicación utiliza las APIs de **Together** y **Serper** para investigar y generar el título, la descripción y la tabla de contenidos de un posible bestseller de no ficción que podría venderse en Amazon.
""")

# Función para realizar una búsqueda con la API de Serper
def buscar_serper(query):
    url = "https://google.serper.dev/search"
    headers = {
        "X-API-KEY": st.secrets["SERPER_API_KEY"],
        "Content-Type": "application/json"
    }
    payload = {
        "q": query
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error en la búsqueda: {response.status_code}")
        return None

# Función para generar contenido con la API de Together
def generar_contenido(prompt):
    url = "https://api.together.xyz/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {st.secrets['TOGETHER_API_KEY']}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "Qwen/Qwen2.5-7B-Instruct-Turbo",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 2000,
        "temperature": 0.7,
        "top_p": 0.7,
        "top_k": 50,
        "repetition_penalty": 1,
        "stop": ["<|eot_id|>"],
        "stream": False  # Para simplificar, usamos stream=False
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        data = response.json()
        return data.get("choices", [{}])[0].get("message", {}).get("content", "")
    else:
        st.error(f"Error al generar contenido: {response.status_code}")
        return ""

# Entrada del usuario para el tema del libro
tema = st.text_input("Introduce el tema principal del libro de no ficción:", "")

# Entrada del usuario para el número de capítulos
numero_caps = st.number_input("Número de capítulos deseados:", min_value=5, max_value=20, value=10, step=1)

# Botón para generar el bestseller
if st.button("Generar Bestseller"):
    if tema.strip() == "":
        st.warning("Por favor, introduce un tema para generar el bestseller.")
    else:
        with st.spinner("Realizando investigación..."):
            # Realizar una búsqueda para obtener información relevante
            resultados = buscar_serper(f"bestsellers de no ficción en Amazon sobre {tema}")
        
        if resultados:
            # Preparar la información para el prompt
            # Por ejemplo, extraer algunos snippets de los resultados de búsqueda
            snippets = ""
            for item in resultados.get("organic", [])[:3]:  # Tomamos los primeros 3 resultados
                snippets += f"{item.get('title')}:\n{item.get('snippet')}\n\n"
            
            # Crear el prompt para Together
            prompt = f"""
Basándote en la siguiente información sobre bestsellers de no ficción en Amazon, genera un título atractivo, una descripción persuasiva y una tabla de contenidos detallada para un nuevo libro que podría ser un éxito de ventas.

Información de referencia:
{snippets}

Por favor, proporciona:

Título del libro:
Descripción del libro:
Tabla de Contenidos (con {numero_caps} capítulos):
"""
            
            with st.spinner("Generando contenido..."):
                contenido = generar_contenido(prompt)
            
            if contenido:
                st.subheader("Contenido Generado")
                st.text(contenido)
                
                # Utilizar expresiones regulares para extraer las secciones
                titulo_match = re.search(r"Título del libro[:\s]*(.*)", contenido, re.IGNORECASE)
                descripcion_match = re.search(r"Descripción del libro[:\s]*(.*)", contenido, re.IGNORECASE)
                tabla_match = re.search(r"Tabla de Contenidos[:\s]*(.*)", contenido, re.IGNORECASE | re.DOTALL)
                
                titulo = titulo_match.group(1).strip() if titulo_match else "No se pudo extraer el título."
                descripcion = descripcion_match.group(1).strip() if descripcion_match else "No se pudo extraer la descripción."
                tabla_contenidos = tabla_match.group(1).strip() if tabla_match else "No se pudo extraer la tabla de contenidos."
                
                # Contar los capítulos generados
                capitulos = re.findall(r"\d+\.\s+.+", tabla_contenidos)
                numero_de_capitulos = len(capitulos)
                
                # Mostrar advertencia si el número de capítulos es menor que el solicitado
                if numero_de_capitulos < numero_caps:
                    st.warning(f"Solo se generaron {numero_de_capitulos} capítulos, en lugar de los {numero_caps} solicitados.")
                
                # Mostrar los resultados
                st.subheader("Título del Libro")
                st.success(titulo)
                
                st.subheader("Descripción del Libro")
                st.info(descripcion)
                
                st.subheader("Tabla de Contenidos")
                st.text("\n".join(capitulos))
