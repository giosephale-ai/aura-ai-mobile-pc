import streamlit as st
from google import genai
from duckduckgo_search import DDGS  # La nostra arma segreta

st.set_page_config(page_title="Aura AI - Web", page_icon="🌐")

api_key = st.secrets["API_KEY"]
client = genai.Client(api_key=api_key)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Funzione "Scamotage": Cerca su internet per noi
def cerca_su_internet(query):
    try:
        with DDGS() as ddgs:
            # Prende i primi 3 risultati
            results = list(ddgs.text(query, max_results=3))
            testo_risultati = "\n".join([f"- {r['body']}" for r in results])
            return testo_risultati
    except:
        return "Non sono riuscita a connettermi a internet."

# --- SIDEBAR ---
with st.sidebar:
    st.title("⚙️ Controllo")
    usa_web = st.checkbox("🌐 Cerca su Internet", value=False)
    
    if st.button("🗑️ Cancella Chat"):
        st.session_state.messages = []
        st.rerun()

# --- INTERFACCIA ---
st.title("✨ Aura AI - Connessa")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Chiedi qualcosa..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Aura sta cercando..."):
            try:
                final_prompt = prompt
                
                # Se l'utente vuole internet, facciamo lo scamotage
                if usa_web:
                    info_web = cerca_su_internet(prompt)
                    final_prompt = f"Usa queste informazioni trovate su internet per rispondere: {info_web}. \n\n Domanda dell'utente: {prompt}"
                
                # Inviamo a Gemma (che ora ha tutte le info!)
                response = client.models.generate_content(
                    model="models/gemma-4-26b-a4b-it",
                    contents=final_prompt
                )
                
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
                
            except Exception as e:
                st.error("Errore: " + str(e))
