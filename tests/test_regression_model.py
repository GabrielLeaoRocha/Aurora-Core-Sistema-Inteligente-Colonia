"""Testes unitários para o módulo regression_model."""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.regression_model import (
    calculate_mean,
    calculate_linear_regression,
    predict,
    calculate_r_squared,
)


def test_calculate_mean():
    """Testa cálculo de média."""
    assert calculate_mean([10, 20, 30]) == 20.0
    assert calculate_mean([5.0]) == 5.0
    print("  [PASS] test_calculate_mean")


def test_perfect_linear_relationship():
    """Testa regressão com relação linear perfeita."""
    x = [1, 2, 3, 4, 5]
    y = [3, 5, 7, 9, 11]

    beta_0, beta_1 = calculate_linear_regression(x, y)

    assert abs(beta_1 - 2.0) < 0.001, f"beta_1 should be 2.0, got {beta_1}"
    assert abs(beta_0 - 1.0) < 0.001, f"beta_0 should be 1.0, got {beta_0}"

    r_squared = calculate_r_squared(x, y, beta_0, beta_1)
    assert abs(r_squared - 1.0) < 0.001, f"R² should be 1.0, got {r_squared}"

    print("  [PASS] test_perfect_linear_relationship")


def test_predict():
    """Testa previsão."""
    result = predict(10.0, 5.0, 2.5)
    assert abs(result - 30.0) < 0.001
    print("  [PASS] test_predict")


def test_regression_with_noise():
    """Testa regressão com dados ruidosos."""
    x = [8, 10, 12, 14, 16]
    y = [20, 26, 29, 35, 38]

    beta_0, beta_1 = calculate_linear_regression(x, y)

    assert beta_1 > 0, "Slope should be positive"
    assert beta_0 > 0, "Intercept should be positive"

    r_squared = calculate_r_squared(x, y, beta_0, beta_1)
    assert r_squared > 0.9, f"R² should be > 0.9, got {r_squared}"

    print("  [PASS] test_regression_with_noise")


def test_constant_x():
    """Testa caso degenerado com X constante."""
    x = [5, 5, 5, 5]
    y = [10, 20, 30, 40]

    beta_0, beta_1 = calculate_linear_regression(x, y)
    assert beta_1 == 0.0
    print("  [PASS] test_constant_x")


if __name__ == "__main__":
    print("\n  Running regression_model tests...")
    test_calculate_mean()
    test_perfect_linear_relationship()
    test_predict()
    test_regression_with_noise()
    test_constant_x()
    print("  All tests passed!\n")
