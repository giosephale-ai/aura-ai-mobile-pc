import streamlit as st
from google import genai

st.set_page_config(page_title="Aura AI Manager", page_icon="📝")

# --- CONFIGURAZIONE ---
api_key = st.secrets["API_KEY"]
client = genai.Client(api_key=api_key)

# Inizializza memoria chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- SIDEBAR (Il tuo pannello di controllo) ---
with st.sidebar:
    st.title("⚙️ Impostazioni")
    
    # Selezione "Umori" (System Prompt)
    persona = st.selectbox("Come deve rispondere Aura?", 
                           ["Assistente Utile", "Creativo/Scrittore", "Breve e Tecnico"])
    
    st.divider()
    
    # Pulsante per cancellare
    if st.button("🗑️ Cancella Chat"):
        st.session_state.messages = []
        st.rerun()
    
    # Pulsante per scaricare la chat
    if st.session_state.messages:
        chat_text = "\n\n".join([f"{m['role'].upper()}: {m['content']}" for m in st.session_state.messages])
        st.download_button(label="💾 Scarica Chat (TXT)", data=chat_text, file_name="aura_chat.txt")

# --- INTERFACCIA CHAT ---
st.title("✨ Aura AI - Archivio")

# Mappa delle persone
system_instructions = {
    "Assistente Utile": "Sei un assistente cordiale, preciso e utile.",
    "Creativo/Scrittore": "Sei un assistente creativo, usi un tono ispirante ed eloquente.",
    "Breve e Tecnico": "Sei estremamente sintetico, vai dritto al punto, usa elenchi puntati."
}

# Mostra messaggi
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input utente
if prompt := st.chat_input("Chiedi qualcosa ad Aura..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Aura sta riflettendo..."):
            try:
                # Usiamo Gemma come base stabile
                response = client.models.generate_content(
                    model="models/gemma-4-26b-a4b-it",
                    contents=f"Istruzione: {system_instructions[persona]}. Domanda: {prompt}"
                )
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error("Errore temporaneo. Riprova.")
