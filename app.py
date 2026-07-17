import streamlit as st
import requests
from google import genai

st.set_page_config(page_title="Aura AI - Master", page_icon="🔥")
st.title("🔥 Aura AI - Sbloccata")

api_key = st.secrets["API_KEY"]
client = genai.Client(api_key=api_key)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Funzione per recuperare il meteo (senza API Key, senza Gemini)
def get_meteo(citta):
    try:
        url = f"https://wttr.in/{citta}?format=3"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return response.text
        return "Non sono riuscita a recuperare il meteo."
    except:
        return "Errore nella connessione meteo."

# UI
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Chiedi qualcosa..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Aura sta ragionando..."):
            # Logica: Se chiedi il meteo, il codice lo cerca ORA
            risposta_finale = ""
            
            if "meteo" in prompt.lower() or "gradi" in prompt.lower():
                # Estraiamo la città (molto semplice)
                citta = "Mondragone" # Di default
                if "a " in prompt.lower():
                    citta = prompt.lower().split("a ")[-1].replace("?", "").strip()
                
                info_meteo = get_meteo(citta)
                context = f"L'utente vuole sapere il meteo. Ecco il dato preso in tempo reale: {info_meteo}. Rispondi in modo naturale all'utente."
            else:
                context = prompt

            try:
                # Usiamo SEMPRE Gemma (che funziona)
                response = client.models.generate_content(
                    model="models/gemma-4-26b-a4b-it",
                    contents=context
                )
                risposta_finale = response.text
                st.markdown(risposta_finale)
                st.session_state.messages.append({"role": "assistant", "content": risposta_finale})
            except Exception as e:
                st.error("Errore: " + str(e))
