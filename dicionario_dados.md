
# Dicionário de Dados — VDP ALECE 2025

| Campo | Descrição | Tipo esperado |
|---|---|---|
| DEPUTADO | Nome do parlamentar associado à despesa | Texto |
| PERIODO | Período original informado no arquivo mensal | Texto |
| EMPENHO | Número do empenho | Texto |
| DESCRICAO | Descrição da despesa ou anulação | Texto |
| CNPJ | CNPJ/CPF do credor; pode apresentar notação científica | Texto |
| CREDOR | Nome do credor/fornecedor | Texto |
| VALOR | Valor líquido do lançamento; negativo quando for anulação | Numérico |
| MES | Nome do mês | Texto |
| MES_NUMERO | Número do mês para ordenação cronológica | Inteiro |
| ANO | Ano de referência | Inteiro |
| MES_ANO | Mês/Ano formatado para filtros e gráficos | Texto |
| TIPO_MOVIMENTO | Despesa ou Anulação | Texto |
| VALOR_ABSOLUTO | Valor absoluto do lançamento | Numérico |
| TIPO_ANULACAO | Classificação dos registros negativos | Texto |

## Regras de classificação das anulações

- **Correções administrativas**: descrições com termos associados a correção, ajuste ou retificação.
- **Desistência**: descrições com termos associados a desistência ou solicitação do deputado.
- **Motivo não especificado**: registros negativos cuja descrição informa anulação sem explicitar o motivo.
- **Não se aplica**: registros positivos.
