import streamlit as st
import logging
from google import genai
from duckduckgo_search import DDGS

# --- CONFIGURAZIONE LOGGING (Per capire gli errori) ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

st.set_page_config(page_title="Aura AI Architect", page_icon="🏗️", layout="wide")

# --- INIZIALIZZAZIONE ---
try:
    api_key = st.secrets["API_KEY"]
    client = genai.Client(api_key=api_key)
except Exception as e:
    st.error("Errore critico: Configurazione API fallita. Controlla i Secrets.")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- FUNZIONI DI SERVIZIO ---
def cerca_su_internet(query):
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=3))
            if results:
                return "\n".join([f"- {r['title']}: {r['body']}" for r in results])
        return None
    except Exception as e:
        logger.error(f"Errore ricerca web: {e}")
        return None

# --- UI SIDEBAR ---
with st.sidebar:
    st.title("🛠️ Pannello Controllo")
    use_web = st.checkbox("🌐 Abilita Ricerca Web", value=True)
    if st.button("🗑️ Reset Chat"):
        st.session_state.messages = []
        st.rerun()

# --- MAIN LOOP ---
st.title("🏗️ Aura AI Architect")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Scrivi codice o chiedi info..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Aura sta lavorando..."):
            try:
                # Logica RAG (Retrieval Augmented Generation)
                system_prompt = "Sei un senior software engineer. Rispondi in modo tecnico, preciso e scrivi codice pulito."
                
                final_content = prompt
                if use_web:
                    info_web = cerca_su_internet(prompt)
                    if info_web:
                        final_content = f"Dati Web:\n{info_web}\n\nDomanda: {prompt}"

                response = client.models.generate_content(
                    model="models/gemma-4-26b-a4b-it",
                    contents=f"{system_prompt}\n\n{final_content}"
                )
                
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
                
            except Exception as e:
                logger.error(f"Errore generazione: {e}")
                st.error("Errore: Il cervello ha riscontrato un problema. Verifica la console.")
