import streamlit as st
from google import genai
from google.genai import types

st.set_page_config(page_title="Aura AI - Stabile", page_icon="✨", layout="centered")
st.title("✨ Aura AI - Stabile")

# Leggiamo la chiave
api_key = st.secrets["API_KEY"]
client = genai.Client(api_key=api_key)

# Usiamo SOLO gemma, l'unico che sappiamo funzionare per te
model_name = "models/gemma-4-26b-a4b-it"

uploaded_file = st.file_uploader("Carica una foto...", type=['jpg', 'jpeg', 'png'])
user_input = st.text_area("Cosa vuoi chiedere?", placeholder="Scrivi qui...")

if st.button("Invia Domanda"):
    if user_input or uploaded_file:
        # Messaggio di attesa chiaro
        with st.spinner("Aura sta riflettendo... (questo modello richiede qualche secondo)"):
            contents = []
            if uploaded_file:
                bytes_data = uploaded_file.getvalue()
                mime_type = uploaded_file.type
                contents.append(types.Part.from_bytes(data=bytes_data, mime_type=mime_type))
            
            if user_input:
                contents.append(user_input)
            elif uploaded_file:
                contents.append("Cosa vedi in questa immagine? Spiegamelo.")
            
            try:
                # Chiamata classica senza streaming (niente più 'none')
                response = client.models.generate_content(
                    model=model_name,
                    contents=contents
                )
                st.subheader("Risposta:")
                st.write(response.text)
            except Exception as e:
                st.error("Si è verificato un errore, ma Aura è ancora qui. Riprova tra un istante.")
    else:
        st.warning("Inserisci del testo o carica una foto!")
