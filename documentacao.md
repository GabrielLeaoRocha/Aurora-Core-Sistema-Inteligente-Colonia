# ATIVIDADE INTEGRADORA — FASE 3
## Aurora Core: Sistema Inteligente da Colônia

**Curso:** Engenharia de Software — FIAP  
**Turma:** 1ESPR  
**Integrantes:**
- Gabriel de Leão Rocha — RM 571330

**Repositório GitHub:** https://github.com/GabrielLeaoRocha/Aurora-Core-Sistema-Inteligente-Colonia

---

# SUMÁRIO

1. Introdução
2. Organização dos Dados
3. Árvore Binária de Busca (BST)
4. Regras de Decisão Lógica
5. Modelo de Previsão (Regressão Linear)
6. Análise Energética
7. Arquitetura do Sistema
8. Resultados e Exemplos
9. Conclusão
10. Referências

---

# 1 INTRODUÇÃO

O projeto **Aurora Core** representa a implementação do módulo computacional da colônia Aurora Siger. O sistema foi desenvolvido para operar de forma autônoma, integrando conceitos de:

- **Estruturação de dados** (listas, dicionários, hierarquias)
- **Lógica booleana** (regras de decisão AND/OR)
- **Modelagem matemática** (regressão linear simples)
- **Estruturas avançadas** (árvore binária de busca)

O objetivo é demonstrar como dados brutos de telemetria podem ser transformados em decisões inteligentes que garantam a operação segura e eficiente da colônia.

---

# 2 ORGANIZAÇÃO DOS DADOS

## 2.1 Fontes de Dados

Os dados de telemetria são armazenados em três arquivos CSV que representam um mês de operação (30 leituras diárias):

| Arquivo | Descrição | Campos Principais |
|---------|-----------|-------------------|
| `telemetry_energy.csv` | Geração de energia | day, solar_generation_kwh, wind_generation_kwh, battery_reserve_kwh |
| `telemetry_consumption.csv` | Consumo por subsistema | day, life_support_kwh, habitat_kwh, laboratory_kwh, non_essential_kwh |
| `telemetry_climate.csv` | Condições climáticas | day, wind_speed_ms, temperature_c, irradiance_wm2 |

## 2.2 Estrutura Hierárquica

Os dados são organizados em uma **hierarquia de 3 níveis** que representa os sistemas da colônia:

```
            [Colony Aurora Siger]            ← Nível 0: Raiz
                    |
       ┌────────────┼────────────┐
    [Energy]   [Consumption] [Climate]       ← Nível 1: Sistemas
      |              |
  ┌───┴───┐    ┌────┼─────┬──────────┐
[Solar][Wind][Life][Habitat][Lab.][Non-Ess.] ← Nível 2: Subsistemas
```

**Implementação em Python** (dicionário hierárquico):

```python
colony = {
    "name": "Aurora Siger",
    "systems": {
        "energy": {
            "solar": {"generation_kwh": [...], "status": "active"},
            "wind":  {"generation_kwh": [...], "status": "active"}
        },
        "consumption": {
            "life_support":  {"consumption_kwh": [...], "priority": 1},
            "habitat":       {"consumption_kwh": [...], "priority": 2},
            "laboratory":    {"consumption_kwh": [...], "priority": 3},
            "non_essential": {"consumption_kwh": [...], "priority": 4}
        },
        "climate": {
            "wind_speed_ms":  [...],
            "temperature_c":  [...],
            "irradiance_wm2": [...]
        }
    }
}
```

A navegação por esta hierarquia é feita por uma **função recursiva**:

```python
def navigate_hierarchy(colony: dict, path: list) -> any:
    if not path:
        return colony
    key = path[0]
    if isinstance(colony, dict) and key in colony:
        return navigate_hierarchy(colony[key], path[1:])
    return None
```

**Conceitos aplicados:** Listas e dicionários (Cap 1/2), organização hierárquica tipo árvore (Cap 4), funções e recursividade (Cap 3).

---

# 3 ÁRVORE BINÁRIA DE BUSCA (BST)

## 3.1 Motivação

Com 30 leituras diárias, a busca sequencial por um dia específico pode exigir até **30 comparações** (O(n)). A BST organiza os dados de forma que cada busca exige no máximo **5 comparações** (O(log n)).

## 3.2 Conceito

A BST é uma estrutura hierárquica onde:
- Cada nó armazena uma **chave** (dia) e **dados** (leitura do dia)
- Todos os valores à **esquerda** são **menores** que o nó
- Todos os valores à **direita** são **maiores** que o nó

## 3.3 Construção Balanceada

Para evitar uma árvore degenerada (que seria idêntica a uma lista), a BST é construída inserindo os elementos pela **mediana recursiva**:

```python
def _build_balanced(sorted_list, start, end):
    if start > end:
        return None
    mid = (start + end) // 2
    node = BinaryTreeNode(sorted_list[mid]["day"], sorted_list[mid])
    node.left = _build_balanced(sorted_list, start, mid - 1)
    node.right = _build_balanced(sorted_list, mid + 1, end)
    return node
```

## 3.4 Visualização

BST construída com 30 dias de dados (altura = 5):

```
                    [day 15]                    ← raiz
                   /        \
           [day 8]          [day 23]
          /      \          /      \
      [day 4]  [day 11]  [day 19] [day 27]
      /    \    /    \    /    \    /    \
   [3]   [6] [9]  [13] [17] [21] [25] [29]
   ...
```

## 3.5 Operações Implementadas

| Operação | Complexidade | Descrição |
|----------|-------------|-----------|
| `insert(root, day, data)` | O(log n) | Insere leitura na posição correta |
| `search(root, day)` | O(log n) | Busca dados de um dia específico |
| `in_order_traversal(root)` | O(n) | Lista todos os dados em ordem crescente |
| `build_bst(readings)` | O(n log n) | Constrói árvore balanceada |

## 3.6 Exemplo de Busca

Buscando o dia 12:
```
1. Raiz (dia 15): 12 < 15 → vai para ESQUERDA
2. Nó (dia 8):   12 > 8  → vai para DIREITA
3. Nó (dia 11):  12 > 11 → vai para DIREITA
4. Nó (dia 12):  ENCONTRADO ✓ (4 comparações)
```

**Conceitos aplicados:** Árvore binária de busca (Cap 4), complexidade O(log n) vs O(n) (Cap 4), recursividade (Cap 3).

---

# 4 REGRAS DE DECISÃO LÓGICA

## 4.1 Estrutura de Decisão

O sistema aplica **regras booleanas combinadas** para gerar decisões automáticas. As condições utilizam operadores AND/OR conforme a álgebra de Boole estudada no Cap 2.

## 4.2 Tabela de Regras

| # | Condição | Decisão | Prioridade |
|---|----------|---------|------------|
| 1 | `generation < 30` **AND** `consumption > 70` | CRITICAL: activate emergency mode | 1 (máxima) |
| 2 | `generation < 50` **AND** `consumption > generation` | ALERT: reduce consumption | 2 |
| 3 | `generation < 50` | WARNING: low generation | 3 |
| 4 | `consumption > generation` **AND** `battery < 30` | ALERT: low battery + deficit | 2 |
| 5 | `consumption > generation` | ALERT: consumption exceeds generation | 2 |
| 6 | `generation > consumption × 1.5` | SUGGESTION: store excess energy | 4 |
| 7 | Nenhuma condição acima | STATUS: normal operation | 5 |

## 4.3 Priorização de Subsistemas

Quando é necessário reduzir consumo, os subsistemas são desligados em **ordem inversa de prioridade**:

| Ordem de desligamento | Subsistema | Prioridade |
|----------------------|------------|------------|
| 1º a desligar | Non-essential | 4 (menor) |
| 2º a desligar | Laboratory | 3 |
| 3º a desligar | Habitat | 2 |
| NUNCA desliga | Life Support | 1 (máxima) |

## 4.4 Implementação (trecho)

```python
def evaluate_energy_status(total_generation, total_consumption, battery_reserve):
    # Regra 1: CRÍTICO
    if total_generation < 30 and total_consumption > 70:
        return {"level": "CRITICAL", "action": "Activate emergency mode"}
    
    # Regra 2: ALERTA
    if total_generation < 50 and total_consumption > total_generation:
        return {"level": "ALERT", "action": "Reduce consumption"}
    
    # ... demais regras
```

## 4.5 Exemplo de Execução

**Entrada:** geração = 40 kWh, consumo = 55 kWh, bateria = 50 kWh

**Avaliação lógica:**
- Regra 1: `40 < 30` → **FALSO** (não entra)
- Regra 2: `40 < 50` → VERDADEIRO **AND** `55 > 40` → VERDADEIRO → **ATIVA**

**Saída:** `ALERT: Low generation with consumption exceeding production`  
**Ação:** `Reduce consumption — shutdown non-essential systems`

**Conceitos aplicados:** Lógica booleana AND/OR (Cap 2), simplificação algébrica (Cap 2), funções com retorno (Cap 3), if/elif/else encadeado (Cap 3).

---

# 5 MODELO DE PREVISÃO (REGRESSÃO LINEAR)

## 5.1 Método dos Mínimos Quadrados

O sistema utiliza **regressão linear simples** para prever a geração de energia com base em dados climáticos. O modelo encontra a reta que melhor se ajusta aos dados históricos:

```
Y = β₀ + β₁ · X
```

Os coeficientes são calculados por:

```
β₁ = Σ[(xᵢ - x̄)(yᵢ - ȳ)] / Σ[(xᵢ - x̄)²]
β₀ = ȳ - β₁ · x̄
```

## 5.2 Modelos Construídos

| Modelo | X (entrada) | Y (saída) | Uso |
|--------|-------------|-----------|-----|
| Eólico | Velocidade do vento (m/s) | Energia eólica (kWh) | Prever geração eólica |
| Solar | Irradiância (W/m²) | Energia solar (kWh) | Prever geração solar |

## 5.3 Avaliação com R²

O **coeficiente de determinação R²** mede a qualidade do ajuste:
- R² = 1.0 → ajuste perfeito
- R² = 0.0 → modelo não explica a variação

```
R² = 1 - (SSres / SStot)
```

## 5.4 Implementação (trecho principal)

```python
def calculate_linear_regression(x_values, y_values):
    n = len(x_values)
    x_mean = calculate_mean(x_values)
    y_mean = calculate_mean(y_values)
    
    numerator = 0.0
    denominator = 0.0
    for i in range(n):
        x_diff = x_values[i] - x_mean
        y_diff = y_values[i] - y_mean
        numerator += x_diff * y_diff
        denominator += x_diff * x_diff
    
    beta_1 = numerator / denominator
    beta_0 = y_mean - beta_1 * x_mean
    return (beta_0, beta_1)
```

## 5.5 Exemplo de Previsão

**Modelo eólico treinado:** y = 2.15 + 2.83x (R² = 0.89)

**Entrada:** velocidade do vento = 11 m/s  
**Cálculo:** y = 2.15 + 2.83 × 11 = **33.3 kWh**  
**Saída:** Previsão de geração eólica ≈ 33.3 kWh

**Conceitos aplicados:** Regressão linear simples (Cap 7), método dos mínimos quadrados (Cap 7), funções com retorno (Cap 3).

---

# 6 ANÁLISE ENERGÉTICA

## 6.1 Balanço Energético

O sistema compara continuamente:
- **Geração total** = Solar + Eólica
- **Consumo total** = Life Support + Habitat + Laboratory + Non-essential
- **Balanço** = Geração - Consumo (positivo = excedente, negativo = déficit)

## 6.2 Tabela de Resultados (30 dias — gerada pela BST in-order)

| Day | Solar (kWh) | Wind (kWh) | Total Gen. | Consumption | Balance |
|-----|-------------|------------|------------|-------------|---------|
| 01  | 45.2 | 22.1 | 67.3 | 64.0 | +3.3 |
| 02  | 52.8 | 28.4 | 81.2 | 66.6 | +14.6 |
| 03  | 38.1 | 35.6 | 73.7 | 64.9 | +8.8 |
| ... | ... | ... | ... | ... | ... |
| 30  | 57.3 | 22.8 | 80.1 | 66.0 | +14.1 |

## 6.3 Cenários Identificados

| Cenário | Dias ocorridos | Ação tomada |
|---------|---------------|-------------|
| Geração excedente (> 1.5× consumo) | Dias com alta solar + alta eólica | Armazenar excedente |
| Consumo > Geração (déficit) | Dias com baixa irradiância ou vento fraco | Reduzir não-essenciais |
| Operação normal | Maioria dos dias | Sem intervenção |
| Geração crítica | Dias com clima adverso | Modo emergência |

## 6.4 Impacto do Sistema na Colônia

O Aurora Core melhora a gestão de energia da colônia ao:
1. **Antecipar** quedas de geração via regressão (previsão do próximo turno)
2. **Reagir automaticamente** a situações de déficit (regras de decisão)
3. **Priorizar** sistemas vitais (life support nunca é desligado)
4. **Otimizar** armazenamento de excedentes (sugestão de carga de bateria)

---

# 7 ARQUITETURA DO SISTEMA

## 7.1 Estrutura de Módulos

```
aurora-core/
├── data/                       ← Dados de entrada (CSVs)
├── src/
│   ├── data_loader.py          ← Leitura e hierarquia
│   ├── binary_tree.py          ← BST: indexação e busca
│   ├── decision_engine.py      ← Motor de decisão
│   ├── regression_model.py     ← Regressão linear
│   └── report_generator.py     ← Relatório formatado
├── tests/                      ← Testes unitários
└── main.py                     ← Integração
```

## 7.2 Fluxo de Execução

```
[1] Lê CSVs → [2] Monta hierarquia → [3] Constrói BST → [4] Treina modelos
                                            ↓
[7] Exibe relatório ← [6] Faz previsão ← [5] Aplica decisão ← Busca dia na BST
```

## 7.3 Tecnologias

| Item | Escolha | Justificativa |
|------|---------|---------------|
| Linguagem | Python 3.8+ | Requisito do projeto |
| Bibliotecas externas | Nenhuma | Apenas `csv` e `os` (stdlib) |
| Estrutura de dados | Dict + BST | Hierarquia + busca eficiente |
| Versionamento | Git + GitHub | Entregável obrigatório |

---

# 8 RESULTADOS E EXEMPLOS

## 8.1 Execução do Sistema

Comando:
```bash
python main.py
```

## 8.2 Saída Completa (exemplo para dia 15)

```
============================================================
  AURORA CORE — Sistema Inteligente da Colônia
  Fase 3 — Missão Aurora Siger
============================================================

[1/5] Loading telemetry data from CSVs...
      Loaded: 30 energy records
      Loaded: 30 consumption records
      Loaded: 30 climate records

[2/5] Building colony hierarchical structure...
      Colony: Aurora Siger
      Solar system: active
      Wind system:  active

[3/5] Building Binary Search Tree (indexed by day)...
      BST built with 30 nodes
      Tree height: 5 (optimal for 30 nodes: ~5)

[4/5] Training regression models...
      Wind model:  y = 2.15 + 2.83x  (R² = 0.8900)
      Solar model: y = 8.42 + 0.07x  (R² = 0.8500)

[5/5] Generating colony status report...

╔════════════════════════════════════════════════════════╗
║           AURORA SIGER — COLONY STATUS                ║
╠════════════════════════════════════════════════════════╣
║  BST Query: reading from day 15                       ║
║    Solar Generation:     41.7 kWh                     ║
║    Wind Generation:      36.5 kWh                     ║
║    Total Generation:     78.2 kWh                     ║
║    Total Consumption:    66.7 kWh                     ║
║    Battery Reserve:      78.2 kWh                     ║
╠════════════════════════════════════════════════════════╣
║  [SUGGESTION] Generation significantly exceeds...     ║
║  Action: Store excess energy in battery reserve       ║
╠════════════════════════════════════════════════════════╣
║  Predictions (next shift):                            ║
║    Wind:  11.0 m/s  -> 33.3 kWh                      ║
║    Solar: 550.0 W/m² -> 46.9 kWh                     ║
╚════════════════════════════════════════════════════════╝
```

## 8.3 Testes Unitários

```bash
python -m tests.test_binary_tree
python -m tests.test_decision_engine
python -m tests.test_regression_model
```

Todos os testes passam com sucesso, validando:
- Inserção e busca na BST
- Ordenação via in-order traversal
- Todas as regras de decisão
- Cálculos de regressão linear
- Caso degenerado (X constante)

---

# 9 CONCLUSÃO

O projeto Aurora Core demonstra como conceitos fundamentais de ciência da computação podem ser integrados para criar um sistema inteligente funcional:

1. **Estruturas de dados** (listas, dicionários, hierarquia) permitem organizar informações complexas de forma acessível
2. **Árvore Binária de Busca** otimiza a consulta de dados históricos de O(n) para O(log n)
3. **Lógica booleana** transforma dados brutos em decisões claras e acionáveis
4. **Regressão linear** permite antecipar cenários futuros com base em dados passados
5. **Modularização** em funções e arquivos separados garante código limpo e manutenível

O sistema evolui a colônia de um modelo **reativo** (reagir a problemas) para um modelo **preditivo** (antecipar e prevenir), conforme o objetivo final do projeto.

---

# 10 REFERÊNCIAS

- **Cap 1** — A Aurora Estabelece os Primeiros Sistemas da Colônia (Contexto do Projeto)
- **Cap 2** — A Estrutura de Armazenamento Organizando os Dados (Lógica Booleana)
- **Cap 3** — A Lógica Estruturada que Dá Forma às Soluções (Funções e Recursividade)
- **Cap 4** — As Estruturas Avançadas que Rastreiam Recursos (BST, AVL, Hash)
- **Cap 7** — A Regressão Inicial que Permite Prever Variáveis (Regressão Linear)
- **Cap 8** — As Fontes Renováveis que Alimentam os Sistemas (Energia Solar e Eólica)
