import streamlit as st
from google import genai
from google.genai import types
import io

st.set_page_config(page_title="Aura AI Pro", page_icon="✨", layout="centered")
st.title("✨ Aura AI - Personal Assistant")

api_key = st.secrets["API_KEY"]
client = genai.Client(api_key=api_key)

model_options = [
    "models/gemini-3.5-flash", 
    "models/gemini-3.1-flash-image", 
    "models/gemma-4-26b-a4b-it"
]

model_name = st.selectbox("🧠 Scegli il cervello:", model_options)
use_search = st.checkbox("🔍 Attiva Ricerca Google")
uploaded_file = st.file_uploader("Carica una foto...", type=['jpg', 'jpeg', 'png'])
user_input = st.text_area("Cosa vuoi chiedere?", placeholder="Scrivi qui...")

if st.button("Invia Domanda"):
    if user_input or uploaded_file:
        with st.spinner("Aura sta analizzando..."):
            contents = []
            if uploaded_file:
                bytes_data = uploaded_file.getvalue()
                mime_type = uploaded_file.type
                contents.append(types.Part.from_bytes(data=bytes_data, mime_type=mime_type))
            if user_input:
                contents.append(user_input)
            elif uploaded_file:
                contents.append("Cosa vedi in questa immagine? Spiegamelo.")
            
            config = {}
            if use_search:
                config["tools"] = [types.Tool(google_search=types.GoogleSearch())]
            
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=contents,
                    config=types.GenerateContentConfig(**config)
                )
                st.subheader("Risposta di Aura AI:")
                st.write(response.text)
            except Exception as e:
                st.error(f"Errore tecnico: {e}")
    else:
        st.warning("Inserisci del testo o carica una foto!")
