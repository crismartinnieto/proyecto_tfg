import streamlit as st
import requests
from streamlit_estilos import aplicar_estilos, mostrar_logos

# Aplicar estilos visuales
aplicar_estilos()
mostrar_logos()


# Input del usuario
question = st.text_input("Escribe tu pregunta aquí:")

# Checkboxes de fuentes
st.markdown("Selecciona fuentes adicionales de datos:")
use_wikidata = st.checkbox("Wikidata", value=True)
use_dbpedia = st.checkbox("DBpedia", value=True)

# Enviar petición
if st.button("Enviar"):
    if question:
        try:
            response = requests.post(
                "http://langchain-api:5000/ask_question",
                json={
                    "question": question,
                    "use_wikidata": use_wikidata,
                    "use_dbpedia": use_dbpedia
                }
            )
            if response.status_code == 200:
                respuesta = response.json()["answer"]

                # Mostrar respuesta estilizada con título azul
                st.markdown(f"<h3 style='color:#00629b;'>Respuesta:</h3>", unsafe_allow_html=True)

                # Mostrar respuesta estilizada
                if respuesta.startswith("⚠️"):
                    advertencia, contenido = respuesta.split("\n\n", 1)
                    st.warning(advertencia)
                    st.markdown(f"<div class='respuesta'>{contenido}</div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<div class='respuesta'>{respuesta}</div>", unsafe_allow_html=True)

            else:
                st.error(f"❌ Error {response.status_code}: {response.text}")
        except Exception as e:
            st.error(f"❌ Error de conexión con la API: {str(e)}")
    else:
        st.warning("Por favor, escribe una pregunta antes de enviar.")
