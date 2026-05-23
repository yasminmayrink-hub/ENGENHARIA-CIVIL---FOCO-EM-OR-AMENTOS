import streamlit as st
from groq import Groq
from dotenv import load_dotenv
from rag import construir_banco, buscar_contexto
import os

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

st.title("🏗️Chatbot de Engenharia Civil - Foco em Orçamentos")
st.caption("Especializado em orçamentos, SINAPI e composições de custo.")

if "banco" not in st.session_state:
    st.session_state.banco = construir_banco()

with st.chat_message("assistant", avatar="📈"):
    st.write("Olá! Sou um assistente de Inteligência Artificial especializado em Engenharia Civil. Estou preparado para auxiliar em orçamentos, composições de custo unitário, consultas ao SINAPI e TCPO, levantamento de quantitativos e análise de propostas técnicas. Como posso te ajudar hoje?")

if "historico" not in st.session_state:
    st.session_state.historico = [
        {
            "role": "system",
            "content": """Você é um assistente especializado em Engenharia Civil e Orçamentos.

SUAS ESPECIALIDADES:
- Elaboração e análise de orçamentos de obras
- Composições de custo unitário (SINAPI, TCPO)
- Cálculo de BDI (Benefícios e Despesas Indiretas)
- Levantamento de quantitativos
- Cronograma físico-financeiro
- Análise de propostas técnicas
- Normas ABNT relacionadas à construção civil

REFERÊNCIAS QUE VOCÊ UTILIZA:
- Tabela SINAPI
- TCPO
- PINI, CUB/m², INCC

COMO RESPONDER:
- Sempre de forma técnica e objetiva
- Cite referências quando aplicável
- Se não souber algo específico, indique onde o usuário pode pesquisar
- Responda sempre em português
"""
        }
    ]

for msg in st.session_state.historico:
    if msg["role"] == "system":
        continue
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

pergunta = st.chat_input("Digite sua mensagem...")

if pergunta:
    contexto = ""
    if st.session_state.banco:
        contexto = buscar_contexto(pergunta, st.session_state.banco)

    mensagem_com_contexto = pergunta
    if contexto:
        mensagem_com_contexto = f"Contexto dos documentos:\n{contexto}\n\nPergunta: {pergunta}"

    st.session_state.historico.append({"role": "user", "content": mensagem_com_contexto})
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