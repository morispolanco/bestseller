import streamlit as st
import requests
import json
import re

# Título de la aplicación
st.title("Generador de Bestseller de No Ficción para Amazon")

# Descripción de la aplicación
st.write("""
Esta aplicación genera un posible bestseller de no ficción que podría venderse en Amazon, basado en el rango de edad, el área geográfica y el género del lector, realizando una búsqueda en Amazon utilizando la API de Serper.
""")

# Función para realizar una búsqueda con la API de Serper
def buscar_serper(query):
    url = "https://google.serper.dev/search"
    headers = {
        "X-API-KEY": st.secrets["SERPER_API_KEY"],  # Asegúrate de tener tu clave en secrets
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

# Función para generar el contenido basado en el rango de edad, área geográfica y género
def generar_bestseller(resultados, rango_edad, area_geografica, genero):
    snippets = ""
    for item in resultados.get("organic", [])[:3]:  # Tomamos los primeros 3 resultados
        snippets += f"{item.get('title')}:\n{item.get('snippet')}\n\n"

    # Generar título basado en los resultados obtenidos
    titulo = f"Bestseller Inspirado en {rango_edad} en {area_geografica} para {genero}"
    
    # Crear una tabla de contenidos basada en los snippets
    tabla_contenidos = re.findall(r"\b\d+\.\s+[A-Za-z0-9 ,'.]+", snippets)
    if not tabla_contenidos:
        # Si no se encuentran capítulos específicos, generar una tabla de contenidos genérica
        tabla_contenidos = [
            "1. Introducción",
            "2. Retos y Oportunidades",
            "3. Innovación y Crecimiento",
            "4. Cómo Adaptarse a un Mundo Cambiante",
            "5. Conclusión"
        ]

    return titulo, tabla_contenidos

# Selección de rango de edad
rango_edad = st.selectbox("Selecciona el rango de edad del público objetivo:", 
                          ["15-25", "25-35", "35-45", "45-55", "55-65", "65-75", "75-85", "85-95"])

# Selección de área geográfica
area_geografica = st.selectbox("Selecciona el área geográfica:", 
                               ["Estados Unidos", "Latinoamérica", "Europa"])

# Selección del género del lector
genero = st.selectbox("Selecciona el género del lector:", ["Femenino", "Masculino"])

# Botón para generar el bestseller
if st.button("Generar Bestseller"):
    with st.spinner("Realizando búsqueda en Amazon..."):
        query = f"bestsellers de no ficción en Amazon para {rango_edad} en {area_geografica} para {genero}"
        resultados = buscar_serper(query)
        
        if resultados:
            # Generar título y tabla de contenidos a partir de los resultados
            titulo, tabla_contenidos = generar_bestseller(resultados, rango_edad, area_geografica, genero)
            
            # Mostrar los resultados
            st.subheader("Título del Libro")
            st.success(titulo)
            
            st.subheader("Tabla de Contenidos")
            st.text("\n".join(tabla_contenidos))
