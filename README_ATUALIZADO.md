# Dashboard VDP ALECE 2025

Dashboard interativo para analise da Verba de Desempenho Parlamentar da Assembleia Legislativa do Estado do Ceara (ALECE), com dados publicos do exercicio de 2025.

O painel foi ajustado para seguir a identidade visual institucional da ALECE e ir alem dos requisitos minimos da atividade, incluindo limpeza de dados, categorizacao das despesas e categorizacao das anulacoes.

## Dados

- Base original preservada: `data/base_vdp_alece_2025_tratada.csv`
- Base limpa usada pelo dashboard: `data/base_vdp_alece_2025_limpa.csv`

Resumo da base limpa:

- Registros: 4.219
- Deputados diferentes: 58
- Credores diferentes: 110
- Categorias de despesa: 11
- Categorias efetivas de anulacao: 3
- Despesa apos anulacoes preservada: R$ 19.893.422,35

## Como executar

Opcao simples no Windows:

1. De dois cliques em `iniciar_dashboard.bat`.
2. Aguarde a instalacao das bibliotecas.
3. Abra o endereco exibido no navegador, normalmente `http://localhost:8501`.

Opcao manual:

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Funcionalidades

- Filtros por deputado, mes/ano, credor, categoria da despesa, tipo de movimento e motivo da anulacao.
- Cards com despesa apos anulacoes, despesas empenhadas, anulacoes, deputados e credores.
- Evolucao mensal das despesas.
- Graficos de pizza Top 10 por deputado e por credor.
- Analise de despesas por categoria.
- Analise das anulacoes por motivo.
- Rankings em barras dos deputados e credores.
- Tabela detalhada com nome original e nome padronizado.
- Exportacao da base detalhada em Excel, com coluna de valor formatada como moeda.
- Tema visual com logomarca e cores da ALECE.
- Bloco explicativo sobre o conceito de VDP e normativos aplicáveis.
- Rodape institucional com fonte, sistemas de origem e ultima atualizacao do dashboard.

## Categorias de despesa

- Alimentacao e refeicao
- Combustiveis
- Consultoria e assessoria administrativa
- Consultoria e assessoria juridica
- Divulgacao das atividades parlamentares
- Impressos e servicos graficos
- Locacao de veiculos
- Outras despesas
- Passagens e hospedagem
- Seguro de vida
- Telefonia, internet e dados

## Categorias de anulacao

- Correcao administrativa
- Solicitacao parlamentar
- Motivo nao especificado

## Documentacao

Os principais documentos metodologicos estao em `docs/`:

- `relatorio_limpeza_base.md`
- `metodologia_categorizacao_despesas.md`
- `tema_visual_alece.md`
- `cruzamento_deputados_lista_oficial_alece.md`
- `verificacao_suplentes_deputados.md`

Os valores negativos foram mantidos por representarem anulacoes administrativas. A classificacao preserva a integridade contabil e facilita a leitura publica da despesa apos anulacoes.
