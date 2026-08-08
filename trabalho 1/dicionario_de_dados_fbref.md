# Dicionário de Dados

## Dataset: `fbref_big5_brasileirao_2526_V2.csv`

**Fontes:**

- FBref (Big 5 Ligas Europeias + Campeonato Brasileiro Série A, temporada 2025-26) — `gerar_csv_professor.py`

---

## Identificação do Jogador

| Coluna     | Tipo    | Descrição                                                                                                                           |
| ---------- | ------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| `Rk`     | Integer | Posição na listagem original do FBref (não é um ranking de qualidade)                                                             |
| `Player` | String  | Nome completo do jogador conforme registrado no FBref                                                                                 |
| `Nation` | String  | Código de nacionalidade do jogador (ex:`br BRA`, `pt POR`)                                                                       |
| `Pos`    | String  | Posição principal —`GK` (goleiro), `DF` (defensor), `MF` (meia), `FW` (atacante). Pode conter combinações como `DF,MF` |
| `Squad`  | String  | Nome do clube atual                                                                                                                   |
| `Comp`   | String  | Nome da liga/competição (ex:`Premier League`, `Série A`)                                                                       |
| `Age`    | Integer | Idade do jogador em anos                                                                                                              |
| `Born`   | Integer | Ano de nascimento                                                                                                                     |
| `liga`   | String  | Liga de origem no dataset:`Big5` (ligas europeias) ou `Brasileirao`                                                               |

---

## Tempo em Campo

| Coluna     | Tipo    | Descrição                                                                                                                    |
| ---------- | ------- | ------------------------------------------------------------------------------------------------------------------------------ |
| `MP`     | Integer | **Matches Played** — total de partidas disputadas na temporada                                                          |
| `Starts` | Integer | Partidas em que o jogador foi titular                                                                                          |
| `Min`    | Integer | Total de minutos jogados na temporada                                                                                          |
| `90s`    | Float   | Equivalente em partidas completas (`Min ÷ 90`). Ex: 4,5 significa que o jogador jogou o equivalente a 4,5 partidas inteiras |

---

## Estatísticas Ofensivas

| Coluna      | Tipo    | Descrição                                                                                                                                                                                          |
| ----------- | ------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `Gls`     | Integer | **Goals** — gols marcados na temporada (inclui pênaltis)                                                                                                                                     |
| `Ast`     | Integer | **Assists** — assistências para gol                                                                                                                                                          |
| `G+A`     | Integer | Soma de gols e assistências                                                                                                                                                                         |
| `G-PK`    | Integer | Gols excluindo pênaltis convertidos                                                                                                                                                                 |
| `PK`      | Integer | Pênaltis convertidos                                                                                                                                                                                |
| `PKatt`   | Integer | Pênaltis cobrados (tentativas, convertidos ou não)                                                                                                                                                 |
| `CrdY`    | Integer | **Yellow Cards** — cartões amarelos                                                                                                                                                          |
| `CrdR`    | Integer | **Red Cards** — cartões vermelhos                                                                                                                                                            |
| `G+A-PK`  | Float   | **(por 90 min)** Gols + Assistências excluindo pênaltis por 90 minutos — `goals_assists_pens_per90` no FBref. Métrica de contribuição ofensiva "limpa" normalizada pelo tempo em campo |
| `Matches` | String  | Coluna de link interno do FBref —**ignorar**, não contém dado útil                                                                                                                         |

---

## Estatísticas por 90 Minutos — FBref Standard

Colunas recuperadas na V2 (estavam ausentes na V1 por bug de nomes duplicados no parser).
Todas normalizadas por 90 minutos jogados.

| Coluna                  | Tipo  | Descrição                             |
| ----------------------- | ----- | --------------------------------------- |
| `goals_per90`         | Float | Gols por 90 minutos                     |
| `assists_per90`       | Float | Assistências por 90 minutos            |
| `goals_assists_per90` | Float | Gols + Assistências por 90 minutos     |
| `goals_pens_per90`    | Float | Gols excluindo pênaltis por 90 minutos |

---

## Passes

| Coluna                      | Tipo    | Descrição                                                                                                                                                                                 |
| --------------------------- | ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `Cmp`                     | Integer | **Completed Passes** — passes completados (total)                                                                                                                                    |
| `Att`                     | Integer | **Attempted Passes** — passes tentados (total)                                                                                                                                       |
| `Cmp%`                    | Float   | Percentual de passes completados (`Cmp ÷ Att × 100`)                                                                                                                                    |
| `TotDist`                 | Float   | Distância total percorrida por todos os passes do jogador (em jardas)                                                                                                                      |
| `PrgDist`                 | Float   | **Progressive Distance** — distância acumulada apenas pelos passes que avançaram o campo em direção ao gol adversário (em jardas)                                               |
| `passes_completed_short`  | Integer | Passes curtos completados (menos de ~15 m)                                                                                                                                                  |
| `passes_short`            | Integer | Passes curtos tentados                                                                                                                                                                      |
| `passes_pct_short`        | Float   | Percentual de acerto em passes curtos                                                                                                                                                       |
| `passes_completed_medium` | Integer | Passes médios completados (~15–32 m)                                                                                                                                                      |
| `passes_medium`           | Integer | Passes médios tentados                                                                                                                                                                     |
| `passes_pct_medium`       | Float   | Percentual de acerto em passes médios                                                                                                                                                      |
| `passes_completed_long`   | Integer | Passes longos completados (mais de ~32 m)                                                                                                                                                   |
| `passes_long`             | Integer | Passes longos tentados                                                                                                                                                                      |
| `passes_pct_long`         | Float   | Percentual de acerto em passes longos                                                                                                                                                       |
| `A-xAG`                   | Float   | Diferença entre assistências reais e Expected Assisted Goals (xAG). Valor positivo indica que o jogador converteu mais assistências do que o esperado pelo modelo                        |
| `KP`                      | Integer | **Key Passes** — passes que resultaram diretamente em chute (mesmo que não virem gol)                                                                                               |
| `1/3`                     | Integer | **Passes para o terço final** — passes que chegam ao último terço do campo adversário. O nome pode aparecer como `01/mar` em alguns sistemas que interpretam `1/3` como data |
| `PPA`                     | Integer | **Passes into Penalty Area** — passes que chegam à área adversária                                                                                                                |
| `CrsPA`                   | Integer | **Crosses into Penalty Area** — cruzamentos que chegam à área adversária                                                                                                          |

---

## Ações Defensivas

| Coluna                | Tipo    | Descrição                                                                                                                                         |
| --------------------- | ------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| `Tkl`               | Integer | **Tackles** — total de desarmes realizados                                                                                                   |
| `TklW`              | Integer | **Tackles Won** — desarmes em que o jogador conquistou a bola                                                                                |
| `Def 3rd`           | Integer | Desarmes realizados no terço defensivo do campo                                                                                                    |
| `Mid 3rd`           | Integer | Desarmes realizados no terço médio do campo                                                                                                       |
| `Att 3rd`           | Integer | Desarmes realizados no terço ofensivo do campo                                                                                                     |
| `challenge_tackles` | Integer | Desarmes em situação de disputa direta (`Tkl` da subseção *Challenges*) — distinto do `Tkl` total que inclui todos os tipos de abordagem |
| `Tkl%`              | Float   | Percentual de desarmes ganhos sobre o total de tentativas de desarme em disputa direta                                                              |
| `Lost`              | Integer | Desarmes tentados em que o adversário manteve a posse da bola                                                                                      |
| `blocks`            | Integer | Total de bloqueios (chutes + passes bloqueados)                                                                                                     |
| `Sh`                | Integer | Chutes bloqueados (subcoluna de Blocks)                                                                                                             |
| `Pass`              | Integer | Passes bloqueados (subcoluna de Blocks)                                                                                                             |
| `Int`               | Integer | **Interceptions** — interceptações de passes adversários                                                                                  |
| `Tkl+Int`           | Integer | Soma de desarmes e interceptações — métrica geral de volume defensivo                                                                           |
| `Clr`               | Integer | **Clearances** — cortes e afastamentos da bola da área defensiva                                                                            |
| `Err`               | Integer | **Errors** — erros defensivos que resultaram diretamente em chute adversário                                                                |

---

## Chutes

| Coluna     | Tipo    | Descrição                                                                            |
| ---------- | ------- | -------------------------------------------------------------------------------------- |
| `SoT`    | Integer | **Shots on Target** — chutes que foram no alvo (gol ou defendidos pelo goleiro) |
| `SoT%`   | Float   | Percentual de chutes que foram no alvo (`SoT ÷ chutes totais × 100`)               |
| `Sh/90`  | Float   | Chutes por 90 minutos jogados                                                          |
| `SoT/90` | Float   | Chutes no alvo por 90 minutos jogados                                                  |
| `G/Sh`   | Float   | Gols por chute — eficiência finalizadora geral                                       |
| `G/SoT`  | Float   | Gols por chute no alvo — eficiência finalizadora quando acerta o gol                 |

---

## Goleiros

Estas colunas são preenchidas **apenas para goleiros (GK)**. Para outras posições, o valor será `NaN` (que deve ser tratado como `0` no pré-processamento).

| Coluna               | Tipo    | Descrição                                                                                                       |
| -------------------- | ------- | ----------------------------------------------------------------------------------------------------------------- |
| `GA`               | Integer | **Goals Against** — gols sofridos na temporada                                                             |
| `GA90`             | Float   | Gols sofridos por 90 minutos — métrica padrão de desempenho do goleiro                                         |
| `SoTA`             | Integer | **Shots on Target Against** — chutes no alvo sofridos pelo goleiro                                         |
| `Saves`            | Integer | Defesas realizadas                                                                                                |
| `Save%`            | Float   | Percentual de defesas (`Saves ÷ SoTA × 100`)                                                                  |
| `W`                | Integer | Vitórias do time com o goleiro em campo                                                                          |
| `D`                | Integer | Empates do time com o goleiro em campo                                                                            |
| `L`                | Integer | Derrotas do time com o goleiro em campo                                                                           |
| `CS`               | Integer | **Clean Sheets** — jogos em que o goleiro não sofreu gols                                                 |
| `CS%`              | Float   | Percentual de jogos sem sofrer gols                                                                               |
| `PKA`              | Integer | **Penalty Kicks Against** — pênaltis cobrados contra o goleiro                                            |
| `PKsv`             | Integer | **Penalty Kicks Saved** — pênaltis defendidos                                                             |
| `PKm`              | Integer | **Penalty Kicks Missed** — pênaltis cobrados contra o goleiro que foram para fora (errados pelo cobrador) |
| `gk_pens_save_pct` | Float   | Percentual de pênaltis defendidos pelo goleiro (`PKsv ÷ PKA × 100`)                                          |

---

## Estatísticas Auxiliares (V2)

### Identificação

| Coluna            | Tipo    | Descrição                                                                                |
| ----------------- | ------- | ------------------------------------------------------------------------------------------ |
| `player_id`     | Integer | ID interno do jogador no FotMob                                                            |
| `ccode`         | String  | Código de país da nacionalidade do jogador no FotMob (ex:`BRA`, `NOR`)               |
| `team_id`       | Integer | ID interno do clube no FotMob                                                              |
| `MinutesPlayed` | Integer | Minutos jogados conforme o FotMob (pode diferir levemente do FBref por critério de fonte) |
| `MatchesPlayed` | Integer | Partidas disputadas conforme o FotMob                                                      |

### Estatísticas de Ataque

| Coluna                             | Tipo  | Descrição                                                                                            |
| ---------------------------------- | ----- | ------------------------------------------------------------------------------------------------------ |
| `Gols`                           | Float | Gols marcados na temporada (FotMob)                                                                    |
| `Assistencias`                   | Float | Assistências para gol (FotMob)                                                                        |
| `Gols_e_Assistencias`            | Float | Soma de gols e assistências                                                                           |
| `Gols_por_90`                    | Float | Gols por 90 minutos (FotMob)                                                                           |
| `xG`                             | Float | **Expected Goals** — gols esperados com base na qualidade das finalizações                    |
| `xG_por_90`                      | Float | xG por 90 minutos                                                                                      |
| `xGOT`                           | Float | **Expected Goals on Target** — xG calculado apenas para os chutes que foram ao gol              |
| `Chutes_a_gol_por_90`            | Float | Chutes no alvo por 90 minutos                                                                          |
| `Chutes_por_90`                  | Float | Chutes totais por 90 minutos                                                                           |
| `xA`                             | Float | **Expected Assists** — assistências esperadas com base na qualidade do passe que gerou o chute |
| `xA_por_90`                      | Float | xA por 90 minutos                                                                                      |
| `xG_mais_xA_por_90`              | Float | xG + xA por 90 minutos — métrica combinada de contribuição ofensiva esperada                       |
| `Grandes_chances_criadas`        | Float | Chances claras de gol criadas para companheiros (total)                                                |
| `Chances_criadas`                | Float | Total de chances criadas (passes que geraram chute)                                                    |
| `Grandes_chances_perdidas`       | Float | Grandes chances desperdiçadas pelo próprio jogador                                                   |
| `Dribles_bem_sucedidos_por_90`   | Float | Dribles completados por 90 minutos                                                                     |
| `Passes_acertados_por_90`        | Float | Passes completados por 90 minutos                                                                      |
| `Passes_longos_acertados_por_90` | Float | Passes longos completados por 90 minutos                                                               |
| `Penaltis_sofridos`              | Float | Pênaltis sofridos na temporada                                                                        |

### Estatísticas Defensivas

| Coluna                                     | Tipo  | Descrição                                                                                                                      |
| ------------------------------------------ | ----- | -------------------------------------------------------------------------------------------------------------------------------- |
| `Acoes_defensivas_por_90`                | Float | Ações defensivas totais por 90 minutos (desarmes + interceptações + bloqueios)                                               |
| `Desarmes_por_90`                        | Float | Desarmes por 90 minutos                                                                                                          |
| `Interceptacoes_por_90`                  | Float | Interceptações por 90 minutos                                                                                                  |
| `Bolas_afastadas_por_90`                 | Float | Cortes (clearances) por 90 minutos                                                                                               |
| `Bloqueios_por_90`                       | Float | Bloqueios por 90 minutos                                                                                                         |
| `Recuperacoes_de_posse_por_90`           | Float | Recuperações de posse de bola por 90 minutos                                                                                   |
| `Penaltis_cometidos`                     | Float | Pênaltis cometidos na temporada                                                                                                 |
| `Posse_recuperada_terceiro_final_por_90` | Float | Recuperações de posse no terço ofensivo por 90 minutos.**Ausente para o Brasileirão** (API retorna 403 para esta liga) |

### Avaliação e Disciplina

| Coluna                      | Tipo  | Descrição                                                                                  |
| --------------------------- | ----- | -------------------------------------------------------------------------------------------- |
| `Avaliacao_FotMob`        | Float | Nota média do jogador atribuída pelo FotMob (escala 0–10) com base em ações por partida |
| `Faltas_cometidas_por_90` | Float | Faltas cometidas por 90 minutos                                                              |
| `Cartoes_amarelos`        | Float | Total de cartões amarelos na temporada (FotMob)                                             |
| `Cartoes_vermelhos`       | Float | Total de cartões vermelhos na temporada (FotMob)                                            |

### Estatísticas de Goleiros (FotMob)

Preenchidas apenas para goleiros; `NaN` para demais posições.

| Coluna                    | Tipo  | Descrição                                                                      |
| ------------------------- | ----- | -------------------------------------------------------------------------------- |
| `Jogos_sem_sofrer_gols` | Float | Clean sheets na temporada (FotMob)                                               |
| `Percentual_defesas`    | Float | Percentual de defesas (`saves ÷ finalizações no alvo × 100`)               |
| `Defesas_por_90`        | Float | Defesas por 90 minutos                                                           |
| `Gols_evitados`         | Float | Gols evitados em relação ao xGOT sofrido (`xGOT concedido − gols sofridos`) |
| `Gols_sofridos_por_90`  | Float | Gols sofridos por 90 minutos                                                     |

---

## Notas de Uso

### Colunas a remover antes de modelar

As colunas abaixo não devem ser usadas como features nos modelos:

| Coluna            | Motivo                                                              |
| ----------------- | ------------------------------------------------------------------- |
| `Rk`            | Índice da listagem FBref, sem significado preditivo                |
| `Matches`       | Link interno do FBref, sem dado útil                               |
| `Player`        | Identificador textual — usar apenas para interpretação           |
| `Squad`         | Texto — encode só se necessário para análises específicas      |
| `Comp`          | Redundante com a coluna `liga`                                    |
| `Born`          | Redundante com `Age`                                              |
| `Min`           | Gera o**target** — nunca usar como feature                   |
| `90s`           | Derivado direto de `Min` (`Min ÷ 90`) — remover junto         |
| `Starts`        | Altamente correlacionado com `Min` — remover para evitar leakage |
| `player_id`     | Identificador textual do FotMob — usar apenas para cruzamentos     |
| `ccode`         | Redundante com `Nation` do FBref                                  |
| `team_id`       | Identificador interno do FotMob, sem significado preditivo          |
| `MinutesPlayed` | Altamente correlacionado com `Min` (FBref) — remover             |
| `MatchesPlayed` | Altamente correlacionado com `MP` (FBref) — remover              |
| `valor_mercado` | Usado na EDA e nos clusters — não é o target                     |

### Colunas posicionais (NaN → 0)

**FBref — Goleiros:** `GA`, `GA90`, `SoTA`, `Saves`, `Save%`, `W`, `D`, `L`, `CS`, `CS%`, `PKA`, `PKsv`, `PKm`, `gk_pens_save_pct` — serão `NaN` para jogadores de linha. Preencha com `0`.

**Auxiliar— Goleiros:** `Jogos_sem_sofrer_gols`, `Percentual_defesas`, `Defesas_por_90`, `Gols_evitados`, `Gols_sofridos_por_90` — idem.

Da mesma forma, `Err`, `Clr`, `Int`, `Tkl` e derivados tendem a ser `NaN` para atacantes, e `Gls`, `SoT`, `xG` tendem a ser `NaN` para goleiros.

### NaN do Auxiliar(11,8 % dos jogadores)

349 jogadores do FBref não foram encontrados no Auxiliar— tipicamente jogadores com poucos minutos que não aparecem em nenhum ranking estatístico. As colunas Auxiliares ficam `NaN` para esses jogadores. Estratégias:

- **Imputar zero** para stats de contagem (gols, cartões) onde ausência implica zero.
- **Imputar mediana por posição** para stats de eficiência (xG, rating) onde a ausência é informativa.
- **Usar apenas jogadores com dados completos** se a análise exigir cobertura total.

### Sobre a coluna `1/3`

O FBref nomeia a coluna `1/3` (passes para o último terço). Em alguns ambientes o nome pode ser interpretado como data e aparecer como `01/mar`. No V2 a coluna está grafada como `1/3`. Ao renomear no pré-processamento:

```python
df.rename(columns={'1/3': 'passes_ultimo_terco'}, inplace=True)
```

### Duplicidade FBref × Auxiliar

Algumas métricas aparecem nas duas fontes com nomenclatura diferente. Não usar ambas simultaneamente como features — escolher a de maior confiança ou descartar a redundante:

| Coluna FBref | Coluna FotMob           | Observação                                     |
| ------------ | ----------------------- | ------------------------------------------------ |
| `Gls`      | `Gols`                | Mesma métrica; FBref é a referência canônica |
| `Ast`      | `Assistencias`        | Idem                                             |
| `CrdY`     | `Cartoes_amarelos`    | Idem                                             |
| `CrdR`     | `Cartoes_vermelhos`   | Idem                                             |
| `Sh/90`    | `Chutes_por_90`       | Definição ligeiramente diferente entre fontes  |
| `SoT/90`   | `Chutes_a_gol_por_90` | Idem                                             |

### Diferença de cobertura entre ligas

A coluna `liga` separa Big 5 (`Big5`) e Brasileirão (`Brasileirao`). No FotMob, a coluna `Posse_recuperada_terceiro_final_por_90` está ausente para o Brasileirão (API retorna 403). No FBref, o Brasileirão pode ter mais `NaN` em campos avançados como `PrgDist` dependendo da cobertura Opta para o Brasil.

### Target da classificação

O target binário é derivado dos **minutos jogados** — proxy direto de qualidade, disponível para 100 % dos jogadores:

```python
mediana = df['Min'].median()
df['target'] = (df['Min'] > mediana).astype(int)
# 1 = "Titular Regular" (acima da mediana de minutos)
# 0 = "Rotação/Reserva" (abaixo da mediana)
```

As classes ficam aproximadamente balanceadas por definição da mediana (~50/50).

**Atenção — data leakage:** `Min`, `90s`, `Starts`, `MinutesPlayed` e `MatchesPlayed` são derivados diretamente dos minutos e devem ser removidos das features antes de treinar qualquer modelo.

### Papel do valor de mercado (`valor_mercado`)

O valor de mercado vem do Transfermarkt e cobre apenas os ~500 jogadores mais valiosos do mundo. Após o merge `left`, a maioria dos jogadores terá `NaN` nesta coluna. Por isso, **não é usado como target**. Serve para:

- Enriquecer a análise exploratória (distribuição de valor por posição, liga, etc.)
- Caracterizar os clusters: "qual o valor médio de mercado dos jogadores de cada cluster?"
