
"""Funciones de evaluación para la inteligencia artificial de Pac-Man."""

from .laberinto import Posicion
from .problema import EstadoPacman


def distancia_manhattan(a: Posicion, b: Posicion) -> int:
    """Calcula la distancia Manhattan entre dos posiciones."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def evaluar_estado(estado: EstadoPacman) -> float:
    """Evalúa qué tan favorable es un estado para Pac-Man.

    Valores altos favorecen a Pac-Man.
    Valores bajos favorecen al fantasma.
    """

    if estado.terminado:
        if estado.victoria:
            return 100000 + estado.puntuacion

        return -100000 + estado.puntuacion

    valor = estado.puntuacion * 10
    valor += estado.vidas * 1000

    objetivos = estado.puntos | estado.puntos_poder

    if objetivos:
        distancia_punto = min(
            distancia_manhattan(estado.pacman, punto)
            for punto in objetivos
        )
        valor -= distancia_punto * 5

    for fantasma in estado.fantasmas:
        distancia = distancia_manhattan(estado.pacman, fantasma)

        if distancia == 0:
            valor -= 10000
        elif distancia == 1:
            valor -= 500
        elif distancia == 2:
            valor -= 150
        elif distancia == 3:
            valor -= 50

    return float(valor)
