import streamlit as st

# Título de la aplicación
st.title("Generador de Bestseller de No Ficción para Amazon")

# Descripción de la aplicación
st.write("""
Esta aplicación genera un posible bestseller de no ficción que podría venderse en Amazon, basado en el rango de edad, el área geográfica y el género del lector.
""")

# Función para generar el contenido basado en el rango de edad, área geográfica y género
def generar_bestseller(rango_edad, area_geografica, genero):
    if rango_edad == "15-25" and area_geografica == "Estados Unidos" and genero == "Femenino":
        titulo = "Empowerment: Building Confidence in a Digital World"
        tabla_contenidos = [
            "1. Redefiniendo Belleza: Más Allá de los Filtros y Likes",
            "2. Salud Mental y Autoestima: Superando la Presión Social",
            "3. Empoderamiento Femenino: Ser Tu Propia Líder",
            "4. Igualdad y Activismo: Rompiendo Barreras en el Siglo XXI",
            "5. Relaciones Saludables: Creando Vínculos Sólidos en la Era Digital",
            "6. Encontrando tu Voz: Expresión Personal y Profesional",
            "7. Crecimiento y Futuro: Construyendo tu Propio Camino"
        ]
    elif rango_edad == "15-25" and area_geografica == "Estados Unidos" and genero == "Masculino":
        titulo = "Finding Purpose: Navigating Life in a Digital World"
        tabla_contenidos = [
            "1. La Era de la Ansiedad: Cómo las Redes Sociales Moldean Nuestra Identidad",
            "2. Desbloquear tu Propósito: Más Allá del Éxito Superficial",
            "3. Equilibrar Expectativas: Familia, Amigos y Relaciones en la Era Digital",
            "4. Convertir Pasión en Profesión: Emprendimiento Joven",
            "5. Salud Mental y Autocuidado: Superar el Burnout",
            "6. Activismo y Cambio Social: Cómo Hacer que tu Voz Sea Escuchada",
            "7. Creando una Vida con Propósito: Planificar tu Futuro"
        ]
    elif rango_edad == "25-35" and area_geografica == "Latinoamérica" and genero == "Femenino":
        titulo = "Rompiendo Barreras: Mujeres Líderes en Latinoamérica"
        tabla_contenidos = [
            "1. Liderazgo Femenino: Superando los Desafíos Culturales",
            "2. Emprendimiento en Economías Emergentes: Historias de Éxito",
            "3. Igualdad Salarial: Avances y Retos en Latinoamérica",
            "4. Creando Redes: El Poder de la Comunidad Femenina",
            "5. Innovación y Creatividad: Construyendo el Futuro Profesional",
            "6. Balance Trabajo-Vida Personal: Cómo Lograrlo",
            "7. Empoderamiento y Futuro: La Próxima Generación de Líderes"
        ]
    elif rango_edad == "25-35" and area_geografica == "Latinoamérica" and genero == "Masculino":
        titulo = "Rompiendo Barreras: El Camino al Éxito Profesional en Latinoamérica"
        tabla_contenidos = [
            "1. La Realidad del Emprendimiento en Latinoamérica",
            "2. Networking: Creando Oportunidades Profesionales en Economías Emergentes",
            "3. Superando la Brecha Salarial: Estrategias para Maximizar tu Potencial",
            "4. Hacer más con menos: Innovación en Tiempos de Crisis",
            "5. Liderazgo Resiliente: Cómo Adaptarte a los Cambios Económicos",
            "6. Mujeres y Minorías: Liderando el Cambio en el Mundo Empresarial",
            "7. Trabajo y Vida Personal: Encontrando el Equilibrio en un Mundo Competitivo"
        ]
    elif rango_edad == "35-45" and area_geografica == "Europa" and genero == "Femenino":
        titulo = "El Poder de la Innovación: Mujeres que Lideran en Europa"
        tabla_contenidos = [
            "1. Innovación y Sustentabilidad: Las Nuevas Fronteras",
            "2. Liderazgo Femenino en Europa: Nuevas Oportunidades",
            "3. Retos Económicos: Cómo Superar las Barreras Sistémicas",
            "4. Tecnología y Creatividad: Mujeres Emprendedoras",
            "5. Trabajo Remoto: Cambiando las Normas en Europa",
            "6. Políticas y Regulaciones: Cómo Navegar el Panorama Europeo",
            "7. Futuro del Trabajo: Preparándote para lo que Viene"
        ]
    elif rango_edad == "35-45" and area_geografica == "Europa" and genero == "Masculino":
        titulo = "El Poder de la Innovación: Cómo Liderar en la Economía Europea"
        tabla_contenidos = [
            "1. Innovación y Sustentabilidad: Las Nuevas Fronteras",
            "2. Liderazgo Global: Europa como Potencia en el Siglo XXI",
            "3. Retos Económicos: Adaptarse a un Mundo Cambiante",
            "4. Tecnología y Emprendimiento: El Nuevo Camino hacia el Éxito",
            "5. Trabajo Remoto: Cambiando las Normas en Europa",
            "6. Políticas y Regulaciones: Cómo Navegar el Panorama Europeo",
            "7. Futuro del Trabajo: Preparándote para lo que Viene"
        ]
    else:
        titulo = "Título por Definir"
        tabla_contenidos = ["1. Capítulo 1", "2. Capítulo 2", "3. Capítulo 3"]

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
    with st.spinner("Generando el libro basado en las selecciones..."):
        titulo, tabla_contenidos = generar_bestseller(rango_edad, area_geografica, genero)
        
        # Mostrar los resultados
        st.subheader("Título del Libro")
        st.success(titulo)
        
        st.subheader("Tabla de Contenidos")
        st.text("\n".join(tabla_contenidos))
