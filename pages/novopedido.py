
import streamlit as st
from datetime import datetime, date

from utils.conexao import obter_colecao


# =====================================================
# CONFIGURAÇÃO
# =====================================================

st.set_page_config(
    page_title="Novo Pedido | Bolinuts",
    page_icon="➕",
    layout="wide"
)

colecao = obter_colecao()


# =====================================================
# IDENTIDADE VISUAL BOLINUTS
# =====================================================

st.markdown("""
<style>
.titulo-pagina {
    color: #75465B;
    font-size: 30px;
    font-weight: 700;
    margin-bottom: 5px;
    letter-spacing: -0.7px;
}

.subtitulo {
    color: #81747A;
    font-size: 14px;
    margin-bottom: 25px;
    line-height: 1.6;
}

.secao {
    color: #75465B;
    font-size: 21px;
    font-weight: 650;
    margin-top: 12px;
    margin-bottom: 15px;
    padding-left: 12px;
    border-left: 3px solid #D99AAF;
}

.resumo-financeiro {
    background: #F8EAF0;
    border: 1px solid #EBD5DE;
    border-radius: 16px;
    padding: 20px 22px;
    margin-top: 15px;
    margin-bottom: 18px;
}

.resumo-titulo {
    color: #75465B;
    font-size: 13px;
    font-weight: 600;
    margin-bottom: 5px;
}

.resumo-valor {
    color: #75465B;
    font-size: 23px;
    font-weight: 700;
}

.resumo-restante {
    color: #98627A;
    font-size: 13px;
    margin-top: 5px;
}

/* Botões padronizados: rosa principal, texto branco e contraste consistente */
div.stButton > button,
div[data-testid="stFormSubmitButton"] button {
    background: #B36F8B !important;
    color: #FFFFFF !important;
    border: 1px solid #B36F8B !important;
    border-radius: 11px !important;
    font-weight: 700 !important;
    min-height: 44px;
    transition: all .18s ease;
}
div.stButton > button:hover,
div[data-testid="stFormSubmitButton"] button:hover {
    background: #925A73 !important;
    border-color: #925A73 !important;
    color: #FFFFFF !important;
    transform: translateY(-1px);
}
div[data-testid="stFormSubmitButton"] button p,
div[data-testid="stFormSubmitButton"] button span { color:#FFFFFF !important; }
.st-key-voltar_novo button, .st-key-voltar_editar button {
    background: #FFFFFF !important;
    color: #75465B !important;
    border: 1px solid #E7CBD6 !important;
    box-shadow: none !important;
    min-height: 38px;
    padding: .35rem .9rem;
}
.st-key-voltar_novo button:hover, .st-key-voltar_editar button:hover {
    background: #F8EAF0 !important;
    color: #75465B !important;
    border-color: #D9A8BB !important;
}

div[data-testid="stForm"] {
    border: 1px solid #EEE2E7;
    border-radius: 18px;
    padding: 25px 26px;
    background: linear-gradient(180deg, #FFFFFF 0%, #FFFEFD 100%);
    box-shadow: 0 10px 30px rgba(129, 61, 88, .055);
}

[data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea,
[data-testid="stNumberInput"] input,
[data-testid="stDateInput"] input,
[data-testid="stSelectbox"] [data-baseweb="select"] > div,
[data-testid="stMultiSelect"] [data-baseweb="select"] > div {
    border-radius: 11px !important;
    border-color: #E8D8DE !important;
    background: #FFFEFE;
}

[data-testid="stRadio"] label, [data-testid="stCheckbox"] label {
    color: #684B59;
}

[data-testid="stFormSubmitButton"] button {
    min-height: 48px;
    border-radius: 12px;
    letter-spacing: .2px;
    box-shadow: 0 5px 14px rgba(129, 61, 88, .16);
}

[data-testid="stFormSubmitButton"] button:hover {
    transform: translateY(-1px);
    box-shadow: 0 8px 18px rgba(129, 61, 88, .2);
}

hr { border-color: #F0E4E8; }


/* Botões de formulário com contraste e identidade Bolinuts. */
div[data-testid="stFormSubmitButton"] button {
    background:#B66F8C !important; color:#FFFFFF !important;
    border:1px solid #B66F8C !important; border-radius:11px !important;
    font-weight:700 !important; min-height:48px;
}
div[data-testid="stFormSubmitButton"] button *,
div[data-testid="stDownloadButton"] button * { color:#FFFFFF !important; }
div[data-testid="stFormSubmitButton"] button:hover {
    background:#985873 !important; border-color:#985873 !important;
}
div[data-testid="stDownloadButton"] button {
    background:#75465B !important; color:#FFFFFF !important;
    border:1px solid #75465B !important; border-radius:11px !important;
}
.st-key-voltar_novo button, .st-key-voltar_editar button {
    background:#FFFFFF !important; color:#75465B !important;
    border:1px solid #E7CBD6 !important; box-shadow:none !important;
}
.st-key-voltar_novo button *, .st-key-voltar_editar button * { color:#75465B !important; }
.st-key-voltar_novo button:hover, .st-key-voltar_editar button:hover {
    background:#F8EAF0 !important; color:#75465B !important;
}

/* Override específico do botão Voltar: mantém fundo claro mesmo com o estilo global. */
.st-key-voltar_novo div[data-testid="stButton"] > button,
.st-key-voltar_novo div[data-testid="stButton"] > button p,
.st-key-voltar_novo div[data-testid="stButton"] > button span {
    background:#FFFFFF !important;
    color:#75465B !important;
    border:1px solid #D9B8C7 !important;
    border-radius:11px !important;
    font-weight:700 !important;
    box-shadow:none !important;
}
.st-key-voltar_novo div[data-testid="stButton"] > button:hover {
    background:#F8EAF0 !important;
    color:#75465B !important;
    border-color:#B66F8C !important;
}

/* Correção definitiva do botão Voltar: o contorno pertence somente ao botão,
   nunca aos elementos internos de texto do Streamlit. */
div.st-key-voltar_novo {
    display:flex;
    justify-content:flex-start;
    margin: 4px 0 22px;
}
div.st-key-voltar_novo div[data-testid="stButton"] > button {
    display:inline-flex !important;
    align-items:center !important;
    justify-content:center !important;
    width:auto !important;
    min-width:190px !important;
    min-height:42px !important;
    padding:0.55rem 1rem !important;
    background:#FFFFFF !important;
    color:#75465B !important;
    border:1px solid #D9B8C7 !important;
    border-radius:11px !important;
    box-shadow:0 2px 7px rgba(117,70,91,.06) !important;
    font-weight:650 !important;
    line-height:1.2 !important;
}
div.st-key-voltar_novo div[data-testid="stButton"] > button p,
div.st-key-voltar_novo div[data-testid="stButton"] > button span,
div.st-key-voltar_novo div[data-testid="stButton"] > button div {
    color:#75465B !important;
    background:transparent !important;
    border:0 !important;
    box-shadow:none !important;
    padding:0 !important;
    margin:0 !important;
}
div.st-key-voltar_novo div[data-testid="stButton"] > button:hover {
    background:#F8EAF0 !important;
    color:#75465B !important;
    border-color:#B66F8C !important;
}


/* Botão voltar: contorno único no botão; elementos internos sem borda ou foco duplicado. */
div.st-key-voltar_novo div[data-testid="stButton"] > button,
div.st-key-voltar_novo div[data-testid="stButton"] > button:focus,
div.st-key-voltar_novo div[data-testid="stButton"] > button:focus-visible,
div.st-key-voltar_novo div[data-testid="stButton"] > button:active {
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    width: auto !important;
    min-width: 190px !important;
    min-height: 42px !important;
    padding: .55rem 1rem !important;
    background: #FFFFFF !important;
    color: #75465B !important;
    border: 1px solid #D9B8C7 !important;
    border-radius: 11px !important;
    box-shadow: 0 2px 7px rgba(117,70,91,.06) !important;
    outline: none !important;
    font-weight: 650 !important;
}
div.st-key-voltar_novo div[data-testid="stButton"] > button p,
div.st-key-voltar_novo div[data-testid="stButton"] > button span,
div.st-key-voltar_novo div[data-testid="stButton"] > button div {
    color: #75465B !important;
    background: transparent !important;
    border: 0 !important;
    border-radius: 0 !important;
    box-shadow: none !important;
    outline: none !important;
    padding: 0 !important;
    margin: 0 !important;
}
div.st-key-voltar_novo div[data-testid="stButton"] > button:hover {
    background: #F8EAF0 !important;
    border-color: #B66F8C !important;
    color: #75465B !important;
}
</style>
""", unsafe_allow_html=True)


# =====================================================
# FUNÇÕES
# =====================================================

def gerar_codigo():

    pedidos = list(
        colecao.find({}, {"codigo_pedido": 1})
    )

    numeros = []

    for pedido in pedidos:

        codigo = pedido.get("codigo_pedido", "")

        if isinstance(codigo, str) and codigo.startswith("BOL-"):

            try:
                numeros.append(
                    int(codigo.replace("BOL-", ""))
                )
            except ValueError:
                pass

    proximo = max(numeros, default=0) + 1

    return f"BOL-{proximo:03d}"


def calcular_status(total, recebido):

    if total > 0 and recebido >= total:
        return "Pago"

    elif recebido > 0:
        return "Parcial"

    return "Pendente"


def moeda(valor):

    return (
        f"R$ {valor:,.2f}"
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )


# =====================================================
# CABEÇALHO
# =====================================================

st.markdown(
    '<div class="titulo-pagina">Novo pedido <span style="font-size:20px">✦</span></div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitulo">Cadastre uma nova encomenda e organize os detalhes do pedido.</div>',
    unsafe_allow_html=True
)
with st.container(key="voltar_novo"):
    if st.button("← Voltar para pedidos", key="voltar_para_pedidos_novo"):
        st.switch_page("pages/pedidos.py")
st.markdown(" ")



# Limpa os campos após um cadastro concluído, antes de recriar os widgets.
if st.session_state.pop("_limpar_form_novo", False):
    for _chave in (
        "novo_nome_cliente", "novo_evento", "novo_tema", "novo_data_entrega",
        "novo_horario", "novo_tipo_produto", "novo_quantidade", "novo_massas",
        "novo_decoracao", "novo_observacoes", "novo_tipo_entrega",
        "novo_cep", "novo_logradouro", "novo_numero", "novo_complemento",
        "novo_bairro", "novo_cidade", "novo_referencia",
        "novo_valor_produtos", "novo_taxa_entrega", "novo_valor_sinal",
        "novo_forma_pagamento"
    ):
        st.session_state.pop(_chave, None)

# =====================================================
# FORMULÁRIO
# =====================================================


# -------------------------------------------------
# CLIENTE
# -------------------------------------------------

st.markdown(
    '<div class="secao">01 · Informações do cliente</div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)

with col1:

    nome_cliente = st.text_input(
        "Nome do cliente *",
        placeholder="Digite o nome do cliente",
        key="novo_nome_cliente"
    )

    evento = st.text_input(
        "Evento",
        placeholder="Ex.: Aniversário, casamento...",
        key="novo_evento"
    )

    tema = st.text_input(
        "Tema da decoração",
        placeholder="Ex.: Barbie, Roblox...",
        key="novo_tema"
    )

with col2:

    data_entrega = st.date_input(
        "Data de entrega *",
        value=date.today(),
        format="DD/MM/YYYY",
        key="novo_data_entrega"
    )

    horario = st.text_input(
        "Horário de entrega",
        placeholder="Ex.: 14:00",
        key="novo_horario"
    )

# Pedidos retroativos podem ser cadastrados já finalizados, quando apropriado.
pedido_retroativo_concluido = False
if data_entrega < date.today():
    st.info("Esta encomenda está sendo cadastrada com uma data anterior a hoje.")
    pedido_retroativo_concluido = st.checkbox(
        "Este pedido já foi entregue e está totalmente pago",
        key="novo_retroativo_concluido",
        help="Ao marcar, o pedido será registrado como pago e entregue, sem saldo pendente."
    )

st.divider()

# -------------------------------------------------
# PRODUTO
# -------------------------------------------------

st.markdown(
    '<div class="secao">02 · Detalhes da encomenda</div>',
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns(3)

with col1:

    tipo_produto = st.selectbox(
        "Tipo de produto",
        ["Simples", "Personalizado"],
        key="novo_tipo_produto"
    )

with col2:

    quantidade = st.number_input(
        "Quantidade",
        min_value=1,
        step=1,
        value=1,
        key="novo_quantidade"
    )

with col3:

    massas = st.multiselect(
        "Massa",
        [
            "Chocolate",
            "Cenoura",
            "Baunilha",
            "Canela"
        ],
        key="novo_massas"
    )

decoracao = st.text_input(
    "Descrição da decoração",
    placeholder="Ex.: Rosa e coração",
    key="novo_decoracao"
)

observacoes = st.text_area(
    "Observações",
    placeholder="Informações adicionais sobre o pedido...",
    key="novo_observacoes"
)

st.divider()

# -------------------------------------------------
# ENTREGA
# -------------------------------------------------

st.markdown(
    '<div class="secao">03 · Entrega</div>',
    unsafe_allow_html=True
)

tipo_entrega = st.radio(
    "Forma de entrega",
    ["Retirada", "Entrega"],
    horizontal=True,
    key="novo_tipo_entrega"
)

endereco = ""
cep = logradouro = numero_endereco = complemento = bairro = cidade = referencia = ""

if tipo_entrega == "Entrega":
    st.markdown("**Endereço para entrega**")
    st.caption("Preencha os dados para facilitar a localização e evitar dúvidas na entrega.")
    col_end1, col_end2 = st.columns([2, 1])
    with col_end1:
        logradouro = st.text_input(
            "Rua / Avenida *", placeholder="Nome da rua ou avenida", key="novo_logradouro"
        )
    with col_end2:
        numero_endereco = st.text_input(
            "Número *", placeholder="Nº", key="novo_numero"
        )
    col_end3, col_end4 = st.columns(2)
    with col_end3:
        bairro = st.text_input("Bairro *", placeholder="Bairro", key="novo_bairro")
    with col_end4:
        cidade = st.text_input("Cidade / UF *", placeholder="Ex.: Itapetininga / SP", key="novo_cidade")
    col_end5, col_end6 = st.columns(2)
    with col_end5:
        cep = st.text_input("CEP", placeholder="00000-000", key="novo_cep")
    with col_end6:
        complemento = st.text_input("Complemento", placeholder="Apto, casa, bloco...", key="novo_complemento")
    referencia = st.text_input(
        "Ponto de referência", placeholder="Ex.: próximo à praça", key="novo_referencia"
    )
    partes_endereco = [
        f"{logradouro}, {numero_endereco}".strip(", "),
        complemento, bairro, cidade, f"CEP: {cep}" if cep.strip() else "",
        f"Referência: {referencia}" if referencia.strip() else ""
    ]
    endereco = " - ".join(parte.strip() for parte in partes_endereco if parte.strip())

st.divider()

# -------------------------------------------------
# FINANCEIRO
# -------------------------------------------------

st.markdown(
    '<div class="secao">04 · Informações financeiras</div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)

with col1:

    valor_produtos = st.number_input(
        "Valor dos produtos (R$)",
        min_value=0.0,
        step=1.0,
        format="%.2f",
        key="novo_valor_produtos"
    )

    taxa_entrega = st.number_input(
        "Taxa de entrega (R$)",
        min_value=0.0,
        step=1.0,
        format="%.2f",
        key="novo_taxa_entrega"
    )

with col2:

    valor_sinal = st.number_input(
        "Valor de sinal (R$)",
        min_value=0.0,
        step=1.0,
        format="%.2f",
        key="novo_valor_sinal"
    )

    forma_pagamento = st.selectbox(
        "Forma de pagamento",
        [
            "Pix",
            "Dinheiro",
            "Cartão",
            "Transferência"
        ],
        key="novo_forma_pagamento"
    )

# -------------------------------------------------
# BOTÃO DE SALVAR
# -------------------------------------------------

salvar = st.button(
    "Salvar pedido",
    type="primary",
    use_container_width=True
)


# =====================================================
# CÁLCULO E SALVAMENTO
# =====================================================

# Os valores são calculados após o envio do formulário.
if salvar:

    valor_total = float(valor_produtos + taxa_entrega)
    valor_recebido_final = valor_total if pedido_retroativo_concluido else float(valor_sinal)
    valor_restante = max(valor_total - valor_recebido_final, 0)

    if not nome_cliente.strip():

        st.error("Informe o nome do cliente.")

    elif not massas:

        st.error("Selecione pelo menos uma massa.")

    elif valor_sinal > valor_total:

        st.error("O valor de sinal não pode ser maior que o valor total.")

    elif tipo_entrega == "Entrega" and (
        not logradouro.strip() or not numero_endereco.strip()
        or not bairro.strip() or not cidade.strip()
    ):

        st.error("Preencha rua/avenida, número, bairro e cidade para a entrega.")

    else:

        codigo = gerar_codigo()

        novo_pedido = {

            "codigo_pedido": codigo,

            "nome_cliente": nome_cliente.strip(),

            "data_entrega": datetime.combine(
                data_entrega,
                datetime.min.time()
            ),

            "evento": evento.strip(),

            "tema": tema.strip(),

            "tipo_produto": tipo_produto,

            "quantidade": int(quantidade),

            "massa": massas,

            "massas": massas,

            "decoracao": decoracao.strip(),

            "observacoes": observacoes.strip(),

            "tipo_entrega": tipo_entrega,

            # Campo consolidado mantido para compatibilidade com PDFs e telas antigas.
            "endereco": endereco.strip(),
            "endereco_cep": cep.strip(),
            "endereco_logradouro": logradouro.strip(),
            "endereco_numero": numero_endereco.strip(),
            "endereco_complemento": complemento.strip(),
            "endereco_bairro": bairro.strip(),
            "endereco_cidade": cidade.strip(),
            "endereco_referencia": referencia.strip(),

            "horario": horario.strip(),

            "valor_produtos": float(valor_produtos),

            "taxa_entrega": float(taxa_entrega),

            "valor_total": valor_total,

            "valor_sinal": valor_recebido_final,

            "valor_recebido": valor_recebido_final,

            "valor_restante": valor_restante,

            "forma_pagamento": forma_pagamento,

            "status_pagamento": calcular_status(
                valor_total,
                valor_recebido_final
            ),

            "pedido_concluido": bool(pedido_retroativo_concluido),
            "status_entrega": "Entregue" if pedido_retroativo_concluido else "Aguardando",
            "data_conclusao": datetime.now().strftime("%d/%m/%Y %H:%M") if pedido_retroativo_concluido else None,

            "data_cadastro": datetime.now()
        }

        try:

            colecao.insert_one(novo_pedido)

            st.success(
                f"Pedido {codigo} cadastrado com sucesso!"
            )
            st.session_state["_limpar_form_novo"] = True
            st.rerun()

        except Exception as erro:

            st.error(
                f"Não foi possível salvar o pedido: {erro}"
            )


# =====================================================
# PRÉVIA FINANCEIRA
# =====================================================

st.divider()

st.markdown(
    '<div class="secao">Como funciona o resumo financeiro?</div>',
    unsafe_allow_html=True
)

st.caption(
    "O total do pedido é formado pelo valor dos produtos "
    "somado à taxa de entrega. O restante corresponde ao "
    "total menos o valor já recebido."
)

