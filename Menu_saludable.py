import streamlit as st
from PIL import Image
import google.generativeai as genai
import time
import re

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(page_title="Menú Saludable IA", page_icon="🥗", layout="wide")

# 2. ESTILOS CSS MODERNOS Y RESPONSIVOS
st.markdown("""
    <style>
    /* Fondo con degradado multicolor activo */
    .stApp {
        background: linear-gradient(135deg, #FF0076 0%, #590FB7 45%, #FFD600 100%);
        background-attachment: fixed;
    }

    header[data-testid="stHeader"] { background: transparent !important; }
    footer { visibility: hidden; }

    /* Contenedores Glassmorphism con tamaño responsivo */
    .info-header-container {
        background: rgba(0, 0, 0, 0.25);
        backdrop-filter: blur(15px);
        padding: clamp(15px, 3vw, 30px);
        border-radius: 35px;
        border: 3px solid #FF0076;
        box-shadow: 0 0 25px rgba(255, 0, 118, 0.4);
        text-align: center;
        width: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }

    /* Animaciones (Preservadas) */
    .sidebar-icon { display: inline-block; animation: sidebar-swing 2s ease-in-out infinite; font-size: 1.5em; margin-right: 10px; }
    @keyframes sidebar-swing { 0%, 100% { transform: rotate(0deg); } 25% { transform: rotate(15deg); } 75% { transform: rotate(-15deg); } }
    
    .title-icon-left { display: inline-block; animation: pulse-tilt 4s ease-in-out infinite; }
    .title-icon-right { display: inline-block; animation: rotate-float 5s ease-in-out infinite; }
    @keyframes pulse-tilt { 0%, 100% { transform: scale(1) rotate(0deg); } 50% { transform: scale(1.2) rotate(-15deg); } }
    @keyframes rotate-float { 0%, 100% { transform: translateY(0px) rotate(0deg); } 50% { transform: translateY(-10px) rotate(15deg); } }

    .big-icon {
        font-size: clamp(40px, 10vw, 70px);
        display: block;
        margin-bottom: 10px;
        filter: drop-shadow(0 0 15px rgba(255, 255, 255, 0.5));
        animation: levitate 3s ease-in-out infinite;
    }
    @keyframes levitate { 0%, 100% { transform: translateY(0px); } 50% { transform: translateY(-15px); } }

    .info-header {
        color: #ffffff !important;
        font-family: 'Segoe UI', sans-serif;
        font-size: clamp(18px, 4vw, 24px);
        font-weight: 900;
        text-transform: uppercase;
        letter-spacing: 2px;
        text-shadow: 2px 2px 8px rgba(0,0,0,0.5);
    }

    hr {
        border: 0; height: 5px;
        background: linear-gradient(90deg, #FF0076, #FFD600, #00FFFF);
        border-radius: 10px; margin: 2em 0 !important;
    }

    /* Botón ANALIZAR (Responsivo) */
    .stButton>button {
        width: 100%;
        border-radius: 25px;
        background: linear-gradient(90deg, #FF512F 0%, #DD2476 100%);
        color: white !important;
        font-weight: bold;
        font-size: clamp(16px, 3vw, 24px);
        border: 3px solid #FFD600;
        transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        height: 3.5em;
        box-shadow: 0 10px 30px rgba(221, 36, 118, 0.5);
    }
    .stButton>button:hover { transform: scale(1.03); border-color: white; }

    /* TARJETA DE RESULTADOS UNIFICADA */
    .result-card {
        background: rgba(0, 0, 0, 0.5);
        padding: clamp(20px, 5vw, 40px);
        border-radius: 30px;
        border: 4px solid #FFD600;
        box-shadow: 0 0 30px rgba(0, 0, 0, 0.6);
        color: #f0f0f0 !important;
        margin-top: 20px;
    }

    /* BLOQUES DE ANÁLISIS MEJORADOS CON HOVER */
    .analysis-section {
        background: rgba(255, 255, 255, 0.08);
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 15px;
        border-left: 6px solid #FF0076;
        transition: all 0.4s cubic-bezier(0.165, 0.84, 0.44, 1);
        cursor: default;
    }
    
    .analysis-section:hover {
        background: rgba(255, 255, 255, 0.15);
        border-left-color: #FFD600;
        transform: translateX(10px);
        box-shadow: -5px 5px 15px rgba(255, 214, 0, 0.2);
    }
    
    .section-num {
        color: #FFD600;
        font-weight: 900;
        font-size: 1.2em;
        margin-right: 10px;
        border-bottom: 2px solid rgba(255, 214, 0, 0.3);
        padding-bottom: 5px;
        display: inline-block;
        margin-bottom: 10px;
    }

    .section-content {
        line-height: 1.6;
        font-size: 1.05em;
    }

    /* Estilos para listas dentro de secciones */
    .section-content ul {
        list-style-type: none;
        padding-left: 0;
    }
    .section-content li {
        margin-bottom: 8px;
        padding-left: 25px;
        position: relative;
    }
    .section-content li::before {
        content: "✨";
        position: absolute;
        left: 0;
        color: #FFD600;
    }

    /* Nutri-Score Pill */
    .nutri-score-inline {
        display: inline-block;
        padding: 10px 20px;
        border-radius: 12px;
        font-weight: 800;
        font-size: 20px;
        margin-bottom: 20px;
        color: white;
        text-transform: uppercase;
        box-shadow: 0 4px 10px rgba(0,0,0,0.3);
    }
    .score-A { background-color: #008b4c; }
    .score-B { background-color: #85bb2f; }
    .score-C { background-color: #fecb02; color: #000; }
    .score-D { background-color: #ee8100; }
    .score-E { background-color: #e63e11; }

    /* Barra lateral */
    [data-testid="stSidebar"] { background: linear-gradient(180deg, #590FB7 0%, #FF0076 100%); border-right: 5px solid #FFD600; }
    .stMarkdown, p, label { color: white !important; font-weight: 500; }

    .custom-footer {
        color: white !important; font-weight: 900 !important; text-align: center;
        padding: 30px; font-size: 1.1em; text-shadow: 0 0 10px rgba(255, 255, 255, 0.5);
    }
    </style>
    """, unsafe_allow_html=True)

# 3. BARRA LATERAL
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2424/2424569.png", width=80)
    st.markdown("<h1 style='color: white; text-align: center;'><span class='sidebar-icon'>🍽️</span> Configuración</h1>", unsafe_allow_html=True)
    st.divider()
    demo_mode = st.toggle("🚀 Activar Modo Demo", value=False)
    if demo_mode:
        tipus_demo = st.selectbox("Simulación:", ["Menú Completo", "Plato Único (Receta)"])
    else:
        api_key = st.text_input("Gemini API Key:", type="password")
    
    st.divider()
    idioma_analisis = st.text_input("🌍 Tu lenguaje favorito:", value="Castellano", placeholder="Ej: Japonés, Italiano...")
    
    st.markdown("<br><p style='font-style: italic; color: white;'>Selecciona una foto de un plato o menú para recibir consejos nutricionales personalizados.</p>", unsafe_allow_html=True)

# 4. CABECERA PRINCIPAL
st.markdown("""
    <h1 style='color: white; text-align: center;'>
        <span class='title-icon-left'>🥑</span> 
        Asistente de Menús Saludables 
        <span class='title-icon-right'>🥗</span>
    </h1>
    """, unsafe_allow_html=True)
st.markdown("<h5 style='color: white; text-align: center; font-weight: bold;'>DIGITALITZA TU ALIMENTACIÓN CON IA</h5>", unsafe_allow_html=True)
st.divider()

# 5. CUERPO DE LA APLICACIÓN - LAYOUT MEJORADO
# 5.1 Encabezado Centrado
_, col_header, _ = st.columns([1, 2, 1])
with col_header:
    st.markdown("""
        <div class="info-header-container">
            <span class='big-icon'>📸</span>
            <div class='info-header'>Sube la imagen</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# 5.2 Zona de Carga y Previsualización lado a lado
col_left, col_right = st.columns(2, gap="medium")

with col_left:
    uploaded_file = st.file_uploader("", type=["jpg", "jpeg", "png"], label_visibility="collapsed")
    if not uploaded_file:
        st.info("👈 Selecciona una foto desde tu dispositivo")

with col_right:
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, use_container_width=True, caption="Imagen cargada correctamente")
    else:
        st.markdown("""
            <div style="border: 3px dashed rgba(255,255,255,0.2); border-radius: 20px; height: 150px; display: flex; align-items: center; justify-content: center; color: rgba(255,255,255,0.4); font-weight: bold;">
                📷 Esperando imagen...
            </div>
        """, unsafe_allow_html=True)

# 5.3 Botón ANALIZAR debajo
st.markdown("<br>", unsafe_allow_html=True)
_, col_btn, _ = st.columns([1, 1.2, 1])
with col_btn:
    analitzar = st.button("🔍 ANALIZAR AHORA")

# 6. RESULTADOS UNIFICADOS
if uploaded_file and analitzar:
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<div class='info-header' style='text-align: center;'>📊 RESULTADO DEL ANÁLISIS</div>", unsafe_allow_html=True)
    
    with st.spinner('🌟 Analizando nutrición...'):
        time.sleep(1.5) 
        
        st.markdown("<div class='result-card'>", unsafe_allow_html=True)
        
        if demo_mode:
            st.markdown("<div class='nutri-score-inline score-A'>Calidad Nutricional: A - Excelente</div>", unsafe_allow_html=True)
            demo_sections = [
                ("1. Identificación", "<ul><li>🥗 Ensalada Saludable</li><li>🥑 Aguacate fresco</li><li>🍗 Pechuga de pollo</li></ul>"),
                ("2. Análisis Nutricional", "<ul><li>🔥 Calorías: 450 kcal</li><li>💪 Proteínas: 35g</li><li>🥑 Grasas saludables: 22g</li></ul>"),
                ("3. Recomendación", "<ul><li>🌿 Añade semillas para más fibra</li><li>💧 Bebe agua para acompañar</li></ul>"),
                ("4. Alérgenos", "<ul><li>🚫 Ninguno detectado</li><li>🌾 Libre de gluten</li></ul>")
            ]
            for title, content in demo_sections:
                st.markdown(f"<div class='analysis-section'><span class='section-num'>{title}</span><br><div class='section-content'>{content}</div></div>", unsafe_allow_html=True)
        else:
            try:
                if not api_key:
                    st.warning("⚠️ Introduce tu API Key en la barra lateral.")
                else:
                    genai.configure(api_key=api_key)
                    model = genai.GenerativeModel('gemini-3-flash-preview')
                    
                    prompt = f"""
                    Analiza esta imagen nutricionalmente. Responde en el idioma: {idioma_analisis}.
                    
                    ESTRUCTURA OBLIGATORIA (Usa Markdown y Emojis):
                    - Primera línea: [SCORE:A] o [SCORE:B], [SCORE:C], [SCORE:D], [SCORE:E] según la calidad.
                    - Luego, 4 secciones numeradas así:
                    PARTE 1: Identificación. (Usa una lista con viñetas y emojis de comida para los ingredientes).
                    PARTE 2: Análisis nutricional. (Usa viñetas para calorías, proteínas, grasas, etc.).
                    PARTE 3: Recomendaciones. (Usa viñetas con consejos de salud específicos).
                    PARTE 4: Alérgenos. (Lista clara con símbolos de advertencia ⚠️).
                    
                    IMPORTANTE: No escribas párrafos largos. Usa listas (puntos) para que sea muy visual.
                    """
                    
                    response = model.generate_content([prompt, image])
                    raw_text = response.text
                    
                    # Nutri-Score Pill
                    score_match = re.search(r'\[SCORE:([A-E])\]', raw_text)
                    if score_match:
                        score = score_match.group(1)
                        labels = {"A": "Excelente", "B": "Buena", "C": "Intermedia", "D": "Baja", "E": "Desfavorable"}
                        st.markdown(f"<div class='nutri-score-inline score-{score}'>Calidad Nutricional: {score} - {labels[score]}</div>", unsafe_allow_html=True)
                    
                    # Separar secciones 1, 2, 3, 4
                    sections = re.split(r'PARTE (\d):', raw_text)
                    section_titles = {1: "Identificación", 2: "Análisis Nutricional", 3: "Recomendaciones", 4: "Alérgenos"}
                    
                    for i in range(1, 5):
                        idx = sections.index(str(i)) + 1 if str(i) in sections else None
                        if idx:
                            content = sections[idx].strip()
                            # Convertir Markdown de la IA a HTML de Streamlit (st.markdown procesa markdown dentro de los divs)
                            st.markdown(f"""
                                <div class='analysis-section'>
                                    <span class='section-num'>{i}. {section_titles[i]}</span><br>
                                    <div class='section-content'>{st.markdown(content) if False else content}</div>
                                </div>
                            """, unsafe_allow_html=True)
                            
            except Exception as e:
                st.error(f"❌ Error: {e}")
        
        st.markdown("</div>", unsafe_allow_html=True)

# 7. PIE DE PÁGINA
st.divider()
st.markdown("<div class='custom-footer'>🚀 PROYECTO DIGITALIZACIÓN 2026 | DESARROLLADO CON GEMINI AI</div>", unsafe_allow_html=True)
