
import streamlit as st
from datetime import datetime, date

from utils.conexao import obter_colecao

st.set_page_config(page_title="Editar Pedido | Bolinuts", page_icon="✏️", layout="wide")

st.markdown("""
<style>
.edit-hero { background:linear-gradient(115deg,#75465B 0%,#A96883 62%,#D49AB0 100%); border-radius:19px; padding:22px 26px; margin:0 0 22px; box-shadow:0 10px 25px rgba(113,51,79,.13); }
.edit-hero h2 { color:#fff !important; font-family:'Playfair Display',serif; font-size:27px !important; margin:0 0 4px; }
.edit-hero p { color:#F8EAF0 !important; margin:0; font-size:13px; }
.edit-context { background:#FFF5F8; border:1px solid #EEDCE4; border-radius:14px; padding:13px 17px; margin:14px 0 18px; color:#70445A; }
.edit-section { color:#75465B; font-size:17px; font-weight:750; margin:7px 0 14px; padding-left:11px; border-left:3px solid #D9A5B7; }
div[data-testid="stForm"] { border:1px solid #EEE2E7; border-radius:18px; padding:24px 26px; background:linear-gradient(180deg,#FFFFFF 0%,#FFFEFD 100%); box-shadow:0 10px 30px rgba(129,61,88,.055); }
[data-testid="stTextInput"] input,[data-testid="stTextArea"] textarea,[data-testid="stNumberInput"] input,[data-testid="stDateInput"] input,[data-baseweb="select"] > div { border-radius:11px !important; border-color:#E8D8DE !important; }
[data-testid="stFormSubmitButton"] button {
    min-height:48px; border-radius:12px !important;
    background:#B36F8B !important; color:#FFFFFF !important;
    border:1px solid #B36F8B !important;
    box-shadow:0 5px 14px rgba(129,61,88,.12);
    font-weight:700 !important;
}
[data-testid="stFormSubmitButton"] button:hover {
    background:#925A73 !important; border-color:#925A73 !important;
    color:#FFFFFF !important; transform:translateY(-1px);
}
[data-testid="stFormSubmitButton"] button p,
[data-testid="stFormSubmitButton"] button span { color:#FFFFFF !important; }
.st-key-voltar_editar button {
    background:#FFFFFF !important; color:#75465B !important;
    border:1px solid #E7CBD6 !important; border-radius:10px !important;
    min-height:38px; box-shadow:none !important; font-weight:650 !important;
}
.st-key-voltar_editar button:hover { background:#F8EAF0 !important; color:#75465B !important; }
hr { border-color:#F0E4E8; }

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
.st-key-voltar_editar div[data-testid="stButton"] > button,
.st-key-voltar_editar div[data-testid="stButton"] > button p,
.st-key-voltar_editar div[data-testid="stButton"] > button span {
    background:#FFFFFF !important;
    color:#75465B !important;
    border:1px solid #D9B8C7 !important;
    border-radius:11px !important;
    font-weight:700 !important;
    box-shadow:none !important;
}
.st-key-voltar_editar div[data-testid="stButton"] > button:hover {
    background:#F8EAF0 !important;
    color:#75465B !important;
    border-color:#B66F8C !important;
}

/* Correção definitiva do botão Voltar: o contorno pertence somente ao botão,
   nunca aos elementos internos de texto do Streamlit. */
div.st-key-voltar_editar {
    display:flex;
    justify-content:flex-start;
    margin: 4px 0 22px;
}
div.st-key-voltar_editar div[data-testid="stButton"] > button {
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
div.st-key-voltar_editar div[data-testid="stButton"] > button p,
div.st-key-voltar_editar div[data-testid="stButton"] > button span,
div.st-key-voltar_editar div[data-testid="stButton"] > button div {
    color:#75465B !important;
    background:transparent !important;
    border:0 !important;
    box-shadow:none !important;
    padding:0 !important;
    margin:0 !important;
}
div.st-key-voltar_editar div[data-testid="stButton"] > button:hover {
    background:#F8EAF0 !important;
    color:#75465B !important;
    border-color:#B66F8C !important;
}


/* Botão voltar: contorno único no botão; elementos internos sem borda ou foco duplicado. */
div.st-key-voltar_editar div[data-testid="stButton"] > button,
div.st-key-voltar_editar div[data-testid="stButton"] > button:focus,
div.st-key-voltar_editar div[data-testid="stButton"] > button:focus-visible,
div.st-key-voltar_editar div[data-testid="stButton"] > button:active {
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
div.st-key-voltar_editar div[data-testid="stButton"] > button p,
div.st-key-voltar_editar div[data-testid="stButton"] > button span,
div.st-key-voltar_editar div[data-testid="stButton"] > button div {
    color: #75465B !important;
    background: transparent !important;
    border: 0 !important;
    border-radius: 0 !important;
    box-shadow: none !important;
    outline: none !important;
    padding: 0 !important;
    margin: 0 !important;
}
div.st-key-voltar_editar div[data-testid="stButton"] > button:hover {
    background: #F8EAF0 !important;
    border-color: #B66F8C !important;
    color: #75465B !important;
}
</style>
<div class="edit-hero"><h2>Editar encomenda ✦</h2><p>Atualize os detalhes do pedido com praticidade e mantenha tudo organizado.</p></div>
""", unsafe_allow_html=True)

with st.container(key="voltar_editar"):
    if st.button("← Voltar para pedidos", key="voltar_para_pedidos_editar"):
        st.switch_page("pages/pedidos.py")

colecao = obter_colecao()

pedidos = list(colecao.find().sort("_id", -1))

if not pedidos:
    st.info("Não existem pedidos cadastrados para editar.")
    st.stop()


def converter_para_data(valor):
    if isinstance(valor, datetime):
        return valor.date()

    if isinstance(valor, date):
        return valor

    if isinstance(valor, str):
        try:
            return datetime.fromisoformat(valor).date()
        except ValueError:
            try:
                return datetime.strptime(valor, "%d/%m/%Y").date()
            except ValueError:
                pass

    return date.today()


def texto_seguro(valor):
    return "" if valor in (None, "None") else str(valor)


def calcular_status(total, recebido):
    if total > 0 and recebido >= total:
        return "Pago"
    elif recebido > 0:
        return "Parcial"
    return "Pendente"


pedidos_com_codigo = [
    p for p in pedidos if p.get("codigo_pedido")
]

if not pedidos_com_codigo:
    st.warning("Nenhum pedido possui código cadastrado.")
    st.stop()


opcoes = {
    f"{p.get('codigo_pedido')} - {p.get('nome_cliente', 'Sem nome')}": p
    for p in pedidos_com_codigo
}

selecao = st.selectbox(
    "Selecione o pedido que deseja editar",
    list(opcoes.keys())
)

pedido = opcoes[selecao]

massas_atuais = pedido.get("massas", pedido.get("massa", []))

if isinstance(massas_atuais, str):
    massas_atuais = [massas_atuais]

massas_disponiveis = ["Chocolate", "Cenoura", "Baunilha", "Canela"]

massas_atuais = [
    massa for massa in massas_atuais
    if massa in massas_disponiveis
]

data_atual = converter_para_data(pedido.get("data_entrega"))

with st.form("form_editar_pedido"):

    st.markdown('<div class="edit-section">01 · Informações do cliente</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        nome_cliente = st.text_input(
            "Nome do cliente *",
            value=texto_seguro(pedido.get("nome_cliente", ""))
        )

        evento = st.text_input(
            "Evento",
            value=texto_seguro(pedido.get("evento", ""))
        )

        tema = st.text_input(
            "Tema da decoração",
            value=texto_seguro(pedido.get("tema", ""))
        )

    with col2:
        data_entrega = st.date_input(
            "Data de entrega *",
            value=data_atual
        )

        horario = st.text_input(
            "Horário de entrega",
            value=texto_seguro(pedido.get("horario", ""))
        )

    st.divider()

    st.markdown('<div class="edit-section">02 · Detalhes da encomenda</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    tipo_atual = pedido.get("tipo_produto", "Simples")

    with col1:
        tipo_produto = st.selectbox(
            "Tipo de produto",
            ["Simples", "Personalizado"],
            index=0 if tipo_atual == "Simples" else 1
        )

    with col2:
        quantidade = st.number_input(
            "Quantidade",
            min_value=1,
            step=1,
            value=max(1, int(pedido.get("quantidade", 1) or 1))
        )

    with col3:
        massas = st.multiselect(
            "Massa",
            massas_disponiveis,
            default=massas_atuais
        )

    decoracao = st.text_input(
        "Descrição da decoração",
        value=texto_seguro(pedido.get("decoracao", ""))
    )

    observacoes = st.text_area(
        "Observações",
        value=texto_seguro(pedido.get("observacoes", ""))
    )

    st.divider()

    st.markdown('<div class="edit-section">03 · Entrega</div>', unsafe_allow_html=True)

    tipo_entrega_atual = pedido.get("tipo_entrega", "Retirada")

    tipo_entrega = st.radio(
        "Forma de entrega",
        ["Retirada", "Entrega"],
        index=0 if tipo_entrega_atual == "Retirada" else 1,
        horizontal=True
    )

    endereco = st.text_input(
        "Endereço de entrega",
        value=texto_seguro(pedido.get("endereco", ""))
    )

    st.divider()

    st.markdown('<div class="edit-section">04 · Informações financeiras</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        valor_produtos = st.number_input(
            "Valor dos produtos (R$)",
            min_value=0.0,
            value=float(pedido.get("valor_produtos", 0) or 0),
            step=1.0,
            format="%.2f"
        )

        taxa_entrega = st.number_input(
            "Taxa de entrega (R$)",
            min_value=0.0,
            value=float(pedido.get("taxa_entrega", 0) or 0),
            step=1.0,
            format="%.2f"
        )

    with col2:
        recebido_registrado = st.number_input(
            "Valor já recebido (R$) — corrigir se necessário",
            min_value=0.0,
            value=float(pedido.get("valor_sinal", 0) or 0),
            step=1.0,
            format="%.2f",
            help="Use este campo para corrigir um sinal ou recebimento registrado incorretamente. O saldo e o status serão recalculados ao salvar."
        )

        formas = ["Pix", "Dinheiro", "Cartão", "Transferência"]
        forma_atual = pedido.get("forma_pagamento", "Pix")

        forma_pagamento = st.selectbox(
            "Forma de pagamento",
            formas,
            index=formas.index(forma_atual) if forma_atual in formas else 0
        )

    valor_total = valor_produtos + taxa_entrega
    valor_restante = max(valor_total - recebido_registrado, 0)

    st.markdown(
        f"""<div style="background:#FCEBF1;border:1px solid #E9C8D5;border-radius:14px;padding:17px 20px;margin:8px 0 18px;">
        <div style="font-size:11px;color:#98627A;font-weight:700;letter-spacing:1px;text-transform:uppercase;">Resumo financeiro</div>
        <div style="display:flex;gap:34px;flex-wrap:wrap;margin-top:8px;">
        <div><div style="font-size:12px;color:#98627A;">Total do pedido</div><div style="font-size:23px;font-weight:800;color:#75465B;">R$ {valor_total:,.2f}</div></div>
        <div><div style="font-size:12px;color:#98627A;">Valor restante</div><div style="font-size:20px;font-weight:750;color:#98627A;">R$ {valor_restante:,.2f}</div></div>
        </div></div>""",
        unsafe_allow_html=True
    )

    salvar = st.form_submit_button(
        "Salvar alterações",
        type="primary",
        use_container_width=True
    )


if salvar:

    if not texto_seguro(nome_cliente).strip():
        st.error("Informe o nome do cliente.")
    elif not massas:
        st.error("Selecione pelo menos uma massa.")
    elif recebido_registrado > valor_total:
        st.error("O valor recebido não pode ser maior que o novo total do pedido. Corrija o valor recebido ou o total.")
    elif tipo_entrega == "Entrega" and not texto_seguro(endereco).strip():
        st.error("Informe o endereço de entrega.")
    else:

        atualizacao = {
            "nome_cliente": texto_seguro(nome_cliente).strip(),
            "data_entrega": datetime.combine(data_entrega, datetime.min.time()),
            "evento": texto_seguro(evento).strip(),
            "tema": texto_seguro(tema).strip(),
            "tipo_produto": tipo_produto,
            "quantidade": int(quantidade),
            "massa": massas,
            "massas": massas,
            "decoracao": texto_seguro(decoracao).strip(),
            "observacoes": texto_seguro(observacoes).strip(),
            "tipo_entrega": tipo_entrega,
            "endereco": texto_seguro(endereco).strip() if tipo_entrega == "Entrega" else "",
            "horario": texto_seguro(horario).strip(),
            "valor_produtos": float(valor_produtos),
            "taxa_entrega": float(taxa_entrega),
            "valor_total": float(valor_total),
            "valor_sinal": float(recebido_registrado),
            "valor_restante": float(valor_restante),
            "forma_pagamento": forma_pagamento,
            "status_pagamento": calcular_status(valor_total, recebido_registrado)
        }

        try:
            resultado = colecao.update_one(
                {"_id": pedido["_id"]},
                {"$set": atualizacao}
            )

            if resultado.modified_count > 0:
                st.success("Pedido atualizado com sucesso!")
                st.rerun()
            else:
                st.info("Nenhuma alteração foi identificada.")

        except Exception as erro:
            st.error(f"Não foi possível atualizar o pedido: {erro}")
