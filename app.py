import streamlit as st

from dashboard import main

main()
st.stop()

from io import BytesIO
from pathlib import Path

import pandas as pd
import streamlit as st

from charts import bar_anulacoes, bar_top, line_monthly, pie_top
from utils import (
    anulacoes_summary,
    apply_filters,
    brl,
    load_data,
    monthly_evolution,
    top_n,
)


DATA_PATH = Path(__file__).parent / "data" / "base_vdp_alece_2025_tratada.csv"


st.set_page_config(
    page_title="VDP ALECE 2025",
    page_icon="📊",
    layout="wide",
)


st.markdown(
    """
    <style>
    .main-title {
        font-size: 2.15rem;
        font-weight: 800;
        color: #1F4E79;
        margin-bottom: 0.2rem;
    }
    .subtitle {
        font-size: 1rem;
        color: #555;
        margin-bottom: 1.4rem;
    }
    .metric-card {
        background: #F4F7FA;
        border: 1px solid #E6ECF2;
        border-radius: 14px;
        padding: 16px 18px;
        min-height: 92px;
    }
    .metric-label {
        font-size: 0.82rem;
        color: #57606A;
        margin-bottom: 0.35rem;
    }
    .metric-value {
        font-size: 1.45rem;
        font-weight: 800;
        color: #1D1D1F;
    }
    .section-title {
        font-size: 1.25rem;
        font-weight: 750;
        color: #1F4E79;
        margin-top: 1.3rem;
        margin-bottom: 0.5rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data
def get_data() -> pd.DataFrame:
    return load_data(str(DATA_PATH))


def download_excel(df: pd.DataFrame) -> bytes:
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Base Filtrada")
    return output.getvalue()


df = get_data()

st.markdown('<div class="main-title">Painel da Verba de Desempenho Parlamentar – ALECE</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Dados públicos do Portal da Transparência | Exercício de 2025</div>', unsafe_allow_html=True)

with st.sidebar:
    st.header("Filtros")

    deputados = sorted(df["DEPUTADO"].dropna().unique())
    meses = (
        df[["MES_ANO", "MES_NUMERO"]]
        .drop_duplicates()
        .sort_values("MES_NUMERO")["MES_ANO"]
        .tolist()
    )
    credores = sorted(df["CREDOR"].dropna().unique())

    selected_deputados = st.multiselect("Deputado", deputados)
    selected_meses = st.multiselect("Mês/Ano", meses)
    selected_credores = st.multiselect("Credor", credores)

    st.divider()
    st.caption("Dica: deixe os filtros vazios para visualizar a base completa.")

filtered = apply_filters(df, selected_deputados, selected_meses, selected_credores)

total_liquido = filtered["VALOR"].sum()
total_bruto = filtered.loc[filtered["VALOR"] > 0, "VALOR"].sum()
total_anulacoes_abs = filtered.loc[filtered["VALOR"] < 0, "VALOR_ABSOLUTO"].sum()
qtd_deputados = filtered["DEPUTADO"].nunique()
qtd_credores = filtered["CREDOR"].nunique()
qtd_registros = len(filtered)
qtd_anulacoes = int((filtered["VALOR"] < 0).sum())

col1, col2, col3, col4, col5 = st.columns(5)
metrics = [
    ("Valor líquido", brl(total_liquido)),
    ("Despesas brutas", brl(total_bruto)),
    ("Anulações", f"{qtd_anulacoes} | {brl(total_anulacoes_abs)}"),
    ("Deputados", f"{qtd_deputados}"),
    ("Credores", f"{qtd_credores}"),
]
for col, (label, value) in zip([col1, col2, col3, col4, col5], metrics):
    with col:
        st.markdown(
            f"""
            <div class="metric-card">
              <div class="metric-label">{label}</div>
              <div class="metric-value">{value}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown('<div class="section-title">Visão temporal</div>', unsafe_allow_html=True)
evol = monthly_evolution(filtered)
st.plotly_chart(line_monthly(evol), use_container_width=True)

st.markdown('<div class="section-title">Maiores despesas</div>', unsafe_allow_html=True)
left, right = st.columns(2)

top_dep = top_n(filtered, "DEPUTADO", "VALOR", 10)
top_cred = top_n(filtered, "CREDOR", "VALOR", 10)

with left:
    st.plotly_chart(pie_top(top_dep, "DEPUTADO", "VALOR", "Top 10 despesas por deputado"), use_container_width=True)
with right:
    st.plotly_chart(pie_top(top_cred, "CREDOR", "VALOR", "Top 10 despesas por credor"), use_container_width=True)

left2, right2 = st.columns(2)
with left2:
    st.plotly_chart(bar_top(top_dep, "VALOR", "DEPUTADO", "Ranking Top 10 deputados"), use_container_width=True)
with right2:
    st.plotly_chart(bar_top(top_cred, "VALOR", "CREDOR", "Ranking Top 10 credores"), use_container_width=True)

st.markdown('<div class="section-title">Anulações</div>', unsafe_allow_html=True)
anul = anulacoes_summary(filtered)
a1, a2 = st.columns([1, 1])
with a1:
    st.plotly_chart(bar_anulacoes(anul), use_container_width=True)
with a2:
    st.dataframe(
        anul.rename(
            columns={
                "TIPO_ANULACAO": "Tipo de anulação",
                "REGISTROS": "Registros",
                "VALOR_ABSOLUTO": "Valor absoluto",
            }
        ),
        use_container_width=True,
        hide_index=True,
    )

st.markdown('<div class="section-title">Base detalhada</div>', unsafe_allow_html=True)
columns_to_show = [
    c for c in [
        "DEPUTADO",
        "PERIODO",
        "MES_ANO",
        "EMPENHO",
        "DESCRICAO",
        "CREDOR",
        "VALOR",
        "TIPO_MOVIMENTO",
        "TIPO_ANULACAO",
    ] if c in filtered.columns
]
st.dataframe(filtered[columns_to_show], use_container_width=True, hide_index=True)

csv = filtered.to_csv(sep=";", index=False, encoding="utf-8-sig").encode("utf-8-sig")
excel = download_excel(filtered)

d1, d2 = st.columns([1, 1])
with d1:
    st.download_button(
        "Baixar base filtrada em CSV",
        data=csv,
        file_name="base_vdp_alece_2025_filtrada.csv",
        mime="text/csv",
    )
with d2:
    st.download_button(
        "Baixar base filtrada em Excel",
        data=excel,
        file_name="base_vdp_alece_2025_filtrada.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )

st.caption(
    "Observação metodológica: os valores negativos foram mantidos na base por representarem anulações administrativas. "
    "Eles foram classificados em correções administrativas, desistência e motivo não especificado."
)
