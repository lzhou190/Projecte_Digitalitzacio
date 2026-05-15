# 1. IMPORTACIÓ DE LLIBRERIES
# ---------------------------
import streamlit as st          # Eina per crear la interfície web (recomanada per la IA)
from PIL import Image           # Per obrir i manipular imatges (necessari per llegir les fotos dels plats)
# GOOGLE GENERATIVE AI: És la connexió amb la Intel·ligència Artificial GEMINI.
# utilitzant una clau privada (API Key) per enviar preguntes i rebre respostes.
import google.generativeai as genai 
import time                     # Per controlar el temps i fer animacions de càrrega

# ==================================================
# PAS 2: CONFIGURACIÓ DE LA PÀGINA WEB (Streamlit)
# ==================================================
# Definim com es veurà la finestra del navegador: títol, icona i mida
st.set_page_config(
    page_title="Menú Saludable IA",
    page_icon="🥗",
    layout="wide"  # Utilitzem tota l'amplada de la pantalla per tenir més espai
)

# ==================================================
# PAS 3: ESTILS I DISSENY VISUAL (Millores respecte versió 1)
# ==================================================
# Aquí afegim codi de disseny (CSS) per fer la web molt més atractiva i moderna.
# Aquesta part és estètica: colors, animacions, ombres, vores... no canvia el funcionament,
# però millora molt la presentació del projecte final.
st.markdown("""
    <style>
    /* Fons de pantalla amb degradat de colors vius */
    .stApp {
        background: linear-gradient(135deg, #FF0076 0%, #590FB7 45%, #FFD600 100%);
        background-attachment: fixed;
    }

    /* Amaguem la capçalera que posa Streamlit per defecte */
    header[data-testid="stHeader"] {
        background: transparent !important;
    }
    
    /* Amaguem el peu de pàgina que posa "Made with Streamlit" */
    footer {
        visibility: hidden;
    }

    /* Contenidors amb estil "VIDRE": transparents i amb desenfocament */
    [data-testid="stVerticalBlock"] > div:has(div.info-header) {
        background: rgba(0, 0, 0, 0.25);
        backdrop-filter: blur(15px);
        padding: 40px;
        border-radius: 35px;         /* Cantonades arrodonides */
        border: 3px solid #FF0076;   /* Línia de color rosa */
        box-shadow: 0 0 25px rgba(255, 0, 118, 0.4); /* Brillantor al voltant */
        margin-bottom: 25px;
        text-align: center;
    }

    /* 🌟 NOVETAT: ANIMACIONS PER A LES ICONES DEL TÍTOL 🌟 */
    .title-icon-left {
        display: inline-block;
        animation: pulse-tilt 4s ease-in-out infinite; /* Moviment continu */
    }
    
    .title-icon-right {
        display: inline-block;
        animation: rotate-float 5s ease-in-out infinite;
    }

    /* Definim com serà el moviment de les icones */
    @keyframes pulse-tilt {
        0% { transform: scale(1) rotate(0deg); }
        50% { transform: scale(1.2) rotate(-15deg); } /* Es fa gran i gira */
        100% { transform: scale(1) rotate(0deg); }
    }

    @keyframes rotate-float {
        0% { transform: translateY(0px) rotate(0deg); }
        50% { transform: translateY(-10px) rotate(15deg); } /* Pugeu i baixa */
        100% { transform: translateY(0px) rotate(0deg); }
    }

    /* Icones grans de les seccions (📸 i 📊) que "volen" amunt i avall */
    .big-icon {
        font-size: 80px;
        display: block;
        margin-bottom: 10px;
        filter: drop-shadow(0 0 15px rgba(255, 255, 255, 0.5)); /* Brillantor blanc */
        animation: levitate 3s ease-in-out infinite;
    }

    @keyframes levitate {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-15px); }
        100% { transform: translateY(0px); }
    }

    /* Estil dels títols de cada apartat */
    .info-header {
        color: #ffffff !important;
        font-family: 'Segoe UI', sans-serif;
        font-size: 28px;
        font-weight: 900;
        text-transform: uppercase;
        letter-spacing: 2px; /* Lletra separada, més moderna */
        text-shadow: 2px 2px 8px rgba(0,0,0,0.5); /* Ombra al text */
        margin-bottom: 20px;
    }

    /* Línies separadores de colors (arc de Sant Martí) */
    hr {
        border: 0;
        height: 5px;
        background: linear-gradient(90deg, #FF0076, #FFD600, #00FFFF);
        border-radius: 10px;
        margin: 2em 0 !important;
    }

    /* ESTIL DEL BOTÓ PRINCIPAL: Gran, amb efectes quan hi passes el ratolí */
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
    
    /* ✨ Efecte visual quan passes el ratolí per sobre del botó */
    .stButton>button:hover {
        transform: scale(1.05); /* Es fa una mica més gran */
        box-shadow: 0 15px 40px rgba(255, 214, 0, 0.6);
        border-color: white;
    }

    /* Targeta on surt l'anàlisi: fons fosc i lletres blanques */
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

    /* Barra lateral esquerra amb el mateix estil de colors */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #590FB7 0%, #FF0076 100%);
        border-right: 5px solid #FFD600;
    }

    .stMarkdown, p, label {
        color: white !important;
        font-weight: 500;
    }

    /* Peu de pàgina personalitzat amb el nom del projecte */
    .custom-footer {
        color: white !important;
        font-weight: 900 !important;
        text-align: center;
        padding: 30px;
        font-size: 1.3em;
        text-shadow: 0 0 10px rgba(255, 255, 255, 0.5);
    }
    </style>
    """, unsafe_allow_html=True) # Aquesta ordre permet a Streamlit utilitzar el codi de disseny

# ==================================================
# PAS 4: BARRA LATERAL DE CONFIGURACIÓ
# ==================================================
# Amb Streamlit, 'st.sidebar' crea automàticament la columna de l'esquerra
with st.sidebar:
    # Posem una icona de menjar des d'internet
    st.image("https://cdn-icons-png.flaticon.com/512/2424/2424569.png", width=100)
    
    # Títol amb icona afegida
    st.markdown("<h1 style='color: white; text-align: center;'>🛠️ Configuració</h1>", unsafe_allow_html=True)
    st.divider()

    # INTERRUPTOR: Mode Demo (sense connexió) o Mode Real (amb Intel·ligència Artificial)
    demo_mode = st.toggle("🚀 Activar Mode Demo", value=True)

    if demo_mode:
        # Si estem en demostració: triem quin exemple veure
        tipus_demo = st.selectbox("Simulació:", ["Menú Complet", "Plat Únic (Recepta)"])
    else:
        # 🔑 SI UTILITZEM LA IA: AQUÍ ÉS ON APLIQUEM EL QUE VAREM VEURE A CLASSE
        # Demanem la CLAU D'ACCÉS (API Key), igual que es fa amb ChatGPT o OpenAI.
        # Sense aquesta clau, no podem connectar amb el servidor de Google.
        api_key = st.text_input("Gemini API Key:", type="password") # 'password' amaga el text escrit

    # Text informatiu per a l'usuari
    st.markdown("<br><p style='font-style: italic; color: white;'>Selecciona una foto d'un plat o menú per rebre consells nutricionals personalitzats.</p>", unsafe_allow_html=True)

# ==================================================
# PAS 5: CAPÇALERA PRINCIPAL AMB ANIMACIONS
# ==================================================
# Títol principal amb les icones que es mouen (definides al principi amb CSS)
st.markdown("""
    <h1 style='color: white; text-align: center;'>
        <span class='title-icon-left'>🥑</span> 
        Assistent de Menús Saludables 
        <span class='title-icon-right'>🥗</span>
    </h1>
    """, unsafe_allow_html=True)
st.markdown("<h5 style='color: white; text-align: center; font-weight: bold;'>DIGITALITZA LA TEVA ALIMENTACIÓ AMB IA</h5>", unsafe_allow_html=True)
st.divider()

# ==================================================
# PAS 6: COS DE L'APLICACIÓ - DUES COLUMNES
# ==================================================
# Dividim la pantalla en dues parts: una per pujar foto, una altra per veure resultats
col1, col2 = st.columns([1, 1.2], gap="large")

# ---------- COLUMNA 1: PUJAR IMATGE---------
with col1:
    st.markdown("""
        <div>
            <span class='big-icon'>📸</span>
            <div class='info-header'>Puja la imatge</div>
        </div>
    """, unsafe_allow_html=True)

    # Eina de Streamlit: botó per seleccionar fotos de l'ordinador
    uploaded_file = st.file_uploader("", type=["jpg", "jpeg", "png"])
    
    # Si l'usuari ha pujat una foto...
    if uploaded_file:
        image = Image.open(uploaded_file) # Obrim la imatge
        st.image(image, use_container_width=True, caption="Imatge preparada") # La mostrem
        analitzar = st.button("🔍 ANALITZAR ARA") # Botó per començar
    else:
        # Missatge per defecte si encara no s'ha pujat res
        st.markdown("<p style='text-align: center;'>☝️ Tria una foto per començar</p>", unsafe_allow_html=True)

# ---------- COLUMNA 2: RESULTATS DE L'ANÀLISI ----------
with col2:
    st.markdown("""
        <div>
            <span class='big-icon'>📊</span>
            <div class='info-header'>Resultat anàlisi</div>
        </div>
    """, unsafe_allow_html=True)
    
    # Només treballem si hi ha foto i s'ha premut el botó
    if uploaded_file and 'analitzar' in locals() and analitzar:
        with st.spinner('🌟 Estem analitzant les propietats nutricionals...'):
            time.sleep(2) # Petita espera per simular procés i que es vegi l'animació
            
            st.markdown("<div class='result-card'>", unsafe_allow_html=True)
            
            # 🌟 NOVETAT: DUES SUB-COLUMNES PER POSAR DADES NUMÈRIQUES 🌟
            m1, m2 = st.columns(2)
            
            # --------------------------
            # OPCIÓ 1: MODE DEMO (EXEMPLES)
            # --------------------------
            if demo_mode:
                if tipus_demo == "Menú Complet":
                    # 🔢 NOVETAT: Utilitzem 'metric' per mostrar dades com si fossin indicadors professionals
                    m1.metric("Qualitat Nutricional", "A", "Molt alta")
                    m2.metric("Tipus de Menú", "Equilibrat")
                    st.success("✅ Menú analitzat amb èxit") # Missatge de correcte
                    
                    # Text explicatiu del menú
                    st.markdown("""
                    ### 📋 Detall del Menú:
                    *   **Primer plat:** Crema de carbassa 🎃 o Amanida de tomàquet 🍅.
                    *   **Segon plat:** Llobarro al forn 🐟 o Hamburguesa vegetal 🌿.
                    *   **Postres:** Fruita de temporada 🍎 o Iogurt natural 🥛.
                    
                    ---
                    ### 🥗 El nostre consell:
                    La combinació de **Crema + Llobarro** és excel·lent. Proporciona fibra, proteïna de gran qualitat i greixos saludables.
                    """)
                
                else: # Si hem triat "Plat Únic"
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
                st.info("Penja una imatge o activa el mode demo per veure l'anàlisi.")
    
    st.markdown("</div>", unsafe_allow_html=True)
