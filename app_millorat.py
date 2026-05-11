import streamlit as st
from PIL import Image
import google.generativeai as genai
import time

# 1. CONFIGURACIÓ DE LA PÀGINA
st.set_page_config(page_title="Menú Saludable IA", page_icon="🥗", layout="wide")

# 2. ESTILS CSS MODERNS
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #FF0076 0%, #590FB7 45%, #FFD600 100%);
        background-attachment: fixed;
    }
    header[data-testid="stHeader"] { background: transparent !important; }
    footer { visibility: hidden; }

    /* Contenidors Glassmorphism */

    [data-testid="stVerticalBlock"] > div:has(div.info-header) {
        background: rgba(0, 0, 0, 0.25);
        backdrop-filter: blur(15px);
        padding: 40px;
        border-radius: 35px;
        border: 3px solid #FF0076;
        box-shadow: 0 0 25px rgba(255, 0, 118, 0.4);
        margin-bottom: 25px;
        text-align: center;
    }

    /* Targeta de resultats dinàmica */

    .result-card {
        background: rgba(0, 0, 0, 0.4);
        padding: 35px;
        border-radius: 30px;
        border: 4px solid #FFD600;
        box-shadow: 0 0 20px rgba(255, 214, 0, 0.4);
        color: white;
        font-size: 1.1em;
        text-align: left;
    }
    .result-card.grade-a { border-color: #00FF00 !important; box-shadow: 0 0 30px rgba(0, 255, 0, 0.6) !important; }
    .result-card.grade-bc { border-color: #FFA500 !important; box-shadow: 0 0 30px rgba(255, 165, 0, 0.6) !important; }
    .result-card.grade-bad { border-color: #FF0000 !important; box-shadow: 0 0 30px rgba(255, 0, 0, 0.6) !important; }

    /* Botó ANALITZAR */
    
    .stButton>button {
        width: 100%;
        border-radius: 25px;
        background: linear-gradient(90deg, #FF512F 0%, #DD2476 100%);
        color: white;
        font-weight: bold;
        font-size: 24px;
        border: 3px solid #FFD600;
        height: 4em;
    }

    .info-header {
        color: #ffffff !important;
        font-size: 28px;
        font-weight: 900;
        text-transform: uppercase;
        margin-bottom: 20px;
    }
    
    .big-icon { font-size: 80px; display: block; margin-bottom: 10px; }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #590FB7 0%, #FF0076 100%);
        border-right: 5px solid #FFD600;
    }
    
    .stMarkdown, p, label { color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. BARRA LATERAL
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2424/2424569.png", width=100)
    st.markdown("<h1 style='color: white; text-align: center;'>Configuració</h1>", unsafe_allow_html=True)
    st.divider()
    demo_mode = st.toggle("🚀 Activar Mode Demo", value=True)
    if demo_mode:
        tipus_demo = st.selectbox("Simulació:", ["Menú Complet", "Plat Únic (Recepta)"])
    else:
        api_key = st.text_input("Gemini API Key:", type="password")
    st.markdown("<br><p style='font-style: italic; color: white;'>Selecciona una foto d'un plat o menú per rebre consells nutricionals personalitzats.</p>", unsafe_allow_html=True)

# 4. CAPÇALERA PRINCIPAL
st.markdown("<h1 style='color: white; text-align: center;'>🥑 Assistent de Menús Saludables 🥗</h1>", unsafe_allow_html=True)
st.markdown("<h5 style='color: white; text-align: center; font-weight: bold;'>DIGITALITZA LA TEVA ALIMENTACIÓ AMB IA</h5>", unsafe_allow_html=True)
st.divider()

# 5. COS DE L'APLICACIÓ
col1, col2 = st.columns([1, 1.2], gap="large")

with col1:
    st.markdown("<div><span class='big-icon'>📸</span><div class='info-header'>Puja la imatge</div></div>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, use_container_width=True, caption="Imatge preparada")
        analitzar = st.button("🔍 ANALITZAR ARA")

with col2:
    st.markdown("<div><span class='big-icon'>📊</span><div class='info-header'>Resultat anàlisi</div></div>", unsafe_allow_html=True)
    
    if uploaded_file and 'analitzar' in locals() and analitzar:
        with st.spinner('🌟 Estem analitzant les propietats nutricionals...'):
            grade_class = ""
            analysis_text = ""
            
            if demo_mode:
                time.sleep(1.5)
                grade_class = "grade-a"
            else:
                if not api_key:
                    st.warning("⚠️ Si us plau, introdueix la teva API Key a la barra lateral.")
                else:
                    try:
                        genai.configure(api_key=api_key)
                        model = genai.GenerativeModel('gemini-1.5-flash')
                        prompt = """Analitza aquesta imatge amb deteniment:
                        1. IDENTIFICACIÓ: Detecta en quin idioma està el text de la imatge.
                        2. LECTURA: Llegeix i transcriu els elements clau (plats, ingredients, preus si n'hi ha).
                        3. ANÀLISI: Genera una anàlisi nutricional professional i dóna consells saludables.
                        4. IDIOMA DE RESPOSTA: Respon SEMPRE EN CATALÀ, independentment de l'idioma de la imatge.
                        5. IMPORTANT: Al final de la teva resposta, inclou una línia que digui exactament: 'QUALITAT: [A/B/C/D]' 
                           (A=Molt saludable, B/C=Acceptable, D=No saludable)."""
                        response = model.generate_content([prompt, image])
                        analysis_text = response.text
                        if "QUALITAT: A" in analysis_text: grade_class = "grade-a"
                        elif "QUALITAT: B" in analysis_text or "QUALITAT: C" in analysis_text: grade_class = "grade-bc"
                        elif "QUALITAT: D" in analysis_text: grade_class = "grade-bad"
                    except Exception as e:
                        st.error(f"❌ Error: {e}")
            
            st.markdown(f"<div class='result-card {grade_class}'>", unsafe_allow_html=True)
            if demo_mode:
                if tipus_demo == "Menú Complet":
                    st.markdown("### 🟢 Qualitat: Excel·lent (DEMO)\n* **Primer:** Crema de carbassa\n* **Segon:** Llobarro\n* **Consell:** Menú molt equilibrat.")
                else:
                    st.markdown("### 🟢 Qualitat: Excel·lent (DEMO)\n* **Plat:** Amanida Cobb\n* **Consell:** Rica en proteïna i greixos sans.")
            else:
                if analysis_text:
                    display_text = analysis_text.replace("QUALITAT: A", "🟢 Qualitat: Excel·lent").replace("QUALITAT: B", "🟠 Qualitat: Bona").replace("QUALITAT: C", "🟠 Qualitat: Acceptable").replace("QUALITAT: D", "🔴 Qualitat: Millorable")
                    st.markdown(f"### 🤖 Anàlisi de la IA:\n\n{display_text}")
            st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.markdown("<p style='text-align: center; opacity: 0.7;'>L'informe apareixerà aquí un cop premis el botó.</p>", unsafe_allow_html=True)

st.divider()
st.markdown("<div style='text-align: center; color: white; font-weight: bold;'>🚀 PROJECTE DIGITALITZACIÓ 2026</div>", unsafe_allow_html=True)
