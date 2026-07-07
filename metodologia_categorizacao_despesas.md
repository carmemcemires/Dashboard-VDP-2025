# Metodologia de categorizacao das despesas

Objetivo: tornar o painel mais compreensivel para o cidadao, agrupando descricoes longas de empenhos em categorias de leitura simples.

## Colunas criadas

No arquivo limpo `data/base_vdp_alece_2025_limpa.csv`, foram adicionadas:

- `CATEGORIA_DESPESA`: classifica o assunto principal da despesa.
- `CATEGORIA_ANULACAO`: classifica o motivo administrativo das anulacoes.

## Categorias de despesa

As categorias foram atribuidas por palavras-chave presentes na descricao do empenho:

| Categoria | Exemplos de palavras-chave |
|---|---|
| Divulgação das atividades parlamentares | DIVULGACAO, COMUNICACAO, MARKETING |
| Alimentação e refeição | ALIMENTACAO, REFEICAO |
| Combustíveis | COMBUSTIVEIS, ABASTECIMENTO |
| Consultoria e assessoria jurídica | JURIDICA, ADVOCACIA, ADVOGADOS |
| Consultoria e assessoria administrativa | CONSULTORIA, ASSESSORIA, CONTABIL, TRIBUTARIO, PLANEJAMENTO |
| Telefonia, internet e dados | TELEFONIA, INTERNET, DADOS |
| Locação de veículos | LOCACAO, VEICULOS, HILUX, S10, ARGO |
| Impressos e serviços gráficos | GRAFICA, IMPRESSOES, EDITORA |
| Passagens e hospedagem | PASSAGEM, AEREA, HOSPEDAGEM |
| Seguro de vida | SEGURO DE VIDA |
| Outras despesas | Quando nenhuma regra anterior se aplica |

## Categorias de anulacao

As anulacoes foram classificadas por expressões encontradas na descricao:

| Categoria | Criterio |
|---|---|
| Solicitação parlamentar | SOLICITACAO DO DEPUTADO ou SOLICITACAO DA DEPUTADA |
| Correção administrativa | CORRECAO, ACERTO, AJUSTE, INCLUIR ou ANULACAO PARCIAL |
| Motivo não especificado | Quando nenhuma regra anterior se aplica |
| Não se aplica | Lançamentos positivos, que não são anulações |

## Resultado da categorizacao

Foram identificadas:

- 11 categorias de despesa;
- 3 categorias efetivas de anulacao, alem de `Não se aplica` para despesas positivas.

## Observacao

A classificacao e baseada em regras transparentes de texto. Ela melhora a leitura publica dos dados, mas nao substitui auditoria documental detalhada de cada processo ou empenho.
