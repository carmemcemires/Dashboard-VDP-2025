# Relatorio de qualidade dos nomes dos deputados

Analise feita sobre a coluna `DEPUTADO` da base `base_vdp_alece_2025_tratada.csv`.

## Resumo

- Nomes unicos antes da padronizacao: 71
- Nomes unicos apos aplicar as correcoes sugeridas: 58
- Linhas afetadas pelas suspeitas: 36
- Valor liquido associado as linhas suspeitas: R$ 49.260,64
- Despesas brutas associadas as linhas suspeitas: R$ 159.838,81
- Anulacoes associadas as linhas suspeitas: R$ 110.578,17

## Correcoes sugeridas

| Nome encontrado na base | Nome sugerido | Registros | Valor liquido | Tipo de problema |
|---|---:|---:|---:|---|
| DEP ALCIDERS FERNANDES | DEP ALCIDES FERNANDES | 2 | R$ 0,00 | Letra extra |
| DEP ALMIIR BIE | DEP ALMIR BIE | 2 | R$ 0,00 | Letra extra |
| DEP ALMIR B | DEP ALMIR BIE | 2 | R$ 0,00 | Nome abreviado/incompleto |
| DEP ALYSSON AGUYIAR | DEP ALYSSON AGUIAR | 2 | R$ 0,00 | Letra extra |
| DEP EMIILA PESSOA | DEP EMILIA PESSOA | 2 | R$ 0,00 | Letra extra |
| DEP EMILA PESSOA | DEP EMILIA PESSOA | 2 | R$ 0,00 | Letra faltante |
| DEP FIRMO CAMUCA | DEP FIRMO CAMURCA | 1 | R$ 2.500,00 | Letra faltante |
| DEP GUILHERME BISMARK | DEP GUILHERME BISMARCK | 3 | R$ 5.711,40 | Letra faltante |
| DEP MISSISAS DIAS | DEP MISSIAS DIAS | 2 | R$ 0,00 | Letra extra |
| DEP NIZO COSTA. | DEP NIZO COSTA | 2 | R$ 0,00 | Pontuacao final |
| DEP SERGIO AGUIAR. | DEP SERGIO AGUIAR | 1 | R$ 66,64 | Pontuacao final |
| DEP SERGIO AHUIAR | DEP SERGIO AGUIAR | 2 | R$ 0,00 | Letra trocada |
| DEP CARMELO NETO | DEP CARMELO BOLSONARO | 47 | R$ 246.615,82 | Nome divergente; ajustado para o nome exibido na listagem oficial atual da ALECE |

## Observacoes

- A base usa nomes em caixa alta e sem acentos. Isso nao e necessariamente erro, mas deixa a exibicao menos fiel a grafia publica dos nomes.
- As correcoes acima foram detectadas por comparacao interna de nomes semelhantes, recorrencia na propria base e padroes evidentes de letra extra, letra faltante, abreviacao ou pontuacao.
- Recomenda-se aplicar a padronizacao em uma nova coluna, por exemplo `DEPUTADO_PADRONIZADO`, preservando `DEPUTADO` como veio na fonte.
