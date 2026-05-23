from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
import os

PASTA_DOCUMENTOS = "./documentos"
PASTA_BANCO = "./banco_vetorial"

def construir_banco():
    arquivos = [f for f in os.listdir(PASTA_DOCUMENTOS) if f.endswith(".pdf")]

    if not arquivos:
        return None

    documentos = []
    for arquivo in arquivos:
        loader = PyPDFLoader(os.path.join(PASTA_DOCUMENTOS, arquivo))
        documentos.extend(loader.load())

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.split_documents(documentos)

    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    banco = Chroma.from_documents(chunks, embeddings, persist_directory=PASTA_BANCO)
    return banco

def buscar_contexto(pergunta, banco):
    resultados = banco.similarity_search(pergunta, k=3)
    return "\n\n".join([doc.page_content for doc in resultados])