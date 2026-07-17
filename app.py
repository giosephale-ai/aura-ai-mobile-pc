import streamlit as st
from google import genai
from google.genai import types

st.set_page_config(page_title="Aura AI Pro", page_icon="✨")
st.title("✨ Aura AI - Personal Assistant Pro")

api_key = st.secrets["API_KEY"]
client = genai.Client(api_key=api_key)

# Inizializziamo la memoria delle chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Creiamo due tab: una per chattare, una per creare immagini
tab1, tab2 = st.tabs(["💬 Chat", "🎨 Crea Immagini"])

# --- TAB 1: CHAT ---
with tab1:
    st.header("Chat con Aura")
    
    # Mostriamo la cronologia
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Input dell'utente
    if prompt := st.chat_input("Scrivi a Aura..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Aura sta elaborando..."):
                try:
                    # PROVA IL MODELLO LITE: se fallisce, torna a gemma
                    model = "models/gemini-2.0-flash-lite-001" 
                    response = client.models.generate_content(
                        model=model,
                        contents=prompt
                    )
                    st.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                except:
                    # Fallback automatico su Gemma se Flash Lite fallisce
                    response = client.models.generate_content(
                        model="models/gemma-4-26b-a4b-it",
                        contents=prompt
                    )
                    st.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})

# --- TAB 2: IMMAGINI ---
with tab2:
    st.header("Generatore Immagini")
    prompt_img = st.text_input("Descrivi l'immagine che vuoi creare:")
    if st.button("Crea Immagine"):
        with st.spinner("Aura sta dipingendo..."):
            try:
                result = client.models.generate_images(
                    model="models/imagen-4.0-generate-001",
                    prompt=prompt_img,
                    config=types.GenerateImagesConfig(number_of_images=1)
                )
                for generated_image in result.generated_images:
                    st.image(generated_image.image.image_bytes)
            except Exception as e:
                st.error(f"Impossibile creare l'immagine: {e}")
