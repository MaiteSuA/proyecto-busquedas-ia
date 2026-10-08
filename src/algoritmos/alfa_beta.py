
"""Algoritmo Minimax con poda alfa-beta para Pac-Man."""

from dataclasses import dataclass

from src.problemas.pacman.heuristica import evaluar_estado
from src.problemas.pacman.problema import EstadoPacman, ProblemaPacman


@dataclass
class ResultadoAlfaBeta:
    movimiento: str | None
    valor: float
    nodos_explorados: int
    podas: int


def buscar_alfa_beta(
    juego: ProblemaPacman,
    estado: EstadoPacman,
    profundidad: int = 2,
) -> ResultadoAlfaBeta:
    """Busca la mejor dirección usando Minimax con poda alfa-beta.

    Cada nivel de profundidad representa un ciclo de Pac-Man
    seguido por el fantasma.
    """

    if profundidad < 1:
        raise ValueError("La profundidad debe ser al menos 1.")

    nodos = 0
    podas = 0

    def max_valor(
        actual: EstadoPacman,
        restante: int,
        alfa: float,
        beta: float,
    ) -> float:
        nonlocal nodos, podas
        nodos += 1

        if actual.terminado or restante == 0:
            return evaluar_estado(actual)

        movimientos = juego.movimientos_pacman(actual)

        if not movimientos:
            return evaluar_estado(actual)

        mejor = float("-inf")

        for direccion in movimientos:
            siguiente = juego.mover_pacman(actual, direccion)
            valor = min_valor(siguiente, restante, alfa, beta)
            mejor = max(mejor, valor)

            if mejor >= beta:
                podas += 1
                break

            alfa = max(alfa, mejor)

        return mejor

    def min_valor(
        actual: EstadoPacman,
        restante: int,
        alfa: float,
        beta: float,
    ) -> float:
        nonlocal nodos, podas
        nodos += 1

        if actual.terminado:
            return evaluar_estado(actual)

        movimientos = juego.movimientos_fantasma(actual)

        if not movimientos:
            return max_valor(actual, restante - 1, alfa, beta)

        peor = float("inf")

        for direccion in movimientos:
            siguiente = juego.mover_fantasma(actual, direccion)
            valor = max_valor(siguiente, restante - 1, alfa, beta)
            peor = min(peor, valor)

            if peor <= alfa:
                podas += 1
                break

            beta = min(beta, peor)

        return peor

    if estado.terminado:
        return ResultadoAlfaBeta(
            None, evaluar_estado(estado), 0, 0
        )

    movimientos = juego.movimientos_pacman(estado)

    if not movimientos:
        return ResultadoAlfaBeta(
            None, evaluar_estado(estado), 0, 0
        )

    mejor_movimiento = None
    mejor_valor = float("-inf")
    alfa = float("-inf")
    beta = float("inf")

    for direccion in movimientos:
        siguiente = juego.mover_pacman(estado, direccion)
        valor = min_valor(siguiente, profundidad, alfa, beta)

        if valor > mejor_valor:
            mejor_valor = valor
            mejor_movimiento = direccion

        alfa = max(alfa, mejor_valor)

    return ResultadoAlfaBeta(
        movimiento=mejor_movimiento,
        valor=mejor_valor,
        nodos_explorados=nodos,
        podas=podas,
    )
