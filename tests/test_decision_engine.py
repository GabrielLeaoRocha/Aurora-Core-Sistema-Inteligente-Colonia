"""Testes unitários para o módulo decision_engine."""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.decision_engine import evaluate_energy_status, evaluate_subsystem_priority


def test_critical_situation():
    """Testa condição crítica: geração < 30 E consumo > 70."""
    result = evaluate_energy_status(25.0, 75.0, 10.0)
    assert result["level"] == "CRITICAL"
    assert result["priority"] == 1
    print("  [PASS] test_critical_situation")


def test_alert_low_gen_high_consumption():
    """Testa alerta: geração < 50 E consumo > geração."""
    result = evaluate_energy_status(40.0, 55.0, 50.0)
    assert result["level"] == "ALERT"
    assert result["priority"] == 2
    print("  [PASS] test_alert_low_gen_high_consumption")


def test_warning_low_generation():
    """Testa warning: geração < 50 mas consumo ok."""
    result = evaluate_energy_status(45.0, 40.0, 80.0)
    assert result["level"] == "WARNING"
    assert result["priority"] == 3
    print("  [PASS] test_warning_low_generation")


def test_suggestion_excess():
    """Testa sugestão: geração > consumo * 1.5."""
    result = evaluate_energy_status(100.0, 50.0, 90.0)
    assert result["level"] == "SUGGESTION"
    assert result["priority"] == 4
    print("  [PASS] test_suggestion_excess")


def test_normal_operation():
    """Testa operação normal."""
    result = evaluate_energy_status(70.0, 60.0, 80.0)
    assert result["level"] == "STATUS"
    assert result["priority"] == 5
    print("  [PASS] test_normal_operation")


def test_subsystem_shutdown_priority():
    """Testa lista de desligamento de subsistemas."""
    shutdown = evaluate_subsystem_priority(40.0, 60.0)
    assert "non_essential" in shutdown
    assert "life_support" not in shutdown
    print("  [PASS] test_subsystem_shutdown_priority")


def test_no_shutdown_needed():
    """Testa quando nenhum desligamento é necessário."""
    shutdown = evaluate_subsystem_priority(80.0, 60.0)
    assert shutdown == []
    print("  [PASS] test_no_shutdown_needed")


if __name__ == "__main__":
    print("\n  Running decision_engine tests...")
    test_critical_situation()
    test_alert_low_gen_high_consumption()
    test_warning_low_generation()
    test_suggestion_excess()
    test_normal_operation()
    test_subsystem_shutdown_priority()
    test_no_shutdown_needed()
    print("  All tests passed!\n")
