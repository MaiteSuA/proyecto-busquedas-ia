
"""Algoritmo Minimax para Pac-Man con un fantasma adversario."""

from dataclasses import dataclass

from src.problemas.pacman.heuristica import evaluar_estado
from src.problemas.pacman.problema import EstadoPacman, ProblemaPacman


@dataclass
class ResultadoMinimax:
    movimiento: str | None
    valor: float
    nodos_explorados: int


def buscar_minimax(
    juego: ProblemaPacman,
    estado: EstadoPacman,
    profundidad: int = 2,
) -> ResultadoMinimax:
    """Busca la mejor dirección para Pac-Man.

    Una profundidad representa un ciclo completo:
    movimiento de Pac-Man seguido del fantasma.
    """

    if profundidad < 1:
        raise ValueError("La profundidad debe ser al menos 1.")

    nodos = 0

    def max_valor(actual: EstadoPacman, restante: int) -> float:
        nonlocal nodos
        nodos += 1

        if actual.terminado or restante == 0:
            return evaluar_estado(actual)

        movimientos = juego.movimientos_pacman(actual)

        if not movimientos:
            return evaluar_estado(actual)

        mejor = float("-inf")

        for direccion in movimientos:
            siguiente = juego.mover_pacman(actual, direccion)
            valor = min_valor(siguiente, restante)
            mejor = max(mejor, valor)

        return mejor

    def min_valor(actual: EstadoPacman, restante: int) -> float:
        nonlocal nodos
        nodos += 1

        if actual.terminado:
            return evaluar_estado(actual)

        movimientos = juego.movimientos_fantasma(actual)

        if not movimientos:
            return max_valor(actual, restante - 1)

        peor = float("inf")

        for direccion in movimientos:
            siguiente = juego.mover_fantasma(actual, direccion)
            valor = max_valor(siguiente, restante - 1)
            peor = min(peor, valor)

        return peor

    if estado.terminado:
        return ResultadoMinimax(None, evaluar_estado(estado), 0)

    movimientos = juego.movimientos_pacman(estado)

    if not movimientos:
        return ResultadoMinimax(None, evaluar_estado(estado), 0)

    mejor_movimiento = None
    mejor_valor = float("-inf")

    for direccion in movimientos:
        siguiente = juego.mover_pacman(estado, direccion)
        valor = min_valor(siguiente, profundidad)

        if valor > mejor_valor:
            mejor_valor = valor
            mejor_movimiento = direccion

    return ResultadoMinimax(
        movimiento=mejor_movimiento,
        valor=mejor_valor,
        nodos_explorados=nodos,
    )
