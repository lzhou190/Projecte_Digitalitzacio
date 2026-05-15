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
st.title("🥗 Assistent de Menús Saludables")
st.write("Digitalitza la teva alimentació amb Intel·ligència Artificial.")
st.write("---")

# 4. COS DE L'APLICACIÓ
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown("<div class='info-header'>📸 Puja la teva imatge</div>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("", type=["jpg", "jpeg", "png"])
    
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, use_container_width=True)
        analitzar = st.button("🔍 ANALITZAR AMB IA")
with col2:
    st.markdown("<div class='info-header'>📊 Resultat de l'Anàlisi</div>", unsafe_allow_html=True)
    if uploaded_file and analitzar:
        with st.spinner('Processant...'):
            time.sleep(2)
            st.markdown("<div class='result-card'>", unsafe_allow_html=True)
            if demo_mode:
                if tipus_demo == "Menú Complet":
                    st.success("✅ Menú detectat")
                    st.markdown("""
                    **📋 Detall del Menú:**
                    * **Primer plat:** Crema de carbassa o Amanida de tomàquet.
                    * **Segon plat:** Llobarro al forn o Hamburguesa amb formatge.
                    * **Postres:** Fruita o Iogurt natural.
                    * **Beguda:** Aigua mineral.
                    
                    **🥗 Recomanació:**
                    Tria la **Crema + Llobarro** per un dinar equilibrat.
                    """)
                else:
                    st.success("✅ Plat detectat")
                    st.markdown("""
                    **🥗 Plat:** Amanida Cobb.
                    * **Ingredients:** Pollastre, ou, alvocat, formatge.
                    * **Al·lèrgens:** Ous i Lactosa.
                    * **Consell:** Molta proteïna, però vigila amb les salses!
                    """)
            else:
                try:
                    genai.configure(api_key=api_key)
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    prompt = "Analitza aquesta imatge. Si és menú, transcriu-lo. Si és plat, dona consells nutricionals. Respon en català."
                    response = model.generate_content([prompt, image])
                    st.write(response.text)
                except Exception as e:
                    st.error(f"Error: {e}")
            st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.info("Surtirà aquí un cop pugis la foto.")
