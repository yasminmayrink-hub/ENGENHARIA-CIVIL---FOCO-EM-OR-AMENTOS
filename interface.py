import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

st.title("Chatbot de Engenharia Civil - Foco em Orçamentos")
st.caption("Assistente especializado em orçamentos, SINAPI e composições de custo.")

with st.chat_message("assistant"):
    st.write("Olá! Sou um assistente de Inteligência Artificial especializado em Engenharia Civil. Estou preparado para auxiliar em orçamentos, composições de custo unitário, consultas ao SINAPI e TCPO, levantamento de quantitativos e análise de propostas técnicas. Como posso te ajudar hoje?")

if "historico" not in st.session_state:
    st.session_state.historico = [
        {
            "role": "system",
            "content": """Você é um assistente especializado em Engenharia Civil e Orçamentos. 
Você ajuda com elaboração de orçamentos, composições de custos, insumos, produtividades, 
propostas técnicas e índices de construção civil como SINAPI e TCPO. 
Responda sempre de forma técnica e objetiva, como um especialista da área."""
        }
    ]

for msg in st.session_state.historico:
    if msg["role"] == "system":
        continue
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

pergunta = st.chat_input("Digite sua mensagem...")

if pergunta:
    st.session_state.historico.append({"role": "user", "content": pergunta})
    with st.chat_message("user"):
        st.write(pergunta)

    resposta = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=st.session_state.historico
    )

    mensagem = resposta.choices[0].message.content
    st.session_state.historico.append({"role": "assistant", "content": mensagem})
    with st.chat_message("assistant"):
        st.write(mensagem)

