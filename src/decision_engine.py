"""
decision_engine.py — Motor de decisões lógicas da colônia.

Aplica regras booleanas combinadas (AND/OR) para gerar ações automáticas
baseadas nos níveis de geração e consumo de energia da colônia.
"""


PRIORITY_CRITICAL = 1
PRIORITY_ALERT = 2
PRIORITY_WARNING = 3
PRIORITY_SUGGESTION = 4
PRIORITY_NORMAL = 5


def evaluate_energy_status(total_generation: float,
                           total_consumption: float,
                           battery_reserve: float) -> dict:
    """
    Avalia o status energético e retorna a decisão do sistema.

    Regras de decisão (em ordem de prioridade):
    1. Geração < 30 AND consumo > 70 → CRÍTICO
    2. Geração < 50 AND consumo > geração → ALERTA
    3. Geração < 50 → ATENÇÃO
    4. Consumo > geração AND reserva < 30 → ALERTA
    5. Consumo > geração → ALERTA
    6. Geração > consumo * 1.5 → SUGESTÃO
    7. Padrão → NORMAL

    Args:
        total_generation: Geração total de energia (kWh).
        total_consumption: Consumo total de energia (kWh).
        battery_reserve: Reserva atual da bateria (kWh).

    Returns:
        Dicionário com level, priority, message e action.
    """
    if total_generation < 30 and total_consumption > 70:
        return _build_decision(
            level="CRITICAL",
            priority=PRIORITY_CRITICAL,
            message="Generation critically low with high consumption",
            action="Activate emergency mode — shutdown all non-essential systems"
        )

    if total_generation < 50 and total_consumption > total_generation:
        return _build_decision(
            level="ALERT",
            priority=PRIORITY_ALERT,
            message="Low generation with consumption exceeding production",
            action="Reduce consumption — shutdown non-essential systems"
        )

    if total_generation < 50:
        return _build_decision(
            level="WARNING",
            priority=PRIORITY_WARNING,
            message="Generation below optimal threshold",
            action="Monitor systems — prepare for possible reduction"
        )

    if total_consumption > total_generation and battery_reserve < 30:
        return _build_decision(
            level="ALERT",
            priority=PRIORITY_ALERT,
            message="Consumption exceeds generation with low battery reserve",
            action="Reduce consumption — prioritize life support"
        )

    if total_consumption > total_generation:
        return _build_decision(
            level="ALERT",
            priority=PRIORITY_ALERT,
            message="Consumption exceeds generation",
            action="Reduce non-essential consumption"
        )

    if total_generation > total_consumption * 1.5:
        return _build_decision(
            level="SUGGESTION",
            priority=PRIORITY_SUGGESTION,
            message="Generation significantly exceeds consumption",
            action="Store excess energy in battery reserve"
        )

    return _build_decision(
        level="STATUS",
        priority=PRIORITY_NORMAL,
        message="All systems operating within normal parameters",
        action="Normal operation — no action required"
    )


def evaluate_subsystem_priority(total_generation: float,
                                total_consumption: float) -> list:
    """
    Determina quais subsistemas devem ser desligados em ordem de prioridade.

    Subsistemas (ordem de desligamento — menor prioridade primeiro):
    4. Non-essential (primeiro a desligar)
    3. Laboratory
    2. Habitat
    1. Life support (nunca desligar)

    Args:
        total_generation: Geração total.
        total_consumption: Consumo total.

    Returns:
        Lista de subsistemas a desligar (vazia se operação normal).
    """
    shutdown_list = []

    if total_generation >= total_consumption:
        return shutdown_list

    deficit = total_consumption - total_generation

    subsystems_by_priority = [
        {"name": "non_essential", "priority": 4, "avg_consumption": 9.5},
        {"name": "laboratory", "priority": 3, "avg_consumption": 13.2},
        {"name": "habitat", "priority": 2, "avg_consumption": 18.0},
    ]

    accumulated_savings = 0.0
    for subsystem in subsystems_by_priority:
        if accumulated_savings >= deficit:
            break
        shutdown_list.append(subsystem["name"])
        accumulated_savings += subsystem["avg_consumption"]

    return shutdown_list


def _build_decision(level: str, priority: int, message: str, action: str) -> dict:
    """
    Constrói o dicionário de decisão padronizado.

    Args:
        level: Nível de severidade.
        priority: Prioridade numérica (1 = mais urgente).
        message: Descrição da situação.
        action: Ação recomendada.

    Returns:
        Dicionário de decisão.
    """
    return {
        "level": level,
        "priority": priority,
        "message": message,
        "action": action
    }
