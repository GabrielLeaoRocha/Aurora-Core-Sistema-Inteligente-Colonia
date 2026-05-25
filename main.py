"""
main.py — Aurora Core: Sistema Inteligente da Colônia.

Ponto de entrada do sistema. Interface interativa que exibe:
  - Resumo do dia atual (último dia de dados)
  - Previsões para o próximo dia
  - Menu para busca de dias específicos via BST em tempo real
"""

from src.data_loader import (
    load_energy_data,
    load_consumption_data,
    load_climate_data,
    build_colony_structure,
    get_day_summary,
    navigate_hierarchy,
)
from src.binary_tree import build_bst, search, in_order_traversal, get_tree_height
from src.decision_engine import evaluate_energy_status, evaluate_subsystem_priority
from src.regression_model import (
    build_wind_model,
    build_solar_model,
    predict,
)
from src.report_generator import generate_summary_table


TOTAL_DAYS = 30


def clear_screen():
    """Limpa o terminal."""
    import os
    os.system("cls" if os.name == "nt" else "clear")


def print_header():
    """Exibe o cabeçalho do sistema."""
    print("\n╔════════════════════════════════════════════════════════╗")
    print("║         AURORA CORE — Colony Intelligence System       ║")
    print("║              Missão Aurora Siger · Fase 3              ║")
    print("╚════════════════════════════════════════════════════════╝")


def print_day_report(day_data: dict, decision: dict, shutdown_list: list):
    """
    Exibe o relatório detalhado de um dia.

    Args:
        day_data: Resumo do dia.
        decision: Decisão do motor lógico.
        shutdown_list: Lista de subsistemas a desligar.
    """
    day = day_data["day"]
    balance = day_data["total_generation_kwh"] - day_data["total_consumption_kwh"]
    balance_symbol = "+" if balance >= 0 else ""

    print(f"\n  ┌─────────────────────────────────────────────────┐")
    print(f"  │  DAY {day:02d} — Telemetry Summary                    │")
    print(f"  ├─────────────────────────────────────────────────┤")
    print(f"  │  GENERATION                                     │")
    print(f"  │    Solar:           {day_data['solar_generation_kwh']:>7.1f} kWh              │")
    print(f"  │    Wind:            {day_data['wind_generation_kwh']:>7.1f} kWh              │")
    print(f"  │    Total:           {day_data['total_generation_kwh']:>7.1f} kWh              │")
    print(f"  │                                                 │")
    print(f"  │  CONSUMPTION                                    │")
    print(f"  │    Life Support:    {day_data['life_support_kwh']:>7.1f} kWh  [P1]          │")
    print(f"  │    Habitat:         {day_data['habitat_kwh']:>7.1f} kWh  [P2]          │")
    print(f"  │    Laboratory:      {day_data['laboratory_kwh']:>7.1f} kWh  [P3]          │")
    print(f"  │    Non-essential:   {day_data['non_essential_kwh']:>7.1f} kWh  [P4]          │")
    print(f"  │    Total:           {day_data['total_consumption_kwh']:>7.1f} kWh              │")
    print(f"  │                                                 │")
    print(f"  │  BALANCE:          {balance_symbol}{balance:>7.1f} kWh              │")
    print(f"  │  Battery Reserve:  {day_data['battery_reserve_kwh']:>7.1f} kWh              │")
    print(f"  ├─────────────────────────────────────────────────┤")
    print(f"  │  CLIMATE                                        │")
    print(f"  │    Wind Speed:      {day_data['wind_speed_ms']:>7.1f} m/s              │")
    print(f"  │    Temperature:     {day_data['temperature_c']:>7.1f} °C               │")
    print(f"  │    Irradiance:      {day_data['irradiance_wm2']:>7.1f} W/m²             │")
    print(f"  ├─────────────────────────────────────────────────┤")
    print(f"  │  DECISION: [{decision['level']}]")
    print(f"  │  {decision['message']}")
    print(f"  │  Action: {decision['action']}")

    if shutdown_list:
        print(f"  │  Shutdown: {', '.join(shutdown_list)}")

    print(f"  └─────────────────────────────────────────────────┘")


def print_predictions(wind_model: dict, solar_model: dict,
                      last_climate: dict):
    """
    Exibe previsões para o próximo dia baseadas no último clima.

    Args:
        wind_model: Modelo de regressão eólica.
        solar_model: Modelo de regressão solar.
        last_climate: Dados climáticos do último dia.
    """
    wind_speed = last_climate["wind_speed_ms"]
    irradiance = last_climate["irradiance_wm2"]

    predicted_wind = predict(wind_speed, wind_model["beta_0"], wind_model["beta_1"])
    predicted_solar = predict(irradiance, solar_model["beta_0"], solar_model["beta_1"])
    predicted_total = predicted_wind + predicted_solar

    print(f"\n  ┌─────────────────────────────────────────────────┐")
    print(f"  │  PREDICTIONS — Next Day (Day 31)                 │")
    print(f"  │  Based on last climate readings                  │")
    print(f"  ├─────────────────────────────────────────────────┤")
    print(f"  │  Wind Model:  y = {wind_model['beta_0']:.2f} + {wind_model['beta_1']:.2f}x")
    print(f"  │               R² = {wind_model['r_squared']:.4f}")
    print(f"  │  Input:       wind = {wind_speed:.1f} m/s")
    print(f"  │  Predicted:   wind energy ≈ {predicted_wind:.1f} kWh")
    print(f"  │                                                 │")
    print(f"  │  Solar Model: y = {solar_model['beta_0']:.2f} + {solar_model['beta_1']:.2f}x")
    print(f"  │               R² = {solar_model['r_squared']:.4f}")
    print(f"  │  Input:       irradiance = {irradiance:.1f} W/m²")
    print(f"  │  Predicted:   solar energy ≈ {predicted_solar:.1f} kWh")
    print(f"  │                                                 │")
    print(f"  │  TOTAL PREDICTED GENERATION ≈ {predicted_total:.1f} kWh")
    print(f"  └─────────────────────────────────────────────────┘")


def print_menu():
    """Exibe o menu interativo."""
    print("\n  ╔═══════════════════════════════════════╗")
    print("  ║            MENU PRINCIPAL             ║")
    print("  ╠═══════════════════════════════════════╣")
    print("  ║  [1] Search day (BST lookup)          ║")
    print("  ║  [2] Show full history table          ║")
    print("  ║  [3] Show current day summary         ║")
    print("  ║  [4] Show predictions (next day)      ║")
    print("  ║  [5] System info                      ║")
    print("  ║  [0] Exit                             ║")
    print("  ╚═══════════════════════════════════════╝")


def handle_search(bst_root):
    """
    Realiza busca na BST pelo dia informado pelo usuário.

    Args:
        bst_root: Raiz da BST.
    """
    print("\n  ── BST Search ──────────────────────────────────────")

    try:
        day_input = input("  Enter day (1-30): ").strip()
        day = int(day_input)
    except (ValueError, EOFError):
        print("  [ERROR] Invalid input. Please enter a number between 1 and 30.")
        return

    if day < 1 or day > TOTAL_DAYS:
        print(f"  [ERROR] Day must be between 1 and {TOTAL_DAYS}.")
        return

    print(f"\n  Searching BST for day {day}...")
    print(f"  Traversal path:")

    day_data = _search_with_trace(bst_root, day)

    if day_data is None:
        print(f"  [ERROR] Day {day} not found in BST.")
        return

    decision = evaluate_energy_status(
        total_generation=day_data["total_generation_kwh"],
        total_consumption=day_data["total_consumption_kwh"],
        battery_reserve=day_data["battery_reserve_kwh"]
    )
    shutdown_list = evaluate_subsystem_priority(
        total_generation=day_data["total_generation_kwh"],
        total_consumption=day_data["total_consumption_kwh"]
    )

    print_day_report(day_data, decision, shutdown_list)


def _search_with_trace(root, day: int, depth: int = 1):
    """
    Busca na BST exibindo o caminho percorrido.

    Args:
        root: Nó atual.
        day: Dia a buscar.
        depth: Profundidade atual.

    Returns:
        Dados do dia ou None.
    """
    if root is None:
        return None

    indent = "    " * depth

    if day == root.day:
        print(f"{indent}→ Node [day {root.day:02d}]: FOUND ✓  (depth {depth})")
        return root.data
    elif day < root.day:
        print(f"{indent}→ Node [day {root.day:02d}]: {day} < {root.day} → go LEFT")
        return _search_with_trace(root.left, day, depth + 1)
    else:
        print(f"{indent}→ Node [day {root.day:02d}]: {day} > {root.day} → go RIGHT")
        return _search_with_trace(root.right, day, depth + 1)


def handle_history(bst_root):
    """
    Exibe tabela completa do histórico via in-order traversal.

    Args:
        bst_root: Raiz da BST.
    """
    ordered_history = in_order_traversal(bst_root)
    print("\n  ── Full History (BST in-order traversal) ───────────\n")
    print(generate_summary_table(ordered_history))


def handle_system_info(colony: dict, bst_root, wind_model: dict,
                       solar_model: dict):
    """
    Exibe informações do sistema.

    Args:
        colony: Estrutura hierárquica.
        bst_root: Raiz da BST.
        wind_model: Modelo eólico.
        solar_model: Modelo solar.
    """
    tree_height = get_tree_height(bst_root)

    print(f"\n  ── System Info ─────────────────────────────────────")
    print(f"  Colony:        {colony['name']}")
    print(f"  Solar status:  {navigate_hierarchy(colony, ['systems', 'energy', 'solar', 'status'])}")
    print(f"  Wind status:   {navigate_hierarchy(colony, ['systems', 'energy', 'wind', 'status'])}")
    print(f"  BST height:    {tree_height} levels")
    print(f"  Total records: {TOTAL_DAYS} days")
    print(f"  Max BST ops:   {tree_height} comparisons (O(log n))")
    print(f"  Wind model:    y = {wind_model['beta_0']:.2f} + {wind_model['beta_1']:.2f}x  (R²={wind_model['r_squared']:.4f})")
    print(f"  Solar model:   y = {solar_model['beta_0']:.2f} + {solar_model['beta_1']:.2f}x  (R²={solar_model['r_squared']:.4f})")


def initialize_system():
    """
    Carrega dados, constrói estruturas e treina modelos.

    Returns:
        Tupla com (bst_root, colony, wind_model, solar_model, climate_data).
    """
    print("  Loading telemetry data...")
    energy_data = load_energy_data()
    consumption_data = load_consumption_data()
    climate_data = load_climate_data()
    print(f"  ✓ {len(energy_data)} records loaded per dataset")

    print("  Building hierarchical structure...")
    colony = build_colony_structure(energy_data, consumption_data, climate_data)
    print(f"  ✓ Colony '{colony['name']}' structured")

    print("  Building BST (indexed by day)...")
    all_readings = []
    for i in range(len(energy_data)):
        day_data = get_day_summary(energy_data, consumption_data, climate_data, i + 1)
        all_readings.append(day_data)

    bst_root = build_bst(all_readings)
    tree_height = get_tree_height(bst_root)
    print(f"  ✓ BST built: {len(all_readings)} nodes, height {tree_height}")

    print("  Training regression models...")
    wind_model = build_wind_model(climate_data, energy_data)
    solar_model = build_solar_model(climate_data, energy_data)
    print(f"  ✓ Wind model R²={wind_model['r_squared']:.4f}")
    print(f"  ✓ Solar model R²={solar_model['r_squared']:.4f}")

    return bst_root, colony, wind_model, solar_model, climate_data


def main():
    """Executa o sistema Aurora Core com interface interativa."""
    clear_screen()
    print_header()

    print("\n  Initializing systems...\n")
    bst_root, colony, wind_model, solar_model, climate_data = initialize_system()

    print("\n  ════════════════════════════════════════════════════")
    print("  System ready. Displaying current status...")
    print("  ════════════════════════════════════════════════════")

    # --- RESUMO DO DIA ATUAL (último dia) ---
    current_day = search(bst_root, TOTAL_DAYS)
    decision = evaluate_energy_status(
        total_generation=current_day["total_generation_kwh"],
        total_consumption=current_day["total_consumption_kwh"],
        battery_reserve=current_day["battery_reserve_kwh"]
    )
    shutdown_list = evaluate_subsystem_priority(
        total_generation=current_day["total_generation_kwh"],
        total_consumption=current_day["total_consumption_kwh"]
    )

    print_day_report(current_day, decision, shutdown_list)

    # --- PREVISÕES PARA O PRÓXIMO DIA ---
    last_climate = climate_data[-1]
    print_predictions(wind_model, solar_model, last_climate)

    # --- LOOP INTERATIVO ---
    while True:
        print_menu()

        try:
            choice = input("\n  Select option: ").strip()
        except (EOFError, KeyboardInterrupt):
            break

        if choice == "1":
            handle_search(bst_root)
        elif choice == "2":
            handle_history(bst_root)
        elif choice == "3":
            print_day_report(current_day, decision, shutdown_list)
        elif choice == "4":
            print_predictions(wind_model, solar_model, last_climate)
        elif choice == "5":
            handle_system_info(colony, bst_root, wind_model, solar_model)
        elif choice == "0":
            print("\n  Aurora Core — Shutting down. Goodbye.")
            break
        else:
            print("  [ERROR] Invalid option. Please select 0-5.")


if __name__ == "__main__":
    main()
