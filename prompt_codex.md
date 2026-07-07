
# Prompt sugerido para o Codex

Você está trabalhando em um projeto Streamlit chamado `dashboard-vdp-alece`.

Objetivo: criar e aperfeiçoar um dashboard interativo sobre a Verba de Desempenho Parlamentar da ALECE em 2025, usando a base `data/base_vdp_alece_2025_tratada.csv`.

Requisitos mínimos do trabalho:
1. Filtro por deputado.
2. Filtro por mês/ano.
3. Filtro por credor.
4. Gráfico de pizza Top 10 despesas por deputado.
5. Gráfico de pizza Top 10 despesas por credor.
6. Gráfico de evolução mensal das despesas.
7. Visualização específica das anulações por categoria.

Diretrizes:
- Preservar os registros negativos, pois representam anulações.
- Usar o campo `VALOR` para análises líquidas.
- Usar `VALOR_ABSOLUTO` para análises específicas de anulações.
- Usar `MES_NUMERO` para ordenar meses corretamente.
- Manter linguagem em português do Brasil.
- Manter layout executivo, limpo e institucional.
- Priorizar clareza, filtros simples e gráficos interativos.
