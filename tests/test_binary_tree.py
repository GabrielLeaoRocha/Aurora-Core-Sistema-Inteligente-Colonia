"""Testes unitários para o módulo binary_tree."""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.binary_tree import (
    BinaryTreeNode,
    insert,
    search,
    in_order_traversal,
    build_bst,
    get_tree_height,
)


def test_insert_and_search():
    """Testa inserção e busca na BST."""
    root = None
    root = insert(root, 15, {"day": 15, "value": "day_15"})
    root = insert(root, 8, {"day": 8, "value": "day_8"})
    root = insert(root, 22, {"day": 22, "value": "day_22"})
    root = insert(root, 4, {"day": 4, "value": "day_4"})
    root = insert(root, 12, {"day": 12, "value": "day_12"})

    result = search(root, 12)
    assert result is not None, "Day 12 should be found"
    assert result["value"] == "day_12"

    result = search(root, 99)
    assert result is None, "Day 99 should not be found"

    print("  [PASS] test_insert_and_search")


def test_in_order_traversal():
    """Testa percurso in-order (deve retornar ordenado)."""
    root = None
    days = [15, 8, 22, 4, 12, 18, 28]
    for d in days:
        root = insert(root, d, {"day": d})

    ordered = in_order_traversal(root)
    ordered_days = [item[0] for item in ordered]

    assert ordered_days == sorted(days), f"Expected sorted but got {ordered_days}"
    print("  [PASS] test_in_order_traversal")


def test_build_bst_balanced():
    """Testa construção balanceada da BST."""
    readings = [{"day": i} for i in range(1, 31)]
    root = build_bst(readings)

    height = get_tree_height(root)
    assert height <= 6, f"Height {height} too large for 30 nodes (expected <=6)"

    ordered = in_order_traversal(root)
    assert len(ordered) == 30

    print("  [PASS] test_build_bst_balanced")


def test_empty_tree():
    """Testa operações em árvore vazia."""
    result = search(None, 1)
    assert result is None

    ordered = in_order_traversal(None)
    assert ordered == []

    height = get_tree_height(None)
    assert height == 0

    print("  [PASS] test_empty_tree")


if __name__ == "__main__":
    print("\n  Running binary_tree tests...")
    test_insert_and_search()
    test_in_order_traversal()
    test_build_bst_balanced()
    test_empty_tree()
    print("  All tests passed!\n")
