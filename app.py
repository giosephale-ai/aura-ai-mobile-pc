import streamlit as st
from google import genai
from google.genai import types

st.set_page_config(page_title="Aura AI Turbo", page_icon="⚡", layout="centered")
st.title("⚡ Aura AI - Turbo Mode")

api_key = st.secrets["API_KEY"]
client = genai.Client(api_key=api_key)

# Abbiamo messo i modelli FLASH al primo posto perché sono i più veloci
model_options = [
    "models/gemini-2.0-flash", 
    "models/gemini-3.5-flash",
    "models/gemma-4-26b-a4b-it" 
]
model_name = st.selectbox("🧠 Scegli il cervello (Flash è più veloce):", model_options)

uploaded_file = st.file_uploader("Carica una foto...", type=['jpg', 'jpeg', 'png'])
user_input = st.text_area("Cosa vuoi chiedere?", placeholder="Scrivi qui...")

if st.button("Invia Domanda"):
    if user_input or uploaded_file:
        contents = []
        if uploaded_file:
            bytes_data = uploaded_file.getvalue()
            mime_type = uploaded_file.type
            contents.append(types.Part.from_bytes(data=bytes_data, mime_type=mime_type))
        if user_input:
            contents.append(user_input)
        elif uploaded_file:
            contents.append("Cosa vedi qui? Spiegamelo brevemente.")
            
        with st.chat_message("assistant"):
            try:
                # Usiamo generate_content_stream per vedere la risposta che arriva "a pezzi"
                response = client.models.generate_content_stream(
                    model=model_name,
                    contents=contents
                )
                # Streamlit scriverà i pezzi man mano che arrivano
                st.write_stream(chunk.text for chunk in response)
            except Exception as e:
                st.error(f"Errore: {e}. Prova a cambiare modello nel menu!")
    else:
        st.warning("Inserisci del testo o carica una foto!")
