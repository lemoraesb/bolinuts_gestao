
import streamlit as st
from pathlib import Path


# =====================================================
# CONFIGURAÇÃO GERAL
# =====================================================

st.set_page_config(
    page_title="Bolinuts Gestão",
    page_icon="🍩",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =====================================================
# CAMINHOS
# =====================================================

PASTA_PROJETO = Path(__file__).parent
CAMINHO_LOGO = PASTA_PROJETO / "imagens" / "logo_bolinuts.png"


# =====================================================
# IDENTIDADE VISUAL
# =====================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Playfair+Display:wght@600;700&display=swap');
:root { --berry:#B36F8B; --berry-dark:#75465B; --rose:#D99AAF; --rose-soft:#F8EAF0; --cream:#FFFBF8; --ink:#3F3439; --muted:#81747A; --line:#EEE2E7; --lavender:#B9A7C9; }
html, body, [class*="css"] { font-family:'DM Sans',sans-serif; }
.stApp { background:linear-gradient(180deg,#FFFBF8 0%,#FAF7F6 100%); color:var(--ink); }
.block-container { padding-top:2rem; padding-bottom:3rem; max-width:1440px; }
[data-testid="stHeader"] { background:rgba(255,251,248,.92); }
h1,h2,h3 { color:var(--berry-dark); letter-spacing:-.035em; }
h1 { font-family:'Playfair Display',serif; font-size:2.25rem !important; }
h2 { font-size:1.45rem !important; }
h3 { font-size:1.12rem !important; }
p, label { color:var(--ink); }
[data-testid="stCaptionContainer"] p { color:var(--muted); }
section[data-testid="stSidebar"] { background:linear-gradient(180deg,#F8EDF1 0%,#FBF4F0 100%); border-right:1px solid #EEDDE4; }
section[data-testid="stSidebar"] > div { padding:22px 18px; }
[data-testid="stSidebarNav"] { display:none; }
.marca-titulo { color:var(--berry-dark); font-family:'Playfair Display',serif; font-size:25px; font-weight:700; text-align:center; margin:8px 0 4px; }
.marca-subtitulo { color:#947681; font-size:12px; text-align:center; margin-bottom:25px; letter-spacing:.02em; }
.menu-titulo { color:#A17D8B; font-size:10px; font-weight:800; letter-spacing:1.5px; margin:22px 0 10px; }
section[data-testid="stSidebar"] a[data-testid="stPageLink-NavLink"] { border-radius:11px; padding:10px 12px; margin:4px 0; color:#624653; font-weight:600; transition:all .18s ease; }
section[data-testid="stSidebar"] a[data-testid="stPageLink-NavLink"]:hover { background:#F1DCE5; color:var(--berry-dark); }
section[data-testid="stSidebar"] a[data-testid="stPageLink-NavLink"][aria-current="page"] { background:#F0DCE4; color:var(--berry-dark); font-weight:800; }
.divisor-sidebar { border-top:1px solid #EAD6DF; margin:20px 0; }
.status-banco,.status-erro { border-radius:12px; padding:12px; font-size:12px; font-weight:700; }
.status-banco { background:#EAF5ED; border:1px solid #D7EBDD; color:#34734A; }
.status-erro { background:#FBEAEC; border:1px solid #F1D2D8; color:#A0445A; }
.rodape-sidebar { color:#A18B94; text-align:center; font-size:10px; margin-top:22px; }
/* Estilo padrão dos botões. Cada página pode definir cores próprias por ação. */
.stButton > button, .stDownloadButton > button,
[data-testid="stFormSubmitButton"] button {
    border-radius: 11px;
    border: 1px solid #B36F8B;
    background: #B36F8B;
    color: #FFFFFF;
    font-weight: 700;
    padding: .55rem 1rem;
    transition: all .2s ease;
    box-shadow: 0 3px 10px rgba(117,70,91,.08);
}
.stButton > button *, .stDownloadButton > button *,
[data-testid="stFormSubmitButton"] button * { color: #FFFFFF; }
.stButton > button:hover, .stDownloadButton > button:hover,
[data-testid="stFormSubmitButton"] button:hover {
    background: #925A73;
    border-color: #925A73;
    color: #FFFFFF;
}
[data-testid="stTextInput"] input,[data-testid="stNumberInput"] input,[data-testid="stDateInput"] input,[data-testid="stSelectbox"] div[data-baseweb="select"] { border-radius:10px; }
[data-testid="stMetric"] { background:#FFFFFF; border:1px solid var(--line); border-radius:16px; padding:17px 19px; box-shadow:0 5px 18px rgba(103,49,73,.045); }
[data-testid="stMetricLabel"] { color:var(--muted); font-size:12px; font-weight:600; }
[data-testid="stMetricValue"] { color:var(--berry-dark); font-size:25px; font-weight:750; }
[data-testid="stMetric"] { box-shadow:0 4px 14px rgba(117,70,91,.035); }
[data-testid="stDataFrame"] { border:1px solid var(--line); border-radius:13px; overflow:hidden; }
hr { border-color:var(--line); }
[data-testid="stAlert"] { border-radius:12px; }
footer { visibility:hidden; }
</style>
""", unsafe_allow_html=True)


# =====================================================
# REGISTRO DAS PÁGINAS
# =====================================================

dashboard = st.Page(
    "pages/dashboard.py",
    title="Dashboard",
    icon=":material/dashboard:",
    default=True
)

desempenho = st.Page(
    "pages/desempenhovendas.py",
    title="Desempenho de Vendas",
    icon=":material/monitoring:"
)

pedidos = st.Page(
    "pages/pedidos.py",
    title="Pedidos",
    icon=":material/assignment:"
)

agenda = st.Page(
    "pages/agenda.py",
    title="Agenda de Encomendas",
    icon=":material/calendar_month:"
)

# Consultas técnicas permanecem implementadas em pages/consultas.py
# para demonstração acadêmica, sem aparecer no menu principal.

# Páginas internas: continuam disponíveis
# para os botões de cadastro e edição.

novo_pedido = st.Page(
    "pages/novopedido.py",
    title="Novo Pedido",
    icon=":material/add_circle:"
)

editar_pedido = st.Page(
    "pages/editarpedido.py",
    title="Editar Pedido",
    icon=":material/edit:"
)


# =====================================================
# NAVEGAÇÃO
# =====================================================

navegacao = st.navigation(
    [
        dashboard,
        desempenho,
        pedidos,
        agenda,
        novo_pedido,
        editar_pedido
    ],
    position="hidden"
)


# =====================================================
# BARRA LATERAL
# =====================================================

with st.sidebar:

    # -------------------------------------------------
    # LOGO CENTRALIZADA E AMPLIADA
    # -------------------------------------------------

    if CAMINHO_LOGO.exists():

        espaco_esquerda, centro, espaco_direita = st.columns(
            [0.1, 1, 0.1]
        )

        with centro:

            st.image(
                str(CAMINHO_LOGO),
                width=190
            )

    else:

        st.warning(
            "Logo não encontrada na pasta imagens."
        )

    # Frase de apoio abaixo do logo, sem repetir o nome da marca
    st.markdown(
        '<div style="text-align:center;color:#947681;font-size:12px;'
        'font-style:italic;margin:8px 0 24px;">'
        'Gestão com carinho, sabor e organização</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="divisor-sidebar"></div>',
        unsafe_allow_html=True
    )

    # -------------------------------------------------
    # MENU PRINCIPAL
    # -------------------------------------------------

    st.markdown(
        '<div class="menu-titulo">MENU PRINCIPAL</div>',
        unsafe_allow_html=True
    )

    st.page_link(
        dashboard,
        label="Dashboard"
    )

    st.page_link(
        desempenho,
        label="Desempenho de Vendas"
    )

    st.page_link(
        pedidos,
        label="Pedidos"
    )

    st.page_link(
        agenda,
        label="Agenda de Encomendas"
    )

    # -------------------------------------------------
    # DIVISOR
    # -------------------------------------------------

    st.markdown(
        '<div class="divisor-sidebar"></div>',
        unsafe_allow_html=True
    )

    # -------------------------------------------------
    # RODAPÉ
    # -------------------------------------------------

    st.markdown(
        """
        <div class="rodape-sidebar">
            Versão visual revisada · 19/11/2026
        </div>
        """,
        unsafe_allow_html=True
    )


# =====================================================
# EXECUTAR PÁGINA SELECIONADA
# =====================================================

navegacao.run()





























