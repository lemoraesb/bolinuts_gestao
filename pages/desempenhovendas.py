
import streamlit as st
from html import escape
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path

from io import BytesIO

from utils.conexao import obter_colecao
from utils.funcoes import buscar_pedidos

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
    Image as RLImage,
    KeepTogether
)


# =====================================================
# CONFIGURAÇÕES VISUAIS
# =====================================================

VINHO = "#75465B"
ROSA = "#B97892"
ROSA_CLARO = "#E9C8D5"
CINZA = "#81747A"
BRANCO = "#FFFFFF"

VINHO_PDF = colors.HexColor("#75465B")
ROSA_PDF = colors.HexColor("#F7E8ED")
CINZA_PDF = colors.HexColor("#77716F")


st.markdown("""
<style>

.stApp {
    background-color: #FFFBF8;
}

.block-container {
    max-width: 1500px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

h1, h2, h3 {
    color: #75465B;
}

div[data-testid="stMetric"] {
    background-color: #FFFFFF;
    border: 1px solid #EEE2E7;
    border-radius: 12px;
    padding: 17px 19px;
    min-height: 105px;
    box-shadow: 0 3px 10px rgba(129, 61, 88, 0.04);
}

div[data-testid="stMetricLabel"] {
    color: #77716F;
    font-size: 13px;
}

div[data-testid="stMetricValue"] {
    color: #75465B;
    font-size: 25px;
    font-weight: 650;
}

div[data-testid="stPlotlyChart"] {
    background: linear-gradient(180deg, #FFFFFF 0%, #FFFCFD 100%);
    border: 1px solid #F0E4E8;
    border-radius: 17px;
    padding: 5px 8px 2px;
    box-shadow: 0 7px 22px rgba(129, 61, 88, .045);
}

div[data-testid="stDownloadButton"] button {
    background: #B36F8B; color: #FFFFFF !important;
    border: 1px solid #B36F8B; border-radius: 10px;
    min-height: 39px; padding: .42rem .9rem;
    font-size: 13px; font-weight: 700; width: auto;
    box-shadow: 0 3px 10px rgba(137,77,104,.09);
}
div[data-testid="stDownloadButton"] button:hover {
    background: #925A73; border-color: #925A73; color: #FFFFFF !important;
}
div[data-testid="stPlotlyChart"] .modebar { display:none !important; }

hr {
    border-color: #E8DFDA;
}


/* Padronização final dos botões: vinho escuro + texto branco */
div.stButton > button,
div[data-testid="stFormSubmitButton"] button,
div[data-testid="stDownloadButton"] button {
    background: #75465B !important;
    border: 1px solid #75465B !important;
    color: #FFFFFF !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
}
div.stButton > button *,
div[data-testid="stFormSubmitButton"] button *,
div[data-testid="stDownloadButton"] button * { color: #FFFFFF !important; }
div.stButton > button:hover,
div[data-testid="stFormSubmitButton"] button:hover,
div[data-testid="stDownloadButton"] button:hover {
    background: #5E3448 !important;
    border-color: #5E3448 !important;
    color: #FFFFFF !important;
}

</style>
""", unsafe_allow_html=True)


# =====================================================
# FUNÇÕES AUXILIARES
# =====================================================

def moeda(valor):
    valor = float(valor or 0)

    texto = f"{valor:,.2f}"
    texto = texto.replace(",", "X")
    texto = texto.replace(".", ",")
    texto = texto.replace("X", ".")

    return f"R$ {texto}"


def converter_data(valor):
    if not valor:
        return pd.NaT

    return pd.to_datetime(valor, errors="coerce")


def nome_mes(numero):
    meses = {
        1: "Janeiro",
        2: "Fevereiro",
        3: "Março",
        4: "Abril",
        5: "Maio",
        6: "Junho",
        7: "Julho",
        8: "Agosto",
        9: "Setembro",
        10: "Outubro",
        11: "Novembro",
        12: "Dezembro"
    }

    return meses[numero]


def normalizar_produto(valor):

    if isinstance(valor, (list, tuple, set)):
        itens = valor
    elif valor is None:
        itens = []
    else:
        itens = [valor]

    nomes = []

    for item in itens:
        nome = str(item).strip().lower()

        if nome and nome not in ["none", "nan"]:
            if nome not in nomes:
                nomes.append(nome)

    if not nomes:
        return "Não informado"

    if len(nomes) == 1:
        return nomes[0].title()

    if "simples" in nomes and "personalizado" in nomes:
        return "Simples e personalizado"

    return " e ".join(nomes).title()


def obter_massas(valor):

    if isinstance(valor, str):
        return [valor] if valor.strip() else []

    if isinstance(valor, (list, tuple, set)):
        return list(valor)

    return []


def configurar_grafico(fig, altura=350):

    fig.update_layout(
        height=altura,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(
            family="DM Sans, Arial, sans-serif",
            color="#806F77",
            size=11
        ),
        margin=dict(
            l=18,
            r=18,
            t=22,
            b=28
        ),
        showlegend=False
    )

    fig.update_xaxes(
        showgrid=False,
        zeroline=False,
        linecolor="#F0E4E8",
        tickfont=dict(size=10, color="#907E86")
    )

    fig.update_yaxes(
        showgrid=True,
        gridcolor="#F4ECEF",
        gridwidth=1,
        zeroline=False,
        tickfont=dict(size=10, color="#907E86")
    )

    return fig




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
# GERAR RELATÓRIO PDF
# =====================================================

def gerar_pdf(
    indicadores,
    mensal,
    produtos,
    massas,
    vendas,
    data_inicio,
    data_fim,
    titulo_periodo
):
    """Gera relatório comercial organizado em páginas com identidade visual Bolinuts."""
    buffer = BytesIO()
    margem = 1.35 * cm
    largura_conteudo = landscape(A4)[0] - (2 * margem)
    documento = SimpleDocTemplate(
        buffer,
        pagesize=landscape(A4),
        rightMargin=margem,
        leftMargin=margem,
        topMargin=1.15 * cm,
        bottomMargin=1.35 * cm,
        title=f"Relatório comercial - {titulo_periodo}",
        author="Bolinuts Gestão",
    )

    estilos = getSampleStyleSheet()
    vinho = VINHO_PDF
    rosa = colors.HexColor("#B66F8C")
    rosa_claro = colors.HexColor("#F8EAF0")
    rosa_borda = colors.HexColor("#EAD6DF")
    creme = colors.HexColor("#FFFBF8")
    texto = colors.HexColor("#493C42")
    cinza = CINZA_PDF

    titulo_principal = ParagraphStyle(
        "BolinutsRelatorioTitulo", parent=estilos["Title"],
        fontName="Helvetica-Bold", fontSize=19, leading=23,
        textColor=vinho, alignment=0, spaceAfter=3,
    )
    subtitulo = ParagraphStyle(
        "BolinutsRelatorioSubtitulo", parent=estilos["Normal"],
        fontName="Helvetica", fontSize=9, leading=12,
        textColor=cinza, spaceAfter=0,
    )
    titulo_secundario = ParagraphStyle(
        "BolinutsRelatorioTituloSecundario", parent=estilos["Heading2"],
        fontName="Helvetica-Bold", fontSize=15, leading=18,
        textColor=vinho, spaceAfter=2,
    )
    texto_periodo = ParagraphStyle(
        "BolinutsRelatorioPeriodo", parent=estilos["Normal"],
        fontName="Helvetica-Bold", fontSize=8.5, leading=11,
        textColor=vinho,
    )
    texto_secao = ParagraphStyle(
        "BolinutsRelatorioSecao", parent=estilos["Heading3"],
        fontName="Helvetica-Bold", fontSize=11, leading=13,
        textColor=vinho,
    )
    celula = ParagraphStyle(
        "BolinutsRelatorioCelula", parent=estilos["Normal"],
        fontName="Helvetica", fontSize=8.2, leading=10.5,
        textColor=texto, wordWrap="CJK",
    )
    celula_cabecalho = ParagraphStyle(
        "BolinutsRelatorioCabecalho", parent=celula,
        fontName="Helvetica-Bold", textColor=colors.white,
    )

    def par(valor, estilo=celula):
        return Paragraph(escape(str(valor if valor not in (None, "") else "—")), estilo)

    def cabecalho_pdf(titulo, descricao, largura_logo=3.0):
        logo = criar_logo_pdf(largura_logo)
        bloco_texto = [Paragraph(titulo, titulo_principal if titulo == "Relatório de desempenho comercial" else titulo_secundario),
                       Paragraph(descricao, subtitulo)]
        if logo is None:
            tabela = Table([[bloco_texto]], colWidths=[largura_conteudo], hAlign="LEFT")
        else:
            tabela = Table([[logo, bloco_texto]],
                           colWidths=[largura_logo * cm, largura_conteudo - largura_logo * cm],
                           hAlign="LEFT")
        tabela.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), creme),
            ("BOX", (0, 0), (-1, -1), 0.7, rosa_borda),
            ("LINEBELOW", (0, 0), (-1, -1), 2, rosa),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (0, 0), (-1, -1), 12),
            ("RIGHTPADDING", (0, 0), (-1, -1), 12),
            ("TOPPADDING", (0, 0), (-1, -1), 8),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ]))
        return tabela

    def secao_pdf(texto):
        tabela = Table([[Paragraph(escape(texto), texto_secao)]],
                       colWidths=[largura_conteudo], hAlign="LEFT")
        tabela.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), rosa_claro),
            ("BOX", (0, 0), (-1, -1), 0.45, rosa_borda),
            ("LINEBEFORE", (0, 0), (0, -1), 2.5, rosa),
            ("LEFTPADDING", (0, 0), (-1, -1), 9),
            ("RIGHTPADDING", (0, 0), (-1, -1), 8),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ]))
        return tabela

    def estilo_tabela(tabela, total=False, fonte=8.2):
        comandos = [
            ("BACKGROUND", (0, 0), (-1, 0), vinho),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("GRID", (0, 0), (-1, -1), 0.35, rosa_borda),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, rosa_claro]),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("FONTSIZE", (0, 0), (-1, -1), fonte),
            ("LEFTPADDING", (0, 0), (-1, -1), 7),
            ("RIGHTPADDING", (0, 0), (-1, -1), 7),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ]
        if total:
            comandos.extend([
                ("BACKGROUND", (0, -1), (-1, -1), colors.HexColor("#F1DFE7")),
                ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
                ("TEXTCOLOR", (0, -1), (-1, -1), vinho),
            ])
        tabela.setStyle(TableStyle(comandos))
        return tabela

    elementos = []
    elementos.append(cabecalho_pdf(
        "Relatório de desempenho comercial",
        "Resumo financeiro, vendas e indicadores do período selecionado",
        3.4,
    ))
    elementos.append(Spacer(1, 8))

    faixa_periodo = Table([[
        Paragraph(
            f"<b>PERÍODO</b>  ·  {escape(str(titulo_periodo))}<br/>"
            f"<font color='#81747A'>De {data_inicio.strftime('%d/%m/%Y')} até {data_fim.strftime('%d/%m/%Y')}</font>",
            texto_periodo,
        )
    ]], colWidths=[largura_conteudo], hAlign="LEFT")
    faixa_periodo.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), rosa_claro),
        ("BOX", (0, 0), (-1, -1), 0.5, rosa_borda),
        ("LINEBEFORE", (0, 0), (0, -1), 2.5, rosa),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    elementos.extend([faixa_periodo, Spacer(1, 10), secao_pdf("Resumo financeiro")])

    resumo = [
        [par("Indicador", celula_cabecalho), par("Resultado", celula_cabecalho)],
        [par("Faturamento"), par(moeda(indicadores["faturamento"]))],
        [par("Pedidos"), par(str(indicadores["pedidos"]))],
        [par("Unidades vendidas"), par(str(indicadores["unidades"]))],
        [par("Valores recebidos"), par(moeda(indicadores["recebido"]))],
        [par("Valores a receber"), par(moeda(indicadores["a_receber"]))],
        [par("Ticket médio"), par(moeda(indicadores["ticket"]))],
    ]
    tabela_resumo = Table(resumo, colWidths=[largura_conteudo * .58, largura_conteudo * .42],
                          repeatRows=1, hAlign="LEFT")
    elementos.extend([estilo_tabela(tabela_resumo), Spacer(1, 8), secao_pdf("Faturamento no período")])

    dados_mensais = [[par("Data / período", celula_cabecalho), par("Pedidos", celula_cabecalho),
                      par("Faturamento", celula_cabecalho)]]
    if not mensal.empty:
        mensal_com_movimento = mensal[
            (pd.to_numeric(mensal["Pedidos"], errors="coerce").fillna(0) > 0)
            | (pd.to_numeric(mensal["Faturamento"], errors="coerce").fillna(0) > 0)
        ]
    else:
        mensal_com_movimento = mensal
    for _, linha in mensal_com_movimento.iterrows():
        dados_mensais.append([par(linha["Período"]), par(str(int(linha["Pedidos"]))),
                              par(moeda(linha["Faturamento"]))])
    if len(dados_mensais) == 1:
        dados_mensais.append([par("Nenhuma venda registrada no período"), par("0"), par(moeda(0))])
    dados_mensais.append([par("TOTAL"), par(str(int(mensal["Pedidos"].sum()))),
                          par(moeda(mensal["Faturamento"].sum()))])
    tabela_mensal = Table(dados_mensais,
                          colWidths=[largura_conteudo * .52, largura_conteudo * .18, largura_conteudo * .30],
                          repeatRows=1, hAlign="LEFT")
    elementos.extend([estilo_tabela(tabela_mensal, total=True), Spacer(1, 8), secao_pdf("Desempenho por produto")])

    dados_produtos = [[par("Produto", celula_cabecalho), par("Pedidos", celula_cabecalho),
                       par("Unidades", celula_cabecalho), par("Faturamento", celula_cabecalho)]]
    for _, linha in produtos.iterrows():
        dados_produtos.append([par(linha["Produto"]), par(str(int(linha["Pedidos"]))),
                               par(str(int(linha["Unidades"]))), par(moeda(linha["Faturamento"]))])
    if len(dados_produtos) == 1:
        dados_produtos.append([par("Sem dados"), par("—"), par("—"), par("—")])
    tabela_produtos = Table(dados_produtos,
                            colWidths=[largura_conteudo * .40, largura_conteudo * .17,
                                       largura_conteudo * .18, largura_conteudo * .25],
                            repeatRows=1, hAlign="LEFT")
    elementos.append(estilo_tabela(tabela_produtos))

    # Segunda página: detalhes operacionais, com cabeçalho no mesmo padrão da primeira.
    elementos.append(PageBreak())
    elementos.append(cabecalho_pdf(
        "Detalhamento das encomendas",
        f"Relação de massas e pedidos · {titulo_periodo}",
        2.8,
    ))
    elementos.extend([Spacer(1, 10), secao_pdf("Massas mais utilizadas")])

    dados_massas = [[par("Massa", celula_cabecalho), par("Ocorrências nos pedidos", celula_cabecalho)]]
    for _, linha in massas.iterrows():
        dados_massas.append([par(linha["Massa"]), par(str(int(linha["Pedidos"])))])
    if len(dados_massas) == 1:
        dados_massas.append([par("Sem dados no período"), par("—")])
    tabela_massas = Table(dados_massas,
                          colWidths=[largura_conteudo * .58, largura_conteudo * .42],
                          repeatRows=1, hAlign="LEFT")
    elementos.extend([estilo_tabela(tabela_massas), Spacer(1, 10), secao_pdf("Detalhamento dos pedidos")])

    dados_vendas = [[par(c, celula_cabecalho) for c in
                     ["Código", "Cliente", "Entrega", "Produto", "Qtd.", "Valor", "Pagamento"]]]
    for _, linha in vendas.iterrows():
        dados_vendas.append([
            par(linha["Código"]), par(linha["Cliente"]), par(linha["Entrega"]),
            par(linha["Produto"]), par(str(int(linha["Quantidade"]))),
            par(moeda(linha["Valor"])), par(linha["Pagamento"]),
        ])
    if len(dados_vendas) == 1:
        dados_vendas.append([par("Nenhum pedido encontrado no período"), par(""), par(""),
                             par(""), par(""), par(""), par("")])
    tabela_vendas = Table(
        dados_vendas,
        colWidths=[largura_conteudo * x for x in (.12, .19, .14, .18, .07, .14, .16)],
        repeatRows=1,
        hAlign="LEFT",
    )
    elementos.append(estilo_tabela(tabela_vendas, fonte=7.7))

    def rodape_pagina(canvas, doc):
        canvas.saveState()
        canvas.setStrokeColor(rosa_borda)
        canvas.setLineWidth(.5)
        canvas.line(margem, .95 * cm, landscape(A4)[0] - margem, .95 * cm)
        canvas.setFont("Helvetica", 7)
        canvas.setFillColor(cinza)
        canvas.drawString(margem, .62 * cm, "Bolinuts Gestão · Relatório comercial")
        canvas.drawRightString(landscape(A4)[0] - margem, .62 * cm, f"Página {doc.page}")
        canvas.restoreState()

    documento.build(elementos, onFirstPage=rodape_pagina, onLaterPages=rodape_pagina)
    buffer.seek(0)
    return buffer.getvalue()

# =====================================================
# CABEÇALHO
# =====================================================

st.title("📈 Desempenho de Vendas")

st.caption(
    "Acompanhe o faturamento, os produtos vendidos "
    "e os resultados comerciais da Bolinuts."
)

st.divider()


# =====================================================
# CONEXÃO COM MONGODB
# =====================================================

try:
    colecao = obter_colecao()
    pedidos = buscar_pedidos(colecao)

except Exception as erro:
    st.error(f"Erro ao consultar o MongoDB: {erro}")
    st.stop()


if not pedidos:
    st.info("Ainda não existem pedidos cadastrados.")
    st.stop()


# =====================================================
# ORGANIZAÇÃO DOS DADOS
# =====================================================

dados = []

for pedido in pedidos:

    dados.append({
        "Código": pedido.get("codigo_pedido", ""),
        "Cliente": pedido.get("nome_cliente") if pedido.get("nome_cliente") not in (None, "", "None") else "—",
        "Data": converter_data(pedido.get("data_entrega")),
        "Produto": normalizar_produto(
            pedido.get("tipo_produto", "")
        ),
        "Quantidade": int(
            pedido.get("quantidade", 0) or 0
        ),
        "Valor": float(
            pedido.get("valor_total", 0) or 0
        ),
        "Recebido": float(
            pedido.get("valor_sinal", 0) or 0
        ),
        "Restante": float(
            pedido.get("valor_restante", 0) or 0
        ),
        "Pagamento": pedido.get(
            "status_pagamento", "Não informado"
        ),
        "Massas": obter_massas(
            pedido.get("massa", pedido.get("massas", []))
        )
    })


df = pd.DataFrame(dados)

df["Data"] = pd.to_datetime(
    df["Data"],
    errors="coerce"
)

df = df.dropna(subset=["Data"]).copy()

if df.empty:
    st.warning("Não existem pedidos com datas válidas.")
    st.stop()


# =====================================================
# SELEÇÃO DO PERÍODO
# =====================================================

st.subheader("Período do relatório")

anos_disponiveis = sorted(
    df["Data"].dt.year.unique().tolist(),
    reverse=True
)

col1, col2, col3 = st.columns(3)

with col1:

    tipo_relatorio = st.selectbox(
        "Tipo de relatório",
        ["Mensal", "Trimestral", "Anual"]
    )

with col2:

    ano_selecionado = st.selectbox(
        "Ano",
        anos_disponiveis
    )

meses = {
    "Janeiro": 1,
    "Fevereiro": 2,
    "Março": 3,
    "Abril": 4,
    "Maio": 5,
    "Junho": 6,
    "Julho": 7,
    "Agosto": 8,
    "Setembro": 9,
    "Outubro": 10,
    "Novembro": 11,
    "Dezembro": 12
}

with col3:

    if tipo_relatorio == "Mensal":

        mes_selecionado = st.selectbox(
            "Mês",
            list(meses.keys())
        )

    elif tipo_relatorio == "Trimestral":

        trimestre_selecionado = st.selectbox(
            "Trimestre",
            [
                "1º trimestre",
                "2º trimestre",
                "3º trimestre",
                "4º trimestre"
            ]
        )

    else:

        st.info(f"Ano completo: {ano_selecionado}")


# DEFINIR DATA INICIAL E FINAL

if tipo_relatorio == "Mensal":

    numero_mes = meses[mes_selecionado]

    data_inicio = pd.Timestamp(
        year=ano_selecionado,
        month=numero_mes,
        day=1
    )

    data_fim = (
        data_inicio + pd.offsets.MonthEnd(1)
        + pd.Timedelta(days=1) - pd.Timedelta(microseconds=1)
    )

    titulo_periodo = (
        f"{mes_selecionado} de {ano_selecionado}"
    )

    nome_arquivo = (
        f"relatorio_bolinuts_{ano_selecionado}_"
        f"{numero_mes:02d}_{mes_selecionado.lower()}.pdf"
    )

elif tipo_relatorio == "Trimestral":

    numero_trimestre = int(
        trimestre_selecionado[0]
    )

    primeiro_mes = (
        (numero_trimestre - 1) * 3 + 1
    )

    data_inicio = pd.Timestamp(
        year=ano_selecionado,
        month=primeiro_mes,
        day=1
    )

    data_fim = (
        data_inicio + pd.DateOffset(months=3)
        - pd.Timedelta(microseconds=1)
    )

    titulo_periodo = (
        f"{trimestre_selecionado} de {ano_selecionado}"
    )

    nome_arquivo = (
        f"relatorio_bolinuts_{ano_selecionado}_"
        f"trimestre_{numero_trimestre}.pdf"
    )

else:

    data_inicio = pd.Timestamp(
        year=ano_selecionado,
        month=1,
        day=1
    )

    data_fim = pd.Timestamp(
        year=ano_selecionado,
        month=12,
        day=31,
        hour=23,
        minute=59,
        second=59,
        microsecond=999999
    )

    titulo_periodo = f"Ano de {ano_selecionado}"

    nome_arquivo = (
        f"relatorio_bolinuts_{ano_selecionado}.pdf"
    )


# APLICAR FILTRO

df_filtrado = df[
    (df["Data"] >= data_inicio) &
    (df["Data"] <= data_fim)
].copy()


if df_filtrado.empty:

    st.warning(
        "Não existem pedidos cadastrados para esse período."
    )

    st.stop()


st.success(
    f"Relatório selecionado: {titulo_periodo}"
)

st.divider()


# =====================================================
# INDICADORES
# =====================================================

total_pedidos = len(df_filtrado)

unidades = int(
    df_filtrado["Quantidade"].sum()
)

faturamento = float(
    df_filtrado["Valor"].sum()
)

recebido = float(
    df_filtrado["Recebido"].sum()
)

a_receber = float(
    df_filtrado["Restante"].sum()
)

ticket = (
    faturamento / total_pedidos
    if total_pedidos else 0
)


st.subheader("Indicadores comerciais")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Faturamento", moeda(faturamento))

with col2:
    st.metric("Pedidos no período", total_pedidos)

with col3:
    st.metric(
        "Unidades vendidas",
        f"{unidades:,}".replace(",", ".")
    )


col4, col5, col6 = st.columns(3)

with col4:
    st.metric("Valores recebidos", moeda(recebido))

with col5:
    st.metric("Valores a receber", moeda(a_receber))

with col6:
    st.metric("Ticket médio", moeda(ticket))


st.divider()


# =====================================================
# FATURAMENTO CONFORME O PERÍODO SELECIONADO
# =====================================================

if tipo_relatorio == "Mensal":
    st.subheader(f"Faturamento diário · {titulo_periodo}")
    datas_periodo = pd.date_range(data_inicio, data_fim, freq="D")
    serie = df_filtrado.groupby(df_filtrado["Data"].dt.normalize()).agg(
        Pedidos=("Código", "count"), Faturamento=("Valor", "sum")
    )
    serie = serie.reindex(datas_periodo, fill_value=0).rename_axis("Data").reset_index()
    serie_periodo = pd.DataFrame({
        "Período": serie["Data"].dt.strftime("%d/%m"),
        "Pedidos": serie["Pedidos"].astype(int),
        "Faturamento": serie["Faturamento"].astype(float),
    })
    eixo_x = serie_periodo["Período"]
    titulo_grafico = f"Movimento diário de {mes_selecionado}"
    tickvals = serie_periodo["Período"].iloc[::max(1, len(serie_periodo)//7)].tolist()
elif tipo_relatorio == "Trimestral":
    st.subheader(f"Faturamento mensal · {titulo_periodo}")
    periodos = pd.period_range(data_inicio.to_period("M"), data_fim.to_period("M"), freq="M")
    serie = df_filtrado.groupby(df_filtrado["Data"].dt.to_period("M")).agg(
        Pedidos=("Código", "count"), Faturamento=("Valor", "sum")
    ).reindex(periodos, fill_value=0).rename_axis("Periodo").reset_index()
    serie_periodo = pd.DataFrame({
        "Período": serie["Periodo"].apply(lambda x: f"{nome_mes(x.month)}/{x.year}"),
        "Pedidos": serie["Pedidos"].astype(int),
        "Faturamento": serie["Faturamento"].astype(float),
    })
    eixo_x = serie_periodo["Período"]
    titulo_grafico = "Comparativo dos três meses"
    tickvals = eixo_x.tolist()
else:
    st.subheader(f"Faturamento mensal · {ano_selecionado}")
    periodos = pd.period_range(f"{ano_selecionado}-01", f"{ano_selecionado}-12", freq="M")
    serie = df_filtrado.groupby(df_filtrado["Data"].dt.to_period("M")).agg(
        Pedidos=("Código", "count"), Faturamento=("Valor", "sum")
    ).reindex(periodos, fill_value=0).rename_axis("Periodo").reset_index()
    serie_periodo = pd.DataFrame({
        "Período": serie["Periodo"].apply(lambda x: f"{nome_mes(x.month)[:3]}/{str(x.year)[-2:]}"),
        "Pedidos": serie["Pedidos"].astype(int),
        "Faturamento": serie["Faturamento"].astype(float),
    })
    eixo_x = serie_periodo["Período"]
    titulo_grafico = f"Evolução anual do faturamento · {ano_selecionado}"
    tickvals = eixo_x.tolist()

# Indicadores auxiliares seguem o mesmo recorte do gráfico.
if tipo_relatorio == "Anual":
    meses_com_venda = serie_periodo[serie_periodo["Faturamento"] > 0]
    melhor_mes = "Sem vendas"
    if not meses_com_venda.empty:
        melhor_idx = meses_com_venda["Faturamento"].idxmax()
        melhor_periodo = periodos[int(melhor_idx)] if int(melhor_idx) < len(periodos) else None
        melhor_mes = f"{nome_mes(melhor_periodo.month)}/{melhor_periodo.year}" if melhor_periodo is not None else meses_com_venda.loc[melhor_idx, "Período"]
    r1, r2, r3 = st.columns(3)
    r1.metric("Faturamento no ano", moeda(serie_periodo["Faturamento"].sum()))
    r2.metric("Melhor mês", melhor_mes)
    r3.metric("Meses com vendas", int((serie_periodo["Faturamento"] > 0).sum()))
elif tipo_relatorio == "Trimestral":
    r1, r2, r3 = st.columns(3)
    r1.metric("Faturamento no trimestre", moeda(serie_periodo["Faturamento"].sum()))
    r2.metric("Meses com vendas", int((serie_periodo["Faturamento"] > 0).sum()))
    r3.metric("Pedidos no trimestre", int(serie_periodo["Pedidos"].sum()))

fig_periodo = go.Figure()
fig_periodo.add_trace(go.Scatter(
    x=eixo_x,
    y=serie_periodo["Faturamento"],
    mode="lines+markers",
    line=dict(color=ROSA, width=3, shape="spline", smoothing=0.85),
    marker=dict(size=6, color=VINHO, line=dict(color="#FFFFFF", width=2)),
    fill="tozeroy", fillcolor="rgba(185,120,146,0.13)",
    hovertemplate="<b>%{x}</b><br>Faturamento: R$ %{y:,.2f}<extra></extra>"
))
fig_periodo.update_layout(
    title=dict(text=titulo_grafico, x=0.02, font=dict(size=13, color=VINHO)),
    xaxis_title="", yaxis_title="", hovermode="x unified",
    showlegend=False, height=300,
    margin=dict(l=24, r=72, t=48, b=42),
    font=dict(family="DM Sans, sans-serif", color="#75666D", size=11),
    plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)"
)
fig_periodo.update_yaxes(
    tickprefix="R$ ", tickformat=",.0f", rangemode="tozero", zeroline=False,
    gridcolor="#F1E7EB", tickfont=dict(color="#8A7B82", size=10)
)
fig_periodo.update_xaxes(
    type="category", tickmode="array", tickvals=tickvals,
    showgrid=False, tickangle=0, automargin=True,
    tickfont=dict(color="#8A7B82", size=10),
    ticklabeloverflow="allow"
)
fig_periodo = configurar_grafico(fig_periodo, altura=300)
fig_periodo.update_layout(title=dict(text=titulo_grafico, x=0.02, font=dict(size=13, color=VINHO)))
st.plotly_chart(
    fig_periodo, use_container_width=True,
    config={"displayModeBar": False, "displaylogo": False, "responsive": True}
)

st.markdown(f"**Detalhamento do faturamento · {titulo_periodo}**")
tabela_mensal = serie_periodo.copy()
# No relatório mensal, exibir somente os dias que tiveram pedidos.
if tipo_relatorio == "Mensal":
    tabela_mensal = tabela_mensal[tabela_mensal["Pedidos"] > 0].copy()
tabela_mensal["Faturamento"] = tabela_mensal["Faturamento"].apply(moeda)
st.dataframe(tabela_mensal, use_container_width=True, hide_index=True)
st.caption(
    f"Os gráficos, indicadores, tabelas e arquivos exportados consideram somente: {titulo_periodo}."
)


st.divider()


# =====================================================
# DESEMPENHO POR PRODUTO
# =====================================================

st.subheader("Desempenho por produto")

produtos = (
    df_filtrado.groupby("Produto")
    .agg(
        Pedidos=("Código", "count"),
        Unidades=("Quantidade", "sum"),
        Faturamento=("Valor", "sum")
    )
    .reset_index()
    .sort_values("Unidades", ascending=True)
)

col_produto1, col_produto2 = st.columns(2)

with col_produto1:

    st.markdown("**Unidades vendidas**")

    fig_unidades = go.Figure(
        go.Bar(
            x=produtos["Unidades"],
            y=produtos["Produto"],
            orientation="h",
            marker_color=ROSA,
            marker_line_width=0,
            opacity=0.9,
            text=produtos["Unidades"],
            textposition="outside",
            cliponaxis=False
        )
    )

    max_unidades = max(float(produtos["Unidades"].max()), 1)
    fig_unidades.update_layout(
        xaxis_title="",
        yaxis_title="",
        bargap=0.58,
        margin=dict(l=18, r=72, t=18, b=30)
    )
    fig_unidades.update_xaxes(range=[0, max_unidades * 1.22], automargin=True)

    altura_produtos = max(190, min(260, 135 + 42 * len(produtos)))
    fig_unidades = configurar_grafico(fig_unidades, altura=altura_produtos)
    fig_unidades.update_layout(margin=dict(l=18, r=58, t=12, b=28))
    fig_unidades.update_xaxes(range=[0, max_unidades * 1.18], automargin=True)

    st.plotly_chart(
        fig_unidades,
        use_container_width=True,
        config={"displayModeBar": False, "displaylogo": False, "responsive": True}
    )


with col_produto2:

    st.markdown("**Faturamento por produto**")

    fig_produto = go.Figure(
        go.Bar(
            x=produtos["Faturamento"],
            y=produtos["Produto"],
            orientation="h",
            marker_color=VINHO,
            marker_line_width=0,
            opacity=0.9,
            text=[
                moeda(v) for v in produtos["Faturamento"]
            ],
            textposition="outside",
            cliponaxis=False
        )
    )

    max_faturamento_produto = max(float(produtos["Faturamento"].max()), 1)
    fig_produto.update_layout(
        xaxis_title="",
        yaxis_title="",
        bargap=0.58,
        margin=dict(l=18, r=105, t=18, b=30)
    )
    fig_produto.update_xaxes(range=[0, max_faturamento_produto * 1.38], automargin=True)

    fig_produto.update_xaxes(
        tickprefix="R$ ",
        tickformat=",.0f"
    )

    fig_produto = configurar_grafico(fig_produto, altura=altura_produtos)
    # Reserva espaço para o rótulo em reais sem provocar rolagem vertical.
    fig_produto.update_layout(margin=dict(l=18, r=88, t=12, b=28))
    fig_produto.update_xaxes(range=[0, max_faturamento_produto * 1.30], automargin=True)

    st.plotly_chart(
        fig_produto,
        use_container_width=True,
        config={"displayModeBar": False, "displaylogo": False, "responsive": True}
    )


st.divider()


# =====================================================
# MASSAS UTILIZADAS
# =====================================================

st.subheader("Massas mais utilizadas")

contagem_massas = {}

for _, pedido in df_filtrado.iterrows():

    for massa in pedido["Massas"]:

        nome = str(massa).strip().title()

        if nome:

            contagem_massas[nome] = (
                contagem_massas.get(nome, 0) + 1
            )


if contagem_massas:

    massas_df = pd.DataFrame(
        list(contagem_massas.items()),
        columns=["Massa", "Pedidos"]
    )

    massas_df = massas_df.sort_values(
        "Pedidos",
        ascending=True
    )

    fig_massas = go.Figure(
        go.Bar(
            x=massas_df["Pedidos"],
            y=massas_df["Massa"],
            orientation="h",
            marker_color=ROSA_CLARO,
            marker_line_width=0,
            opacity=0.95,
            text=massas_df["Pedidos"],
            textposition="outside"
        )
    )

    fig_massas.update_layout(
        xaxis_title="",
        yaxis_title="",
        bargap=0.58
    )

    fig_massas = configurar_grafico(
        fig_massas,
        altura=max(175, min(260, 105 + 45 * len(massas_df)))
    )

    st.plotly_chart(
        fig_massas,
        use_container_width=True
    )

else:

    st.info("Não existem informações de massas cadastradas.")


st.divider()


# =====================================================
# RANKING DE PRODUTOS
# =====================================================

st.subheader("Ranking de produtos")

ranking = produtos.copy()

ranking["Faturamento"] = (
    ranking["Faturamento"].apply(moeda)
)

ranking = ranking.rename(
    columns={
        "Unidades": "Unidades vendidas"
    }
)

st.dataframe(
    ranking,
    use_container_width=True,
    hide_index=True
)


st.divider()


# =====================================================
# DETALHAMENTO DAS VENDAS
# =====================================================

st.subheader("Detalhamento das vendas")

tabela_vendas = df_filtrado[
    [
        "Código",
        "Cliente",
        "Data",
        "Produto",
        "Quantidade",
        "Valor",
        "Pagamento"
    ]
].copy()

tabela_vendas["Entrega"] = (
    tabela_vendas["Data"].dt.strftime("%d/%m/%Y")
)

tabela_vendas = tabela_vendas.drop(
    columns=["Data"]
)

tabela_exibicao = tabela_vendas.copy()

tabela_exibicao["Valor"] = (
    tabela_exibicao["Valor"].apply(moeda)
)

tabela_exibicao = tabela_exibicao.rename(
    columns={"Valor": "Valor (R$)"}
)

st.dataframe(
    tabela_exibicao[
        [
            "Código",
            "Cliente",
            "Entrega",
            "Produto",
            "Quantidade",
            "Valor (R$)",
            "Pagamento"
        ]
    ],
    use_container_width=True,
    hide_index=True
)


# =====================================================
# GERAR PDF
# =====================================================

st.divider()

with st.container(border=True):
    st.subheader("Relatórios e exportação")
    st.caption("Baixe os resultados do período selecionado para compartilhar ou analisar depois.")

    tabela_mensal_pdf = serie_periodo.copy()
    indicadores_pdf = {
        "faturamento": faturamento,
        "pedidos": total_pedidos,
        "unidades": unidades,
        "recebido": recebido,
        "a_receber": a_receber,
        "ticket": ticket
    }

    massas_pdf = pd.DataFrame(
        list(contagem_massas.items()),
        columns=["Massa", "Pedidos"]
    )

    col_esq, col_pdf, col_csv, col_dir = st.columns([1.3, 1.7, 1.7, 1.3])

    try:
        arquivo_pdf = gerar_pdf(
            indicadores_pdf,
            tabela_mensal_pdf,
            produtos,
            massas_pdf,
            tabela_vendas,
            data_inicio,
            data_fim,
            titulo_periodo
        )

        with col_pdf:
            st.download_button(
                label="📄  Baixar relatório em PDF",
                data=arquivo_pdf,
                file_name=nome_arquivo,
                mime="application/pdf",
                use_container_width=True
            )

    except Exception as erro:
        st.error(f"Erro ao gerar o relatório PDF: {erro}")

    csv = df_filtrado.drop(
        columns=["Massas"],
        errors="ignore"
    ).to_csv(
        index=False,
        sep=";",
        encoding="utf-8-sig"
    )

    with col_csv:
        st.download_button(
            label="▦  Exportar dados em CSV",
            data=csv,
            file_name=nome_arquivo.replace(".pdf", ".csv"),
            mime="text/csv",
            use_container_width=True
        )


# =====================================================
# RODAPÉ
# =====================================================

st.divider()

st.caption(
    "Bolinuts Gestão | Controle e desempenho comercial"
)


