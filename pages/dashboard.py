
import streamlit as st
import pandas as pd

from utils.conexao import obter_colecao
from utils.funcoes import buscar_pedidos, resumo_financeiro, converter_data


# ==========================================
# CONFIGURAÇÃO VISUAL
# ==========================================

st.markdown("""
<style>
.dashboard-hero { background:linear-gradient(115deg,#75465B 0%,#A96883 58%,#D49AB0 100%); border-radius:22px; padding:27px 30px; color:white; margin:0 0 24px; box-shadow:0 12px 28px rgba(113,51,79,.16); position:relative; overflow:hidden; }
.dashboard-hero:after { content:'✿'; position:absolute; right:35px; top:-26px; font-size:150px; color:rgba(255,255,255,.09); transform:rotate(15deg); }
.dashboard-hero h2 { color:white !important; font-family:'Playfair Display',serif; font-size:29px !important; margin:0 0 5px; }
.dashboard-hero p { color:#F8EAF0 !important; margin:0; font-size:13px; }
.section-kicker { color:#9A7D89; font-size:10px; font-weight:800; letter-spacing:1.5px; text-transform:uppercase; margin:8px 0 8px; }
.metric-note { color:#81747A; font-size:11px; margin-top:-8px; }
.delivery-card { border:1px solid var(--card-border); background:var(--card-bg); border-radius:15px; padding:14px 15px; min-height:126px; box-shadow:0 4px 13px rgba(117,70,91,.045); }
.delivery-card .delivery-date { display:inline-block; background:var(--date-bg); color:#fff; border-radius:8px; padding:5px 9px; font-size:11px; font-weight:800; margin-bottom:9px; }
.delivery-card .delivery-name { color:#49333D; font-size:14px; font-weight:750; margin-bottom:3px; }
.delivery-card .delivery-info { color:#806777; font-size:11px; line-height:1.55; }

</style>
""", unsafe_allow_html=True)


# ==========================================
# FUNÇÃO DE FORMATAÇÃO
# ==========================================

def moeda(valor):

    valor = float(valor or 0)

    texto = f"{valor:,.2f}"
    texto = texto.replace(",", "X")
    texto = texto.replace(".", ",")
    texto = texto.replace("X", ".")

    return f"R$ {texto}"


# ==========================================
# CABEÇALHO
# ==========================================

st.markdown("""
<div class="dashboard-hero">
  <h2>Visão geral do negócio</h2>
  <p>Acompanhe suas encomendas, recebimentos e próximos compromissos em um só lugar.</p>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="section-kicker">Resumo operacional</div>', unsafe_allow_html=True)
st.subheader("Pedidos e pagamentos")


# ==========================================
# CONEXÃO COM MONGODB
# ==========================================

try:

    colecao = obter_colecao()
    pedidos = buscar_pedidos(colecao)

except Exception as erro:

    st.error(
        f"Não foi possível carregar os pedidos: {erro}"
    )

    st.stop()


# ==========================================
# INDICADORES DE PEDIDOS
# ==========================================

total_pedidos = len(pedidos)

resumos = [resumo_financeiro(pedido) for pedido in pedidos]

pedidos_pagos = sum(1 for item in resumos if item["status"] == "Pago")
pedidos_parciais = sum(1 for item in resumos if item["status"] == "Parcial")
pedidos_pendentes = sum(1 for item in resumos if item["status"] == "Pendente")

pedidos_abertos = (
    pedidos_parciais + pedidos_pendentes
)


# ==========================================
# INDICADORES FINANCEIROS
# ==========================================

valor_recebido = sum(item["recebido"] for item in resumos)
total_vendas = sum(item["total"] for item in resumos)
valor_receber = sum(item["restante"] for item in resumos)


# ==========================================
# RESUMO DOS PEDIDOS
# ==========================================

st.subheader("Resumo dos pedidos")

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "Total de pedidos",
        total_pedidos
    )

with col2:

    st.metric(
        "Pedidos pagos",
        pedidos_pagos
    )

with col3:

    st.metric(
        "Pedidos em aberto",
        pedidos_abertos
    )


# ==========================================
# RESUMO DE STATUS SEM REPETIR CARTÕES
# ==========================================

percentual_pago = (
    (pedidos_pagos / total_pedidos) * 100
    if total_pedidos > 0 else 0
)
st.caption(
    f"Situação dos pagamentos: {pedidos_pagos} pagos · "
    f"{pedidos_parciais} parciais · {pedidos_pendentes} pendentes "
    f"· {percentual_pago:.0f}% dos pedidos quitados."
)

st.divider()


# ==========================================
# RESUMO FINANCEIRO
# ==========================================

st.markdown("<div class='section-kicker'>Financeiro</div>", unsafe_allow_html=True)
st.subheader("Resumo financeiro")

col7, col8, col9 = st.columns(3)

with col7:

    st.metric(
        "Valores recebidos",
        moeda(valor_recebido)
    )

with col8:

    st.metric(
        "Total em vendas",
        moeda(total_vendas)
    )

with col9:

    st.metric(
        "Valores a receber",
        moeda(valor_receber)
    )


st.divider()


# ==========================================
# PRÓXIMAS ENTREGAS
# ==========================================

from datetime import date, timedelta

st.markdown("<div class='section-kicker'>Agenda</div>", unsafe_allow_html=True)
st.subheader("Próximas entregas")
hoje = date.today()
proximas_entregas = []
for pedido in pedidos:
    data_pedido = converter_data(pedido.get("data_entrega"))
    if data_pedido and hoje <= data_pedido <= hoje + timedelta(days=7):
        proximas_entregas.append((data_pedido, pedido))

proximas_entregas.sort(key=lambda item: item[0])
if proximas_entregas:
    from html import escape
    paleta_cards = [("#FFF3F6", "#EBD0DB", "#B66F8C"), ("#F4F0F8", "#DED3E8", "#927BAA"), ("#FFF5EE", "#F0DCCF", "#C58B70")]
    colunas = st.columns(min(3, len(proximas_entregas)))
    for indice, (data_pedido, pedido) in enumerate(proximas_entregas[:3]):
        fundo, borda, cor_data = paleta_cards[indice % len(paleta_cards)]
        nome = escape(str(pedido.get("nome_cliente", "Sem nome")))
        codigo = escape(str(pedido.get("codigo_pedido", "")))
        evento = escape(str(pedido.get("evento") or pedido.get("tema") or "Evento não informado"))
        quantidade = escape(str(pedido.get("quantidade") or "—"))
        horario = escape(str(pedido.get("horario") or "Horário não informado"))
        with colunas[indice]:
            st.markdown(f'''<div class="delivery-card" style="--card-bg:{fundo};--card-border:{borda};--date-bg:{cor_data};">
              <div class="delivery-date">{data_pedido.strftime('%d/%m/%Y')}</div>
              <div class="delivery-name">{nome}</div>
              <div class="delivery-info">{codigo} · {evento}<br>🍩 {quantidade} unidades<br>🕒 {horario}</div>
            </div>''', unsafe_allow_html=True)
else:
    st.success("Nenhuma entrega prevista para os próximos 7 dias.")

st.divider()


# ==========================================
# ÚLTIMOS PEDIDOS
# ==========================================

st.markdown("<div class='section-kicker'>Atividade recente</div>", unsafe_allow_html=True)
st.subheader("Últimos pedidos cadastrados")

if pedidos:

    dados = []

    for pedido in pedidos:

        dados.append({

            "Código": pedido.get(
                "codigo_pedido", ""
            ),

            "Cliente": pedido.get(
                "nome_cliente", ""
            ),

            "Entrega": str(
                pedido.get("data_entrega", "")
            )[:10],

            "Produto": str(
                pedido.get("tipo_produto", "") if pedido.get("tipo_produto") not in (None, "None") else "—"
            ).title(),

            "Quantidade": pedido.get(
                "quantidade", 0
            ),

            "Total": moeda(
                pedido.get("valor_total", 0)
            ),

            "Pagamento": resumo_financeiro(pedido)["status"]
        })

    tabela = pd.DataFrame(dados)

    st.dataframe(
        tabela.head(10),
        use_container_width=True,
        hide_index=True
    )

else:

    st.info(
        "Nenhum pedido cadastrado ainda."
    )


# ==========================================
# RODAPÉ
# ==========================================

st.divider()

st.caption(
    "Bolinuts Gestão | Painel de gerenciamento"
)




