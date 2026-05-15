import streamlit as st
from PIL import Image
import google.generativeai as genai
import time

st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        background-color: #2e7d32;
        color: white;
        font-weight: bold;
        height: 3em;
    }
    .result-card {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        border-left: 10px solid #4caf50;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    .info-header {
        color: #2e7d32;
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 15px;
        border-bottom: 2px solid #e0e0e0;
        padding-bottom: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

    # 2. BARRA LATERAL
with st.sidebar:
    st.title("⚙️ Configuració")
    demo_mode = st.toggle("🚀 Activar Mode Demo", value=True)
    if demo_mode:
        tipus_demo = st.selectbox("Tipus de simulació:", ["Menú Complet", "Plat Únic (Recepta)"])
    else:
        api_key = st.text_input("Gemini API Key:", type="password")

    # 3. CAPÇALERA
￼
46
+
st.title("🥗 Assistent de Menús Saludables")
￼
47
+
st.write("Digitalitza la teva alimentació amb Intel·ligència Artificial.")
￼
48
+
st.write("---")