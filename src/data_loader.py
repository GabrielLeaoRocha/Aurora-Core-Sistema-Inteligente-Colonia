"""
data_loader.py — Leitura de CSVs e organização hierárquica dos dados da colônia.

Responsável por carregar os arquivos de telemetria e montar a estrutura
hierárquica que representa os sistemas da colônia Aurora Siger.
"""

import csv
import os


DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")


def load_csv(filepath: str) -> list:
    """
    Carrega um arquivo CSV e retorna uma lista de dicionários.

    Args:
        filepath: Caminho completo do arquivo CSV.

    Returns:
        Lista de dicionários (cada linha é um dict com headers como chave).
    """
    records = []

    with open(filepath, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            parsed_row = {}
            for key, value in row.items():
                try:
                    parsed_row[key] = int(value) if "." not in value else float(value)
                except ValueError:
                    parsed_row[key] = value
            records.append(parsed_row)

    return records


def load_energy_data() -> list:
    """Carrega dados de geração de energia."""
    return load_csv(os.path.join(DATA_DIR, "telemetry_energy.csv"))


def load_consumption_data() -> list:
    """Carrega dados de consumo por subsistema."""
    return load_csv(os.path.join(DATA_DIR, "telemetry_consumption.csv"))


def load_climate_data() -> list:
    """Carrega dados climáticos."""
    return load_csv(os.path.join(DATA_DIR, "telemetry_climate.csv"))


def build_colony_structure(energy_data: list, consumption_data: list,
                           climate_data: list) -> dict:
    """
    Constrói a estrutura hierárquica da colônia.

    Organiza os dados em 3 níveis:
      - Nível 0: Colônia (raiz)
      - Nível 1: Sistemas (energy, consumption, climate)
      - Nível 2: Subsistemas (solar, wind, life_support, etc.)

    Args:
        energy_data: Lista de registros de energia.
        consumption_data: Lista de registros de consumo.
        climate_data: Lista de registros climáticos.

    Returns:
        Dicionário representando a hierarquia da colônia.
    """
    colony = {
        "name": "Aurora Siger",
        "systems": {
            "energy": {
                "solar": {
                    "generation_kwh": [r["solar_generation_kwh"] for r in energy_data],
                    "status": "active"
                },
                "wind": {
                    "generation_kwh": [r["wind_generation_kwh"] for r in energy_data],
                    "status": "active"
                },
                "battery": {
                    "reserve_kwh": [r["battery_reserve_kwh"] for r in energy_data],
                    "status": "active"
                }
            },
            "consumption": {
                "life_support": {
                    "consumption_kwh": [r["life_support_kwh"] for r in consumption_data],
                    "priority": 1
                },
                "habitat": {
                    "consumption_kwh": [r["habitat_kwh"] for r in consumption_data],
                    "priority": 2
                },
                "laboratory": {
                    "consumption_kwh": [r["laboratory_kwh"] for r in consumption_data],
                    "priority": 3
                },
                "non_essential": {
                    "consumption_kwh": [r["non_essential_kwh"] for r in consumption_data],
                    "priority": 4
                }
            },
            "climate": {
                "wind_speed_ms": [r["wind_speed_ms"] for r in climate_data],
                "temperature_c": [r["temperature_c"] for r in climate_data],
                "irradiance_wm2": [r["irradiance_wm2"] for r in climate_data]
            }
        }
    }

    return colony


def get_day_summary(energy_data: list, consumption_data: list,
                    climate_data: list, day: int) -> dict:
    """
    Monta um resumo consolidado de um dia específico.

    Args:
        energy_data: Lista de registros de energia.
        consumption_data: Lista de registros de consumo.
        climate_data: Lista de registros climáticos.
        day: Dia da leitura (1-30).

    Returns:
        Dicionário com resumo do dia.
    """
    idx = day - 1

    if idx < 0 or idx >= len(energy_data):
        return None

    energy = energy_data[idx]
    consumption = consumption_data[idx]
    climate = climate_data[idx]

    total_generation = energy["solar_generation_kwh"] + energy["wind_generation_kwh"]
    total_consumption = (
        consumption["life_support_kwh"]
        + consumption["habitat_kwh"]
        + consumption["laboratory_kwh"]
        + consumption["non_essential_kwh"]
    )

    return {
        "day": day,
        "solar_generation_kwh": energy["solar_generation_kwh"],
        "wind_generation_kwh": energy["wind_generation_kwh"],
        "total_generation_kwh": round(total_generation, 2),
        "battery_reserve_kwh": energy["battery_reserve_kwh"],
        "life_support_kwh": consumption["life_support_kwh"],
        "habitat_kwh": consumption["habitat_kwh"],
        "laboratory_kwh": consumption["laboratory_kwh"],
        "non_essential_kwh": consumption["non_essential_kwh"],
        "total_consumption_kwh": round(total_consumption, 2),
        "wind_speed_ms": climate["wind_speed_ms"],
        "temperature_c": climate["temperature_c"],
        "irradiance_wm2": climate["irradiance_wm2"]
    }


def navigate_hierarchy(colony: dict, path: list) -> any:
    """
    Navega pela hierarquia da colônia seguindo um caminho (recursivo).

    Args:
        colony: Dicionário hierárquico.
        path: Lista de chaves representando o caminho (ex: ["systems", "energy", "solar"]).

    Returns:
        Valor encontrado na hierarquia ou None.
    """
    if not path:
        return colony

    key = path[0]

    if isinstance(colony, dict) and key in colony:
        return navigate_hierarchy(colony[key], path[1:])

    return None
