
from __future__ import annotations

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


TEMPLATE = "plotly_white"
ALECE_GREEN = "#46794A"
ALECE_GREEN_DARK = "#2F5634"
ALECE_GOLD = "#CDA85B"
ALECE_TEAL = "#2C8C7A"
ALECE_RED = "#B85C4B"
ALECE_INK = "#212529"
COLOR_DISCRETE = [ALECE_GREEN, ALECE_GOLD, ALECE_TEAL, ALECE_RED, "#6C757D", ALECE_GREEN_DARK]


def brl_label(value: float) -> str:
    formatted = f"R$ {value:,.2f}"
    return formatted.replace(",", "X").replace(".", ",").replace("X", ".")


def add_brl_column(df: pd.DataFrame, value_col: str, label_col: str = "VALOR_FORMATADO") -> pd.DataFrame:
    out = df.copy()
    if value_col in out.columns:
        out[label_col] = out[value_col].apply(brl_label)
    return out


def empty_figure(message: str = "Sem dados para o recorte selecionado") -> go.Figure:
    fig = go.Figure()
    fig.add_annotation(
        text=message,
        x=0.5,
        y=0.5,
        xref="paper",
        yref="paper",
        showarrow=False,
        font={"size": 16, "color": "#57606A"},
    )
    fig.update_layout(template=TEMPLATE, height=360, xaxis_visible=False, yaxis_visible=False)
    return fig


def line_monthly(df: pd.DataFrame) -> go.Figure:
    fig = px.line(
        df,
        x="MES_ANO",
        y="VALOR",
        markers=True,
        title="Evolução mensal da despesa após anulações",
        labels={"MES_ANO": "Mês/Ano", "VALOR": "Despesa após anulações (R$)"},
        template=TEMPLATE,
    )
    fig.update_traces(line_width=3)
    fig.update_layout(hovermode="x unified", title_x=0.02)
    return fig


def pie_top(df: pd.DataFrame, names_col: str, values_col: str, title: str) -> go.Figure:
    fig = px.pie(
        df,
        names=names_col,
        values=values_col,
        title=title,
        hole=0.35,
        template=TEMPLATE,
    )
    fig.update_traces(textposition="inside", textinfo="percent+label")
    fig.update_layout(title_x=0.02, legend_title_text="")
    return fig


def bar_top(df: pd.DataFrame, x_col: str, y_col: str, title: str) -> go.Figure:
    df_plot = df.sort_values(x_col, ascending=True)
    fig = px.bar(
        df_plot,
        x=x_col,
        y=y_col,
        orientation="h",
        title=title,
        labels={x_col: "Valor (R$)", y_col: ""},
        template=TEMPLATE,
    )
    fig.update_layout(title_x=0.02, yaxis={"categoryorder": "total ascending"})
    return fig


def bar_anulacoes(df: pd.DataFrame) -> go.Figure:
    fig = px.bar(
        df,
        x="TIPO_ANULACAO",
        y="REGISTROS",
        title="Anulações por categoria",
        labels={"TIPO_ANULACAO": "Tipo de anulação", "REGISTROS": "Quantidade de registros"},
        text="REGISTROS",
        template=TEMPLATE,
    )
    fig.update_traces(textposition="outside")
    fig.update_layout(title_x=0.02)
    return fig


def line_monthly(df: pd.DataFrame) -> go.Figure:
    if df.empty:
        return empty_figure()

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=df["MES_ANO"],
            y=df["DESPESAS_BRUTAS"],
            mode="lines+markers",
            name="Despesas empenhadas",
            line={"width": 3, "color": ALECE_GREEN_DARK},
        )
    )
    fig.add_trace(
        go.Scatter(
            x=df["MES_ANO"],
            y=df["VALOR"],
            mode="lines+markers",
            name="Despesa após anulações",
            line={"width": 3, "color": ALECE_GREEN},
        )
    )
    fig.add_trace(
        go.Bar(
            x=df["MES_ANO"],
            y=df["ANULACOES"],
            name="Anulações",
            marker_color=ALECE_GOLD,
            opacity=0.72,
        )
    )
    fig.update_layout(
        template=TEMPLATE,
        title="Evolução mensal",
        title_x=0.02,
        hovermode="x unified",
        separators=",.",
        yaxis_title="Valor (R$)",
        xaxis_title="Mês/Ano",
        legend_title_text="",
        font={"color": ALECE_INK},
    )
    return fig


def pie_top(df: pd.DataFrame, names_col: str, values_col: str, title: str) -> go.Figure:
    if df.empty:
        return empty_figure()

    fig = px.pie(
        df,
        names=names_col,
        values=values_col,
        title=title,
        hole=0.35,
        template=TEMPLATE,
        color_discrete_sequence=COLOR_DISCRETE,
    )
    fig.update_traces(textposition="inside", textinfo="percent")
    fig.update_layout(title_x=0.02, legend_title_text="", separators=",.")
    return fig


def bar_top(df: pd.DataFrame, x_col: str, y_col: str, title: str) -> go.Figure:
    if df.empty:
        return empty_figure()

    df_plot = df.sort_values(x_col, ascending=True)
    fig = px.bar(
        df_plot,
        x=x_col,
        y=y_col,
        orientation="h",
        title=title,
        labels={x_col: "Valor (R$)", y_col: ""},
        template=TEMPLATE,
        color=x_col,
        color_continuous_scale=["#DDE9DD", ALECE_GREEN_DARK],
    )
    fig.update_layout(title_x=0.02, yaxis={"categoryorder": "total ascending"}, coloraxis_showscale=False, separators=",.")
    return fig


def bar_anulacoes(df: pd.DataFrame) -> go.Figure:
    if df.empty:
        return empty_figure("Nenhuma anulação no recorte selecionado")

    fig = px.bar(
        df,
        x="TIPO_ANULACAO",
        y="REGISTROS",
        title="Anulações por categoria",
        labels={"TIPO_ANULACAO": "Tipo de anulação", "REGISTROS": "Quantidade de registros"},
        text="REGISTROS",
        template=TEMPLATE,
        color="VALOR_ABSOLUTO",
        color_continuous_scale=["#F3E7C5", ALECE_RED],
    )
    fig.update_traces(textposition="outside")
    fig.update_layout(title_x=0.02, coloraxis_colorbar_title="Valor", separators=",.")
    return fig


def bar_categories(df: pd.DataFrame) -> go.Figure:
    if df.empty:
        return empty_figure()

    df_plot = df.sort_values("VALOR", ascending=True)
    fig = px.bar(
        df_plot,
        x="VALOR",
        y="CATEGORIA_DESPESA",
        orientation="h",
        title="Despesas por categoria",
        labels={"VALOR": "Valor (R$)", "CATEGORIA_DESPESA": ""},
        template=TEMPLATE,
        color="VALOR",
        color_continuous_scale=["#DDE9DD", ALECE_GREEN_DARK],
    )
    fig.update_layout(title_x=0.02, coloraxis_showscale=False, separators=",.")
    return fig


def bar_cancellation_categories(df: pd.DataFrame) -> go.Figure:
    if df.empty:
        return empty_figure("Nenhuma anulação no recorte selecionado")

    df_plot = df.sort_values("VALOR_ABSOLUTO", ascending=True)
    fig = px.bar(
        df_plot,
        x="VALOR_ABSOLUTO",
        y="CATEGORIA_ANULACAO",
        orientation="h",
        title="Anulações por motivo",
        labels={"VALOR_ABSOLUTO": "Valor absoluto (R$)", "CATEGORIA_ANULACAO": ""},
        template=TEMPLATE,
        color="VALOR_ABSOLUTO",
        color_continuous_scale=["#F3E7C5", ALECE_RED],
        text="REGISTROS",
    )
    fig.update_traces(texttemplate="%{text} reg.", textposition="outside")
    fig.update_layout(title_x=0.02, coloraxis_showscale=False, separators=",.")
    return fig


def line_monthly(df: pd.DataFrame) -> go.Figure:
    if df.empty:
        return empty_figure()

    df_plot = add_brl_column(df, "DESPESAS_BRUTAS", "DESPESAS_BRUTAS_FORMATADO")
    df_plot = add_brl_column(df_plot, "VALOR", "VALOR_FORMATADO")
    df_plot = add_brl_column(df_plot, "ANULACOES", "ANULACOES_FORMATADO")

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=df_plot["MES_ANO"],
            y=df_plot["DESPESAS_BRUTAS"],
            customdata=df_plot["DESPESAS_BRUTAS_FORMATADO"],
            mode="lines+markers",
            name="Despesas empenhadas",
            line={"width": 3, "color": ALECE_GREEN_DARK},
            hovertemplate="%{x}<br>Despesas empenhadas: %{customdata}<extra></extra>",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=df_plot["MES_ANO"],
            y=df_plot["VALOR"],
            customdata=df_plot["VALOR_FORMATADO"],
            mode="lines+markers",
            name="Despesa após anulações",
            line={"width": 3, "color": ALECE_GREEN},
            hovertemplate="%{x}<br>Despesa após anulações: %{customdata}<extra></extra>",
        )
    )
    fig.add_trace(
        go.Bar(
            x=df_plot["MES_ANO"],
            y=df_plot["ANULACOES"],
            customdata=df_plot["ANULACOES_FORMATADO"],
            name="Anulações",
            marker_color=ALECE_GOLD,
            opacity=0.72,
            hovertemplate="%{x}<br>Anulações: %{customdata}<extra></extra>",
        )
    )
    fig.update_layout(
        template=TEMPLATE,
        title="Evolução mensal",
        title_x=0.02,
        hovermode="x unified",
        yaxis_title="Valor (R$)",
        xaxis_title="Mês/Ano",
        legend_title_text="",
        font={"color": ALECE_INK},
    )
    return fig


def pie_top(df: pd.DataFrame, names_col: str, values_col: str, title: str) -> go.Figure:
    if df.empty:
        return empty_figure()

    df_plot = add_brl_column(df, values_col)
    fig = px.pie(
        df_plot,
        names=names_col,
        values=values_col,
        title=title,
        hole=0.35,
        template=TEMPLATE,
        color_discrete_sequence=COLOR_DISCRETE,
        custom_data=["VALOR_FORMATADO"],
    )
    fig.update_traces(
        textposition="inside",
        textinfo="percent",
        hovertemplate="%{label}<br>Valor: %{customdata[0]}<br>Participação: %{percent}<extra></extra>",
    )
    fig.update_layout(title_x=0.02, legend_title_text="")
    return fig


def bar_top(df: pd.DataFrame, x_col: str, y_col: str, title: str) -> go.Figure:
    if df.empty:
        return empty_figure()

    df_plot = add_brl_column(df.sort_values(x_col, ascending=True), x_col)
    fig = px.bar(
        df_plot,
        x=x_col,
        y=y_col,
        orientation="h",
        title=title,
        labels={x_col: "Valor (R$)", y_col: ""},
        template=TEMPLATE,
        color=x_col,
        color_continuous_scale=["#DDE9DD", ALECE_GREEN_DARK],
        custom_data=["VALOR_FORMATADO"],
    )
    fig.update_traces(hovertemplate="%{y}<br>Valor: %{customdata[0]}<extra></extra>")
    fig.update_layout(title_x=0.02, yaxis={"categoryorder": "total ascending"}, coloraxis_showscale=False)
    return fig


def bar_anulacoes(df: pd.DataFrame) -> go.Figure:
    if df.empty:
        return empty_figure("Nenhuma anulação no recorte selecionado")

    df_plot = add_brl_column(df, "VALOR_ABSOLUTO")
    fig = px.bar(
        df_plot,
        x="TIPO_ANULACAO",
        y="REGISTROS",
        title="Anulações por categoria",
        labels={"TIPO_ANULACAO": "Tipo de anulação", "REGISTROS": "Quantidade de registros"},
        text="REGISTROS",
        template=TEMPLATE,
        color="VALOR_ABSOLUTO",
        color_continuous_scale=["#F3E7C5", ALECE_RED],
        custom_data=["VALOR_FORMATADO"],
    )
    fig.update_traces(
        textposition="outside",
        hovertemplate="%{x}<br>Registros: %{y}<br>Valor: %{customdata[0]}<extra></extra>",
    )
    fig.update_layout(title_x=0.02, coloraxis_colorbar_title="Valor")
    return fig


def bar_categories(df: pd.DataFrame) -> go.Figure:
    if df.empty:
        return empty_figure()

    df_plot = add_brl_column(df.sort_values("VALOR", ascending=True), "VALOR")
    fig = px.bar(
        df_plot,
        x="VALOR",
        y="CATEGORIA_DESPESA",
        orientation="h",
        title="Despesas por categoria",
        labels={"VALOR": "Valor (R$)", "CATEGORIA_DESPESA": ""},
        template=TEMPLATE,
        color="VALOR",
        color_continuous_scale=["#DDE9DD", ALECE_GREEN_DARK],
        custom_data=["VALOR_FORMATADO"],
    )
    fig.update_traces(hovertemplate="%{y}<br>Valor: %{customdata[0]}<extra></extra>")
    fig.update_layout(title_x=0.02, coloraxis_showscale=False)
    return fig


def bar_cancellation_categories(df: pd.DataFrame) -> go.Figure:
    if df.empty:
        return empty_figure("Nenhuma anulação no recorte selecionado")

    df_plot = add_brl_column(df.sort_values("VALOR_ABSOLUTO", ascending=True), "VALOR_ABSOLUTO")
    fig = px.bar(
        df_plot,
        x="VALOR_ABSOLUTO",
        y="CATEGORIA_ANULACAO",
        orientation="h",
        title="Anulações por motivo",
        labels={"VALOR_ABSOLUTO": "Valor absoluto (R$)", "CATEGORIA_ANULACAO": ""},
        template=TEMPLATE,
        color="VALOR_ABSOLUTO",
        color_continuous_scale=["#F3E7C5", ALECE_RED],
        text="REGISTROS",
        custom_data=["VALOR_FORMATADO"],
    )
    fig.update_traces(
        texttemplate="%{text} reg.",
        textposition="outside",
        hovertemplate="%{y}<br>Valor: %{customdata[0]}<br>Registros: %{text}<extra></extra>",
    )
    fig.update_layout(title_x=0.02, coloraxis_showscale=False)
    return fig
