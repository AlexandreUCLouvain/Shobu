from typing import List, Set


def compter_occurrences(board: List[List[Set[int]]]) -> int:
    player_zero = sum(len(ensemble) for liste_sets in board for ensemble in liste_sets[::2])
    player_one = sum(len(ensemble) for liste_sets in board for ensemble in liste_sets[1::2])
    return player_zero - player_one



board = [
    [{0, 1}, {12, 14, 3}],
    [{0, 1, 2, 3}, {12, 13, 14, 15}],
    [{1, 2, 3}, {12, 13, 14, 15}],
    [{3}, {12, 13, 14}]
]

resultats = compter_occurrences(board)

print(resultats)
