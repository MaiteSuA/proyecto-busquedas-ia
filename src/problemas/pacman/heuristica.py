
"""Funciones de evaluación para la inteligencia artificial de Pac-Man."""

from collections import deque
from functools import lru_cache

from .laberinto import Laberinto, Posicion
from .problema import EstadoPacman


def distancia_manhattan(a: Posicion, b: Posicion) -> int:
    """Calcula la distancia Manhattan entre dos posiciones."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


@lru_cache(maxsize=1024)
def _distancias_desde(
    mapa: tuple[str, ...],
    origen: Posicion,
) -> dict[Posicion, int]:
    """Calcula distancias mínimas mediante BFS respetando las paredes."""

    laberinto = Laberinto(mapa=mapa)

    distancias = {origen: 0}
    cola = deque([origen])

    while cola:
        actual = cola.popleft()

        for vecino in laberinto.vecinos(actual):
            if vecino not in distancias:
                distancias[vecino] = distancias[actual] + 1
                cola.append(vecino)

    return distancias


def distancia_laberinto(
    laberinto: Laberinto,
    origen: Posicion,
    destino: Posicion,
) -> float:
    """Devuelve la distancia mínima considerando las paredes."""

    distancias = _distancias_desde(
        laberinto.mapa,
        origen,
    )

    return float(
        distancias.get(destino, float("inf"))
    )


def evaluar_estado(
    estado: EstadoPacman,
    laberinto: Laberinto | None = None,
) -> float:
    """Evalúa qué tan favorable es un estado para Pac-Man."""

    # 1. Comprobar si la partida terminó.
    if estado.terminado:
        if estado.victoria:
            return float(100000 + estado.puntuacion)

        return float(-100000 + estado.puntuacion)

    # 2. Recompensar la puntuación y las vidas restantes.
    valor = estado.puntuacion * 10
    valor += estado.vidas * 1000

    # 3. Evaluar la distancia hasta los puntos restantes.
    objetivos = estado.puntos | estado.puntos_poder

    if objetivos:
        if laberinto is not None:
            # Calcular distancias reales mediante BFS.
            distancias = _distancias_desde(
                laberinto.mapa,
                estado.pacman,
            )

            distancias_objetivos = [
                distancias[punto]
                for punto in objetivos
                if punto in distancias
            ]

            if distancias_objetivos:
                distancia_punto = min(
                    distancias_objetivos
                )

                # Incentivar acercarse a los puntos.
                valor -= distancia_punto * 15
            else:
                # Penalizar estados sin acceso a los puntos.
                valor -= 1000

        else:
            # Alternativa cuando no se proporciona laberinto.
            distancia_punto = min(
                distancia_manhattan(
                    estado.pacman,
                    punto,
                )
                for punto in objetivos
            )

            valor -= distancia_punto * 15

    # 4. Penalizar la cercanía de los fantasmas.
    for fantasma in estado.fantasmas:
        if laberinto is not None:
            distancia = distancia_laberinto(
                laberinto,
                estado.pacman,
                fantasma,
            )
        else:
            distancia = distancia_manhattan(
                estado.pacman,
                fantasma,
            )

        if distancia == 0:
            valor -= 10000
        elif distancia == 1:
            valor -= 500
        elif distancia == 2:
            valor -= 150
        elif distancia == 3:
            valor -= 50

    # 5. Penalizar posiciones visitadas recientemente.
    repeticiones = estado.historial.count(
        estado.pacman
    )

    if repeticiones > 0:
        valor -= repeticiones * 35

    # 6. Penalizar oscilaciones entre dos casillas.
    if len(estado.historial) >= 2:
        if estado.pacman == estado.historial[-2]:
            valor -= 60

    # 7. Penalizar el estancamiento prolongado.
    # Se activa después de 15 turnos sin recoger puntos.
    if estado.turnos_sin_puntos > 15:
        exceso = estado.turnos_sin_puntos - 15

        # Limitar la penalización para evitar valores excesivos.
        valor -= min(exceso, 30) * 3

    # 8. Devolver el valor final de evaluación.
    return float(valor)
