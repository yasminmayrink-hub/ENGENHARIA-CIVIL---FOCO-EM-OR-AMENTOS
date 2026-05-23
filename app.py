from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

historico = []

print("Chatbot iniciado! Digite 'sair' para encerrar.")
historico = [
    {
        "role": "system",
        "content": """Você é um assistente especializado em engenharia civil com foco em orçamentos.
        Você ajuda profissionais e estudantes com cálculos de orçamento, composição de custos, 
        planilhas SINAPI, BDI, quantitativos de materiais, cronograma físico-financeiro e 
        normas técnicas da construção civil brasileira.
        Responda sempre em português, a menos que te peçam outro idioma, de forma clara e objetiva."""
    }
]
while True:
    pergunta = input("Você: ")
    if pergunta.lower() == "sair":
        break

    historico.append({"role": "user", "content": pergunta})

    resposta = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=historico
    )

    mensagem = resposta.choices[0].message.content
    historico.append({"role": "assistant", "content": mensagem})
    print(f"Bot: {mensagem}")