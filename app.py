import streamlit as st
import requests
import json
import re

# Título de la aplicación
st.title("Generador de Bestseller de No Ficción para Amazon")

# Descripción de la aplicación
st.write("""
Esta aplicación genera un posible bestseller de no ficción que podría venderse en Amazon, basado en el tema que elijas. Los campos de rango de edad, área geográfica y género son opcionales. También generará una descripción larga del libro.
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

# Función para generar el contenido basado en los resultados, tema, rango de edad, área geográfica y género
def generar_bestseller(resultados, tema, rango_edad, area_geografica, genero):
    snippets = ""
    for item in resultados.get("organic", [])[:3]:  # Tomamos los primeros 3 resultados
        snippets += f"{item.get('title')}:\n{item.get('snippet')}\n\n"

    # Generar título basado en los resultados obtenidos
    titulo = f"Bestseller sobre {tema} para {rango_edad} en {area_geografica} para {genero}"
    
    # Crear una tabla de contenidos basada en los snippets
    tabla_contenidos = re.findall(r"\b\d+\.\s+[A-Za-z0-9 ,'.]+", snippets)
    if not tabla_contenidos:
        # Si no se encuentran capítulos específicos, generar una tabla de contenidos genérica
        tabla_contenidos = [
            "1. Introducción",
            f"2. El impacto de {tema} en la sociedad",
            "3. Retos y Oportunidades",
            f"4. {tema} en el contexto de {area_geografica}",
            "5. Innovación y Crecimiento",
            "6. Conclusión"
        ]
    
    # Generar una descripción larga basada en los datos y el tema
    descripcion = (f"Este libro explora en profundidad el tema de {tema} y cómo influye "
                   f"en {rango_edad} de {area_geografica}. Diseñado para {genero}, ofrece "
                   f"una mirada única y detallada sobre los retos y oportunidades que presenta "
                   f"{tema} en el mundo actual. A través de capítulos cuidadosamente organizados, "
                   f"los lectores encontrarán valiosos insights sobre el impacto de {tema} en diversas "
                   f"esferas, así como estrategias para aprovechar su potencial en contextos personales "
                   f"y profesionales. Este libro es una guía esencial para aquellos interesados en "
                   f"comprender y adaptarse a los cambios impulsados por {tema} en la sociedad.")
    
    return titulo, tabla_contenidos, descripcion

# Entrada del usuario para el tema del libro (obligatorio)
tema = st.text_input("Introduce el tema principal del libro de no ficción (obligatorio):", "")

# Selección de rango de edad (opcional)
rango_edad = st.selectbox("Selecciona el rango de edad del público objetivo (opcional):", 
                          ["No especificar", "15-25", "25-35", "35-45", "45-55", "55-65", "65-75", "75-85", "85-95"])

# Selección de área geográfica (opcional)
area_geografica = st.selectbox("Selecciona el área geográfica (opcional):", 
                               ["No especificar", "Estados Unidos", "Latinoamérica", "Europa"])

# Selección del género del lector (opcional)
genero = st.selectbox("Selecciona el género del lector (opcional):", ["No especificar", "Femenino", "Masculino"])

# Botón para generar el bestseller
if st.button("Generar Bestseller"):
    if tema.strip() == "":
        st.warning("Por favor, introduce un tema para generar el bestseller.")
    else:
        # Asignar valores predeterminados si no se especifican los campos opcionales
        if rango_edad == "No especificar":
            rango_edad = "todas las edades"
        if area_geografica == "No especificar":
            area_geografica = "cualquier lugar"
        if genero == "No especificar":
            genero = "todas las personas"
        
        # Realizar la búsqueda con Serper
        with st.spinner("Realizando búsqueda en Amazon..."):
            query = f"bestsellers de no ficción sobre {tema} para {rango_edad} en {area_geografica} para {genero}"
            resultados = buscar_serper(query)
            
            if resultados:
                # Generar título, tabla de contenidos y descripción a partir de los resultados
                titulo, tabla_contenidos, descripcion = generar_bestseller(resultados, tema, rango_edad, area_geografica, genero)
                
                # Mostrar los resultados
                st.subheader("Título del Libro")
                st.success(titulo)
                
                st.subheader("Tabla de Contenidos")
                st.text("\n".join(tabla_contenidos))
                
                st.subheader("Descripción del Libro")
                st.info(descripcion)
