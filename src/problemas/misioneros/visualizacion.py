"""Preparación de la ruta para visualizar Misioneros y Caníbales."""

from .problema import IZQUIERDA


NOMBRES_MOVIMIENTOS = {
    (0, 2): "Cruzan dos caníbales",
    (0, 1): "Cruza un caníbal",
    (2, 0): "Cruzan dos misioneros",
    (1, 1): "Cruzan un misionero y un caníbal",
    (1, 0): "Cruza un misionero",
}


def describir_estado(estado):
    """Convierte un estado en información de ambas orillas."""
    m_izq, c_izq, posicion_canoa = estado

    return {
        "misioneros_izquierda": m_izq,
        "canibales_izquierda": c_izq,
        "misioneros_derecha": 3 - m_izq,
        "canibales_derecha": 3 - c_izq,
        "canoa": "Izquierda" if posicion_canoa == IZQUIERDA else "Derecha",
    }


def describir_movimiento(movimiento, estado_origen):
    """Describe quién viaja y en qué dirección."""
    descripcion = NOMBRES_MOVIMIENTOS[movimiento]

    if estado_origen[2] == IZQUIERDA:
        direccion = "de izquierda a derecha"
    else:
        direccion = "de derecha a izquierda"

    return f"{descripcion} {direccion}"


def preparar_pasos(ruta, movimientos):
    """
    Prepara todos los pasos de la solución para mostrarlos
    posteriormente en la interfaz.
    """
    pasos = []

    pasos.append(
        {
            "numero": 0,
            "accion": "Estado inicial",
            "estado": ruta[0],
            **describir_estado(ruta[0]),
        }
    )

    for indice, movimiento in enumerate(movimientos):
        estado_origen = ruta[indice]
        estado_destino = ruta[indice + 1]

        pasos.append(
            {
                "numero": indice + 1,
                "accion": describir_movimiento(
                    movimiento,
                    estado_origen,
                ),
                "estado": estado_destino,
                **describir_estado(estado_destino),
            }
        )

    return pasos


def preparar_metricas(resultado):
    """Selecciona las métricas que se mostrarán en la interfaz."""
    return {
        "Solución encontrada": resultado["encontrado"],
        "Nodos visitados": resultado["nodos_visitados"],
        "Máximo tamaño de la pila": resultado["maximo_pila"],
        "Costo de búsqueda": resultado["costo_busqueda"],
        "Costo de ruta": resultado["costo_ruta"],
        "Costo total": resultado["costo_total"],
    }
