import streamlit as st
from google import genai
from duckduckgo_search import DDGS
import logging

# Configurazione Logging per debugging professionale
logging.basicConfig(level=logging.INFO)

st.set_page_config(page_title="Aura AI Architect", page_icon="🤖", layout="wide")

# --- CONFIGURAZIONE E COSTANTI ---
PERSONA_PROMPTS = {
    "Assistente Generalista": "Sei Aura, un assistente utile, cordiale e versatile.",
    "Software Architect": "Sei un programmatore esperto. Analizza le richieste di codice, suggerisci soluzioni efficienti, scrivi codice pulito in blocchi Markdown e anticipa i bug."
}

# --- BACKEND ---
@st.cache_resource
def get_client():
    """Usa cache per non ricreare il client ad ogni rerun di Streamlit."""
    try:
        return genai.Client(api_key=st.secrets["API_KEY"])
    except Exception as e:
        st.error(f"Errore configurazione API: {e}")
        return None

client = get_client()

def cerca_su_internet(query: str) -> str:
    """Esegue una ricerca web e formatta i risultati."""
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=3))
            if not results:
                return ""
            formatted_results = "\n".join([f"- {r['body']}" for r in results])
            return f"DATI RILEVATI DA WEB:\n{formatted_results}"
    except Exception as e:
        logging.error(f"Errore ricerca web: {e}")
        return ""

# --- STATE MANAGEMENT ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- SIDEBAR ---
with st.sidebar:
    st.title("🤖 Aura Architect")
    mode = st.radio("Modalità Aura:", list(PERSONA_PROMPTS.keys()))
    use_web = st.checkbox("🌐 Cerca su Internet", value=True)

    st.divider()
    if st.button("🗑️ Reset Chat"):
        st.session_state.messages = []
        st.rerun()

    if st.session_state.messages:
        # Esportazione pulita
        chat_history = "\n".join([f"{m['role'].upper()}: {m['content']}" for m in st.session_state.messages])
        st.download_button("💾 Esporta Memoria", chat_history, "aura_memoria.txt")

# --- INTERFACCIA PRINCIPALE ---
st.title(f"✨ Aura AI: {mode}")

# Visualizzazione cronologia
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- LOGICA DI CHAT ---
if prompt := st.chat_input("Cosa dobbiamo fare oggi?"):
    # 1. Mostra e salva messaggio utente
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Elaborazione risposta
    with st.chat_message("assistant"):
        with st.spinner("Aura sta elaborando..."):
            try:
                # Preparazione contesto: System Prompt + Ricerca Web (se necessaria)
                system_instruction = PERSONA_PROMPTS[mode]

                web_context = ""
                if use_web:
                    web_context = cerca_su_internet(prompt)

                # Costruzione della lista messaggi per l'API (Mantenimento Memoria)
                # Inseriamo il System Prompt come primo elemento o come istruzione speciale
                api_messages = []

                # Aggiungiamo il System Prompt come un messaggio di sistema (se supportato) 
                # o lo iniettiamo all'inizio della conversazione
                api_messages.append({"role": "user", "content": f"SYSTEM INSTRUCTION: {system_instruction}"})
                api_messages.append({"role": "model", "content": "Understood. I will act according to these instructions."})

                # Aggiungiamo la cronologia esistente
                for m in st.session_state.messages:
                    # Mappiamo il ruolo 'assistant' in 'model' per l'API di Google
                    role = "model" if m["role"] == "assistant" else "user"
                    api_messages.append({"role": role, "content": m["content"]})

                # Se abbiamo dati dal web, li iniettiamo come un messaggio di sistema/utente speciale
                if web_context:
                    api_messages.append({"role": "user", "content": f"{web_context}\n\nUsa queste informazioni per rispondere alla domanda precedente."})

                # 3. Chiamata al modello
                # Nota: Assicurati che il nome del modello sia corretto per il tuo ambiente
                response = client.models.generate_content(
                    model="gemini-2.0-flash", # Suggerisco un modello aggiornato e veloce
                    contents=api_messages
                )

                full_response = response.text
                st.markdown(full_response)

                # 4. Salva risposta assistant
                st.session_state.messages.append({"role": "assistant", "content": full_response})

            except Exception as e:
                logging.error(f"Errore durante la generazione: {e}")
                st.error("⚠️ Errore di comunicazione con il cervello AI. Controlla la connessione o la chiave API.")
