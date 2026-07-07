
# Dashboard VDP ALECE 2025

Dashboard interativo para análise da **Verba de Desempenho Parlamentar da Assembleia Legislativa do Estado do Ceará (ALECE)**, com dados públicos de janeiro a dezembro de 2025.

## Tecnologias

- Python
- Streamlit
- Pandas
- Plotly

## Estrutura

```text
dashboard-vdp-alece/
├── app.py
├── charts.py
├── utils.py
├── requirements.txt
├── data/
│   └── base_vdp_alece_2025_tratada.csv
├── docs/
│   ├── dicionario_dados.md
│   └── prompt_codex.md
└── .streamlit/
    └── config.toml
```

## Como executar localmente

1. Criar ambiente virtual, se desejar:

```bash
python -m venv .venv
```

2. Ativar o ambiente virtual:

Windows:

```bash
.venv\Scripts\activate
```

Mac/Linux:

```bash
source .venv/bin/activate
```

3. Instalar dependências:

```bash
pip install -r requirements.txt
```

4. Rodar o dashboard:

```bash
streamlit run app.py
```

5. Abrir no navegador o endereço exibido no terminal.

## Funcionalidades

O painel inclui:

- filtros por deputado, mês/ano e credor;
- cards com valor líquido, despesas brutas, anulações, deputados e credores;
- evolução mensal das despesas;
- gráfico de pizza Top 10 despesas por deputado;
- gráfico de pizza Top 10 despesas por credor;
- rankings em barras dos deputados e credores;
- análise das anulações por categoria;
- tabela detalhada pesquisável;
- exportação da base filtrada em CSV e Excel.

## Observação metodológica

Os valores negativos foram mantidos na base, pois representam anulações administrativas. Foi criada uma classificação específica:

- Correções administrativas;
- Desistência;
- Motivo não especificado.

Essa decisão preserva a integridade contábil da base e permite analisar o valor líquido das despesas.
