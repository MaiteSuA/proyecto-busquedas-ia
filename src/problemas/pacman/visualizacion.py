from html import escape

from .laberinto import Laberinto
from .problema import EstadoPacman


TAMANO_CELDA = 24

COLORES_FANTASMAS = (
    "#FF4040",
    "#FFB8FF",
    "#00FFFF",
    "#FFB852",
)


def generar_svg(
    laberinto: Laberinto,
    estado: EstadoPacman,
    tamano_celda: int = TAMANO_CELDA,
) -> str:
    """Genera el tablero SVG a partir del estado actual."""

    ancho = laberinto.ancho * tamano_celda
    alto = laberinto.alto * tamano_celda

    elementos = [
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'viewBox="0 0 {ancho} {alto}" '
        f'width="{ancho}" height="{alto}">',
        f'<rect width="{ancho}" height="{alto}" fill="#050509"/>',
    ]

    for fila, columna in laberinto.paredes:
        x = columna * tamano_celda
        y = fila * tamano_celda

        elementos.append(
            f'<rect x="{x + 1}" y="{y + 1}" '
            f'width="{tamano_celda - 2}" '
            f'height="{tamano_celda - 2}" '
            f'rx="4" fill="#102A88" '
            f'stroke="#235BFF" stroke-width="1.5"/>'
        )

    for fila, columna in estado.puntos:
        cx = columna * tamano_celda + tamano_celda / 2
        cy = fila * tamano_celda + tamano_celda / 2

        elementos.append(
            f'<circle cx="{cx}" cy="{cy}" r="2.5" '
            f'fill="#FFE4A0"/>'
        )

    for fila, columna in estado.puntos_poder:
        cx = columna * tamano_celda + tamano_celda / 2
        cy = fila * tamano_celda + tamano_celda / 2

        elementos.append(
            f'<circle cx="{cx}" cy="{cy}" r="6" '
            f'fill="#FFE4A0"/>'
        )

    # Pac-Man
    fila, columna = estado.pacman
    cx = columna * tamano_celda + tamano_celda / 2
    cy = fila * tamano_celda + tamano_celda / 2
    radio = tamano_celda * 0.42

    elementos.append(
        f'<path d="M {cx} {cy} '
        f'L {cx + radio * 0.7} {cy - radio * 0.7} '
        f'A {radio} {radio} 0 1 0 '
        f'{cx + radio * 0.7} {cy + radio * 0.7} Z" '
        f'fill="#FFD700"/>'
    )

    # Fantasmas
    for indice, (fila, columna) in enumerate(estado.fantasmas):
        x = columna * tamano_celda
        y = fila * tamano_celda
        color = COLORES_FANTASMAS[indice % len(COLORES_FANTASMAS)]

        elementos.append(
            f'<path d="M {x + 3} {y + 20} '
            f'L {x + 3} {y + 11} '
            f'A 9 9 0 0 1 {x + 21} {y + 11} '
            f'L {x + 21} {y + 20} '
            f'L {x + 17} {y + 17} '
            f'L {x + 13} {y + 20} '
            f'L {x + 9} {y + 17} '
            f'L {x + 5} {y + 20} Z" '
            f'fill="{escape(color)}"/>'
        )

        for ojo_x in (x + 9, x + 16):
            elementos.append(
                f'<circle cx="{ojo_x}" cy="{y + 11}" '
                f'r="3" fill="white"/>'
            )
            elementos.append(
                f'<circle cx="{ojo_x + 1}" cy="{y + 11}" '
                f'r="1.5" fill="#172554"/>'
            )

    elementos.append("</svg>")

    return "\n".join(elementos)
