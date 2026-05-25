# Aurora Core — Sistema Inteligente da Colônia

**Curso:** Engenharia de Software — FIAP  
**Turma:** 1ESPR  
**Fase:** 3 — Missão Aurora Siger  
**Integrantes:** Gabriel de Leão Rocha (RM 571330)

---

## O que é

O **Aurora Core** é o módulo computacional inteligente da colônia Aurora Siger. Ele lê dados de telemetria (energia, consumo e clima) armazenados em CSV, organiza as informações em estruturas hierárquicas, indexa as leituras em uma Árvore Binária de Busca (BST) para consulta eficiente, aplica regras de decisão lógica (AND/OR), realiza previsões de geração de energia por regressão linear e apresenta tudo em uma **interface interativa** no terminal.

---

## Funcionalidades

| Funcionalidade | Descrição |
|----------------|-----------|
| Organização hierárquica | Dados estruturados em 3 níveis: Colônia → Sistemas → Subsistemas |
| BST (Árvore Binária de Busca) | Indexação dos 30 dias por chave, busca em O(log n) |
| Regras de decisão | Lógica booleana (AND/OR) para gerar alertas automáticos |
| Regressão linear | Previsão de geração eólica e solar baseada em dados climáticos |
| Interface interativa | Menu com busca em tempo real e visualização do caminho na BST |

---

## Estrutura do Projeto

```
aurora-core/
├── data/
│   ├── telemetry_energy.csv        # Geração solar + eólica + bateria (30 dias)
│   ├── telemetry_consumption.csv   # Consumo por subsistema (30 dias)
│   └── telemetry_climate.csv       # Vento, temperatura, irradiância (30 dias)
├── src/
│   ├── __init__.py
│   ├── data_loader.py              # Leitura dos CSVs e estrutura hierárquica
│   ├── binary_tree.py              # BST: inserção, busca, traversal
│   ├── decision_engine.py          # Motor de decisão (regras booleanas)
│   ├── regression_model.py         # Regressão linear (mínimos quadrados)
│   └── report_generator.py         # Tabelas formatadas
├── tests/
│   ├── __init__.py
│   ├── test_binary_tree.py
│   ├── test_decision_engine.py
│   └── test_regression_model.py
├── main.py                         # Ponto de entrada (interface interativa)
├── requirements.txt
└── README.md
```

---

## Como Executar

**Requisitos:** Python 3.8+ (sem dependências externas)

```bash
# Clonar o repositório
git clone https://github.com/GabrielLeaoRocha/Aurora-Core-Sistema-Inteligente-Colonia.git
cd Aurora-Core-Sistema-Inteligente-Colonia

# Executar o sistema
python3 main.py
```

---

## Como Funciona

### 1. Organização dos Dados

Os dados de telemetria são lidos dos CSVs e organizados em uma **hierarquia de dicionários**:

```
Colony "Aurora Siger"
├── Energy
│   ├── Solar (geração diária em kWh)
│   └── Wind (geração diária em kWh)
├── Consumption
│   ├── Life Support [P1 - nunca desliga]
│   ├── Habitat [P2]
│   ├── Laboratory [P3]
│   └── Non-essential [P4 - primeiro a desligar]
└── Climate
    ├── Wind Speed (m/s)
    ├── Temperature (°C)
    └── Irradiance (W/m²)
```

### 2. Árvore Binária de Busca (BST)

As 30 leituras diárias são indexadas em uma BST balanceada (altura = 5), permitindo buscar qualquer dia com no máximo **5 comparações** em vez de 30:

```
Busca pelo dia 12:
  → Node [day 15]: 12 < 15 → go LEFT
      → Node [day 07]: 12 > 7 → go RIGHT
          → Node [day 11]: 12 > 11 → go RIGHT
              → Node [day 13]: 12 < 13 → go LEFT
                  → Node [day 12]: FOUND ✓  (5 comparações)
```

### 3. Regras de Decisão

O sistema avalia as condições energéticas e gera decisões automáticas:

| Condição | Decisão |
|----------|---------|
| `geração < 30` AND `consumo > 70` | CRITICAL: modo emergência |
| `geração < 50` AND `consumo > geração` | ALERT: reduzir consumo |
| `consumo > geração` AND `bateria < 30` | ALERT: bateria baixa |
| `geração > consumo × 1.5` | SUGGESTION: armazenar excedente |
| Nenhuma condição acima | STATUS: operação normal |

### 4. Previsão por Regressão Linear

Dois modelos treinados com dados históricos:

- **Eólico:** `energia = -0.10 + 2.96 × velocidade_vento` (R² = 0.9992)
- **Solar:** `energia = -4.14 + 0.10 × irradiância` (R² = 0.9904)

---

## Exemplos de Entrada e Saída

### Exemplo 1 — Tela inicial (resumo automático)

O sistema exibe o status do último dia ao iniciar:

**Entrada (dados do CSV — Day 30):**
- Geração solar: 57.3 kWh | Eólica: 22.8 kWh | Total: 80.1 kWh
- Consumo total: 66.0 kWh
- Bateria: 60.1 kWh

**Saída:**
```
DECISION: [STATUS]
All systems operating within normal parameters
Action: Normal operation — no action required
```

### Exemplo 2 — Previsão para o próximo dia

**Entrada (clima do Day 30):**
- Vento: 7.7 m/s
- Irradiância: 610.5 W/m²

**Saída:**
```
Predicted wind energy ≈ 22.7 kWh
Predicted solar energy ≈ 56.2 kWh
TOTAL PREDICTED GENERATION ≈ 78.9 kWh
```

### Exemplo 3 — Busca interativa (BST)

**Entrada do operador:** `dia = 12`

**Saída:**
```
Searching BST for day 12...
Traversal path:
    → Node [day 15]: 12 < 15 → go LEFT
        → Node [day 07]: 12 > 7 → go RIGHT
            → Node [day 11]: 12 > 11 → go RIGHT
                → Node [day 13]: 12 < 13 → go LEFT
                    → Node [day 12]: FOUND ✓  (depth 5)

DAY 12 — Telemetry Summary
  Solar: 58.2 kWh | Wind: 20.5 kWh | Total: 78.7 kWh
  Consumption: 70.9 kWh | Balance: +7.8 kWh
  DECISION: [STATUS] Normal operation
```

### Exemplo 4 — Cenário de alerta

**Entrada (hipotética):** `geração = 40 kWh`, `consumo = 55 kWh`

**Saída:**
```
DECISION: [ALERT]
Low generation with consumption exceeding production
Action: Reduce consumption — shutdown non-essential systems
Shutdown: non_essential, laboratory
```

---

## Testes

```bash
python3 -m tests.test_binary_tree
python3 -m tests.test_decision_engine
python3 -m tests.test_regression_model
```

Todos os testes passam com sucesso.

---

## Conceitos Aplicados

| Capítulo | Conceito | Onde é usado |
|----------|----------|--------------|
| Cap 1 | Contexto da colônia, autonomia | Projeto inteiro |
| Cap 2 | Lógica booleana (AND/OR) | `decision_engine.py` |
| Cap 3 | Funções, recursividade, modularização | Todos os módulos |
| Cap 4 | BST, complexidade O(log n) | `binary_tree.py` |
| Cap 7 | Regressão linear simples | `regression_model.py` |
| Cap 8 | Energia solar e eólica | Dados de telemetria |

---

## Licença

Projeto acadêmico — FIAP 2025.
