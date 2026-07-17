import streamlit as st
from google import genai
from google.genai import types

st.set_page_config(page_title="Aura AI Pro", page_icon="✨")
st.title("✨ Aura AI - Pro Studio")

api_key = st.secrets["API_KEY"]
client = genai.Client(api_key=api_key)

# Inizializziamo memoria
if "messages" not in st.session_state:
    st.session_state.messages = []

tab1, tab2 = st.tabs(["💬 Chat", "🎨 Crea Immagini"])

# --- TAB 1: CHAT ---
with tab1:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Scrivi a Aura..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Aura sta elaborando..."):
                try:
                    # Tentiamo con Lite
                    model = "models/gemini-2.0-flash-lite-001" 
                    response = client.models.generate_content(model=model, contents=prompt)
                    st.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                except Exception as e:
                    # Se fallisce, usiamo Gemma (fallback)
                    response = client.models.generate_content(
                        model="models/gemma-4-26b-a4b-it",
                        contents=prompt
                    )
                    st.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})

# --- TAB 2: IMMAGINI ---
with tab2:
    st.header("Generatore Immagini")
    prompt_img = st.text_input("Descrivi l'immagine:")
    if st.button("Crea Immagine"):
        with st.spinner("Aura sta creando..."):
            try:
                # Proviamo il modello Fast
                result = client.models.generate_images(
                    model="models/imagen-4.0-fast-generate-001",
                    prompt=prompt_img,
                    config=types.GenerateImagesConfig(number_of_images=1)
                )
                for generated_image in result.generated_images:
                    st.image(generated_image.image.image_bytes)
            except Exception as e:
                # Qui vedremo l'errore reale se succede ancora
                st.error(f"Errore tecnico (copialo e dimmelo): {e}")
