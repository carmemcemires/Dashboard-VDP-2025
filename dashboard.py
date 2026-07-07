from __future__ import annotations

import base64
from datetime import datetime
from io import BytesIO
from pathlib import Path

import pandas as pd
import streamlit as st

from charts import bar_anulacoes, bar_cancellation_categories, bar_categories, bar_top, line_monthly, pie_top
from utils import (
    anulacoes_summary,
    apply_filters,
    brl,
    cancellation_category_summary,
    category_summary,
    load_data,
    monthly_evolution,
    pct,
    top_n,
)


BASE_DIR = Path(__file__).parent
DATA_PATH = BASE_DIR / "base_vdp_alece_2025_limpa.csv"
LOGO_PATH = BASE_DIR / "alece-logo-header.png"
SOURCE_URL = "https://transparencia.al.ce.gov.br/despesas/verba-desempenho-parlamentar"
Ato_URL = "https://transparencia.al.ce.gov.br/userfiles/files/vdp/2023-ato-deliberativo-n-929_1775043845.pdf"
RESOLUCAO_URL = "https://transparencia.al.ce.gov.br/userfiles/files/vdp/resolucao-762-23-publicacao_1775043845.pdf"
ATO_NORMATIVO_URL = "https://transparencia.al.ce.gov.br/userfiles/files/vdp/ato-normativo-343-24_1775043845.pdf"


def get_data() -> pd.DataFrame:
    return load_data(str(DATA_PATH))


def public_detail_base(df: pd.DataFrame) -> pd.DataFrame:
    citizen_columns = [
        "DEPUTADO",
        "MES_ANO",
        "EMPENHO",
        "DESCRICAO",
        "CREDOR",
        "VALOR",
        "CATEGORIA_DESPESA",
        "CATEGORIA_ANULACAO",
        "TIPO_MOVIMENTO",
        "TIPO_ANULACAO",
    ]
    return df[[col for col in citizen_columns if col in df.columns]].copy()


def prepare_public_columns(df: pd.DataFrame) -> pd.DataFrame:
    return df.rename(
        columns={
            "DEPUTADO": "Deputado",
            "PERIODO": "Período",
            "MES_ANO": "Mês/Ano",
            "EMPENHO": "Empenho",
            "DESCRICAO": "Descrição",
            "CREDOR": "Credor",
            "VALOR": "Valor",
            "CATEGORIA_DESPESA": "Categoria da despesa",
            "CATEGORIA_ANULACAO": "Motivo da anulação",
            "TIPO_MOVIMENTO": "Tipo de movimento",
            "TIPO_ANULACAO": "Tipo de anulação",
        }
    )


def download_excel(df: pd.DataFrame) -> bytes:
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Base detalhada")
        worksheet = writer.sheets["Base detalhada"]
        for column in worksheet.iter_cols(1, worksheet.max_column):
            header = column[0].value
            if header == "Valor":
                for cell in column[1:]:
                    cell.number_format = '"R$" #,##0.00;-"R$" #,##0.00'
            width = min(max(len(str(cell.value)) if cell.value is not None else 0 for cell in column) + 2, 55)
            worksheet.column_dimensions[column[0].column_letter].width = width
    return output.getvalue()


def top_for_chart(df: pd.DataFrame, group_col: str, label: str) -> pd.DataFrame:
    chart_df = top_n(df, group_col, positive_only=True).rename(columns={group_col: label, "VALOR": "Valor"})
    return chart_df


def metric_card(label: str, value: str, hint: str | None = None) -> None:
    hint_html = f'<div class="metric-hint">{hint}</div>' if hint else ""
    st.markdown(
        f"""
        <div class="metric-card">
          <div class="metric-label">{label}</div>
          <div class="metric-value">{value}</div>
          {hint_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def dashboard_updated_at() -> str:
    watched_files = [DATA_PATH, BASE_DIR / "dashboard.py", BASE_DIR / "charts.py", BASE_DIR / "utils.py"]
    last_modified = max(path.stat().st_mtime for path in watched_files if path.exists())
    return datetime.fromtimestamp(last_modified).strftime("%d/%m/%Y %H:%M:%S")


def build_sidebar(df: pd.DataFrame) -> tuple[list[str], list[str], list[str], list[str], str, list[str], list[str]]:
    with st.sidebar:
        st.header("Filtros")

        deputado_col = "DEPUTADO_PADRONIZADO" if "DEPUTADO_PADRONIZADO" in df.columns else "DEPUTADO"
        credor_col = "CREDOR_PADRONIZADO" if "CREDOR_PADRONIZADO" in df.columns else "CREDOR"

        deputados = sorted(df[deputado_col].dropna().unique())
        meses = (
            df[["MES_ANO", "MES_NUMERO"]]
            .drop_duplicates()
            .sort_values("MES_NUMERO")["MES_ANO"]
            .tolist()
        )
        credores = sorted(df[credor_col].dropna().unique())
        movimentos = sorted(df["TIPO_MOVIMENTO"].dropna().unique())
        categorias = sorted(df["CATEGORIA_DESPESA"].dropna().unique()) if "CATEGORIA_DESPESA" in df.columns else []
        categorias_anulacao = (
            sorted(df.loc[df["VALOR"] < 0, "CATEGORIA_ANULACAO"].dropna().unique())
            if "CATEGORIA_ANULACAO" in df.columns
            else []
        )

        selected_deputados = st.multiselect("Deputado", deputados, placeholder="Todos")
        selected_meses = st.multiselect("Mês/Ano", meses, placeholder="Todos")
        selected_credores = st.multiselect("Credor", credores, placeholder="Todos")
        selected_categorias = st.multiselect("Categoria da despesa", categorias, placeholder="Todas")
        selected_movimentos = st.multiselect("Tipo de movimento", movimentos, placeholder="Todos")
        selected_categorias_anulacao = st.multiselect("Motivo da anulação", categorias_anulacao, placeholder="Todos")
        texto = st.text_input("Busca livre", placeholder="Descrição, empenho, credor ou deputado")

        st.divider()
        st.caption("Filtros vazios mostram a base completa.")

    return (
        selected_deputados,
        selected_meses,
        selected_credores,
        selected_movimentos,
        texto,
        selected_categorias,
        selected_categorias_anulacao,
    )


def apply_style() -> None:
    st.markdown(
        """
        <style>
        :root {
            --alece-green: #46794A;
            --alece-green-dark: #2F5634;
            --alece-gold: #CDA85B;
            --alece-ink: #212529;
            --alece-muted: #6C757D;
            --alece-line: #DEE2E6;
            --alece-bg: #F8FAFC;
        }
        .block-container {
            padding-top: 1.1rem;
            padding-bottom: 2rem;
            max-width: 1320px;
        }
        [data-testid="stAppViewContainer"] {
            background: var(--alece-bg);
        }
        [data-testid="stSidebar"] {
            background: #FFFFFF;
            border-right: 1px solid var(--alece-line);
        }
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3 {
            color: var(--alece-green-dark);
        }
        .alece-header {
            background: linear-gradient(90deg, var(--alece-green-dark), var(--alece-green));
            border-bottom: 4px solid var(--alece-gold);
            padding: 18px 22px;
            margin-bottom: 18px;
            min-height: 116px;
            display: flex;
            align-items: center;
            gap: 28px;
        }
        .alece-header-text {
            color: #FFFFFF;
            font-weight: 700;
            letter-spacing: 0;
            margin: 0;
        }
        .alece-kicker {
            color: #F3E7C5;
            font-size: 0.78rem;
            font-weight: 700;
            margin-bottom: 0.3rem;
            text-transform: uppercase;
        }
        .main-title {
            color: #FFFFFF;
            font-size: 1.7rem;
            font-weight: 800;
            line-height: 1.12;
            margin-bottom: 0.25rem;
        }
        .subtitle {
            color: #EEF6EF;
            font-size: 0.98rem;
            margin-bottom: 0;
        }
        .metric-card {
            background: #FFFFFF;
            border: 1px solid var(--alece-line);
            border-left: 4px solid var(--alece-green);
            border-radius: 8px;
            padding: 14px 15px;
            min-height: 94px;
        }
        .metric-label {
            color: var(--alece-muted);
            font-size: 0.78rem;
            margin-bottom: 0.35rem;
            text-transform: uppercase;
        }
        .metric-value {
            color: var(--alece-ink);
            font-size: 1.28rem;
            font-weight: 800;
            overflow-wrap: anywhere;
        }
        .metric-hint {
            color: var(--alece-muted);
            font-size: 0.76rem;
            margin-top: 0.2rem;
        }
        .info-panel {
            background: #FFFFFF;
            border: 1px solid var(--alece-line);
            border-left: 4px solid var(--alece-gold);
            border-radius: 8px;
            padding: 16px 18px;
            margin-bottom: 18px;
        }
        .info-panel h3 {
            color: var(--alece-green-dark);
            font-size: 1.05rem;
            margin: 0 0 0.45rem 0;
        }
        .info-panel p {
            color: var(--alece-ink);
            margin: 0 0 0.45rem 0;
            line-height: 1.45;
        }
        .info-panel a {
            color: var(--alece-green-dark);
            font-weight: 700;
            text-decoration: underline;
        }
        .section-title {
            color: var(--alece-green-dark);
            font-size: 1.15rem;
            font-weight: 750;
            margin-top: 1rem;
            margin-bottom: 0.35rem;
        }
        .stTabs [data-baseweb="tab-list"] {
            gap: 4px;
            border-bottom: 1px solid var(--alece-line);
        }
        .stTabs [data-baseweb="tab"] {
            color: var(--alece-ink);
            font-weight: 600;
        }
        .stTabs [aria-selected="true"] {
            color: var(--alece-green-dark);
            border-bottom-color: var(--alece-green);
        }
        div[data-testid="stDownloadButton"] button {
            background: var(--alece-green);
            color: #FFFFFF;
            border: 1px solid var(--alece-green);
            border-radius: 6px;
        }
        div[data-testid="stDownloadButton"] button:hover {
            background: var(--alece-green-dark);
            border-color: var(--alece-green-dark);
            color: #FFFFFF;
        }
        .source-block {
            color: var(--alece-ink);
            font-size: 0.9rem;
            line-height: 1.55;
            margin-top: 1.2rem;
            margin-bottom: 1.4rem;
        }
        .source-block a {
            color: var(--alece-green-dark);
            font-weight: 700;
            text-decoration: underline;
        }
        .alece-footer {
            background: var(--alece-green);
            color: #FFFFFF;
            margin-top: 1.5rem;
            padding: 18px 22px;
            display: grid;
            grid-template-columns: 1fr 1.4fr;
            gap: 16px;
            align-items: center;
            border-top: 4px solid var(--alece-gold);
        }
        .alece-footer strong {
            display: block;
            font-weight: 800;
            margin-bottom: 0.35rem;
        }
        .alece-footer a {
            color: #FFFFFF;
            font-weight: 800;
            text-decoration: underline;
        }
        .alece-footer-right {
            text-align: center;
            line-height: 1.5;
        }
        @media (max-width: 760px) {
            .alece-header {
                align-items: flex-start;
                flex-direction: column;
                gap: 12px;
                padding: 16px;
            }
            .main-title {
                font-size: 1.35rem;
            }
            .subtitle {
                font-size: 0.88rem;
            }
            .alece-footer {
                grid-template-columns: 1fr;
            }
            .alece-footer-right {
                text-align: left;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_header() -> None:
    logo_data = base64.b64encode(LOGO_PATH.read_bytes()).decode("ascii")
    st.markdown(
        f"""
        <div class="alece-header">
            <img src="data:image/png;base64,{logo_data}" alt="ALECE" style="width: min(380px, 38vw); height: auto;" />
            <div>
                <div class="alece-kicker">Ferramenta institucional de transparência</div>
                <div class="main-title">Painel da Verba de Desempenho Parlamentar</div>
                <div class="subtitle">Exercício 2025</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_vdp_context() -> None:
    st.markdown(
        f"""
        <div class="info-panel">
            <h3>O que é a Verba de Desempenho Parlamentar?</h3>
            <p>
                A Verba de Desempenho Parlamentar (VDP) é uma verba mensal destinada às despesas de custeio
                dos gabinetes dos Deputados Estaduais, para viabilizar o exercício do mandato parlamentar.
            </p>
            <p>
                Na ALECE, a VDP é disciplinada pelos seguintes normativos:
                <a href="{Ato_URL}" target="_blank">Ato Deliberativo nº 929, de 14 de março de 2023</a>,
                <a href="{RESOLUCAO_URL}" target="_blank">Resolução nº 762, de 21 de dezembro de 2023</a>
                e <a href="{ATO_NORMATIVO_URL}" target="_blank">Ato Normativo nº 343, de 05 de fevereiro de 2024</a>.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_footer() -> None:
    st.markdown(
        f"""
        <div class="source-block">
            <strong>Fonte:</strong><br>
            <a href="{SOURCE_URL}" target="_blank">Portal da Transparência da ALECE - Verba de Desempenho Parlamentar</a><br>
            Sistema de Gestão Governamental por Resultados - S2GPR até 2021<br>
            Sistema Integrado de Planejamento e Administração Financeira do Estado do Ceará - SiafeCE a partir de 2022<br>
            <strong>Última atualização do dashboard:</strong> {dashboard_updated_at()}
        </div>
        <div class="alece-footer">
            <div>
                <strong>Assembleia Legislativa do Ceará</strong>
                31ª Legislatura<br>
                <a href="https://www.al.ce.gov.br/" target="_blank">MAPA DO SITE</a>
            </div>
            <div class="alece-footer-right">
                Av. Desembargador Moreira, 2807, Dionísio Torres<br>
                CEP: 60.170-900 - Fortaleza, CE<br>
                Fone: (85) 3277.2500 / segunda a sexta-feira, das 8h às 17h
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def main() -> None:
    st.set_page_config(page_title="VDP ALECE 2025", page_icon=str(LOGO_PATH), layout="wide")
    apply_style()

    df = get_data()
    (
        selected_deputados,
        selected_meses,
        selected_credores,
        selected_movimentos,
        texto,
        selected_categorias,
        selected_categorias_anulacao,
    ) = build_sidebar(df)
    filtered = apply_filters(
        df,
        selected_deputados,
        selected_meses,
        selected_credores,
        selected_movimentos,
        texto,
        selected_categorias,
        selected_categorias_anulacao,
    )

    total_apos_anulacoes = filtered["VALOR"].sum()
    total_empenhado = filtered.loc[filtered["VALOR"] > 0, "VALOR"].sum()
    total_anulacoes_abs = filtered.loc[filtered["VALOR"] < 0, "VALOR_ABSOLUTO"].sum()
    deputado_col = "DEPUTADO_PADRONIZADO" if "DEPUTADO_PADRONIZADO" in filtered.columns else "DEPUTADO"
    credor_col = "CREDOR_PADRONIZADO" if "CREDOR_PADRONIZADO" in filtered.columns else "CREDOR"
    qtd_deputados = filtered[deputado_col].nunique()
    qtd_credores = filtered[credor_col].nunique()
    qtd_registros = len(filtered)
    qtd_anulacoes = int((filtered["VALOR"] < 0).sum())
    taxa_anulacao = total_anulacoes_abs / total_empenhado if total_empenhado else 0

    render_header()
    render_vdp_context()

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        metric_card("Despesa após anulações", brl(total_apos_anulacoes), f"{qtd_registros:,}".replace(",", ".") + " registros")
    with col2:
        metric_card("Despesas empenhadas", brl(total_empenhado), "Antes das anulações")
    with col3:
        metric_card("Anulações", brl(total_anulacoes_abs), f"{qtd_anulacoes} registros | {pct(taxa_anulacao)}")
    with col4:
        metric_card("Deputados", str(qtd_deputados), "Com movimentação no recorte")
    with col5:
        metric_card("Credores", str(qtd_credores), "Fornecedores distintos")

    tab_overview, tab_categories, tab_rankings, tab_anulacoes, tab_base = st.tabs(
        ["Visão geral", "Categorias", "Rankings", "Anulações", "Base detalhada"]
    )

    with tab_overview:
        st.markdown('<div class="section-title">Evolução temporal</div>', unsafe_allow_html=True)
        st.plotly_chart(line_monthly(monthly_evolution(filtered)), use_container_width=True, key="chart_monthly_evolution")

        left, right = st.columns(2)
        with left:
            st.plotly_chart(
                pie_top(
                    top_for_chart(filtered, deputado_col, "Deputado"),
                    "Deputado",
                    "Valor",
                    "Top 10 maiores despesas por deputado",
                ),
                use_container_width=True,
                key="chart_pie_deputados",
            )
        with right:
            st.plotly_chart(
                pie_top(
                    top_for_chart(filtered, credor_col, "Credor"),
                    "Credor",
                    "Valor",
                    "Top 10 maiores despesas por credor",
                ),
                use_container_width=True,
                key="chart_pie_credores",
            )

    with tab_categories:
        st.markdown('<div class="section-title">Como o dinheiro foi gasto</div>', unsafe_allow_html=True)
        cat = category_summary(filtered)
        left, right = st.columns([1.2, 0.8])
        with left:
            st.plotly_chart(bar_categories(cat), use_container_width=True, key="chart_categories")
        with right:
            table = cat.rename(
                columns={
                    "CATEGORIA_DESPESA": "Categoria",
                    "REGISTROS": "Registros",
                    "VALOR": "Valor",
                }
            )
            if not table.empty:
                table["Valor"] = table["Valor"].apply(brl)
            st.dataframe(table, use_container_width=True, hide_index=True)

    with tab_rankings:
        left, right = st.columns(2)
        with left:
            st.plotly_chart(
                bar_top(top_for_chart(filtered, deputado_col, "Deputado"), "Valor", "Deputado", "Top 10 deputados"),
                use_container_width=True,
                key="chart_bar_deputados",
            )
        with right:
            st.plotly_chart(
                bar_top(top_for_chart(filtered, credor_col, "Credor"), "Valor", "Credor", "Top 10 credores"),
                use_container_width=True,
                key="chart_bar_credores",
            )

    with tab_anulacoes:
        anul = anulacoes_summary(filtered)
        anul_cat = cancellation_category_summary(filtered)
        left, right = st.columns([1.1, 0.9])
        with left:
            st.plotly_chart(bar_cancellation_categories(anul_cat), use_container_width=True, key="chart_cancellation_categories")
        with right:
            st.plotly_chart(bar_anulacoes(anul), use_container_width=True, key="chart_cancellation_types")
        st.markdown('<div class="section-title">Detalhamento das anulações</div>', unsafe_allow_html=True)
        a1, a2 = st.columns(2)
        with a1:
            table_cat = anul_cat.rename(
                columns={
                    "CATEGORIA_ANULACAO": "Motivo da anulação",
                    "REGISTROS": "Registros",
                    "VALOR_ABSOLUTO": "Valor absoluto",
                }
            )
            if not table_cat.empty:
                table_cat["Valor absoluto"] = table_cat["Valor absoluto"].apply(brl)
            st.dataframe(table_cat, use_container_width=True, hide_index=True)
        with a2:
            table = anul.rename(
                columns={
                    "TIPO_ANULACAO": "Tipo de anulação",
                    "REGISTROS": "Registros",
                    "VALOR_ABSOLUTO": "Valor absoluto",
                }
            )
            if not table.empty:
                table["Valor absoluto"] = table["Valor absoluto"].apply(brl)
            st.dataframe(table, use_container_width=True, hide_index=True)

    with tab_base:
        export_df = public_detail_base(filtered)
        export_named_df = prepare_public_columns(export_df)
        display_df = export_df.rename(
            columns={
                "DEPUTADO": "Deputado",
                "PERIODO": "Período",
                "MES_ANO": "Mês/Ano",
                "EMPENHO": "Empenho",
                "DESCRICAO": "Descrição",
                "CREDOR": "Credor",
                "VALOR": "Valor",
                "CATEGORIA_DESPESA": "Categoria da despesa",
                "CATEGORIA_ANULACAO": "Motivo da anulação",
                "TIPO_MOVIMENTO": "Tipo de movimento",
                "TIPO_ANULACAO": "Tipo de anulação",
            }
        )
        if "Valor" in display_df.columns:
            display_df["Valor"] = display_df["Valor"].apply(brl)
        st.dataframe(display_df, use_container_width=True, hide_index=True)

        excel_data = download_excel(export_named_df)
        st.download_button(
            "Baixar base detalhada em Excel",
            data=excel_data,
            file_name="base_vdp_alece_2025_filtrada.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )

    st.caption(
        "Valores negativos foram mantidos porque representam anulações administrativas. "
        "A despesa após anulações considera as despesas empenhadas menos as anulações."
    )
    render_footer()
    st.stop()
