
from __future__ import annotations

import csv
from pathlib import Path

import pandas as pd


MONTH_ORDER = {
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
    "Dezembro": 12,
}

DEPUTADO_CORRECTIONS = {
    "DEP ALCIDERS FERNANDES": "DEP ALCIDES FERNANDES",
    "DEP ALMIIR BIE": "DEP ALMIR BIE",
    "DEP ALMIR B": "DEP ALMIR BIE",
    "DEP ALYSSON AGUYIAR": "DEP ALYSSON AGUIAR",
    "DEP EMIILA PESSOA": "DEP EMILIA PESSOA",
    "DEP EMILA PESSOA": "DEP EMILIA PESSOA",
    "DEP FIRMO CAMUCA": "DEP FIRMO CAMURCA",
    "DEP GUILHERME BISMARK": "DEP GUILHERME BISMARCK",
    "DEP MISSISAS DIAS": "DEP MISSIAS DIAS",
    "DEP NIZO COSTA.": "DEP NIZO COSTA",
    "DEP SERGIO AGUIAR.": "DEP SERGIO AGUIAR",
    "DEP SERGIO AHUIAR": "DEP SERGIO AGUIAR",
    "DEP CARMELO NETO": "DEP CARMELO BOLSONARO",
}

CREDOR_CORRECTIONS = {
    "RONNY FELICIO SOCIEDADE INDIV.DE ADVOGACIA": "RONNY FELICIO SOCIEDADE INDIV. DE ADVOCACIA",
    "GP  SERVICOS ADMINISTRATIVOS LT": "GP SERVICOS ADMINISTRATIVOS LT",
    "GLOBAL EMPREENDIMENTOS E SERV.LT": "GLOBAL EMPREENDIMENTOS E SERV. LT",
    "EMPRESA BRAS DE CORREIOS E TELEGRAFOS": "EMPRESA BRASILEIRA DE CORREIOS E TELEGRAFOS",
    "Guilherme Sampaio Landim": "GUILHERME SAMPAIO LANDIM",
    "Simao Pedro Alves Pequeno": "SIMAO PEDRO ALVES PEQUENO",
    "P R  M COMUNICACAO": "P R M COMUNICACAO",
    "ALCIMOR  SILVEIRA FIGUEIREDO SA  BRAGA ADVOGADOS": "ALCIMOR SILVEIRA FIGUEIREDO SA BRAGA ADVOGADOS",
    "BARBOSA  MORAES SOCIEDADE DE ADVOGADOS": "BARBOSA MORAES SOCIEDADE DE ADVOGADOS",
    "BGQS MORAIS  RS NOG  E T DA S FER LTDA": "BGQS MORAIS RS NOG E T DA S FER LTDA",
    "CARMELO SILVEIRA  CARNEIRO LEAO NETO": "CARMELO SILVEIRA CARNEIRO LEAO NETO",
    "VICTOR SILVA TORRES SOC.IND.DE ADV": "VICTOR SILVA TORRES SOC. IND. DE ADV.",
    "TIM S A": "TIM S.A.",
    "TICKET SERVICOS S/A": "TICKET SERVICOS S.A.",
    "TICKET SOLUCOES HDFGT S/A": "TICKET SOLUCOES HDFGT S.A.",
    "WALDIR XAVIER E ADVOGADOS ASSOCIADOS S/C": "WALDIR XAVIER E ADVOGADOS ASSOCIADOS S.C.",
    "JOSE FIRMO AGUIAR NETO": "JOSE FIRMO DE CAMURCA NETO",
}

EXPENSE_CATEGORY_RULES = [
    ("Divulgação das atividades parlamentares", ["DIVULGACAO", "COMUNICACAO", "MARKETING", "CONTEUDOS"]),
    ("Alimentação e refeição", ["ALIMENTACAO", "REFEICAO"]),
    ("Combustíveis", ["COMBUSTIVEIS", "ABASTECIMENTO"]),
    ("Consultoria e assessoria jurídica", ["JURIDICA", "ADVOCACIA", "ADVOGADOS"]),
    ("Consultoria e assessoria administrativa", ["CONSULTORIA", "ASSESSORIA", "CONTABIL", "TRIBUTARIO", "PLANEJAMENTO"]),
    ("Telefonia, internet e dados", ["TELEFONIA", "INTERNET", "DADOS", "TELEFONICA", "TIM"]),
    ("Locação de veículos", ["LOCACAO", "LOCACOES", "VEICULO", "VEICULOS", "HILUX", "S10", "ARGO", "POLO"]),
    ("Impressos e serviços gráficos", ["GRAFICA", "GRAFICAS", "IMPRESSOES", "EDITORA", "PRINT"]),
    ("Passagens e hospedagem", ["PASSAGEM", "AEREA", "HOSPEDAGEM"]),
    ("Seguro de vida", ["SEGURO DE VIDA"]),
]


def categorize_expense(description: str) -> str:
    text = str(description).upper()
    for category, keywords in EXPENSE_CATEGORY_RULES:
        if any(keyword in text for keyword in keywords):
            return category
    return "Outras despesas"


def categorize_cancellation(row: pd.Series) -> str:
    description = str(row.get("DESCRICAO", "")).upper()
    if row.get("VALOR", 0) >= 0:
        return "Não se aplica"
    if "SOLICITACAO DO DEPUTADO" in description or "SOLICITACAO DA DEPUTADA" in description:
        return "Solicitação parlamentar"
    if (
        "CORRECAO" in description
        or "ACERTO" in description
        or "AJUSTE" in description
        or "INCLUIR" in description
        or "ANULACAO PARCIAL" in description
    ):
        return "Correção administrativa"
    return "Motivo não especificado"


def _read_csv(path: str) -> pd.DataFrame:
    """Read the dataset, including exports with each row wrapped in quotes."""
    csv_path = Path(path)
    raw_lines = csv_path.read_text(encoding="utf-8-sig").splitlines()
    if not raw_lines:
        return pd.DataFrame()

    has_wrapped_rows = len(raw_lines) > 1 and raw_lines[1].strip().startswith('"') and raw_lines[1].strip().endswith('"')
    if not has_wrapped_rows:
        return pd.read_csv(csv_path, sep=None, engine="python", encoding="utf-8-sig")

    header = next(csv.reader([raw_lines[0]]))
    cleaned_rows = []
    for line in raw_lines[1:]:
        if not line.strip():
            continue
        cleaned = line.strip()
        if cleaned.startswith('"') and cleaned.endswith('"'):
            cleaned = cleaned[1:-1].replace('""', '"')
        cleaned_rows.append(next(csv.reader([cleaned])))

    return pd.DataFrame(cleaned_rows, columns=header)


def load_data(path: str) -> pd.DataFrame:
    """Load and normalize the treated VDP dataset."""
    df = _read_csv(path)

    # Defensive cleanup in case columns arrive with extra spaces.
    df.columns = [c.strip().upper() for c in df.columns]

    # Coerce numeric columns.
    for col in ["VALOR", "VALOR_ABSOLUTO", "MES_NUMERO", "ANO"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    if "MES" not in df.columns and "MES_NOME" in df.columns:
        df["MES"] = df["MES_NOME"]

    if "PERIODO" not in df.columns and "PERIODO_ORIGINAL" in df.columns:
        df["PERIODO"] = df["PERIODO_ORIGINAL"]

    # Ensure category columns exist.
    if "TIPO_MOVIMENTO" not in df.columns and "VALOR" in df.columns:
        df["TIPO_MOVIMENTO"] = df["VALOR"].apply(lambda x: "Anulação" if x < 0 else "Despesa")

    if "VALOR_ABSOLUTO" not in df.columns and "VALOR" in df.columns:
        df["VALOR_ABSOLUTO"] = df["VALOR"].abs()

    if "TIPO_ANULACAO" not in df.columns:
        df["TIPO_ANULACAO"] = "Não se aplica"

    # Ensure correct temporal ordering.
    if "MES_NUMERO" not in df.columns and "MES" in df.columns:
        df["MES_NUMERO"] = df["MES"].map(MONTH_ORDER)

    if "MES_ANO" not in df.columns and {"MES", "ANO"}.issubset(df.columns):
        df["MES_ANO"] = df["MES"].astype(str) + "/" + df["ANO"].astype(str)

    for col in ["DEPUTADO", "CREDOR", "DESCRICAO", "TIPO_MOVIMENTO", "TIPO_ANULACAO"]:
        if col in df.columns:
            df[col] = df[col].fillna("Não informado").astype(str).str.strip()

    if "DEPUTADO" in df.columns:
        df["DEPUTADO_PADRONIZADO"] = df["DEPUTADO"].replace(DEPUTADO_CORRECTIONS)

    if "CREDOR" in df.columns:
        df["CREDOR_PADRONIZADO"] = df["CREDOR"].replace(CREDOR_CORRECTIONS)

    if "DESCRICAO" in df.columns:
        df["CATEGORIA_DESPESA"] = df["DESCRICAO"].apply(categorize_expense)
        df["CATEGORIA_ANULACAO"] = df.apply(categorize_cancellation, axis=1)

    return df


def brl(value: float) -> str:
    """Format number as Brazilian Real."""
    if pd.isna(value):
        return "R$ 0,00"
    formatted = f"R$ {value:,.2f}"
    return formatted.replace(",", "X").replace(".", ",").replace("X", ".")


def pct(value: float) -> str:
    if pd.isna(value):
        return "0,0%"
    return f"{value:.1%}".replace(".", ",")


def apply_filters(
    df: pd.DataFrame,
    deputados: list[str] | None,
    meses: list[str] | None,
    credores: list[str] | None,
    tipos_movimento: list[str] | None = None,
    texto: str | None = None,
    categorias: list[str] | None = None,
    categorias_anulacao: list[str] | None = None,
) -> pd.DataFrame:
    filtered = df.copy()
    deputado_col = "DEPUTADO_PADRONIZADO" if "DEPUTADO_PADRONIZADO" in filtered.columns else "DEPUTADO"
    credor_col = "CREDOR_PADRONIZADO" if "CREDOR_PADRONIZADO" in filtered.columns else "CREDOR"

    if deputados:
        filtered = filtered[filtered[deputado_col].isin(deputados)]

    if meses:
        filtered = filtered[filtered["MES_ANO"].isin(meses)]

    if credores:
        filtered = filtered[filtered[credor_col].isin(credores)]

    if tipos_movimento and "TIPO_MOVIMENTO" in filtered.columns:
        filtered = filtered[filtered["TIPO_MOVIMENTO"].isin(tipos_movimento)]

    if categorias and "CATEGORIA_DESPESA" in filtered.columns:
        filtered = filtered[filtered["CATEGORIA_DESPESA"].isin(categorias)]

    if categorias_anulacao and "CATEGORIA_ANULACAO" in filtered.columns:
        filtered = filtered[filtered["CATEGORIA_ANULACAO"].isin(categorias_anulacao)]

    if texto:
        termo = texto.strip().casefold()
        if termo:
            searchable = ["DEPUTADO_PADRONIZADO", "CREDOR_PADRONIZADO", "DEPUTADO", "CREDOR", "DESCRICAO", "EMPENHO"]
            mask = pd.Series(False, index=filtered.index)
            for col in searchable:
                if col in filtered.columns:
                    mask = mask | filtered[col].astype(str).str.casefold().str.contains(termo, na=False)
            filtered = filtered[mask]

    return filtered


def top_n(
    df: pd.DataFrame,
    group_col: str,
    value_col: str = "VALOR",
    n: int = 10,
    positive_only: bool = False,
) -> pd.DataFrame:
    data = df[df[value_col] > 0] if positive_only else df
    if data.empty or group_col not in data.columns:
        return pd.DataFrame(columns=[group_col, value_col])

    return (
        data.groupby(group_col, as_index=False)[value_col]
        .sum()
        .sort_values(value_col, ascending=False)
        .head(n)
    )


def monthly_evolution(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame(columns=["MES_NUMERO", "MES", "MES_ANO", "VALOR", "DESPESAS_BRUTAS", "ANULACOES"])

    data = df.copy()
    data["DESPESAS_BRUTAS"] = data["VALOR"].clip(lower=0)
    data["ANULACOES"] = data["VALOR"].clip(upper=0).abs()
    return (
        data.groupby(["MES_NUMERO", "MES", "MES_ANO"], as_index=False)
        .agg(
            VALOR=("VALOR", "sum"),
            DESPESAS_BRUTAS=("DESPESAS_BRUTAS", "sum"),
            ANULACOES=("ANULACOES", "sum"),
        )
        .sort_values("MES_NUMERO")
    )


def anulacoes_summary(df: pd.DataFrame) -> pd.DataFrame:
    neg = df[df["VALOR"] < 0].copy()
    if neg.empty:
        return pd.DataFrame(columns=["TIPO_ANULACAO", "REGISTROS", "VALOR_ABSOLUTO"])
    return (
        neg.groupby("TIPO_ANULACAO", as_index=False)
        .agg(REGISTROS=("TIPO_ANULACAO", "size"), VALOR_ABSOLUTO=("VALOR_ABSOLUTO", "sum"))
        .sort_values("REGISTROS", ascending=False)
    )


def category_summary(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty or "CATEGORIA_DESPESA" not in df.columns:
        return pd.DataFrame(columns=["CATEGORIA_DESPESA", "REGISTROS", "VALOR"])
    data = df[df["VALOR"] > 0].copy()
    if data.empty:
        return pd.DataFrame(columns=["CATEGORIA_DESPESA", "REGISTROS", "VALOR"])
    return (
        data.groupby("CATEGORIA_DESPESA", as_index=False)
        .agg(REGISTROS=("CATEGORIA_DESPESA", "size"), VALOR=("VALOR", "sum"))
        .sort_values("VALOR", ascending=False)
    )


def cancellation_category_summary(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty or "CATEGORIA_ANULACAO" not in df.columns:
        return pd.DataFrame(columns=["CATEGORIA_ANULACAO", "REGISTROS", "VALOR_ABSOLUTO"])
    data = df[df["VALOR"] < 0].copy()
    if data.empty:
        return pd.DataFrame(columns=["CATEGORIA_ANULACAO", "REGISTROS", "VALOR_ABSOLUTO"])
    return (
        data.groupby("CATEGORIA_ANULACAO", as_index=False)
        .agg(REGISTROS=("CATEGORIA_ANULACAO", "size"), VALOR_ABSOLUTO=("VALOR_ABSOLUTO", "sum"))
        .sort_values("VALOR_ABSOLUTO", ascending=False)
    )
