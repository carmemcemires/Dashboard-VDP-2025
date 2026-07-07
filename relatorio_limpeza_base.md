# Relatorio da limpeza da base

Arquivo original preservado:

- `data/base_vdp_alece_2025_tratada.csv`

Arquivo limpo criado:

- `data/base_vdp_alece_2025_limpa.csv`

O dashboard passou a usar o arquivo limpo.

## Resultado geral

- Registros: 4.219
- Deputados diferentes apos limpeza: 58
- Credores diferentes apos limpeza: 110
- Categorias de despesa: 11
- Categorias de anulacao: 3 categorias efetivas, alem de `Não se aplica`
- Total liquido preservado: R$ 19.893.422,35
- Linhas com deputado corrigido: 70
- Linhas com credor corrigido/padronizado: 2.088

## Rastreabilidade

No arquivo limpo:

- `DEPUTADO` contem o nome limpo usado no dashboard.
- `DEPUTADO_ORIGINAL` preserva o nome como estava na base original.
- `DEPUTADO_CORRIGIDO` indica se houve alteracao.
- `CREDOR` contem o nome limpo usado no dashboard.
- `CREDOR_ORIGINAL` preserva o nome como estava na base original.
- `CREDOR_CORRIGIDO` indica se houve alteracao.
- `CATEGORIA_DESPESA` classifica a natureza do gasto.
- `CATEGORIA_ANULACAO` classifica o motivo administrativo das anulacoes.

## Correcoes de deputados aplicadas

| Original | Limpo | Registros | Valor liquido |
|---|---|---:|---:|
| DEP ALCIDERS FERNANDES | DEP ALCIDES FERNANDES | 2 | R$ 0,00 |
| DEP ALMIIR BIE | DEP ALMIR BIE | 2 | R$ 0,00 |
| DEP ALMIR B | DEP ALMIR BIE | 2 | R$ 0,00 |
| DEP ALYSSON AGUYIAR | DEP ALYSSON AGUIAR | 2 | R$ 0,00 |
| DEP CARMELO NETO | DEP CARMELO BOLSONARO | 47 | R$ 246.615,82 |
| DEP EMIILA PESSOA | DEP EMILIA PESSOA | 2 | R$ 0,00 |
| DEP EMILA PESSOA | DEP EMILIA PESSOA | 2 | R$ 0,00 |
| DEP FIRMO CAMUCA | DEP FIRMO CAMURCA | 1 | R$ 2.500,00 |
| DEP GUILHERME BISMARK | DEP GUILHERME BISMARCK | 3 | R$ 5.711,40 |
| DEP MISSISAS DIAS | DEP MISSIAS DIAS | 2 | R$ 0,00 |
| DEP NIZO COSTA. | DEP NIZO COSTA | 2 | R$ 0,00 |
| DEP SERGIO AGUIAR. | DEP SERGIO AGUIAR | 1 | R$ 66,64 |
| DEP SERGIO AHUIAR | DEP SERGIO AGUIAR | 2 | R$ 0,00 |

## Correcoes e padronizacoes de credores aplicadas

| Original | Limpo | Registros | Valor liquido |
|---|---|---:|---:|
| ALCIMOR  SILVEIRA FIGUEIREDO SA  BRAGA ADVOGADOS | ALCIMOR SILVEIRA FIGUEIREDO SA BRAGA ADVOGADOS | 11 | R$ 75.500,00 |
| BARBOSA  MORAES SOCIEDADE DE ADVOGADOS | BARBOSA MORAES SOCIEDADE DE ADVOGADOS | 11 | R$ 154.000,00 |
| BGQS MORAIS  RS NOG  E T DA S FER LTDA | BGQS MORAIS RS NOG E T DA S FER LTDA | 11 | R$ 74.000,00 |
| CARMELO SILVEIRA  CARNEIRO LEAO NETO | CARMELO SILVEIRA CARNEIRO LEAO NETO | 11 | R$ 31.871,60 |
| EMPRESA BRAS DE CORREIOS E TELEGRAFOS | EMPRESA BRASILEIRA DE CORREIOS E TELEGRAFOS | 14 | R$ 19.722,03 |
| GLOBAL EMPREENDIMENTOS E SERV.LT | GLOBAL EMPREENDIMENTOS E SERV. LT | 3 | R$ 12.382,02 |
| GP  SERVICOS ADMINISTRATIVOS LT | GP SERVICOS ADMINISTRATIVOS LT | 221 | R$ 2.192.500,00 |
| Guilherme Sampaio Landim | GUILHERME SAMPAIO LANDIM | 52 | R$ 112.121,87 |
| JOSE FIRMO AGUIAR NETO | JOSE FIRMO DE CAMURCA NETO | 4 | R$ 0,00 |
| P R  M COMUNICACAO | P R M COMUNICACAO | 48 | R$ 521.250,00 |
| RONNY FELICIO SOCIEDADE INDIV.DE ADVOGACIA | RONNY FELICIO SOCIEDADE INDIV. DE ADVOCACIA | 27 | R$ 152.250,00 |
| Simao Pedro Alves Pequeno | SIMAO PEDRO ALVES PEQUENO | 15 | R$ 68.717,66 |
| TICKET SERVICOS S/A | TICKET SERVICOS S.A. | 1.057 | R$ 2.361.788,00 |
| TICKET SOLUCOES HDFGT S/A | TICKET SOLUCOES HDFGT S.A. | 560 | R$ 2.732.206,93 |
| TIM S A | TIM S.A. | 40 | R$ 2.303,03 |
| VICTOR SILVA TORRES SOC.IND.DE ADV | VICTOR SILVA TORRES SOC. IND. DE ADV. | 2 | R$ 24.000,00 |
| WALDIR XAVIER E ADVOGADOS ASSOCIADOS S/C | WALDIR XAVIER E ADVOGADOS ASSOCIADOS S.C. | 1 | R$ 10.000,00 |
