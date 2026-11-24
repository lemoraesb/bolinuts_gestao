
import streamlit as st
import pandas as pd
from datetime import datetime, date
from html import escape
from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage, KeepTogether

from utils.conexao import obter_colecao
from utils.funcoes import resumo_financeiro
from pathlib import Path


# =====================================================
# CONFIGURAÇÃO
# =====================================================

st.set_page_config(
    page_title="Pedidos | Bolinuts",
    page_icon="📋",
    layout="wide"
)

colecao = obter_colecao()


# =====================================================
# IDENTIDADE VISUAL
# =====================================================

st.markdown("""
<style>

    .stApp {
        background-color: #FFFBF8;
    }

    .titulo-pagina {
        color: #75465B;
        font-size: 30px;
        font-weight: 750;
        margin-bottom: 3px;
    }

    .subtitulo {
        color: #81747A;
        font-size: 14px;
        margin-bottom: 22px;
    }

    .secao {
        color: #75465B;
        font-size: 20px;
        font-weight: 700;
        margin-top: 12px;
        margin-bottom: 15px;
    }

    /* Painel único para organizar todos os detalhes do pedido */
    .st-key-painel_detalhes_pedido {
        background: #FFFEFD;
        border: 1px solid #E7D3DC;
        border-radius: 18px;
        padding: 1.25rem 1.35rem 1.1rem;
        margin-top: 1rem;
        margin-bottom: 1.2rem;
        box-shadow: 0 5px 18px rgba(117,70,91,.045);
    }
    .st-key-painel_detalhes_pedido hr {
        border-color: #EADDE3;
    }
    .st-key-painel_detalhes_pedido .secao {
        border-left: 4px solid #B97892;
        padding-left: 10px;
        margin-top: 8px;
    }

    /* Cartões de informação */

    .info-card {
        background: #FFFFFF;
        border: 1px solid #EEE2E7;
        border-left: 4px solid #D7A4B8;
        border-radius: 13px;
        padding: 14px 17px;
        min-height: 78px;
        margin-bottom: 9px;
        box-shadow: 0 3px 10px rgba(117,70,91,.035);
        transition: transform .18s ease, box-shadow .18s ease;
    }
    .info-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 7px 16px rgba(117,70,91,.08);
    }
    .info-card.info-rosa,
    .info-card.info-lilas,
    .info-card.info-creme {
        background: #FFFEFD;
        border: 1px solid #E8D6DE;
        border-left: 4px solid #B97892;
    }

    .info-label {
        color: #81747A;
        font-size: 12px;
        font-weight: 650;
        text-transform: uppercase;
        margin-bottom: 7px;
    }

    .info-valor {
        color: #49333D;
        font-size: 17px;
        font-weight: 600;
        overflow-wrap: anywhere;
    }

    /* Cartões financeiros */

    .financeiro-card {
        background: #FFFFFF;
        border: 1px solid #EEE2E7;
        border-radius: 13px;
        padding: 19px;
        min-height: 105px;
    }

    .financeiro-label {
        color: #81747A;
        font-size: 13px;
        margin-bottom: 8px;
    }

    .financeiro-valor {
        color: #75465B;
        font-size: 25px;
        font-weight: 750;
    }

    /* Status */

    .status-pago {
        display: inline-block;
        background: #E5F4EA;
        color: #287343;
        padding: 7px 13px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: 650;
    }

    .status-parcial {
        display: inline-block;
        background: #FFF0D5;
        color: #98620C;
        padding: 7px 13px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: 650;
    }

    .status-pendente {
        display: inline-block;
        background: #F9E8EE;
        color: #A34B61;
        padding: 7px 13px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: 650;
    }

    /* Confirmação de exclusão */

    .confirmacao-exclusao {
        background: linear-gradient(135deg, #FFF5F6 0%, #FCEBED 100%);
        border: 1px solid #E8BFC7;
        border-radius: 17px;
        padding: 22px 24px;
        margin-top: 18px;
        margin-bottom: 16px;
        box-shadow: 0 8px 22px rgba(185,67,80,.07);
    }

    .confirmacao-titulo {
        color: #963541;
        font-size: 18px;
        font-weight: 700;
        margin-bottom: 10px;
    }

    .confirmacao-texto {
        color: #49333D;
        font-size: 14px;
    }

    /* Indicadores */

    div[data-testid="stMetric"] {
        background: #FFFFFF;
        border: 1px solid #EEE2E7;
        padding: 15px;
        border-radius: 12px;
    }

    div[data-testid="stMetricValue"] {
        color: #75465B;
    }

    /* Botões gerais */

    div.stButton > button {
        border-radius: 12px;
        min-height: 46px;
        font-weight: 650;
        transition: all 0.2s ease;
        box-shadow: 0 3px 10px rgba(80,45,60,.06);
    }

    div.stButton > button:hover { transform: translateY(-1px); box-shadow: 0 7px 16px rgba(80,45,60,.11); }

    .acao-legenda { color:#81747A; font-size:12px; margin:2px 0 10px; }
    .confirmacao-titulo { font-size:19px; letter-spacing:-.3px; }
    .confirmacao-texto { line-height:1.65; }

    /* Ações com paleta suave e consistente */
    .st-key-botao_novo div.stButton > button {
        min-height: 43px; font-size: 13px;
        background: #B36F8B !important;
        color: #FFFFFF !important;
        border: 1px solid #B36F8B !important;
    }
    .st-key-botao_novo div.stButton > button:hover {
        background: #925A73 !important;
        border-color: #925A73 !important;
        color: #FFFFFF !important;
    }

    .st-key-botao_editar div.stButton > button {
        min-height: 43px; font-size: 13px;
        background: #F7EAF0 !important;
        color: #75465B !important;
        border: 1px solid #EBD8E1 !important;
    }
    .st-key-botao_editar div.stButton > button:hover {
        background: #EEDCE4 !important;
        border-color: #DABAC8 !important;
        color: #673149 !important;
    }

    .st-key-botao_excluir button {
        min-height: 43px; font-size: 13px;
        background: #FBEFF1 !important;
        color: #A34F60 !important;
        border: 1px solid #EBCBD1 !important;
    }
    .st-key-botao_excluir button:hover {
        background: #F5DFE3 !important;
        border-color: #DFAFB9 !important;
        color: #873C50 !important;
    }
    .st-key-botao_novo button p, .st-key-botao_editar button p,
    .st-key-botao_excluir button p { font-weight:700 !important; }
    .st-key-cancelar_exclusao button {
        background:#927BAA !important; color:#FFFFFF !important;
        border:1px solid #927BAA !important;
        min-height:48px !important; font-weight:700 !important;
        opacity:1 !important; visibility:visible !important;
    }

    .st-key-confirmar_exclusao button {
        background: #A34F60 !important;
        color: #FFFFFF !important;
        border: 1px solid #A34F60 !important;
    }
    .st-key-confirmar_exclusao button:hover {
        background: #873C50 !important;
        color: #FFFFFF !important;
    }

    /* Botão de cancelamento: seletores pelo key do próprio botão e do container. */
    .st-key-botao_cancelar_exclusao button,
    .st-key-botao_cancelar_exclusao button:focus,
    .st-key-botao_cancelar_exclusao button:active,
    .st-key-cancelar_exclusao button {
        background: #927BAA !important;
        background-color: #927BAA !important;
        color: #FFFFFF !important;
        border: 1px solid #927BAA !important;
        min-height: 48px !important;
        font-weight: 700 !important;
        opacity: 1 !important;
        visibility: visible !important;
    }
    .st-key-botao_cancelar_exclusao button *,
    .st-key-botao_cancelar_exclusao button p,
    .st-key-botao_cancelar_exclusao button span,
    .st-key-cancelar_exclusao button * {
        color: #FFFFFF !important;
        opacity: 1 !important;
        visibility: visible !important;
    }
    .st-key-botao_cancelar_exclusao button:hover,
    .st-key-cancelar_exclusao button:hover {
        background: #78628F !important;
        background-color: #78628F !important;
        border-color: #78628F !important;
        color: #FFFFFF !important;
    }

    /* Botão de cancelamento: lilás sólido e texto branco com contraste alto. */
    .st-key-cancelar_exclusao div[data-testid="stButton"] > button,
    .st-key-cancelar_exclusao div[data-testid="stButton"] > button:focus,
    .st-key-cancelar_exclusao div[data-testid="stButton"] > button:active {
        background: #927BAA !important;
        color: #FFFFFF !important;
        border: 1px solid #927BAA !important;
        opacity: 1 !important;
        min-height: 48px !important;
        box-shadow: 0 2px 6px rgba(90, 60, 100, .12) !important;
    }
    .st-key-cancelar_exclusao div[data-testid="stButton"] > button *,
    .st-key-cancelar_exclusao div[data-testid="stButton"] > button p,
    .st-key-cancelar_exclusao div[data-testid="stButton"] > button span {
        color: #FFFFFF !important;
        opacity: 1 !important;
        visibility: visible !important;
        display: inline !important;
    }
    .st-key-cancelar_exclusao div[data-testid="stButton"] > button:hover {
        background: #78628F !important;
        border-color: #78628F !important;
        color: #FFFFFF !important;
    }

    /* Campos */

    div[data-baseweb="input"] > div,
    div[data-baseweb="select"] > div {
        border-radius: 9px;
    }

    hr {
        border-color: #EEE2E7;
    }


/* Cores distintas por ação; seletores específicos prevalecem sobre o tema global. */
.st-key-botao_novo div[data-testid="stButton"] > button {
    background:#B66F8C !important; border:1px solid #B66F8C !important;
    color:#FFFFFF !important; border-radius:11px !important; font-weight:700 !important;
}
.st-key-botao_editar div[data-testid="stButton"] > button {
    background:#927BAA !important; border:1px solid #927BAA !important;
    color:#FFFFFF !important; border-radius:11px !important; font-weight:700 !important;
}
.st-key-botao_excluir div[data-testid="stButton"] > button,
.st-key-confirmar_exclusao div[data-testid="stButton"] > button {
    background:#B85D6B !important; border:1px solid #B85D6B !important;
    color:#FFFFFF !important; border-radius:11px !important; font-weight:700 !important;
}
.st-key-botao_novo div[data-testid="stButton"] > button *,
.st-key-botao_editar div[data-testid="stButton"] > button *,
.st-key-botao_excluir div[data-testid="stButton"] > button *,
.st-key-confirmar_exclusao div[data-testid="stButton"] > button * { color:#FFFFFF !important; }
.st-key-botao_novo div[data-testid="stButton"] > button:hover { background:#985873 !important; border-color:#985873 !important; }
.st-key-botao_editar div[data-testid="stButton"] > button:hover { background:#78628F !important; border-color:#78628F !important; }
.st-key-botao_excluir div[data-testid="stButton"] > button:hover,
.st-key-confirmar_exclusao div[data-testid="stButton"] > button:hover { background:#994653 !important; border-color:#994653 !important; }

/* Ações rápidas: botões com contraste, inclusive quando desabilitados. */
div[class*="st-key-quick_pay_action"] div[data-testid="stButton"] > button {
    background:#237A57 !important; color:#FFFFFF !important; border:1px solid #237A57 !important;
    min-height:46px !important; border-radius:11px !important; font-weight:700 !important; opacity:1 !important;
}
div[class*="st-key-quick_pay_action"] div[data-testid="stButton"] > button * { color:#FFFFFF !important; opacity:1 !important; }
div[class*="st-key-quick_pay_action"] div[data-testid="stButton"] > button:hover:not(:disabled) { background:#185D41 !important; border-color:#185D41 !important; }
div[class*="st-key-quick_pay_action"] div[data-testid="stButton"] > button:disabled { background:#DCECE3 !important; border-color:#C6DFD1 !important; color:#315E49 !important; opacity:1 !important; }
div[class*="st-key-quick_pay_action"] div[data-testid="stButton"] > button:disabled * { color:#315E49 !important; opacity:1 !important; }
div[class*="st-key-quick_delivery_action"] div[data-testid="stButton"] > button {
    background:#75465B !important; color:#FFFFFF !important; border:1px solid #75465B !important;
    min-height:46px !important; border-radius:11px !important; font-weight:700 !important; opacity:1 !important;
}
div[class*="st-key-quick_delivery_action"] div[data-testid="stButton"] > button * { color:#FFFFFF !important; opacity:1 !important; }
div[class*="st-key-quick_delivery_action"] div[data-testid="stButton"] > button:hover:not(:disabled) { background:#5E3548 !important; border-color:#5E3548 !important; }
div[class*="st-key-quick_delivery_action"] div[data-testid="stButton"] > button:disabled { background:#F0E4EA !important; border-color:#DCC6D1 !important; color:#684D5A !important; opacity:1 !important; }
div[class*="st-key-quick_delivery_action"] div[data-testid="stButton"] > button:disabled * { color:#684D5A !important; opacity:1 !important; }

</style>
""", unsafe_allow_html=True)


# =====================================================
# FUNÇÕES AUXILIARES
# =====================================================

def moeda(valor):
    try:
        valor = float(valor or 0)
        return (
            f"R$ {valor:,.2f}"
            .replace(",", "X")
            .replace(".", ",")
            .replace("X", ".")
        )
    except (ValueError, TypeError):
        return "R$ 0,00"


def converter_data(valor):

    if isinstance(valor, datetime):
        return valor

    if isinstance(valor, date):
        return datetime.combine(valor, datetime.min.time())

    if isinstance(valor, str):
        return pd.to_datetime(valor, errors="coerce")

    return pd.NaT


def texto_seguro(valor):

    if valor is None or valor == "":
        return "Não informado"

    if isinstance(valor, list):
        return ", ".join(str(item) for item in valor)

    return str(valor)


def formatar_lista(valor):
    """Apresenta valores legados armazenados como lista de forma legível."""
    if isinstance(valor, (list, tuple, set)):
        itens = [str(item).strip() for item in valor if str(item).strip()]
        return " • ".join(itens) if itens else "Não informado"
    if valor is None or valor == "":
        return "Não informado"
    return str(valor)


def mostrar_info(rotulo, valor, variante="rosa"):

    rotulo = escape(str(rotulo))
    valor = escape(str(valor))
    variante = variante if variante in {"rosa", "lilas", "creme"} else "rosa"

    st.markdown(
        f"""
        <div class="info-card info-{variante}">
            <div class="info-label">{rotulo}</div>
            <div class="info-valor">{valor}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def pedido_entregue(pedido):
    return bool(pedido.get("pedido_concluido") or str(pedido.get("status_entrega", "")).lower() in ("entregue", "concluído", "concluido"))


def pedido_com_pendencia(pedido):
    # Pendência operacional/financeira: saldo a receber ou entrega ainda não realizada.
    return calcular_status(pedido) in ("Pendente", "Parcial") or not pedido_entregue(pedido)


def calcular_status(pedido):
    return resumo_financeiro(pedido)["status"]


def mostrar_status(status):

    classes = {
        "Pago": "status-pago",
        "Parcial": "status-parcial",
        "Pendente": "status-pendente"
    }

    classe = classes.get(status, "status-pendente")

    st.markdown(
        f'<span class="{classe}">{escape(status)}</span>',
        unsafe_allow_html=True
    )


# =====================================================
# MENSAGENS DE RETORNO
# =====================================================

if st.session_state.get("mensagem_pedido_excluido"):

    st.success(
        st.session_state["mensagem_pedido_excluido"],
        icon="✅"
    )

    del st.session_state["mensagem_pedido_excluido"]


if st.session_state.get("mensagem_cancelamento"):

    st.info(st.session_state["mensagem_cancelamento"])

    del st.session_state["mensagem_cancelamento"]


# =====================================================
# CABEÇALHO
# =====================================================

st.markdown(
    '<div class="titulo-pagina">📋 Pedidos</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitulo">'
    'Gerencie suas encomendas, consulte informações e acompanhe pagamentos.'
    '</div>',
    unsafe_allow_html=True
)


# =====================================================
# BUSCAR PEDIDOS
# =====================================================

try:

    pedidos = list(
        colecao.find().sort("_id", -1)
    )

except Exception as erro:

    st.error(f"Erro ao acessar o banco de dados: {erro}")
    st.stop()


if not pedidos:

    st.info("Ainda não existem pedidos cadastrados.")

    with st.container(key="botao_novo"):
        if st.button(
            "＋ Novo pedido",
            use_container_width=True
        ):
            st.switch_page("pages/novopedido.py")

    st.stop()


# =====================================================
# INDICADORES CLICÁVEIS (FILTRO RÁPIDO)
# =====================================================

total_pedidos = len(pedidos)
pagos = sum(1 for p in pedidos if calcular_status(p) == "Pago")
parciais = sum(1 for p in pedidos if calcular_status(p) == "Parcial")
pendentes = sum(1 for p in pedidos if pedido_com_pendencia(p))

st.caption("Clique em um indicador para filtrar a lista de pedidos.")
cols_ind = st.columns(4)
indicadores = [("Todos", "Total de pedidos", total_pedidos),
               ("Pago", "Pagamentos", pagos),
               ("Parcial", "Parciais", parciais),
               ("Pendente", "Pendentes", pendentes)]
for col, (filtro_val, label, valor) in zip(cols_ind, indicadores):
    with col:
        if st.button(f"{label} · {valor}", key=f"indicador_{filtro_val}", use_container_width=True):
            st.session_state["filtro_indicador_pedido"] = filtro_val
            st.rerun()

filtro_indicador = st.session_state.get("filtro_indicador_pedido", "Todos")

st.divider()


# =====================================================
# PESQUISA E FILTROS
# =====================================================

st.markdown(
    '<div class="secao">Consultar pedidos</div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns([2, 1])

with col1:

    pesquisa = st.text_input(
        "Pesquisar pedido",
        placeholder="Digite o nome do cliente ou código..."
    )

with col2:

    opcoes_status = ["Todos", "Pago", "Parcial", "Pendente"]
    indice_status = opcoes_status.index(filtro_indicador) if filtro_indicador in opcoes_status else 0
    filtro_status = st.selectbox(
        "Status do pagamento",
        opcoes_status,
        index=indice_status
    )


# =====================================================
# PREPARAR TABELA
# =====================================================

dados = []

for p in pedidos:

    data = converter_data(p.get("data_entrega"))

    if pd.isna(data):
        data_formatada = "Não informada"
    else:
        data_formatada = data.strftime("%d/%m/%Y")

    dados.append({
        "Código": p.get("codigo_pedido", ""),
        "Cliente": (p.get("nome_cliente") if p.get("nome_cliente") not in (None, "", "None") else "—"),
        "Evento": (p.get("evento") if p.get("evento") not in (None, "", "None") else "—"),
        "Data entrega": data_formatada,
        "Produto": formatar_lista(p.get("tipo_produto", "")) if p.get("tipo_produto") not in (None, "", "None") else "—",
        "Quantidade": (p.get("quantidade") if p.get("quantidade") not in (None, "") else "—"),
        "Total": moeda(p.get("valor_total", 0)),
        "Status": calcular_status(p),
        "Situação entrega": "Entregue" if (p.get("pedido_concluido") or str(p.get("status_entrega", "")).lower() in ("entregue", "concluído", "concluido")) else "Aguardando"
    })


df = pd.DataFrame(dados)
df_filtrado = df.copy()

if pesquisa:

    pesquisa = pesquisa.strip()

    df_filtrado = df_filtrado[
        df_filtrado["Cliente"].astype(str).str.contains(
            pesquisa,
            case=False,
            na=False
        )
        |
        df_filtrado["Código"].astype(str).str.contains(
            pesquisa,
            case=False,
            na=False
        )
    ]


if filtro_status != "Todos":
    if filtro_status == "Pendente":
        ids_pendentes_operacionais = {
            str(p.get("codigo_pedido", "")) for p in pedidos if pedido_com_pendencia(p)
        }
        df_filtrado = df_filtrado[df_filtrado["Código"].astype(str).isin(ids_pendentes_operacionais)]
    else:
        df_filtrado = df_filtrado[df_filtrado["Status"] == filtro_status]


st.caption(
    f"{len(df_filtrado)} pedido(s) encontrado(s)."
)

st.dataframe(
    df_filtrado,
    use_container_width=True,
    hide_index=True
)

# =====================================================
# AÇÕES RÁPIDAS SOMENTE NOS FILTROS PARCIAIS E PENDENTES
# =====================================================

if filtro_status in ("Parcial", "Pendente"):
    st.markdown('<div class="secao">Ações rápidas</div>', unsafe_allow_html=True)
    if filtro_status == "Parcial":
        st.caption("Pedidos com saldo a receber. Registre o recebimento e/ou a entrega diretamente na lista.")
    else:
        st.caption("Pedidos com pagamento pendente ou já pagos que ainda aguardam entrega.")

    lista_acao = []
    for p_acao in pedidos:
        cod_acao = str(p_acao.get("codigo_pedido", ""))
        cli_acao = str(p_acao.get("nome_cliente", ""))
        stat_acao = calcular_status(p_acao)
        entregue_acao = bool(p_acao.get("pedido_concluido", False) or str(p_acao.get("status_entrega", "")).lower() in ("entregue", "concluído", "concluido"))
        corresponde_pesq_acao = (not pesquisa or pesquisa.lower() in cod_acao.lower() or pesquisa.lower() in cli_acao.lower())

        if filtro_status == "Parcial":
            corresponde_acao = stat_acao == "Parcial"
        else:
            # Pendentes: pagamento ainda não quitado OU pagamento quitado aguardando entrega.
            corresponde_acao = pedido_com_pendencia(p_acao)

        if corresponde_pesq_acao and corresponde_acao:
            lista_acao.append(p_acao)

    if not lista_acao:
        st.info("Não há pendências nessa seleção.")
    else:
        for p_acao in lista_acao:
            fin_acao = resumo_financeiro(p_acao)
            entregue_acao = bool(p_acao.get("pedido_concluido", False) or str(p_acao.get("status_entrega", "")).lower() in ("entregue", "concluído", "concluido"))
            codigo_acao = str(p_acao.get("codigo_pedido", "Sem código"))
            nome_acao = str(p_acao.get("nome_cliente", "Sem nome"))
            pid_acao = str(p_acao["_id"])
            situacao_pag = fin_acao["status"]
            with st.expander(f"{codigo_acao} · {nome_acao} | {situacao_pag} | Saldo: {moeda(fin_acao['restante'])} | {'Entregue' if entregue_acao else 'Aguardando entrega'}"):
                c1, c2, c3 = st.columns(3)
                c1.metric("Total", moeda(fin_acao["total"]))
                c2.metric("Recebido", moeda(fin_acao["recebido"]))
                c3.metric("Saldo", moeda(fin_acao["restante"]))
                ca, cb = st.columns(2)
                with ca:
                    if fin_acao["restante"] > 0:
                        ck_pag = st.checkbox(f"Confirmo recebimento de {moeda(fin_acao['restante'])}", key=f"quick_pay_check_{pid_acao}")
                        with st.container(key=f"quick_pay_action_{pid_acao}"):
                            btn_registrar_saldo = st.button("Registrar saldo", key=f"quick_pay_{pid_acao}", disabled=not ck_pag, use_container_width=True)
                        if btn_registrar_saldo:
                            try:
                                novo_recebido = min(fin_acao["total"], fin_acao["recebido"] + fin_acao["restante"])
                                colecao.update_one({"_id": p_acao["_id"]}, {"$set": {"valor_sinal": novo_recebido, "valor_restante": max(fin_acao["total"]-novo_recebido,0), "status_pagamento": "Pago" if novo_recebido >= fin_acao["total"] else "Parcial"}})
                                st.success(f"Saldo de {codigo_acao} registrado.")
                                st.rerun()
                            except Exception as erro:
                                st.error(f"Erro ao registrar saldo: {erro}")
                    else:
                        st.success("Pagamento quitado")
                with cb:
                    if not entregue_acao:
                        ck_ent = st.checkbox("Confirmo que foi entregue", key=f"quick_delivery_check_{pid_acao}")
                        with st.container(key=f"quick_delivery_action_{pid_acao}"):
                            btn_concluir_entrega = st.button("Concluir entrega", key=f"quick_delivery_{pid_acao}", disabled=not ck_ent, use_container_width=True)
                        if btn_concluir_entrega:
                            try:
                                colecao.update_one({"_id": p_acao["_id"]}, {"$set": {"pedido_concluido": True, "status_entrega": "Entregue", "data_conclusao": datetime.now().strftime("%d/%m/%Y %H:%M")}})
                                st.success(f"Entrega de {codigo_acao} registrada.")
                                st.rerun()
                            except Exception as erro:
                                st.error(f"Erro ao registrar entrega: {erro}")
                    else:
                        st.success("Entrega concluída")
                        ck_undo_quick = st.checkbox("Confirmo que esta entrega foi marcada por engano", key=f"quick_undo_check_{pid_acao}")
                        if st.button("Desfazer entrega", key=f"quick_undo_{pid_acao}", disabled=not ck_undo_quick, use_container_width=True):
                            try:
                                colecao.update_one({"_id": p_acao["_id"]}, {"$set": {"pedido_concluido": False, "status_entrega": "Aguardando"}, "$unset": {"data_conclusao": ""}})
                                st.success(f"Entrega de {codigo_acao} reaberta. O financeiro foi preservado.")
                                st.rerun()
                            except Exception as erro:
                                st.error(f"Erro ao reabrir entrega: {erro}")

# =====================================================
# SELEÇÃO DO PEDIDO
# =====================================================

st.divider()

st.markdown(
    '<div class="secao">Gerenciar encomenda</div>',
    unsafe_allow_html=True
)

st.caption("Escolha uma encomenda para consultar, atualizar ou remover.")


pedidos_filtrados = []

for p in pedidos:

    codigo = str(p.get("codigo_pedido", ""))
    cliente = str(p.get("nome_cliente", ""))
    status = calcular_status(p)

    corresponde_pesquisa = (
        not pesquisa
        or pesquisa.lower() in codigo.lower()
        or pesquisa.lower() in cliente.lower()
    )

    corresponde_status = (
        filtro_status == "Todos"
        or (filtro_status == "Pendente" and pedido_com_pendencia(p))
        or (filtro_status != "Pendente" and status == filtro_status)
    )

    if corresponde_pesquisa and corresponde_status:
        pedidos_filtrados.append(p)


if not pedidos_filtrados:

    st.warning(
        "Nenhum pedido disponível para as ações com esses filtros."
    )

    st.stop()


opcoes = {
    f"{p.get('codigo_pedido', 'Sem código')} - "
    f"{p.get('nome_cliente', 'Sem nome')}": p
    for p in pedidos_filtrados
}

lista_opcoes = list(opcoes.keys())

chave_anterior = st.session_state.get(
    "pedido_selecionado_acoes"
)

indice_inicial = (
    lista_opcoes.index(chave_anterior)
    if chave_anterior in lista_opcoes
    else 0
)

selecao = st.selectbox(
    "Selecione o pedido",
    lista_opcoes,
    index=indice_inicial,
    key="pedido_selecionado_acoes"
)

pedido = opcoes[selecao]
id_pedido = str(pedido["_id"])


# =====================================================
# BOTÕES DE AÇÃO
# =====================================================

col_esq, col_novo, col_editar, col_excluir, col_dir = st.columns([1, 2, 2, 2, 1])

with col_novo:

    with st.container(key="botao_novo"):

        if st.button(
            "＋ Novo pedido",
            use_container_width=True,
            key="acao_novo_pedido"
        ):

            st.switch_page("pages/novopedido.py")


with col_editar:

    with st.container(key="botao_editar"):

        if st.button(
            "✏ Editar pedido",
            use_container_width=True,
            key="acao_editar_pedido"
        ):

            st.session_state["pedido_para_editar_id"] = id_pedido

            st.switch_page("pages/editarpedido.py")


with col_excluir:

    with st.container(key="botao_excluir"):

        if st.button(
            "🗑 Excluir pedido",
            use_container_width=True,
            key="acao_excluir_pedido"
        ):

            st.session_state["pedido_para_excluir"] = id_pedido

            st.rerun()


# =====================================================
# CONFIRMAÇÃO DE EXCLUSÃO
# =====================================================

if st.session_state.get("pedido_para_excluir") == id_pedido:

    st.markdown(
        f"""
        <div class="confirmacao-exclusao">
            <div class="confirmacao-titulo">
                ⚠ Confirmar exclusão?
            </div>
            <div class="confirmacao-texto">
                Você está prestes a remover <strong>{escape(str(pedido.get('codigo_pedido', '')))} · {escape(str(pedido.get('nome_cliente', '')))}</strong>.
                Essa ação é permanente e não poderá ser desfeita.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:

        with st.container(key="confirmar_exclusao"):

            confirmar = st.button(
                "Sim, excluir pedido",
                use_container_width=True,
                key="botao_confirmar_exclusao"
            )

    with col2:

        with st.container(key="cancelar_exclusao"):

            cancelar = st.button(
                "↩ Não, manter pedido",
                use_container_width=True,
                key="botao_cancelar_exclusao",
                type="secondary"
            )


    if confirmar:

        try:

            resultado = colecao.delete_one(
                {"_id": pedido["_id"]}
            )

            if resultado.deleted_count == 1:

                st.session_state["pedido_para_excluir"] = None

                st.session_state["mensagem_pedido_excluido"] = (
                    f"Pedido {pedido.get('codigo_pedido', '')} "
                    "excluído com sucesso!"
                )

                st.rerun()

            else:

                st.error(
                    "Não foi possível localizar o pedido."
                )

        except Exception as erro:

            st.error(
                f"Erro ao excluir pedido: {erro}"
            )


    if cancelar:

        st.session_state["pedido_para_excluir"] = None

        st.session_state["mensagem_cancelamento"] = (
            "Exclusão cancelada. O pedido foi mantido."
        )

        st.rerun()


# =====================================================
# DETALHES DO PEDIDO
# =====================================================

with st.container(key="painel_detalhes_pedido"):
    st.divider()

    st.markdown(
        '<div class="secao">Detalhes do pedido</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns([2, 1])

    with col1:

        st.markdown(
            f"### Pedido {escape(str(pedido.get('codigo_pedido', '')))}"
        )

    with col2:

        mostrar_status(calcular_status(pedido))


    # =====================================================
    # INFORMAÇÕES DO CLIENTE
    # =====================================================

    st.markdown("**Informações do cliente**")

    data_entrega = converter_data(
        pedido.get("data_entrega")
    )

    if pd.isna(data_entrega):
        data_formatada = "Não informada"
    else:
        data_formatada = data_entrega.strftime("%d/%m/%Y")


    col1, col2, col3 = st.columns(3)

    with col1:

        mostrar_info(
            "Cliente",
            texto_seguro(pedido.get("nome_cliente")),
            "rosa"
        )

    with col2:

        mostrar_info(
            "Evento",
            texto_seguro(pedido.get("evento")),
            "rosa"
        )

    with col3:

        mostrar_info(
            "Tema",
            texto_seguro(pedido.get("tema")),
            "lilas"
        )


    col1, col2, col3 = st.columns(3)

    with col1:

        mostrar_info(
            "Data de entrega",
            data_formatada,
            "rosa"
        )

    with col2:

        mostrar_info(
            "Horário",
            texto_seguro(pedido.get("horario")),
            "lilas"
        )

    with col3:

        mostrar_info(
            "Forma de entrega",
            texto_seguro(pedido.get("tipo_entrega")),
            "creme"
        )


    # =====================================================
    # DETALHES DA ENCOMENDA
    # =====================================================

    st.markdown("**Detalhes da encomenda**")

    massas = pedido.get(
        "massas",
        pedido.get("massa", [])
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        mostrar_info(
            "Produto",
            formatar_lista(pedido.get("tipo_produto")),
            "lilas"
        )

    with col2:

        mostrar_info(
            "Quantidade",
            f"{pedido.get('quantidade', 0)} unidades",
            "rosa"
        )

    with col3:

        mostrar_info(
            "Massa",
            texto_seguro(massas),
            "creme"
        )


    col1, col2 = st.columns(2)

    with col1:

        mostrar_info(
            "Decoração",
            texto_seguro(pedido.get("decoracao")),
            "lilas"
        )

    with col2:

        mostrar_info(
            "Endereço de entrega",
            texto_seguro(pedido.get("endereco")),
            "creme"
        )


    st.markdown("**Observações**")

    observacoes = pedido.get("observacoes", "")

    if observacoes:
        st.info(observacoes)
    else:
        st.caption("Nenhuma observação cadastrada.")


    # =====================================================
    # RESUMO FINANCEIRO
    # =====================================================

    st.divider()

    st.markdown(
        '<div class="secao">Resumo financeiro</div>',
        unsafe_allow_html=True
    )

    financeiro = resumo_financeiro(pedido)
    valor_total = financeiro["total"]
    valor_recebido = financeiro["recebido"]
    valor_restante = financeiro["restante"]


    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown(
            f"""
            <div class="financeiro-card">
                <div class="financeiro-label">Valor total</div>
                <div class="financeiro-valor">{moeda(valor_total)}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:

        st.markdown(
            f"""
            <div class="financeiro-card">
                <div class="financeiro-label">Valor recebido</div>
                <div class="financeiro-valor">{moeda(valor_recebido)}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:

        st.markdown(
            f"""
            <div class="financeiro-card">
                <div class="financeiro-label">Valor restante</div>
                <div class="financeiro-valor">{moeda(valor_restante)}</div>
            </div>
            """,
            unsafe_allow_html=True
        )


    st.caption(
        "Forma de pagamento: "
        + texto_seguro(pedido.get("forma_pagamento"))
    )












def criar_logo_pdf(largura_cm=3.8):
    """Carrega o logo do pacote e o prepara em RGB para incorporação confiável no PDF."""
    candidatos = [
        Path(__file__).resolve().parents[1] / "imagens" / "logo_bolinuts.png",
        Path.cwd() / "imagens" / "logo_bolinuts.png",
        Path.cwd() / "bolinuts_gestao" / "imagens" / "logo_bolinuts.png",
    ]
    for caminho in candidatos:
        if caminho.is_file():
            try:
                from PIL import Image as PILImage
                imagem = PILImage.open(caminho).convert("RGBA")
                fundo = PILImage.new("RGBA", imagem.size, (255, 251, 248, 255))
                fundo.alpha_composite(imagem)
                buffer_logo = BytesIO()
                fundo.convert("RGB").save(buffer_logo, format="JPEG", quality=94, optimize=True)
                buffer_logo.seek(0)
                logo = RLImage(buffer_logo, width=largura_cm * cm,
                               height=(largura_cm * 2 / 3) * cm, kind="proportional")
                logo.hAlign = "LEFT"
                return logo
            except Exception:
                continue
    return None


# =====================================================
# COMPROVANTE DO PEDIDO EM PDF
# =====================================================

def gerar_comprovante_pdf(pedido, financeiro):
    """Gera um comprovante de encomenda com identidade visual Bolinuts."""
    buffer = BytesIO()
    margem_lateral = 1.65 * cm
    largura_util = A4[0] - (2 * margem_lateral)
    documento = SimpleDocTemplate(
        buffer, pagesize=A4, rightMargin=margem_lateral, leftMargin=margem_lateral,
        topMargin=1.25*cm, bottomMargin=1.35*cm,
        title=f"Comprovante {pedido.get('codigo_pedido', 'Bolinuts')}",
        author="Bolinuts Gestão",
    )
    estilos = getSampleStyleSheet()
    vinho = colors.HexColor("#75465B")
    rosa = colors.HexColor("#B66F8C")
    rosa_claro = colors.HexColor("#F8EAF0")
    rosa_borda = colors.HexColor("#E8C9D5")
    creme = colors.HexColor("#FFFBF8")
    texto = colors.HexColor("#493C42")
    cinza = colors.HexColor("#81747A")
    verde_claro = colors.HexColor("#EAF5EF")
    verde = colors.HexColor("#397A58")
    vermelho_claro = colors.HexColor("#FCEDEF")
    vermelho = colors.HexColor("#A94E5B")

    titulo = ParagraphStyle(
        "BolinutsTituloRecibo", parent=estilos["Title"], textColor=vinho,
        fontName="Helvetica-Bold", fontSize=21, leading=25, alignment=0,
        spaceAfter=3,
    )
    subtitulo = ParagraphStyle(
        "BolinutsSubtituloRecibo", parent=estilos["Normal"], textColor=cinza,
        fontName="Helvetica", fontSize=9.5, leading=13,
    )
    secao = ParagraphStyle(
        "BolinutsSecaoRecibo", parent=estilos["Heading2"], textColor=vinho,
        fontName="Helvetica-Bold", fontSize=11.5, leading=14,
        spaceBefore=10, spaceAfter=6,
    )
    rotulo = ParagraphStyle(
        "BolinutsRotuloRecibo", parent=estilos["Normal"], textColor=vinho,
        fontName="Helvetica-Bold", fontSize=8.6, leading=11,
    )
    valor = ParagraphStyle(
        "BolinutsValorRecibo", parent=estilos["Normal"], textColor=texto,
        fontName="Helvetica", fontSize=9, leading=12,
        wordWrap="CJK",
    )
    rodape = ParagraphStyle(
        "BolinutsRodapeRecibo", parent=estilos["Normal"], textColor=vinho,
        fontName="Helvetica-Bold", fontSize=9.5, leading=13,
        alignment=1,
    )
    pequeno = ParagraphStyle(
        "BolinutsPequenoRecibo", parent=estilos["Normal"], textColor=cinza,
        fontSize=8, leading=10,
    )
    rodape_secundario = ParagraphStyle(
        "BolinutsRodapeSecundario", parent=pequeno, alignment=1,
        fontSize=8, leading=11,
    )

    def P(conteudo, estilo=valor):
        return Paragraph(escape(str(conteudo if conteudo not in (None, "") else "—")), estilo)

    elementos = []
    logo = criar_logo_pdf(3.35)
    texto_cabecalho = [
        Paragraph("COMPROVANTE DE ENCOMENDA", ParagraphStyle(
            "BolinutsRotuloCabecalho", parent=titulo, textColor=vinho,
            fontName="Helvetica-Bold", fontSize=16, leading=20,
            spaceAfter=5,
        )),
        Paragraph("Uma encomenda preparada com carinho para você.", subtitulo),
        Paragraph("Confira os dados e os valores da sua encomenda.", pequeno),
    ]
    if logo is not None:
        cabecalho = Table(
            [[logo, texto_cabecalho]],
            colWidths=[4.0*cm, largura_util - (4.0*cm)],
            hAlign="LEFT",
        )
        cabecalho.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,-1), creme),
            ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
            ("BOX", (0,0), (-1,-1), 0.7, rosa_borda),
            ("LINEBELOW", (0,0), (-1,-1), 2.2, rosa),
            ("LEFTPADDING", (0,0), (-1,-1), 11),
            ("RIGHTPADDING", (0,0), (-1,-1), 11),
            ("TOPPADDING", (0,0), (-1,-1), 9),
            ("BOTTOMPADDING", (0,0), (-1,-1), 9),
        ]))
        elementos.append(cabecalho)
    else:
        elementos.extend(texto_cabecalho)

    elementos.append(Spacer(1, 11))
    codigo = escape(str(pedido.get("codigo_pedido", "—")))
    faixa_codigo = Table([[
        Paragraph(f"ENCOMENDA <b>{codigo}</b>", ParagraphStyle(
            "BolinutsCodigoRecibo", parent=rotulo, fontSize=10, leading=13,
        )),
        Paragraph("GUARDE ESTE COMPROVANTE", ParagraphStyle(
            "BolinutsCodigoAjuda", parent=pequeno, alignment=2,
            textColor=vinho, fontName="Helvetica-Bold", fontSize=7.5,
        )),
    ]], colWidths=[largura_util / 2, largura_util / 2], hAlign="LEFT")
    faixa_codigo.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), rosa_claro),
        ("BOX", (0,0), (-1,-1), 0.6, rosa_borda),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("LEFTPADDING", (0,0), (-1,-1), 10),
        ("RIGHTPADDING", (0,0), (-1,-1), 10),
        ("TOPPADDING", (0,0), (-1,-1), 8),
        ("BOTTOMPADDING", (0,0), (-1,-1), 8),
    ]))
    elementos.append(faixa_codigo)

    data_pdf = converter_data(pedido.get("data_entrega"))
    data_texto = data_pdf.strftime("%d/%m/%Y") if data_pdf is not None and not pd.isna(data_pdf) else "Não informada"
    titulo_detalhes = Paragraph("INFORMAÇÕES DA ENCOMENDA", secao)
    dados = [
        [P("Cliente", rotulo), P(pedido.get("nome_cliente", "—"))],
        [P("Evento / tema", rotulo), P(pedido.get("evento") or pedido.get("tema") or "Não informado")],
        [P("Data de entrega", rotulo), P(data_texto)],
        [P("Horário", rotulo), P(pedido.get("horario") or "Não definido")],
        [P("Produto", rotulo), P(pedido.get("tipo_produto", "—"))],
        [P("Quantidade", rotulo), P(f"{pedido.get('quantidade') or '—'} unidades")],
        [P("Massa", rotulo), P(texto_seguro(pedido.get("massa", pedido.get("massas", "Não informada"))))],
        [P("Decoração", rotulo), P(texto_seguro(pedido.get("decoracao", "Não informada")))],
        [P("Entrega", rotulo), P(pedido.get("tipo_entrega") or "Não informada")],
        [P("Endereço", rotulo), P(pedido.get("endereco") or "—")],
        [P("Forma de pagamento", rotulo), P(pedido.get("forma_pagamento") or "Não informada")],
        [P("Observações", rotulo), P(pedido.get("observacoes") or "Nenhuma")],
    ]
    tabela = Table(
        dados,
        colWidths=[4.1*cm, largura_util - (4.1*cm)],
        repeatRows=0,
        hAlign="LEFT",
    )
    tabela.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (0,-1), colors.HexColor("#F5E3EA")),
        ("ROWBACKGROUNDS", (1,0), (1,-1), [colors.white, creme]),
        ("GRID", (0,0), (-1,-1), 0.35, colors.HexColor("#EADFE5")),
        ("LINEBEFORE", (0,0), (0,-1), 2, rosa),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("LEFTPADDING", (0,0), (-1,-1), 9),
        ("RIGHTPADDING", (0,0), (-1,-1), 9),
        ("TOPPADDING", (0,0), (-1,-1), 7),
        ("BOTTOMPADDING", (0,0), (-1,-1), 7),
    ]))
    elementos.append(KeepTogether([titulo_detalhes, tabela]))

    status = str(financeiro.get("status", "Pendente"))
    status_norm = status.strip().lower()
    if status_norm == "pago":
        fundo_status, cor_status = verde_claro, verde
    elif status_norm in ("parcial", "parcialmente pago"):
        fundo_status, cor_status = rosa_claro, vinho
    else:
        fundo_status, cor_status = vermelho_claro, vermelho

    bloco_financeiro = [Paragraph("RESUMO FINANCEIRO", secao)]
    rotulo_financeiro_branco = ParagraphStyle(
        "BolinutsRotuloFinanceiroBranco", parent=rotulo,
        textColor=colors.white, alignment=1, fontSize=8, leading=10,
    )
    financeiro_dados = [
        [P("VALOR TOTAL", rotulo_financeiro_branco), P("VALOR RECEBIDO", rotulo_financeiro_branco), P("SALDO RESTANTE", rotulo_financeiro_branco)],
        [P(moeda(financeiro["total"]), ParagraphStyle("BolinutsTotalRecibo", parent=valor, textColor=vinho, fontName="Helvetica-Bold", fontSize=12, leading=15, alignment=1)),
         P(moeda(financeiro["recebido"]), ParagraphStyle("BolinutsRecebidoRecibo", parent=valor, textColor=vinho, fontName="Helvetica-Bold", fontSize=12, leading=15, alignment=1)),
         P(moeda(financeiro["restante"]), ParagraphStyle("BolinutsSaldoRecibo", parent=valor, textColor=vinho, fontName="Helvetica-Bold", fontSize=12, leading=15, alignment=1))],
    ]
    largura_coluna_financeira = largura_util / 3
    financeiro_tabela = Table(
        financeiro_dados,
        colWidths=[largura_coluna_financeira] * 3,
        hAlign="LEFT",
    )
    financeiro_tabela.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), vinho),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("BACKGROUND", (0,1), (-1,1), rosa_claro),
        ("BOX", (0,0), (-1,-1), 0.7, rosa_borda),
        ("INNERGRID", (0,0), (-1,-1), 0.5, colors.white),
        ("ALIGN", (0,0), (-1,-1), "CENTER"),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("LEFTPADDING", (0,0), (-1,-1), 7),
        ("RIGHTPADDING", (0,0), (-1,-1), 7),
        ("TOPPADDING", (0,0), (-1,-1), 9),
        ("BOTTOMPADDING", (0,0), (-1,-1), 9),
    ]))
    bloco_financeiro.append(financeiro_tabela)
    etiqueta_status = Table([[Paragraph(
        f"<b>SITUAÇÃO DO PAGAMENTO:</b> {escape(status)}",
        ParagraphStyle("BolinutsStatusRecibo", parent=valor, textColor=cor_status, fontSize=8.5, leading=11),
    )]], colWidths=[largura_util], hAlign="LEFT")
    etiqueta_status.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), fundo_status),
        ("BOX", (0,0), (-1,-1), 0.5, rosa_borda),
        ("LEFTPADDING", (0,0), (-1,-1), 9),
        ("RIGHTPADDING", (0,0), (-1,-1), 9),
        ("TOPPADDING", (0,0), (-1,-1), 7),
        ("BOTTOMPADDING", (0,0), (-1,-1), 7),
    ]))
    bloco_financeiro.extend([Spacer(1, 6), etiqueta_status])
    elementos.append(KeepTogether(bloco_financeiro))
    # Rodapé alinhado à mesma largura das tabelas e mantido como um único bloco.
    rodape_conteudo = [
        [Paragraph(
            "Obrigada pela preferência! Será um prazer fazer parte desse momento especial. ♥",
            rodape,
        )],
        [Paragraph(
            "Preparado com carinho para tornar sua comemoração ainda mais especial.",
            rodape_secundario,
        )],
    ]
    rodape_final = Table(
        rodape_conteudo,
        colWidths=[largura_util],
        hAlign="LEFT",
    )
    rodape_final.setStyle(TableStyle([
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (0, 0), 11),
        ("BOTTOMPADDING", (0, 0), (0, 0), 3),
        ("TOPPADDING", (0, 1), (0, 1), 0),
        ("BOTTOMPADDING", (0, 1), (0, 1), 0),
    ]))
    elementos.append(KeepTogether([rodape_final]))

    documento.build(elementos)
    buffer.seek(0)
    return buffer.getvalue()


# =====================================================
# RESUMO FINANCEIRO E STATUS DA ENTREGA (AÇÕES PRINCIPAIS NA LISTA)
# =====================================================

st.divider()
st.markdown('<div class="secao">Financeiro e entrega</div>', unsafe_allow_html=True)

financeiro = resumo_financeiro(pedido)
saldo = financeiro["restante"]
entregue = bool(pedido.get("pedido_concluido", False) or str(pedido.get("status_entrega", "")).lower() in ("entregue", "concluído", "concluido"))
col_receb, col_entrega = st.columns(2)
with col_receb:
    st.markdown("**Pagamento**")
    st.success("Pago" if saldo <= 0 else f"Saldo pendente: {moeda(saldo)}")
with col_entrega:
    st.markdown("**Entrega**")
    if entregue:
        st.success(f"Entregue{(' em ' + str(pedido.get('data_conclusao'))) if pedido.get('data_conclusao') else ''}")
        confirmar_reabrir = st.checkbox("Confirmo que a entrega foi marcada por engano", key=f"confirmar_reabrir_entrega_{id_pedido}")
        if st.button("Desfazer entrega / Reabrir", key=f"reabrir_entrega_{id_pedido}", disabled=not confirmar_reabrir, use_container_width=True):
            try:
                colecao.update_one({"_id": pedido["_id"]}, {"$set": {"pedido_concluido": False, "status_entrega": "Aguardando"}, "$unset": {"data_conclusao": ""}})
                st.success("Entrega desfeita. O pagamento foi preservado.")
                st.rerun()
            except Exception as erro:
                st.error(f"Erro ao reabrir pedido: {erro}")
    else:
        st.warning("Aguardando entrega")

with st.expander("✏️ Corrigir lançamento financeiro (opção avançada)", expanded=False):
    st.caption("Use somente se o valor recebido foi registrado incorretamente. Esta correção não altera o status da entrega.")
    valor_corrigido = st.number_input(
        "Valor efetivamente recebido (R$)", min_value=0.0,
        max_value=float(financeiro["total"]), value=float(financeiro["recebido"]),
        step=1.0, format="%.2f", key=f"corrigir_recebido_{id_pedido}"
    )
    saldo_corrigido_preview = max(float(financeiro["total"]) - float(valor_corrigido), 0)
    st.caption(f"Após salvar, o saldo será: {moeda(saldo_corrigido_preview)}")
    confirmar_correcao = st.checkbox("Confirmo que este valor corrige o lançamento anterior", key=f"confirmar_correcao_fin_{id_pedido}")
    if st.button("Salvar correção", key=f"salvar_correcao_fin_{id_pedido}", disabled=not confirmar_correcao, use_container_width=True):
        try:
            status_corrigido = "Pago" if valor_corrigido >= financeiro["total"] and financeiro["total"] > 0 else ("Parcial" if valor_corrigido > 0 else "Pendente")
            colecao.update_one({"_id": pedido["_id"]}, {"$set": {"valor_sinal": float(valor_corrigido), "valor_restante": saldo_corrigido_preview, "status_pagamento": status_corrigido}})
            st.success("Valor recebido corrigido; saldo e status recalculados. A entrega não foi alterada.")
            st.rerun()
        except Exception as erro:
            st.error(f"Erro ao corrigir recebimento: {erro}")

# =====================================================
# COMPROVANTE DO PEDIDO
# =====================================================
st.divider()
st.markdown("**Comprovante do pedido**")
st.caption("Gere uma cópia em PDF dos dados e do resumo financeiro desta encomenda.")
try:
    pdf_comprovante = gerar_comprovante_pdf(pedido, financeiro)
    st.download_button(
        label="📄 Baixar comprovante em PDF",
        data=pdf_comprovante,
        file_name=f"Comprovante_{pedido.get('codigo_pedido', id_pedido)}.pdf",
        mime="application/pdf",
        key=f"download_comprovante_{id_pedido}",
        use_container_width=True,
    )
except Exception as erro:
    st.error(f"Não foi possível gerar o comprovante: {erro}")

