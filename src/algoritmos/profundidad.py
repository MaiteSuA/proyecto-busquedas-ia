"""Implementación de la búsqueda en profundidad (DFS)."""

from src.problemas.misioneros.problema import ESTADO_INICIAL, es_meta
from src.problemas.misioneros.reglas import generar_sucesores


def busqueda_profundidad():
    """
    Resuelve Misioneros y Caníbales mediante búsqueda en profundidad.

    Utiliza una pila para almacenar los estados pendientes.
    """

    # Cada elemento de la pila contiene:
    # (estado_actual, ruta_de_estados, movimientos_realizados)
    pila = [
        (ESTADO_INICIAL, [ESTADO_INICIAL], [])
    ]

    visitados = set()
    orden_visitados = []

    # Complejidad espacial práctica:
    # mayor cantidad de elementos almacenados en la pila.
    maximo_pila = len(pila)

    while pila:
        # Profundidad utiliza LIFO:
        # se extrae el último elemento agregado.
        estado_actual, ruta, movimientos_ruta = pila.pop()

        # Evita explorar nuevamente un estado repetido.
        if estado_actual in visitados:
            continue

        visitados.add(estado_actual)
        orden_visitados.append(estado_actual)

        # Prueba de meta.
        if es_meta(estado_actual):
            costo_busqueda = len(orden_visitados)
            costo_ruta = len(movimientos_ruta)

            return {
                "encontrado": True,
                "ruta": ruta,
                "movimientos": movimientos_ruta,
                "nodos_visitados": costo_busqueda,
                "maximo_pila": maximo_pila,
                "costo_busqueda": costo_busqueda,
                "costo_ruta": costo_ruta,
                "costo_total": costo_busqueda + costo_ruta,
                "orden_visitados": orden_visitados,
            }

        sucesores = generar_sucesores(estado_actual)

        # Se recorren al revés porque la pila extrae primero
        # el último elemento agregado.
        for nuevo_estado, movimiento in reversed(sucesores):
            if nuevo_estado not in visitados:
                nueva_ruta = ruta + [nuevo_estado]
                nuevos_movimientos = movimientos_ruta + [movimiento]

                pila.append(
                    (nuevo_estado, nueva_ruta, nuevos_movimientos)
                )

        # Actualiza la mayor cantidad de elementos almacenados.
        maximo_pila = max(maximo_pila, len(pila))

    # Se llega aquí si la pila se vacía sin encontrar la meta.
    return {
        "encontrado": False,
        "ruta": [],
        "movimientos": [],
        "nodos_visitados": len(orden_visitados),
        "maximo_pila": maximo_pila,
        "costo_busqueda": len(orden_visitados),
        "costo_ruta": 0,
        "costo_total": len(orden_visitados),
        "orden_visitados": orden_visitados,
    }
