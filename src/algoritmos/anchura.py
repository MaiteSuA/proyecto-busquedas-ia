"""Implementación de la búsqueda en anchura (BFS)."""

from collections import deque

from src.problemas.misioneros.problema import ESTADO_INICIAL, es_meta
from src.problemas.misioneros.reglas import generar_sucesores


def busqueda_anchura():
    """
    Resuelve Misioneros y Caníbales mediante búsqueda en anchura.

    Utiliza una cola para almacenar los estados pendientes.
    """

    # Cada elemento de la cola contiene:
    # (estado_actual, ruta_de_estados, movimientos_realizados)
    cola = deque([
        (ESTADO_INICIAL, [ESTADO_INICIAL], [])
    ])

    visitados = set()
    orden_visitados = []

    # Complejidad espacial práctica:
    # mayor cantidad de elementos almacenados en la cola.
    maximo_cola = len(cola)

    while cola:
        # Anchura utiliza FIFO:
        # se extrae el primer elemento agregado.
        estado_actual, ruta, movimientos_ruta = cola.popleft()

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
                "maximo_cola": maximo_cola,
                "costo_busqueda": costo_busqueda,
                "costo_ruta": costo_ruta,
                "costo_total": costo_busqueda + costo_ruta,
                "orden_visitados": orden_visitados,
            }

        sucesores = generar_sucesores(estado_actual)

        # Se recorren en el orden normal porque la cola extrae primero
        # el primer elemento agregado.
        for nuevo_estado, movimiento in sucesores:
            if nuevo_estado not in visitados:
                nueva_ruta = ruta + [nuevo_estado]
                nuevos_movimientos = movimientos_ruta + [movimiento]

                cola.append(
                    (nuevo_estado, nueva_ruta, nuevos_movimientos)
                )

        # Actualiza la mayor cantidad de elementos almacenados.
        maximo_cola = max(maximo_cola, len(cola))

    # Se llega aquí si la cola se vacía sin encontrar la meta.
    return {
        "encontrado": False,
        "ruta": [],
        "movimientos": [],
        "nodos_visitados": len(orden_visitados),
        "maximo_cola": maximo_cola,
        "costo_busqueda": len(orden_visitados),
        "costo_ruta": 0,
        "costo_total": len(orden_visitados),
        "orden_visitados": orden_visitados,
    }
