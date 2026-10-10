"""Reglas y generación de sucesores para Misioneros y Caníbales."""

from .problema import IZQUIERDA, DERECHA


# Cada movimiento tiene la forma:
# (misioneros_transportados, canibales_transportados)
MOVIMIENTOS = [
    (0, 2),  # Dos caníbales
    (0, 1),  # Un caníbal
    (2, 0),  # Dos misioneros
    (1, 1),  # Un misionero y un caníbal
    (1, 0),  # Un misionero
]


def es_estado_valido(estado):
    """
    Comprueba que las cantidades sean correctas y que los caníbales
    no superen a los misioneros en ninguna orilla.
    """
    m_izq, c_izq, posicion_canoa = estado

    # La posición de la canoa debe ser válida.
    if posicion_canoa not in (IZQUIERDA, DERECHA):
        return False

    # No pueden existir cantidades menores que 0 o mayores que 3.
    if not (0 <= m_izq <= 3 and 0 <= c_izq <= 3):
        return False

    # Calculamos las personas que están en la orilla derecha.
    m_der = 3 - m_izq
    c_der = 3 - c_izq

    # Condición de seguridad en la orilla izquierda.
    if m_izq > 0 and c_izq > m_izq:
        return False

    # Condición de seguridad en la orilla derecha.
    if m_der > 0 and c_der > m_der:
        return False

    return True


def aplicar_movimiento(estado, movimiento):
    """
    Aplica un movimiento según la posición actual de la canoa.

    Retorna el nuevo estado si es válido.
    Retorna None si el movimiento produce un estado inválido.
    """
    m_izq, c_izq, posicion_canoa = estado
    m_transportados, c_transportados = movimiento

    if posicion_canoa == IZQUIERDA:
        nuevo_estado = (
            m_izq - m_transportados,
            c_izq - c_transportados,
            DERECHA,
        )
    else:
        nuevo_estado = (
            m_izq + m_transportados,
            c_izq + c_transportados,
            IZQUIERDA,
        )

    if es_estado_valido(nuevo_estado):
        return nuevo_estado

    return None


def generar_sucesores(estado):
    """
    Genera todos los sucesores válidos de un estado.

    Cada elemento contiene:
    (nuevo_estado, movimiento_realizado)
    """
    sucesores = []

    for movimiento in MOVIMIENTOS:
        nuevo_estado = aplicar_movimiento(estado, movimiento)

        if nuevo_estado is not None:
            sucesores.append((nuevo_estado, movimiento))

    return sucesores