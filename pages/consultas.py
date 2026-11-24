import streamlit as st
import pandas as pd
from datetime import date
from utils.conexao import obter_colecao

st.set_page_config(page_title="Consultas MongoDB | Bolinuts", page_icon="🔎", layout="wide")
st.markdown("""
<style>
.stApp{background:linear-gradient(180deg,#FFFBF8 0%,#FAF7F6 100%);} h1,h2,h3{color:#75465B;}
div[data-testid="stMetric"]{background:#fff;border:1px solid #EEE2E7;border-radius:14px;padding:15px;box-shadow:0 4px 14px rgba(117,70,91,.04);}
div[data-testid="stMetricValue"]{color:#75465B;}
[data-testid="stTabs"] button[aria-selected="true"]{color:#75465B !important;border-bottom-color:#B66F8C !important;}
[data-testid="stDataFrame"]{border:1px solid #EEE2E7;border-radius:12px;overflow:hidden;}
[data-testid="stExpander"]{border:1px solid #EEE2E7;border-radius:12px;background:#FFFEFD;}
[data-testid="stAlert"]{border-radius:12px;}
</style>
""", unsafe_allow_html=True)

st.title("🔎 Consultas e análises MongoDB")
st.caption("Consultas com filtros, projeções, operadores e agregações diretamente na coleção pedidos.")
st.divider()

try:
    colecao = obter_colecao()
    total_documentos = colecao.count_documents({})
except Exception as erro:
    st.error(f"Não foi possível conectar ao MongoDB: {erro}")
    st.stop()

st.metric("Documentos na coleção", total_documentos)

# Consulta 1: faturamento agrupado por mês (agregação + projeção + ordenação).
pipeline_mensal = [
    {"$addFields": {"data_convertida": {"$convert": {"input": "$data_entrega", "to": "date", "onError": None, "onNull": None}},
                     "total_num": {"$convert": {"input": "$valor_total", "to": "double", "onError": 0, "onNull": 0}}}},
    {"$match": {"data_convertida": {"$ne": None}}},
    {"$group": {"_id": {"ano": {"$year": "$data_convertida"}, "mes": {"$month": "$data_convertida"},
                         "mes_nome": {"$dateToString": {"format": "%m/%Y", "date": "$data_convertida"}}},
                "pedidos": {"$sum": 1}, "faturamento": {"$sum": "$total_num"}}},
    {"$project": {"_id": 0, "Período": "$_id.mes_nome", "Pedidos": "$pedidos", "Faturamento (R$)": {"$round": ["$faturamento", 2]},
                   "Ano": "$_id.ano", "Mês": "$_id.mes"}},
    {"$sort": {"Ano": 1, "Mês": 1}}
]

# Consulta 2: clientes com maior volume de compras ($group, $sum, $sort e $limit).
pipeline_clientes = [
    {"$group": {"_id": "$nome_cliente", "quantidade_pedidos": {"$sum": 1},
                "valor_compras": {"$sum": {"$convert": {"input": "$valor_total", "to": "double", "onError": 0, "onNull": 0}}}}},
    {"$sort": {"valor_compras": -1}}, {"$limit": 10},
    {"$project": {"_id": 0, "Cliente": "$_id", "Pedidos": "$quantidade_pedidos", "Total comprado (R$)": {"$round": ["$valor_compras", 2]}}}
]

# Consulta 3: sabores/massas mais utilizados ($unwind e $group).
pipeline_massas = [
    {"$project": {"massa_lista": {"$cond": [{"$isArray": "$massa"}, "$massa", ["$massa"]]},
                   "quantidade_num": {"$convert": {"input": "$quantidade", "to": "double", "onError": 0, "onNull": 0}}}},
    {"$unwind": "$massa_lista"},
    {"$match": {"massa_lista": {"$nin": [None, ""]}}},
    {"$group": {"_id": "$massa_lista", "pedidos": {"$sum": 1}, "unidades": {"$sum": "$quantidade_num"}}},
    {"$sort": {"unidades": -1}},
    {"$project": {"_id": 0, "Massa": "$_id", "Pedidos": "$pedidos", "Unidades": "$unidades"}}
]

# Consulta 4: pedidos com saldo em aberto ($addFields, $expr, $gt e $project).
pipeline_abertos = [
    {"$addFields": {"total_num": {"$convert": {"input": "$valor_total", "to": "double", "onError": 0, "onNull": 0}},
                     "recebido_num": {"$convert": {"input": "$valor_sinal", "to": "double", "onError": 0, "onNull": 0}}}},
    {"$addFields": {"saldo_calculado": {"$max": [0, {"$subtract": ["$total_num", "$recebido_num"]}]}}},
    {"$match": {"$expr": {"$gt": ["$saldo_calculado", 0]}}},
    {"$project": {"_id": 0, "Código": "$codigo_pedido", "Cliente": "$nome_cliente", "Entrega": "$data_entrega",
                   "Total (R$)": "$total_num", "Recebido (R$)": "$recebido_num", "Saldo (R$)": {"$round": ["$saldo_calculado", 2]}}},
    {"$sort": {"Entrega": 1}}
]

consultas = [
    ("Faturamento mensal", pipeline_mensal, "Agrupa os pedidos por mês e calcula o faturamento e a quantidade de encomendas."),
    ("Clientes com maior compra", pipeline_clientes, "Identifica os clientes com maior valor acumulado em pedidos."),
    ("Massas mais utilizadas", pipeline_massas, "Desmembra os sabores cadastrados e soma pedidos e unidades por massa."),
    ("Pedidos com saldo", pipeline_abertos, "Localiza pedidos com valor pendente usando o saldo calculado no próprio MongoDB.")
]

tabs = st.tabs([item[0] for item in consultas])
for tab, (nome, pipeline, descricao) in zip(tabs, consultas):
    with tab:
        st.write(descricao)
        try:
            resultado = list(colecao.aggregate(pipeline))
            if resultado:
                df = pd.DataFrame(resultado)
                st.dataframe(df, use_container_width=True, hide_index=True)
                st.caption(f"Registros retornados: {len(df)}")
            else:
                st.info("Nenhum resultado encontrado para esta consulta.")
        except Exception as erro:
            st.error(f"Não foi possível executar a consulta '{nome}': {erro}")
        with st.expander("Ver pipeline MongoDB utilizado"):
            st.json(pipeline)
