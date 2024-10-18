import streamlit as st
import requests
import json
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración de la página
st.set_page_config(page_title="Humanizador de Texto AI", page_icon="🤖")

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

# Slider para el nivel de fuerza de la reescritura
strength = st.slider("Nivel de reescritura", min_value=1, max_value=4, value=3, 
                     help="1 = Cambios mínimos, 4 = Cambios máximos")

# Función para humanizar el texto
def humanizar_texto(texto, nivel_fuerza):
    url = "https://api.smodin.io/v1/rewrite/single"
    
    payload = {
        "language": "auto",
        "strength": nivel_fuerza,
        "text": texto
    }
    
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "x-api-key": API_KEY
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # Verificar si hay errores en la respuesta
        
        # Imprimir la respuesta para depuración
        st.write("Respuesta de la API (debug):", response.json())
        
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"Error en la solicitud: {str(e)}"}

# Botón para humanizar
if st.button("Humanizar"):
    if texto_input:
        with st.spinner('Humanizando el texto...'):
            resultado = humanizar_texto(texto_input, strength)
            
            if "error" in resultado:
                st.error(resultado["error"])
            else:
                st.success("¡Texto humanizado exitosamente!")
                # Intentar obtener el texto reescrito de diferentes maneras posibles
                texto_humanizado = (
                    resultado.get("data", {}).get("rewritten") or
                    resultado.get("rewritten") or
                    resultado.get("data", {}).get("text") or
                    resultado.get("text")
                )
                
                if texto_humanizado:
                    st.text_area("Texto humanizado:", value=texto_humanizado, height=200)
                else:
                    st.error("No se pudo obtener el texto humanizado de la respuesta")
                    st.json(resultado)  # Mostrar la respuesta completa para depuración
    else:
        st.warning("Por favor, ingresa un texto para humanizar.")

# Información adicional
st.markdown("---")
st.markdown("### Instrucciones:")
st.markdown("1. Pega el texto generado por AI en el área de texto superior")
st.markdown("2. Ajusta el nivel de reescritura según tus necesidades")
st.markdown("3. Haz clic en el botón 'Humanizar'")
st.markdown("4. El texto humanizado aparecerá en el área inferior")

# Información sobre los niveles de reescritura
st.sidebar.markdown("""
### Niveles de reescritura:
- **Nivel 1**: Cambios mínimos al texto original
- **Nivel 2**: Cambios moderados
- **Nivel 3**: Cambios significativos
- **Nivel 4**: Reescritura máxima
""")
