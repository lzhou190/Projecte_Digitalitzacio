import streamlit as st
from PIL import Image
import google.generativeai as genai
import time

# 1. CONFIGURACIÓ DE LA PÀGINA
st.set_page_config(page_title="Menú Saludable IA", page_icon="🥗", layout="wide")

# 2. ESTILS CSS MODERNS (Vibrant, Borders & Animated Icons)
st.markdown("""
    <style>
    /* Fons amb un degradat multicolor actiu */
    .stApp {
        background: linear-gradient(135deg, #FF0076 0%, #590FB7 45%, #FFD600 100%);
        background-attachment: fixed;
    }

    header[data-testid="stHeader"] {
        background: transparent !important;
    }
    
    footer {
        visibility: hidden;
    }

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

    /* ANIMACIÓ PER A LA ICONA DE CONFIGURACIÓ (Sidebar) */
    .sidebar-icon {
        display: inline-block;
        animation: sidebar-swing 2s ease-in-out infinite;
        font-size: 1.5em;
        margin-right: 10px;
    }

    @keyframes sidebar-swing {
        0% { transform: rotate(0deg); }
        25% { transform: rotate(15deg); }
        75% { transform: rotate(-15deg); }
        100% { transform: rotate(0deg); }
    }

    /* ANIMACIONS PER A LES ICONES DEL TÍTOL */
    .title-icon-left {
        display: inline-block;
        animation: pulse-tilt 4s ease-in-out infinite;
    }
    
    .title-icon-right {
        display: inline-block;
        animation: rotate-float 5s ease-in-out infinite;
    }

    @keyframes pulse-tilt {
        0% { transform: scale(1) rotate(0deg); }
        50% { transform: scale(1.2) rotate(-15deg); }
        100% { transform: scale(1) rotate(0deg); }
    }

    @keyframes rotate-float {
        0% { transform: translateY(0px) rotate(0deg); }
        50% { transform: translateY(-10px) rotate(15deg); }
        100% { transform: translateY(0px) rotate(0deg); }
    }

    /* ESTIL PER A LES ICONES GEGANTS DE BAIX */
    .big-icon {
        font-size: 80px;
        display: block;
        margin-bottom: 10px;
        filter: drop-shadow(0 0 15px rgba(255, 255, 255, 0.5));
        animation: levitate 3s ease-in-out infinite;
    }

    @keyframes levitate {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-15px); }
        100% { transform: translateY(0px); }
    }

    /* Capçaleres de secció */
    .info-header {
        color: #ffffff !important;
        font-family: 'Segoe UI', sans-serif;
        font-size: 28px;
        font-weight: 900;
        text-transform: uppercase;
        letter-spacing: 2px;
        text-shadow: 2px 2px 8px rgba(0,0,0,0.5);
        margin-bottom: 20px;
    }

    /* Línies horitzontals elèctriques */
    hr {
        border: 0;
        height: 5px;
        background: linear-gradient(90deg, #FF0076, #FFD600, #00FFFF);
        border-radius: 10px;
        margin: 2em 0 !important;
    }

    /* Botó ANALITZAR */
    .stButton>button {
        width: 100%;
        border-radius: 25px;
        background: linear-gradient(90deg, #FF512F 0%, #DD2476 100%);
        color: white;
        font-weight: bold;
        font-size: 24px;
        border: 3px solid #FFD600;
        transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        height: 4em;
        box-shadow: 0 10px 30px rgba(221, 36, 118, 0.5);
    }
    
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 15px 40px rgba(255, 214, 0, 0.6);
        border-color: white;
    }

    /* Targeta de resultats */
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

    /* Barra lateral */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #590FB7 0%, #FF0076 100%);
        border-right: 5px solid #FFD600;
    }

    .stMarkdown, p, label {
        color: white !important;
        font-weight: 500;
    }

    /* Peu de pàgina */
    .custom-footer {
        color: white !important;
        font-weight: 900 !important;
        text-align: center;
        padding: 30px;
        font-size: 1.3em;
        text-shadow: 0 0 10px rgba(255, 255, 255, 0.5);
    }
    </style>
    """, unsafe_allow_html=True)

# 3. BARRA LATERAL
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2424/2424569.png", width=100)
    st.markdown("<h1 style='color: white; text-align: center;'><span class='sidebar-icon'>🍽️</span> Configuració</h1>", unsafe_allow_html=True)
    st.divider()
    demo_mode = st.toggle("🚀 Activar Mode Demo", value=True)
    if demo_mode:
        tipus_demo = st.selectbox("Simulació:", ["Menú Complet", "Plat Únic (Recepta)"])
    else:
        api_key = st.text_input("Gemini API Key:", type="password")
    st.markdown("<br><p style='font-style: italic; color: white;'>Selecciona una foto d'un plat o menú per rebre consells nutricionals personalitzats.</p>", unsafe_allow_html=True)

# 4. CAPÇALERA PRINCIPAL
st.markdown("""
    <h1 style='color: white; text-align: center;'>
        <span class='title-icon-left'>🥑</span> 
        Assistent de Menús Saludables 
        <span class='title-icon-right'>🥗</span>
    </h1>
    """, unsafe_allow_html=True)
st.markdown("<h5 style='color: white; text-align: center; font-weight: bold;'>DIGITALITZA LA TEVA ALIMENTACIÓ AMB IA</h5>", unsafe_allow_html=True)
st.divider()

# 5. COS DE L'APLICACIÓ
col1, col2 = st.columns([1, 1.2], gap="large")

with col1:
    st.markdown("""
        <div>
            <span class='big-icon'>📸</span>
            <div class='info-header'>Puja la imatge</div>
        </div>
    """, unsafe_allow_html=True)
    uploaded_file = st.file_uploader("", type=["jpg", "jpeg", "png"])
    
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, use_container_width=True, caption="Imatge preparada")
        analitzar = st.button("🔍 ANALITZAR ARA")
    else:
        st.markdown("<p style='text-align: center;'>☝️ Tria una foto per començar</p>", unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div>
            <span class='big-icon'>📊</span>
            <div class='info-header'>Resultat anàlisi</div>
        </div>
    """, unsafe_allow_html=True)
    
    if uploaded_file and 'analitzar' in locals() and analitzar:
        with st.spinner('🌟 Estem analitzant les propietats nutricionals...'):
            time.sleep(2) 
            
            st.markdown("<div class='result-card'>", unsafe_allow_html=True)
            
            m1, m2 = st.columns(2)
            
            if demo_mode:
                if tipus_demo == "Menú Complet":
                    m1.metric("Qualitat Nutricional", "A", "Molt alta")
                    m2.metric("Tipus de Menú", "Equilibrat")
                    st.success("✅ Menú analitzat amb èxit")
                    st.markdown("""
                    ### 📋 Detall del Menú:
                    *   **Primer plat:** Crema de carbassa 🎃 o Amanida de tomàquet 🍅.
                    *   **Segon plat:** Llobarro al forn 🐟 o Hamburguesa vegetal 🌿.
                    *   **Postres:** Fruita de temporada 🍎 o Iogurt natural 🥛.
                    
                    ---
                    ### 🥗 El nostre consell:
                    La combinació de **Crema + Llobarro** és excel·lent. Proporciona fibra, proteïna de gran qualitat i greixos saludables.
                    """)
                else:
                    m1.metric("Nivell Saludable", "85%", "Excel·lent")
                    m2.metric("Proteïna", "24g", "Ideal")
                    st.success("✅ Plat detectat: **Amanida Cobb Saludable**")
                    st.markdown("""
                    ### 🥗 Anàlisi detallada:
                    *   **Base:** Pollastre a la planxa, ou dur i alvocat.
                    *   **Al·lèrgens:** Ous 🥚 i Lactosa 🥛.
                    *   **Consell:** Afegeix llavors de chía per a un extra de minerals. Evita les salses processades.
                    """)
            else:
                try:
                    if not api_key:
                        st.warning("⚠️ Si us plau, introdueix la teva API Key a la barra lateral.")
                    else:
                        genai.configure(api_key=api_key)
                        model = genai.GenerativeModel('gemini-1.5-flash-latest')
                        prompt = "Analitza aquesta imatge. Si és un menú, transcriu-lo i recomana l'opció més sana. Si és un plat, identifica els ingredients i dóna consells nutricionals. Respon en català de forma professional."
                        response = model.generate_content([prompt, image])
                        st.markdown(f"### 🤖 Anàlisi de la IA:\n\n{response.text}")
                except Exception as e:
                    st.error(f"❌ Error en connectar amb Gemini: {e}")
            
            st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.markdown("<p style='text-align: center; opacity: 0.7;'>L'informe apareixerà aquí un cop premis el botó.</p>", unsafe_allow_html=True)

# 6. PEU DE PÀGINA
st.divider()
st.markdown("<div class='custom-footer'>🚀 PROJECTE DIGITALITZACIÓ 2026 | DESENVOLUPAT AMB GEMINI AI</div>", unsafe_allow_html=True)
