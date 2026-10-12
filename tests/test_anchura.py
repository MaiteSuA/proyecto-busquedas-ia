"""Pruebas de la búsqueda en anchura."""

from src.algoritmos.anchura import busqueda_anchura
from src.problemas.misioneros.problema import ESTADO_INICIAL, ESTADO_META
from src.problemas.misioneros.reglas import es_estado_valido


def test_anchura_encuentra_solucion():
    """Comprueba que anchura encuentre una solución."""
    resultado = busqueda_anchura()

    assert resultado["encontrado"] is True


def test_ruta_inicia_y_termina_correctamente():
    """Comprueba el estado inicial y el estado meta de la ruta."""
    resultado = busqueda_anchura()
    ruta = resultado["ruta"]

    assert ruta[0] == ESTADO_INICIAL
    assert ruta[-1] == ESTADO_META


def test_todos_los_estados_son_validos():
    """Comprueba que todos los estados de la ruta sean seguros."""
    resultado = busqueda_anchura()

    for estado in resultado["ruta"]:
        assert es_estado_valido(estado)


def test_ruta_encontrada():
    """Comprueba la ruta exacta que encuentra anchura."""
    resultado = busqueda_anchura()

    assert resultado["ruta"] == [
        (3, 3, "I"),
        (3, 1, "D"),
        (3, 2, "I"),
        (3, 0, "D"),
        (3, 1, "I"),
        (1, 1, "D"),
        (2, 2, "I"),
        (0, 2, "D"),
        (0, 3, "I"),
        (0, 1, "D"),
        (0, 2, "I"),
        (0, 0, "D"),
    ]


def test_costo_de_ruta():
    """Comprueba que la solución encontrada tenga once cruces."""
    resultado = busqueda_anchura()

    assert resultado["costo_ruta"] == 11
    assert len(resultado["movimientos"]) == 11
    assert len(resultado["ruta"]) == 12


def test_orden_de_visita():
    """Comprueba que los estados se visiten por niveles."""
    resultado = busqueda_anchura()

    assert resultado["orden_visitados"] == [
        (3, 3, "I"),
        (3, 1, "D"),
        (3, 2, "D"),
        (2, 2, "D"),
        (3, 2, "I"),
        (3, 0, "D"),
        (3, 1, "I"),
        (1, 1, "D"),
        (2, 2, "I"),
        (0, 2, "D"),
        (0, 3, "I"),
        (0, 1, "D"),
        (0, 2, "I"),
        (1, 1, "I"),
        (0, 0, "D"),
    ]


def test_metricas_esperadas():
    """Comprueba los valores de las métricas de la búsqueda."""
    resultado = busqueda_anchura()

    assert resultado["nodos_visitados"] == 15
    assert resultado["maximo_cola"] == 3
    assert resultado["costo_busqueda"] == 15
    assert resultado["costo_total"] == 26


def test_metricas_coherentes():
    """Comprueba que las métricas sean calculadas correctamente."""
    resultado = busqueda_anchura()

    assert resultado["nodos_visitados"] > 0
    assert resultado["maximo_cola"] > 0

    assert (
        resultado["costo_total"]
        == resultado["costo_busqueda"] + resultado["costo_ruta"]
    )
