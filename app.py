import streamlit as st
import requests
import json
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración de la página


# Título de la aplicación
st.title("Humanizador de Texto AI")

# API key de Smodin desde variables de entorno
API_KEY = os.getenv('SMODIN_API_KEY')

# Verificar si existe la API key
if not API_KEY:
    st.error("Error: No se encontró la API key en las variables de entorno")
    st.stop()

# Área de texto para input
texto_input = st.text_area("Ingresa el texto generado por AI que deseas humanizar:", height=200)

# Función para humanizar el texto
def humanizar_texto(texto):
    url = "https://api.smodin.io/v1/rewrite/single"
    
    payload = {
        "language": "auto",
        "strength": 3,  # Nivel fijo en 3 para reescritura moderada
        "text": texto
    }
    
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "x-api-key": API_KEY
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"Error en la solicitud: {str(e)}"}

# Botón para humanizar
if st.button("Humanizar"):
    if texto_input:
        with st.spinner('Humanizando el texto...'):
            resultado = humanizar_texto(texto_input)
            
            if "error" in resultado:
                st.error(resultado["error"])
            else:
                try:
                    # Extraer el texto reescrito de la estructura correcta
                    texto_humanizado = resultado["rewrites"][0]["rewrite"]
                    st.success("¡Texto humanizado exitosamente!")
                    st.text_area("Texto humanizado:", value=texto_humanizado, height=200)
                except (KeyError, IndexError) as e:
                    st.error("No se pudo obtener el texto humanizado de la respuesta")
                    if st.checkbox("Mostrar detalles del error"):
                        st.json(resultado)
    else:
        st.warning("Por favor, ingresa un texto para humanizar.")

# Instrucciones básicas
st.markdown("---")
st.markdown("### Instrucciones:")
st.markdown("1. Pega el texto generado por AI en el área de texto superior")
st.markdown("2. Haz clic en el botón 'Humanizar'")
st.markdown("3. El texto humanizado aparecerá en el área inferior")
