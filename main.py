"""
main.py — Aurora Core: Sistema Inteligente da Colônia.

Ponto de entrada do sistema. Integra todos os módulos:
  1. data_loader     → Leitura dos CSVs e organização hierárquica
  2. binary_tree     → BST para indexação e busca eficiente por dia
  3. decision_engine → Regras de decisão lógica (AND/OR)
  4. regression_model→ Previsão de energia por regressão linear
  5. report_generator→ Exibição do relatório consolidado
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
from src.report_generator import generate_full_report, generate_summary_table


def main():
    """Executa o sistema Aurora Core."""
    print("\n" + "=" * 60)
    print("  AURORA CORE — Sistema Inteligente da Colônia")
    print("  Fase 3 — Missão Aurora Siger")
    print("=" * 60 + "\n")

    # --- 1. CARREGAMENTO DOS DADOS ---
    print("[1/5] Loading telemetry data from CSVs...")
    energy_data = load_energy_data()
    consumption_data = load_consumption_data()
    climate_data = load_climate_data()
    print(f"      Loaded: {len(energy_data)} energy records")
    print(f"      Loaded: {len(consumption_data)} consumption records")
    print(f"      Loaded: {len(climate_data)} climate records")

    # --- 2. ESTRUTURA HIERÁRQUICA ---
    print("\n[2/5] Building colony hierarchical structure...")
    colony = build_colony_structure(energy_data, consumption_data, climate_data)
    solar_status = navigate_hierarchy(colony, ["systems", "energy", "solar", "status"])
    wind_status = navigate_hierarchy(colony, ["systems", "energy", "wind", "status"])
    print(f"      Colony: {colony['name']}")
    print(f"      Solar system: {solar_status}")
    print(f"      Wind system:  {wind_status}")

    # --- 3. CONSTRUÇÃO DA BST ---
    print("\n[3/5] Building Binary Search Tree (indexed by day)...")
    all_readings = []
    for i in range(len(energy_data)):
        day_data = get_day_summary(energy_data, consumption_data, climate_data, i + 1)
        all_readings.append(day_data)

    bst_root = build_bst(all_readings)
    tree_height = get_tree_height(bst_root)
    print(f"      BST built with {len(all_readings)} nodes")
    print(f"      Tree height: {tree_height} (optimal for 30 nodes: ~5)")

    # --- 4. MODELOS DE REGRESSÃO ---
    print("\n[4/5] Training regression models...")
    wind_model = build_wind_model(climate_data, energy_data)
    solar_model = build_solar_model(climate_data, energy_data)
    print(f"      Wind model:  y = {wind_model['beta_0']:.2f} + {wind_model['beta_1']:.2f}x  (R² = {wind_model['r_squared']:.4f})")
    print(f"      Solar model: y = {solar_model['beta_0']:.2f} + {solar_model['beta_1']:.2f}x  (R² = {solar_model['r_squared']:.4f})")

    # --- 5. CONSULTA E DECISÃO ---
    print("\n[5/5] Generating colony status report...")

    query_day = 15
    day_summary = search(bst_root, query_day)

    if day_summary is None:
        print(f"  ERROR: Day {query_day} not found in BST.")
        return

    decision = evaluate_energy_status(
        total_generation=day_summary["total_generation_kwh"],
        total_consumption=day_summary["total_consumption_kwh"],
        battery_reserve=day_summary["battery_reserve_kwh"]
    )

    shutdown_list = evaluate_subsystem_priority(
        total_generation=day_summary["total_generation_kwh"],
        total_consumption=day_summary["total_consumption_kwh"]
    )

    next_wind_speed = 11.0
    next_irradiance = 550.0

    wind_prediction = {
        "x_value": next_wind_speed,
        "predicted_kwh": round(predict(next_wind_speed, wind_model["beta_0"], wind_model["beta_1"]), 1)
    }
    solar_prediction = {
        "x_value": next_irradiance,
        "predicted_kwh": round(predict(next_irradiance, solar_model["beta_0"], solar_model["beta_1"]), 1)
    }

    ordered_history = in_order_traversal(bst_root)

    # --- RELATÓRIO FINAL ---
    report = generate_full_report(
        day_summary=day_summary,
        decision=decision,
        wind_prediction=wind_prediction,
        solar_prediction=solar_prediction,
        ordered_history=ordered_history,
        wind_model=wind_model,
        solar_model=solar_model
    )

    print("\n" + report)

    if shutdown_list:
        print(f"\n  Subsystems recommended for shutdown: {shutdown_list}")

    # --- TABELA RESUMIDA ---
    print("\n" + "=" * 60)
    print("  FULL HISTORY TABLE (BST in-order traversal)")
    print("=" * 60 + "\n")
    print(generate_summary_table(ordered_history))

    print("\n" + "=" * 60)
    print("  Aurora Core — Execution completed successfully.")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
