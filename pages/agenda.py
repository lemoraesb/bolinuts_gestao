import streamlit as st
import pandas as pd
from datetime import date, timedelta
from html import escape

from utils.conexao import obter_colecao
from utils.funcoes import buscar_pedidos, converter_data, resumo_financeiro, formatar_valor

st.set_page_config(page_title="Agenda | Bolinuts", page_icon="📅", layout="wide")
st.markdown("""
<style>
.stApp { background:linear-gradient(180deg,#FFFBF8 0%,#FAF7F6 100%); }
h1,h2,h3 { color:#75465B; }
[data-testid="stMetric"] { background:#FFFFFF; border:1px solid #EEE2E7; border-radius:15px; padding:15px 17px; box-shadow:0 4px 14px rgba(117,70,91,.04); }
[data-testid="stMetricLabel"] { color:#81747A; }
[data-testid="stMetricValue"] { color:#75465B; }
[data-testid="stTextInput"] input,[data-testid="stDateInput"] input,[data-baseweb="select"] > div { border-radius:10px !important; border-color:#E8D8DE !important; }
[data-testid="stMultiSelect"] [data-baseweb="tag"] { background:#F2EAF6 !important; color:#765F91 !important; }
.agenda-card { border:1px solid var(--card-border); background:var(--card-bg); border-radius:16px; padding:15px 17px; margin:0 0 12px; box-shadow:0 4px 13px rgba(117,70,91,.045); }
.agenda-card-top { display:flex; align-items:center; gap:13px; }
.agenda-date { min-width:62px; text-align:center; border-radius:11px; padding:8px 7px; background:var(--date-bg); color:#fff; }
.agenda-date strong { display:block; font-size:23px; line-height:1.05; }
.agenda-date span { display:block; font-size:10px; font-weight:800; letter-spacing:1px; margin-top:4px; }
.agenda-client { color:#49333D; font-size:15px; font-weight:750; }
.agenda-meta { color:#806777; font-size:12px; margin-top:3px; }
.agenda-status { margin-left:auto; white-space:nowrap; border-radius:20px; padding:5px 10px; font-size:11px; font-weight:750; background:var(--status-bg); color:var(--status-fg); }
.agenda-details { display:flex; flex-wrap:wrap; gap:8px 18px; border-top:1px solid var(--card-border); margin-top:12px; padding-top:10px; color:#684B59; font-size:12px; }
.agenda-details span { display:inline-flex; align-items:center; gap:5px; }
hr { border-color:#EEE2E7; }
</style>
""", unsafe_allow_html=True)

st.title("📅 Agenda de encomendas")
st.caption("Acompanhe as próximas entregas e organize a produção da Bolinuts.")
st.divider()

try:
    pedidos = buscar_pedidos(obter_colecao())
except Exception as erro:
    st.error(f"Não foi possível carregar os pedidos: {erro}")
    st.stop()

registros = []
for p in pedidos:
    data_entrega = converter_data(p.get("data_entrega"))
    if not data_entrega:
        continue
    financeiro = resumo_financeiro(p)
    registros.append({
        "Data": data_entrega,
        "Código": p.get("codigo_pedido", ""),
        "Cliente": p.get("nome_cliente", "Sem nome"),
        "Evento": p.get("evento") if p.get("evento") not in (None, "", "None") else (p.get("tema") or "—"),
        "Quantidade": p.get("quantidade") or "—",
        "Massa": ", ".join(p.get("massa", [])) if isinstance(p.get("massa"), list) else (p.get("massa") or "Não informada"),
        "Horário": p.get("horario") or "Não definido",
        "Entrega": p.get("tipo_entrega") or "Não informado",
        "Pagamento": financeiro["status"],
        "Saldo": financeiro["restante"],
        "Observações": p.get("observacoes") or "",
    })

df = pd.DataFrame(registros)
hoje = date.today()
if not df.empty:
    proximos = df[df["Data"] >= hoje]
    semana = proximos[proximos["Data"] <= hoje + timedelta(days=7)]
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Entregas hoje", int((df["Data"] == hoje).sum()))
    c2.metric("Próximos 7 dias", len(semana))
    c3.metric("Entregas futuras", len(proximos))
    c4.metric("Pedidos com saldo", int((df["Saldo"] > 0).sum()))
    st.divider()

    colf1, colf2 = st.columns(2)
    with colf1:
        periodo = st.date_input("Filtrar período", value=(hoje, hoje + timedelta(days=30)), format="DD/MM/YYYY")
    with colf2:
        status_filtro = st.multiselect("Situação do pagamento", ["Pago", "Parcial", "Pendente"], default=["Pago", "Parcial", "Pendente"])

    filtrado = df.copy()
    if isinstance(periodo, tuple) and len(periodo) == 2:
        filtrado = filtrado[(filtrado["Data"] >= periodo[0]) & (filtrado["Data"] <= periodo[1])]
    if status_filtro:
        filtrado = filtrado[filtrado["Pagamento"].isin(status_filtro)]
    else:
        filtrado = filtrado.iloc[0:0]

    filtrado = filtrado.sort_values(["Data", "Horário", "Cliente"])
    st.subheader("Encomendas programadas")
    if filtrado.empty:
        st.info("Nenhuma encomenda encontrada para os filtros selecionados.")
    else:
        exibir = filtrado.copy()
        exibir["Data"] = exibir["Data"].apply(lambda d: d.strftime("%d/%m/%Y"))
        exibir["Saldo"] = exibir["Saldo"].apply(formatar_valor)
        st.dataframe(exibir, use_container_width=True, hide_index=True)

    st.subheader("Próximas entregas")
    proximos = proximos.sort_values(["Data", "Horário"]).head(5)
    if proximos.empty:
        st.success("Não há entregas futuras cadastradas.")
    else:
        paleta = [
            ("#FFF3F6", "#EBD0DB", "#B66F8C"),
            ("#F4F0F8", "#DED3E8", "#927BAA"),
            ("#FFF5EE", "#F0DCCF", "#C58B70"),
        ]
        status_cores = {
            "Pago": ("#E7F4EA", "#287343"),
            "Parcial": ("#FFF0D5", "#98620C"),
            "Pendente": ("#F9E8EE", "#A34B61"),
        }
        for indice, (_, item) in enumerate(proximos.iterrows()):
            fundo, borda, cor_data = paleta[indice % len(paleta)]
            status_bg, status_fg = status_cores.get(item["Pagamento"], ("#F1EDF4", "#765F91"))
            data_item = item["Data"]
            dia = escape(data_item.strftime("%d"))
            mes = escape(data_item.strftime("%b").upper().replace(".", ""))
            cliente = escape(str(item["Cliente"]))
            codigo = escape(str(item["Código"]))
            evento = escape(str(item["Evento"]))
            horario = escape(str(item["Horário"]))
            quantidade = escape(str(item["Quantidade"]))
            entrega = escape(str(item["Entrega"]))
            pagamento = escape(str(item["Pagamento"]))
            st.markdown(f'''<div class="agenda-card" style="--card-bg:{fundo};--card-border:{borda};--date-bg:{cor_data};--status-bg:{status_bg};--status-fg:{status_fg};">
              <div class="agenda-card-top">
                <div class="agenda-date"><strong>{dia}</strong><span>{mes}</span></div>
                <div style="flex:1;min-width:0"><div class="agenda-client">{cliente}</div><div class="agenda-meta">{codigo} · {evento}</div></div>
                <div class="agenda-status">{pagamento}</div>
              </div>
              <div class="agenda-details"><span>🍩 {quantidade} unidades</span><span>🕒 {horario}</span><span>📦 {entrega}</span></div>
            </div>''', unsafe_allow_html=True)
else:
    st.info("Ainda não existem pedidos com data de entrega válida.")
