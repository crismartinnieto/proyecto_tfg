import streamlit as st
from PIL import Image

# Colores institucionales
GSI_COLOR = "#00a9e0"
UPM_COLOR = "#00629b"

def aplicar_estilos():
    st.set_page_config(page_title="Buscador Universidades", layout="centered")
    st.markdown(f"""
        <style>
            .main {{
                background-color: #ffffff;
                font-family: 'Arial', sans-serif;
            }}
            h1, h2, .stMarkdown h1 {{
                color: {UPM_COLOR};
                font-weight: bold;
                text-align: center;
            }}
            .stButton>button {{
                background-color: {GSI_COLOR};
                color: white;
                border: none;
                border-radius: 8px;
                padding: 0.5rem 1rem;
                font-weight: bold;
                transition: 0.2s ease-in-out;
            }}
            .stButton>button:hover {{
                background-color: {UPM_COLOR};
            }}
            .stCheckbox>div>label {{
                color: {UPM_COLOR};
                font-weight: 600;
            }}
            
            /* SOLUCIÓN DEFINITIVA PARA LOS CHECKBOXES AZULES */
            .stCheckbox .stCheckbox input[type="checkbox"] {{
                -webkit-appearance: none;
                -moz-appearance: none;
                appearance: none;
                width: 16px;
                height: 16px;
                border: 2px solid {UPM_COLOR};
                border-radius: 3px;
                outline: none;
                cursor: pointer;
                position: relative;
                margin-right: 8px;
                vertical-align: middle;
            }}
            
            .stCheckbox .stCheckbox input[type="checkbox"]:checked {{
                background-color: {UPM_COLOR};
                border-color: {UPM_COLOR};
            }}
            
            .stCheckbox .stCheckbox input[type="checkbox"]:checked::after {{
                content: "✓";
                position: absolute;
                color: white;
                font-size: 14px;
                left: 50%;
                top: 50%;
                transform: translate(-50%, -50%);
            }}
            
            /* Eliminar cualquier sombra o efecto por defecto */
            .stCheckbox .stCheckbox input[type="checkbox"]:focus {{
                box-shadow: none !important;
            }}
            
            .respuesta {{
                border-left: 6px solid {UPM_COLOR};
                padding: 1rem;
                border-radius: 5px;
                margin-top: 1rem;
                background-color: #f2f9ff;
                color: #000;
            }}
            .respuesta h3 {{
                margin-top: 0;
                color: {UPM_COLOR};
            }}
        </style>
    """, unsafe_allow_html=True)

def mostrar_logos():
    # Layout con 3 columnas ajustadas para una sola línea
    col1, col2, col3 = st.columns([2, 5, 2])
    
    try:
        logo_upm = Image.open("imgs/logo_upm.png")
        logo_gsi = Image.open("imgs/logo_gsi.png")
        
        with col1:
            st.image(logo_upm, width=180)  # Logo UPM más grande
        
        with col2:
            st.markdown("<h1 style='margin-top: 15px;'>Pregunta sobre universidades</h1>", 
                      unsafe_allow_html=True)
        
        with col3:
            st.image(logo_gsi, width=160)  # Logo GSI más grande
            
    except FileNotFoundError:
        st.warning("⚠️ No se encontraron los logos en la carpeta `imgs/`.")