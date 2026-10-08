
"""Estados y reglas del juego Pac-Man para búsqueda adversarial."""

from dataclasses import dataclass, replace

from .laberinto import Laberinto, Posicion


@dataclass(frozen=True)
class EstadoPacman:
    pacman: Posicion
    fantasmas: tuple[Posicion, ...]
    puntos: frozenset[Posicion]
    puntos_poder: frozenset[Posicion]
    puntuacion: int = 0
    vidas: int = 3
    turnos: int = 0
    terminado: bool = False
    victoria: bool = False


class ProblemaPacman:
    PUNTOS_NORMAL = 10
    PUNTOS_PODER = 50

    def __init__(self, laberinto: Laberinto | None = None):
        self.laberinto = laberinto or Laberinto()

    def estado_inicial(self) -> EstadoPacman:
        return EstadoPacman(
            pacman=self.laberinto.pacman_inicio,
            fantasmas=tuple(self.laberinto.fantasmas_inicio),
            puntos=frozenset(self.laberinto.puntos),
            puntos_poder=frozenset(self.laberinto.puntos_poder),
        )

    def movimientos_pacman(self, estado: EstadoPacman) -> dict[str, Posicion]:
        if estado.terminado:
            return {}

        return self.laberinto.movimientos_validos(estado.pacman)

    def movimientos_fantasma(
        self, estado: EstadoPacman, indice: int = 0
    ) -> dict[str, Posicion]:
        if estado.terminado:
            return {}

        return self.laberinto.movimientos_validos(
            estado.fantasmas[indice]
        )

    def mover_pacman(
        self, estado: EstadoPacman, direccion: str
    ) -> EstadoPacman:
        movimientos = self.movimientos_pacman(estado)

        if direccion not in movimientos:
            raise ValueError(f"Movimiento no permitido: {direccion}")

        nueva_posicion = movimientos[direccion]
        puntos = set(estado.puntos)
        puntos_poder = set(estado.puntos_poder)
        puntuacion = estado.puntuacion

        if nueva_posicion in puntos:
            puntos.remove(nueva_posicion)
            puntuacion += self.PUNTOS_NORMAL

        if nueva_posicion in puntos_poder:
            puntos_poder.remove(nueva_posicion)
            puntuacion += self.PUNTOS_PODER

        nuevo = replace(
            estado,
            pacman=nueva_posicion,
            puntos=frozenset(puntos),
            puntos_poder=frozenset(puntos_poder),
            puntuacion=puntuacion,
            turnos=estado.turnos + 1,
        )

        nuevo = self._resolver_colision(nuevo)

        if not nuevo.terminado and not nuevo.puntos and not nuevo.puntos_poder:
            nuevo = replace(nuevo, terminado=True, victoria=True)

        return nuevo

    def mover_fantasma(
        self,
        estado: EstadoPacman,
        direccion: str,
        indice: int = 0,
    ) -> EstadoPacman:
        movimientos = self.movimientos_fantasma(estado, indice)

        if direccion not in movimientos:
            raise ValueError(f"Movimiento no permitido: {direccion}")

        fantasmas = list(estado.fantasmas)
        fantasmas[indice] = movimientos[direccion]

        nuevo = replace(estado, fantasmas=tuple(fantasmas))
        return self._resolver_colision(nuevo)

    def _resolver_colision(self, estado: EstadoPacman) -> EstadoPacman:
        if estado.pacman not in estado.fantasmas:
            return estado

        vidas_restantes = estado.vidas - 1

        if vidas_restantes <= 0:
            return replace(
                estado,
                vidas=0,
                terminado=True,
                victoria=False,
            )

        return replace(
            estado,
            pacman=self.laberinto.pacman_inicio,
            fantasmas=tuple(self.laberinto.fantasmas_inicio),
            vidas=vidas_restantes,
        )
