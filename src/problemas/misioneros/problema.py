"""Definición del problema de Misioneros y Caníbales."""

# Posiciones posibles de la canoa
IZQUIERDA = "I"
DERECHA = "D"

# Cada estado tiene la forma:
# (misioneros_izquierda, canibales_izquierda, posicion_canoa)

ESTADO_INICIAL = (3, 3, IZQUIERDA)
ESTADO_META = (0, 0, DERECHA)


def es_meta(estado):
    """
    Comprueba si el estado recibido corresponde al estado meta.

    La meta se alcanza cuando todos los misioneros y caníbales
    están en la orilla derecha y la canoa también está a la derecha.
    """
    return estado == ESTADO_META


def obtener_orilla_derecha(estado):
    """
    Calcula la cantidad de misioneros y caníbales
    que se encuentran en la orilla derecha.
    """
    misioneros_izquierda, canibales_izquierda, _ = estado

    misioneros_derecha = 3 - misioneros_izquierda
    canibales_derecha = 3 - canibales_izquierda

    return misioneros_derecha, canibales_derecha