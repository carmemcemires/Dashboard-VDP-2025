# Relatorio consolidado - Ajustes da base e especificacoes do dashboard

## 1. Objetivo do projeto

Desenvolver um dashboard interativo para analise da Verba de Desempenho Parlamentar (VDP) da Assembleia Legislativa do Estado do Ceara (ALECE), com base em dados publicos do exercicio de 2025.

O painel atende aos requisitos minimos indicados para a atividade e acrescenta melhorias voltadas a compreensao cidadã, como limpeza da base, categorizacao das despesas, categorizacao das anulacoes, identidade visual institucional e exportacao da base detalhada.

## 2. Arquivos da base

Base original preservada:

- `data/base_vdp_alece_2025_tratada.csv`

Base limpa utilizada pelo dashboard:

- `data/base_vdp_alece_2025_limpa.csv`

## 3. Resultado geral da base limpa

- Registros: 4.219
- Deputados diferentes: 58
- Credores diferentes: 110
- Categorias de despesa: 11
- Categorias efetivas de anulacao: 3
- Despesas empenhadas: R$ 20.772.356,00
- Anulacoes: R$ 878.933,65
- Despesa apos anulacoes: R$ 19.893.422,35

## 4. Ajustes necessarios na base

### 4.1 Correcao da leitura do arquivo CSV

A base original vinha em formato CSV com linhas encapsuladas de forma que a leitura simples por separador poderia gerar colunas incorretas. Foi ajustada a funcao de carregamento para:

- detectar o formato real do arquivo;
- reconstruir corretamente as linhas;
- padronizar os nomes das colunas;
- converter campos numericos, como `VALOR`, `VALOR_ABSOLUTO`, `MES_NUMERO` e `ANO`;
- criar colunas auxiliares de mes e periodo quando necessario.

### 4.2 Padronizacao dos nomes dos deputados

Foram identificadas inconsistencias de letras, abreviacoes, pontuacao e grafias divergentes. A limpeza reduziu a quantidade de deputados de 71 para 58.

Linhas com deputado corrigido: 70.

Exemplos de correcoes aplicadas:

- `DEP ALCIDERS FERNANDES` -> `DEP ALCIDES FERNANDES`
- `DEP ALMIIR BIE` -> `DEP ALMIR BIE`
- `DEP ALMIR B` -> `DEP ALMIR BIE`
- `DEP ALYSSON AGUYIAR` -> `DEP ALYSSON AGUIAR`
- `DEP EMIILA PESSOA` -> `DEP EMILIA PESSOA`
- `DEP EMILA PESSOA` -> `DEP EMILIA PESSOA`
- `DEP FIRMO CAMUCA` -> `DEP FIRMO CAMURCA`
- `DEP GUILHERME BISMARK` -> `DEP GUILHERME BISMARCK`
- `DEP MISSISAS DIAS` -> `DEP MISSIAS DIAS`
- `DEP NIZO COSTA.` -> `DEP NIZO COSTA`
- `DEP SERGIO AGUIAR.` -> `DEP SERGIO AGUIAR`
- `DEP SERGIO AHUIAR` -> `DEP SERGIO AGUIAR`
- `DEP CARMELO NETO` -> `DEP CARMELO BOLSONARO`

### 4.3 Conferencia com a lista oficial da ALECE e suplentes

Foi feito cruzamento com a lista oficial atual da ALECE. A diferenca entre a base e a lista oficial atual foi interpretada com cautela, porque a base se refere ao exercicio de 2025 e pode conter suplentes que assumiram em periodos especificos.

Foram identificados deputados na base associados a suplencias ou substituicoes temporarias, o que explica parte das diferencas entre a composicao atual e os registros de despesa.

### 4.4 Padronizacao dos nomes dos credores

Foram tratados problemas de espacos duplicados, caixa inconsistente, abreviacoes, pontuacao e duplicidade identificada pelo usuario.

Credores antes da limpeza: 111.

Credores apos a limpeza: 110.

Linhas com credor corrigido ou padronizado: 2.088.

Exemplos de padronizacoes:

- `GP  SERVICOS ADMINISTRATIVOS LT` -> `GP SERVICOS ADMINISTRATIVOS LT`
- `Guilherme Sampaio Landim` -> `GUILHERME SAMPAIO LANDIM`
- `Simao Pedro Alves Pequeno` -> `SIMAO PEDRO ALVES PEQUENO`
- `P R  M COMUNICACAO` -> `P R M COMUNICACAO`
- `RONNY FELICIO SOCIEDADE INDIV.DE ADVOGACIA` -> `RONNY FELICIO SOCIEDADE INDIV. DE ADVOCACIA`
- `TICKET SERVICOS S/A` -> `TICKET SERVICOS S.A.`
- `TICKET SOLUCOES HDFGT S/A` -> `TICKET SOLUCOES HDFGT S.A.`
- `TIM S A` -> `TIM S.A.`
- `JOSE FIRMO AGUIAR NETO` -> `JOSE FIRMO DE CAMURCA NETO`

### 4.5 Preservacao da rastreabilidade

Apesar de o dashboard exibir apenas os nomes limpos, a base limpa preserva colunas de auditoria:

- `DEPUTADO_ORIGINAL`
- `DEPUTADO_CORRIGIDO`
- `CREDOR_ORIGINAL`
- `CREDOR_CORRIGIDO`

Essas colunas permitem verificar o que foi alterado, mas nao aparecem na base detalhada exibida ao cidadao.

### 4.6 Tratamento dos valores negativos

Os valores negativos foram mantidos, pois representam anulacoes administrativas. A decisao preserva a integridade contabil da base.

Foram adotados os seguintes conceitos no dashboard:

- `Despesas empenhadas`: soma dos lancamentos positivos.
- `Anulacoes`: soma absoluta dos lancamentos negativos.
- `Despesa apos anulacoes`: despesas empenhadas menos anulacoes.

### 4.7 Categorizacao das despesas

Foi criada a coluna `CATEGORIA_DESPESA`, com classificacao por palavras-chave da descricao do empenho.

Categorias utilizadas:

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

### 4.8 Categorizacao das anulacoes

Foi criada a coluna `CATEGORIA_ANULACAO`, com categorias simplificadas para facilitar a leitura publica:

- Correcao administrativa
- Solicitacao parlamentar
- Motivo nao especificado
- Nao se aplica, para registros que nao sao anulacoes

As categorias foram consolidadas para evitar excesso de detalhe e facilitar a interpretacao pelo cidadao.

## 5. Especificacoes do dashboard

### 5.1 Tecnologia

- Python
- Streamlit
- Pandas
- Plotly
- OpenPyXL

### 5.2 Arquivo principal

- `app.py`: ponto de entrada do Streamlit.
- `dashboard.py`: estrutura visual e interativa do painel.
- `utils.py`: carregamento, limpeza, filtros e agregacoes.
- `charts.py`: graficos Plotly.

### 5.3 Identidade visual

O dashboard foi adaptado para se aproximar do site da ALECE:

- uso da logomarca oficial;
- cabecalho verde institucional;
- detalhe dourado;
- cores inspiradas no site da ALECE;
- rodape institucional inspirado no site oficial.

### 5.4 Informacao institucional

Foi incluído um bloco explicativo:

> A Verba de Desempenho Parlamentar (VDP) é uma verba mensal destinada às despesas de custeio dos gabinetes dos Deputados Estaduais, para viabilizar o exercício do mandato parlamentar.

Tambem foram incluidos links para os normativos:

- Ato Deliberativo nº 929, de 14 de marco de 2023
- Resolucao nº 762, de 21 de dezembro de 2023
- Ato Normativo nº 343, de 05 de fevereiro de 2024

### 5.5 Fontes exibidas no rodape

O rodape informa:

- Portal da Transparencia da ALECE - Verba de Desempenho Parlamentar
- Sistema de Gestao Governamental por Resultados - S2GPR ate 2021
- Sistema Integrado de Planejamento e Administracao Financeira do Estado do Ceara - SiafeCE a partir de 2022
- Ultima atualizacao do dashboard

### 5.6 Filtros

O painel possui filtros por:

- Deputado
- Mes/Ano
- Credor
- Categoria da despesa
- Tipo de movimento
- Motivo da anulacao
- Busca livre por descricao, empenho, credor ou deputado

### 5.7 Indicadores principais

Cards exibidos no topo:

- Despesa apos anulacoes
- Despesas empenhadas
- Anulacoes
- Deputados
- Credores

### 5.8 Graficos

O dashboard contem:

- grafico de evolucao mensal;
- grafico de pizza Top 10 maiores despesas por deputado;
- grafico de pizza Top 10 maiores despesas por credor;
- grafico de barras das despesas por categoria;
- ranking Top 10 deputados em barras;
- ranking Top 10 credores em barras;
- grafico de anulacoes por motivo;
- grafico de anulacoes por tipo.

Os graficos foram ajustados para:

- nao exibir termos tecnicos como `PADRONIZADO`;
- mostrar valores em formato brasileiro;
- usar nomes amigaveis como `Deputado`, `Credor` e `Valor`.

### 5.9 Base detalhada

A aba de base detalhada foi simplificada para entendimento do cidadao.

Colunas exibidas:

- Deputado
- Mes/Ano
- Empenho
- Descricao
- Credor
- Valor
- Categoria da despesa
- Motivo da anulacao
- Tipo de movimento
- Tipo de anulacao

Foram removidas da exibicao as colunas com termos que poderiam causar confusao:

- `DEPUTADO_ORIGINAL`
- `DEPUTADO_PADRONIZADO`
- `CREDOR_ORIGINAL`
- `CREDOR_PADRONIZADO`

### 5.10 Download da base

O dashboard possui uma unica opcao de download da base detalhada em Excel:

- `base_vdp_alece_2025_filtrada.xlsx`

A opcao em Excel foi escolhida porque permite preservar a coluna `Valor` como moeda brasileira, algo que o CSV nao garante.

## 6. Como executar

Arquivo de abertura:

- `ABRIR_DASHBOARD.bat`

Endereco local esperado:

- `http://localhost:8501`

Pacote atualizado para entrega:

- `dashboard-vdp-alece-atualizado.zip`
