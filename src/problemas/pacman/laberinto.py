
"""Representación y utilidades del laberinto de Pac-Man."""

from dataclasses import dataclass

# Símbolos:
# # = pared
# . = punto
# o = punto de poder
# P = posición inicial de Pac-Man
# G = posición inicial de un fantasma
# espacio = camino libre

MAPA_INICIAL = (
    "###################",
    "#........#........#",
    "#.###.##.#.##.###.#",
    "#o###.##.#.##.###o#",
    "#.................#",
    "#.###.#.###.#.###.#",
    "#.....#..#..#.....#",
    "#####.## # ##.#####",
    "    #.#     #.#    ",
    "#####.# ## ##.#####",
    "#....... G .......#",
    "#####.# ## ##.#####",
    "    #.#     #.#    ",
    "#####.#.###.#.#####",
    "#........P........#",
    "#.###.##.#.##.###.#",
    "#o..#.....#.....o.#",
    "###.#.#.###.#.#.###",
    "#.....#.....#.....#",
    "###################",
)

MOVIMIENTOS = {
    "arriba": (-1, 0),
    "abajo": (1, 0),
    "izquierda": (0, -1),
    "derecha": (0, 1),
}

Posicion = tuple[int, int]


@dataclass
class Laberinto:
    mapa: tuple[str, ...] = MAPA_INICIAL

    def __post_init__(self):
        if not self.mapa:
            raise ValueError("El mapa no puede estar vacío.")

        ancho = len(self.mapa[0])

        if any(len(fila) != ancho for fila in self.mapa):
            raise ValueError("Todas las filas deben tener el mismo ancho.")

        self.alto = len(self.mapa)
        self.ancho = ancho
        self.paredes = set()
        self.puntos = set()
        self.puntos_poder = set()
        self.pacman_inicio = None
        self.fantasmas_inicio = []

        for fila, contenido in enumerate(self.mapa):
            for columna, simbolo in enumerate(contenido):
                posicion = (fila, columna)

                if simbolo == "#":
                    self.paredes.add(posicion)
                elif simbolo == ".":
                    self.puntos.add(posicion)
                elif simbolo == "o":
                    self.puntos_poder.add(posicion)
                elif simbolo == "P":
                    if self.pacman_inicio is not None:
                        raise ValueError("Solo debe existir un Pac-Man inicial.")
                    self.pacman_inicio = posicion
                elif simbolo == "G":
                    self.fantasmas_inicio.append(posicion)
                elif simbolo != " ":
                    raise ValueError(f"Símbolo desconocido: {simbolo}")

        if self.pacman_inicio is None:
            raise ValueError("El mapa necesita una posición inicial de Pac-Man.")

        if not self.fantasmas_inicio:
            raise ValueError("El mapa necesita al menos un fantasma.")

    def dentro_del_mapa(self, posicion: Posicion) -> bool:
        fila, columna = posicion
        return 0 <= fila < self.alto and 0 <= columna < self.ancho

    def es_transitable(self, posicion: Posicion) -> bool:
        return (
            self.dentro_del_mapa(posicion)
            and posicion not in self.paredes
        )

    def vecinos(self, posicion: Posicion) -> list[Posicion]:
        disponibles = []

        for desplazamiento in MOVIMIENTOS.values():
            nueva_posicion = (
                posicion[0] + desplazamiento[0],
                posicion[1] + desplazamiento[1],
            )

            if self.es_transitable(nueva_posicion):
                disponibles.append(nueva_posicion)

        return disponibles

    def movimientos_validos(self, posicion: Posicion) -> dict[str, Posicion]:
        disponibles = {}

        for nombre, desplazamiento in MOVIMIENTOS.items():
            nueva_posicion = (
                posicion[0] + desplazamiento[0],
                posicion[1] + desplazamiento[1],
            )

            if self.es_transitable(nueva_posicion):
                disponibles[nombre] = nueva_posicion

        return disponibles

    def cantidad_puntos(self) -> int:
        return len(self.puntos) + len(self.puntos_poder)
