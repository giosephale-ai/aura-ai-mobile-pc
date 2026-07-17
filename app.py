import streamlit as st
from google import genai
from duckduckgo_search import DDGS

st.set_page_config(page_title="Aura AI Architect", page_icon="🤖", layout="wide")

# --- BACKEND ---
api_key = st.secrets["API_KEY"]
client = genai.Client(api_key=api_key)

if "messages" not in st.session_state:
    st.session_state.messages = []

def cerca_su_internet(query):
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=3))
            return "\n".join([f"- {r['body']}" for r in results]) if results else None
    except:
        return None

# --- SIDEBAR (Centro di Controllo) ---
with st.sidebar:
    st.title("🤖 Aura Architect")
    mode = st.radio("Modalità Aura:", ["Assistente Generalista", "Software Architect"])
    use_web = st.checkbox("🌐 Cerca su Internet", value=True)
    
    st.divider()
    if st.button("🗑️ Reset Chat"):
        st.session_state.messages = []
        st.rerun()
    
    if st.session_state.messages:
        chat_text = "\n\n".join([f"{m['role'].upper()}: {m['content']}" for m in st.session_state.messages])
        st.download_button("💾 Esporta Memoria", chat_text, "aura_memoria.txt")

# --- LOGICA PERSONA ---
persona_prompts = {
    "Assistente Generalista": "Sei Aura, un assistente utile, cordiale e versatile.",
    "Software Architect": "Sei un programmatore esperto. Analizza le richieste di codice, suggerisci soluzioni efficienti, scrivi codice pulito in blocchi Markdown, anticipa problemi di bug."
}

# --- INTERFACCIA ---
st.title(f"✨ Aura AI: {mode}")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Cosa dobbiamo fare oggi?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Aura sta elaborando..."):
            try:
                # Costruiamo il contesto
                contesto = persona_prompts[mode]
                if use_web:
                    info_web = cerca_su_internet(prompt)
                    if info_web:
                        contesto += f"\n\nInformazioni web trovate: {info_web}"
                
                # Chiamata al cervello
                response = client.models.generate_content(
                    model="models/gemma-4-26b-a4b-it",
                    contents=f"{contesto}\n\nDomanda: {prompt}"
                )
                
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error("Errore: Il cervello è sovraccarico, riprova!")
