"""
regression_model.py — Regressão linear simples (método dos mínimos quadrados).

Implementação manual sem bibliotecas externas, usando apenas operações
aritméticas com listas Python, conforme o método do Cap 7.
"""


def calculate_mean(values: list) -> float:
    """
    Calcula a média aritmética de uma lista de valores.

    Args:
        values: Lista de números.

    Returns:
        Média aritmética.
    """
    return sum(values) / len(values)


def calculate_linear_regression(x_values: list, y_values: list) -> tuple:
    """
    Calcula os coeficientes da regressão linear simples.

    Fórmulas:
        β₁ = Σ[(xᵢ - x̄)(yᵢ - ȳ)] / Σ[(xᵢ - x̄)²]
        β₀ = ȳ - β₁ · x̄

    Args:
        x_values: Lista de valores da variável independente.
        y_values: Lista de valores da variável dependente.

    Returns:
        Tupla (beta_0, beta_1) com intercepto e coeficiente angular.
    """
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

    if denominator == 0:
        return (y_mean, 0.0)

    beta_1 = numerator / denominator
    beta_0 = y_mean - beta_1 * x_mean

    return (beta_0, beta_1)


def predict(x: float, beta_0: float, beta_1: float) -> float:
    """
    Faz previsão usando o modelo linear: y = β₀ + β₁ · x.

    Args:
        x: Valor da variável independente.
        beta_0: Intercepto.
        beta_1: Coeficiente angular.

    Returns:
        Valor previsto de y.
    """
    return beta_0 + beta_1 * x


def calculate_r_squared(x_values: list, y_values: list,
                        beta_0: float, beta_1: float) -> float:
    """
    Calcula o coeficiente de determinação R².

    R² = 1 - (SSres / SStot)
    SSres = Σ(yᵢ - ŷᵢ)²
    SStot = Σ(yᵢ - ȳ)²

    Args:
        x_values: Valores de X.
        y_values: Valores de Y.
        beta_0: Intercepto do modelo.
        beta_1: Coeficiente angular do modelo.

    Returns:
        Valor de R² (entre 0 e 1).
    """
    y_mean = calculate_mean(y_values)
    ss_res = 0.0
    ss_tot = 0.0

    for i in range(len(x_values)):
        y_predicted = predict(x_values[i], beta_0, beta_1)
        ss_res += (y_values[i] - y_predicted) ** 2
        ss_tot += (y_values[i] - y_mean) ** 2

    if ss_tot == 0:
        return 0.0

    return 1 - (ss_res / ss_tot)


def build_wind_model(climate_data: list, energy_data: list) -> dict:
    """
    Constrói modelo de regressão: vento → energia eólica.

    Args:
        climate_data: Lista de registros climáticos.
        energy_data: Lista de registros de energia.

    Returns:
        Dicionário com coeficientes e R².
    """
    x_values = [r["wind_speed_ms"] for r in climate_data]
    y_values = [r["wind_generation_kwh"] for r in energy_data]

    beta_0, beta_1 = calculate_linear_regression(x_values, y_values)
    r_squared = calculate_r_squared(x_values, y_values, beta_0, beta_1)

    return {
        "model_name": "Wind Speed → Wind Energy",
        "beta_0": round(beta_0, 4),
        "beta_1": round(beta_1, 4),
        "r_squared": round(r_squared, 4),
        "x_variable": "wind_speed_ms",
        "y_variable": "wind_generation_kwh"
    }


def build_solar_model(climate_data: list, energy_data: list) -> dict:
    """
    Constrói modelo de regressão: irradiância → energia solar.

    Args:
        climate_data: Lista de registros climáticos.
        energy_data: Lista de registros de energia.

    Returns:
        Dicionário com coeficientes e R².
    """
    x_values = [r["irradiance_wm2"] for r in climate_data]
    y_values = [r["solar_generation_kwh"] for r in energy_data]

    beta_0, beta_1 = calculate_linear_regression(x_values, y_values)
    r_squared = calculate_r_squared(x_values, y_values, beta_0, beta_1)

    return {
        "model_name": "Irradiance → Solar Energy",
        "beta_0": round(beta_0, 4),
        "beta_1": round(beta_1, 4),
        "r_squared": round(r_squared, 4),
        "x_variable": "irradiance_wm2",
        "y_variable": "solar_generation_kwh"
    }
