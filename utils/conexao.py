
import streamlit as st
from pymongo import MongoClient

# Configurações do MongoDB
MONGO_URI = "mongodb://localhost:27017/"
NOME_BANCO = "bolinuts"
NOME_COLECAO = "pedidos"


@st.cache_resource
def obter_cliente():

    cliente = MongoClient(
        MONGO_URI,
        serverSelectionTimeoutMS=5000
    )

    # Testar conexão
    cliente.admin.command("ping")

    return cliente


def obter_colecao():

    cliente = obter_cliente()

    banco = cliente[NOME_BANCO]

    colecao = banco[NOME_COLECAO]

    return colecao


def obter_nome_banco():

    return NOME_BANCO



