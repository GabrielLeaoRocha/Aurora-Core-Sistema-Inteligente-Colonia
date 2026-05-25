"""
binary_tree.py — Binary Search Tree (BST) para indexação de leituras de telemetria.

Implementa uma árvore binária de busca onde cada nó armazena uma leitura
diária da colônia, indexada pelo campo 'day'. Permite busca eficiente O(log n)
e listagem ordenada via in-order traversal.
"""


class BinaryTreeNode:
    """Nó da árvore binária de busca."""

    def __init__(self, day: int, data: dict):
        """
        Inicializa um nó da BST.

        Args:
            day: Chave de busca (dia da leitura).
            data: Dicionário com os valores daquele dia.
        """
        self.day = day
        self.data = data
        self.left = None
        self.right = None


def insert(root: BinaryTreeNode, day: int, data: dict) -> BinaryTreeNode:
    """
    Insere uma leitura na BST pelo dia (recursivo).

    Args:
        root: Nó raiz da árvore (ou subárvore).
        day: Dia da leitura a inserir.
        data: Dados associados àquele dia.

    Returns:
        Nó raiz atualizado.
    """
    if root is None:
        return BinaryTreeNode(day, data)

    if day < root.day:
        root.left = insert(root.left, day, data)
    elif day > root.day:
        root.right = insert(root.right, day, data)
    else:
        root.data = data

    return root


def search(root: BinaryTreeNode, day: int) -> dict:
    """
    Busca os dados de um dia específico na BST (recursivo).

    Args:
        root: Nó raiz da árvore.
        day: Dia a buscar.

    Returns:
        Dicionário com dados do dia ou None se não encontrado.
    """
    if root is None:
        return None

    if day == root.day:
        return root.data
    elif day < root.day:
        return search(root.left, day)
    else:
        return search(root.right, day)


def in_order_traversal(root: BinaryTreeNode) -> list:
    """
    Percorre a BST em ordem crescente de dia (in-order).

    Args:
        root: Nó raiz da árvore.

    Returns:
        Lista de tuplas (day, data) ordenada por dia.
    """
    result = []

    if root is None:
        return result

    result.extend(in_order_traversal(root.left))
    result.append((root.day, root.data))
    result.extend(in_order_traversal(root.right))

    return result


def build_bst(readings: list) -> BinaryTreeNode:
    """
    Constrói a BST a partir de uma lista de leituras.

    Insere na ordem mediana para garantir balanceamento.

    Args:
        readings: Lista de dicionários com campo 'day'.

    Returns:
        Nó raiz da BST construída.
    """
    if not readings:
        return None

    sorted_readings = sorted(readings, key=lambda r: r["day"])
    return _build_balanced(sorted_readings, 0, len(sorted_readings) - 1)


def _build_balanced(sorted_list: list, start: int, end: int) -> BinaryTreeNode:
    """
    Constrói BST balanceada recursivamente pela mediana.

    Args:
        sorted_list: Lista ordenada de leituras.
        start: Índice inicial.
        end: Índice final.

    Returns:
        Nó raiz da subárvore.
    """
    if start > end:
        return None

    mid = (start + end) // 2
    reading = sorted_list[mid]
    node = BinaryTreeNode(reading["day"], reading)

    node.left = _build_balanced(sorted_list, start, mid - 1)
    node.right = _build_balanced(sorted_list, mid + 1, end)

    return node


def get_tree_height(root: BinaryTreeNode) -> int:
    """
    Calcula a altura da árvore.

    Args:
        root: Nó raiz.

    Returns:
        Altura da árvore (0 se vazia).
    """
    if root is None:
        return 0

    left_height = get_tree_height(root.left)
    right_height = get_tree_height(root.right)

    return max(left_height, right_height) + 1
