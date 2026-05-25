"""
report_generator.py — Geração do relatório de status da colônia.

Consolida os dados processados pelos módulos de decisão, regressão e BST
e exibe um painel de status formatado no terminal.
"""


BORDER_CHAR = "═"
CORNER_TL = "╔"
CORNER_TR = "╗"
CORNER_BL = "╚"
CORNER_BR = "╝"
SIDE = "║"
SEPARATOR_L = "╠"
SEPARATOR_R = "╣"
WIDTH = 56


def generate_full_report(day_summary: dict, decision: dict,
                         wind_prediction: dict, solar_prediction: dict,
                         ordered_history: list, wind_model: dict,
                         solar_model: dict) -> str:
    """
    Gera o relatório completo de status da colônia.

    Args:
        day_summary: Resumo do dia consultado.
        decision: Resultado do motor de decisão.
        wind_prediction: Previsão de energia eólica.
        solar_prediction: Previsão de energia solar.
        ordered_history: Histórico ordenado (in-order da BST).
        wind_model: Coeficientes do modelo eólico.
        solar_model: Coeficientes do modelo solar.

    Returns:
        String formatada com o relatório completo.
    """
    lines = []

    lines.append(_top_border())
    lines.append(_center_text("AURORA SIGER — COLONY STATUS"))
    lines.append(_separator())

    lines.append(_format_line(f"  BST Query: reading from day {day_summary['day']}"))
    lines.append(_format_line(f"    Solar Generation:   {day_summary['solar_generation_kwh']:>6.1f} kWh"))
    lines.append(_format_line(f"    Wind Generation:    {day_summary['wind_generation_kwh']:>6.1f} kWh"))
    lines.append(_format_line(f"    Total Generation:   {day_summary['total_generation_kwh']:>6.1f} kWh"))
    lines.append(_format_line(f"    Total Consumption:  {day_summary['total_consumption_kwh']:>6.1f} kWh"))
    lines.append(_format_line(f"    Battery Reserve:    {day_summary['battery_reserve_kwh']:>6.1f} kWh"))
    lines.append(_separator())

    lines.append(_format_line(f"  [{decision['level']}] {decision['message']}"))
    lines.append(_format_line(f"  Action: {decision['action']}"))
    lines.append(_separator())

    lines.append(_format_line("  Regression Models:"))
    lines.append(_format_line(f"    Wind:  y = {wind_model['beta_0']:.2f} + {wind_model['beta_1']:.2f}x  (R²={wind_model['r_squared']:.3f})"))
    lines.append(_format_line(f"    Solar: y = {solar_model['beta_0']:.2f} + {solar_model['beta_1']:.2f}x  (R²={solar_model['r_squared']:.3f})"))
    lines.append(_format_line(""))
    lines.append(_format_line("  Predictions (next shift):"))
    lines.append(_format_line(f"    Wind:  {wind_prediction['x_value']:.1f} m/s  -> {wind_prediction['predicted_kwh']:.1f} kWh"))
    lines.append(_format_line(f"    Solar: {solar_prediction['x_value']:.1f} W/m² -> {solar_prediction['predicted_kwh']:.1f} kWh"))
    lines.append(_separator())

    lines.append(_format_line("  Ordered History (BST in-order traversal):"))
    display_count = min(5, len(ordered_history))
    for i in range(display_count):
        day, data = ordered_history[i]
        solar = data["solar_generation_kwh"]
        wind = data["wind_generation_kwh"]
        lines.append(_format_line(f"    Day {day:02d} | Solar: {solar:>5.1f} | Wind: {wind:>5.1f} kWh"))

    if len(ordered_history) > display_count:
        lines.append(_format_line(f"    ... ({len(ordered_history)} days total)"))

    lines.append(_bottom_border())

    return "\n".join(lines)


def generate_summary_table(ordered_history: list) -> str:
    """
    Gera tabela resumida de todo o histórico.

    Args:
        ordered_history: Lista de tuplas (day, data) da BST.

    Returns:
        String formatada com tabela.
    """
    lines = []
    header = f"{'Day':>4} | {'Solar':>7} | {'Wind':>7} | {'Total':>7} | {'Consumption':>12} | {'Balance':>8}"
    lines.append(header)
    lines.append("-" * len(header))

    for day, data in ordered_history:
        solar = data["solar_generation_kwh"]
        wind = data["wind_generation_kwh"]
        total_gen = solar + wind
        total_cons = (
            data["life_support_kwh"]
            + data["habitat_kwh"]
            + data["laboratory_kwh"]
            + data["non_essential_kwh"]
        )
        balance = total_gen - total_cons
        lines.append(
            f"{day:>4} | {solar:>7.1f} | {wind:>7.1f} | {total_gen:>7.1f} | {total_cons:>12.1f} | {balance:>+8.1f}"
        )

    return "\n".join(lines)


def _top_border() -> str:
    """Gera borda superior."""
    return CORNER_TL + BORDER_CHAR * WIDTH + CORNER_TR


def _bottom_border() -> str:
    """Gera borda inferior."""
    return CORNER_BL + BORDER_CHAR * WIDTH + CORNER_BR


def _separator() -> str:
    """Gera separador horizontal."""
    return SEPARATOR_L + BORDER_CHAR * WIDTH + SEPARATOR_R


def _format_line(text: str) -> str:
    """Formata uma linha com bordas laterais."""
    return SIDE + text.ljust(WIDTH) + SIDE


def _center_text(text: str) -> str:
    """Centraliza texto entre bordas."""
    return SIDE + text.center(WIDTH) + SIDE
