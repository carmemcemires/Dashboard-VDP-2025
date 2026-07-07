# Relatorio de qualidade dos nomes dos credores

Analise feita sobre a coluna `CREDOR` da base `base_vdp_alece_2025_tratada.csv`.

## Resumo

- Credores unicos encontrados: 111
- CNPJs com mais de uma grafia de credor: 0
- Grupos duplicados apenas por remocao de pontuacao/acentos: 0
- Pares muito semelhantes detectados automaticamente: 2, mas ambos parecem falsos positivos por nomes comuns de escritorios de advocacia
- Credores com algum problema textual ou padronizacao recomendada: 16

Ao contrario do caso dos deputados, a coluna `CREDOR` nao apresentou duplicidades fortes por similaridade interna. A maioria dos achados e de qualidade textual: espacos duplicados, caixa inconsistente, abreviacoes e possiveis sufixos juridicos truncados.

## Correcoes ou padronizacoes sugeridas

| Nome encontrado na base | Padronizacao sugerida | Registros | Valor liquido | Tipo de problema | Nivel |
|---|---:|---:|---:|---|---|
| RONNY FELICIO SOCIEDADE INDIV.DE ADVOGACIA | RONNY FELICIO SOCIEDADE INDIV. DE ADVOCACIA | 27 | R$ 152.250,00 | Possivel erro de digitacao: ADVOGACIA -> ADVOCACIA | Alta confianca |
| GP  SERVICOS ADMINISTRATIVOS LT | GP SERVICOS ADMINISTRATIVOS LT | 221 | R$ 2.192.500,00 | Espacos duplicados; sufixo `LT` possivelmente truncado | Confirmar sufixo |
| GLOBAL EMPREENDIMENTOS E SERV.LT | GLOBAL EMPREENDIMENTOS E SERV. LT | 3 | R$ 12.382,02 | Pontuacao/abreviacao; sufixo possivelmente truncado | Confirmar sufixo |
| EMPRESA BRAS DE CORREIOS E TELEGRAFOS | EMPRESA BRASILEIRA DE CORREIOS E TELEGRAFOS | 14 | R$ 19.722,03 | Abreviacao `BRAS` | Confirmar com fonte |
| Guilherme Sampaio Landim | GUILHERME SAMPAIO LANDIM | 52 | R$ 112.121,87 | Caixa inconsistente | Alta confianca |
| Simao Pedro Alves Pequeno | SIMAO PEDRO ALVES PEQUENO | 15 | R$ 68.717,66 | Caixa inconsistente | Alta confianca |
| P R  M COMUNICACAO | P R M COMUNICACAO | 48 | R$ 521.250,00 | Espacos duplicados | Alta confianca |
| ALCIMOR  SILVEIRA FIGUEIREDO SA  BRAGA ADVOGADOS | ALCIMOR SILVEIRA FIGUEIREDO SA BRAGA ADVOGADOS | 11 | R$ 75.500,00 | Espacos duplicados | Alta confianca |
| BARBOSA  MORAES SOCIEDADE DE ADVOGADOS | BARBOSA MORAES SOCIEDADE DE ADVOGADOS | 11 | R$ 154.000,00 | Espacos duplicados | Alta confianca |
| BGQS MORAIS  RS NOG  E T DA S FER LTDA | BGQS MORAIS RS NOG E T DA S FER LTDA | 11 | R$ 74.000,00 | Espacos duplicados; nome muito abreviado | Alta confianca para espacos |
| CARMELO SILVEIRA  CARNEIRO LEAO NETO | CARMELO SILVEIRA CARNEIRO LEAO NETO | 11 | R$ 31.871,60 | Espacos duplicados | Alta confianca |
| VICTOR SILVA TORRES SOC.IND.DE ADV | VICTOR SILVA TORRES SOC. IND. DE ADV. | 2 | R$ 24.000,00 | Abreviacao/pontuacao | Padronizacao estetica |
| TIM S A | TIM S.A. | 40 | R$ 2.303,03 | Pontuacao de natureza juridica | Padronizacao estetica |
| TICKET SERVICOS S/A | TICKET SERVICOS S.A. | 1057 | R$ 2.361.788,00 | Pontuacao de natureza juridica | Padronizacao estetica |
| TICKET SOLUCOES HDFGT S/A | TICKET SOLUCOES HDFGT S.A. | 560 | R$ 2.732.206,93 | Pontuacao de natureza juridica | Padronizacao estetica |
| WALDIR XAVIER E ADVOGADOS ASSOCIADOS S/C | WALDIR XAVIER E ADVOGADOS ASSOCIADOS S.C. | 1 | R$ 10.000,00 | Pontuacao de natureza juridica | Padronizacao estetica |

## Pares semelhantes detectados, mas nao recomendados para unificacao

| Credor A | Credor B | Motivo para nao unificar automaticamente |
|---|---|---|
| JULIO OLIVEIRA SOCIEDADE INDIVIDUAL DE ADVOCACIA | LUIZ OLIVEIRA NETO SOCIEDADE INDIVIDUAL DE ADVOCACIA | Pessoas/razoes sociais diferentes, apesar da estrutura parecida |
| JULIO OLIVEIRA SOCIEDADE INDIVIDUAL DE ADVOCACIA | PRISCILA OLIVEIRA SOCIEDADE INDIVIDUAL DE ADVOCACIA | Pessoas/razoes sociais diferentes, apesar da estrutura parecida |

## Recomendacao

Para o dashboard, recomenda-se criar uma coluna nova chamada `CREDOR_PADRONIZADO`, preservando `CREDOR` como veio na fonte.

Aplicacao segura imediata:

- remover espacos duplicados;
- padronizar caixa para maiusculas;
- corrigir `ADVOGACIA` para `ADVOCACIA`;
- padronizar pontuacao de abreviacoes juridicas apenas para exibicao.

Aplicacao com confirmacao manual:

- transformar `LT` em `LTDA`;
- expandir `BRAS` para `BRASILEIRA`;
- expandir abreviacoes muito curtas ou truncadas.
