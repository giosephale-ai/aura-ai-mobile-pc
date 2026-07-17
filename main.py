import streamlit as st
from google import genai
from memory import MemoryManager # Importiamo il nostro modulo!

# Inizializziamo il modulo memoria
memoria = MemoryManager()

st.set_page_config(page_title="Jarvis OS", page_icon="🤖")

st.title("🤖 Jarvis OS - Nucleo Attivo")

# --- INTERFACCIA ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Esempio di come Jarvis "usa" la memoria
if st.sidebar.button("🧠 Leggi Memoria"):
    st.sidebar.json(memoria.leggi_tutta_la_memoria())

# Input Utente
if prompt := st.chat_input("Comanda Jarvis..."):
    # Jarvis salva automaticamente ciò che dici (esempio di base)
    memoria.salva_ricordo("conversazione", prompt)
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("assistant"):
        st.write("Ho archiviato il dato. Sono pronto ad eseguire.")
