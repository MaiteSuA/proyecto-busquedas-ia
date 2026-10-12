"""Pruebas de la búsqueda en profundidad."""

from src.algoritmos.profundidad import busqueda_profundidad
from src.problemas.misioneros.problema import ESTADO_INICIAL, ESTADO_META
from src.problemas.misioneros.reglas import es_estado_valido


def test_profundidad_encuentra_solucion():
    """Comprueba que profundidad encuentre una solución."""
    resultado = busqueda_profundidad()

    assert resultado["encontrado"] is True


def test_ruta_inicia_y_termina_correctamente():
    """Comprueba el estado inicial y el estado meta de la ruta."""
    resultado = busqueda_profundidad()
    ruta = resultado["ruta"]

    assert ruta[0] == ESTADO_INICIAL
    assert ruta[-1] == ESTADO_META


def test_todos_los_estados_son_validos():
    """Comprueba que todos los estados de la ruta sean seguros."""
    resultado = busqueda_profundidad()

    for estado in resultado["ruta"]:
        assert es_estado_valido(estado)


def test_costo_de_ruta():
    """Comprueba que la solución encontrada tenga once cruces."""
    resultado = busqueda_profundidad()

    assert resultado["costo_ruta"] == 11
    assert len(resultado["movimientos"]) == 11
    assert len(resultado["ruta"]) == 12


def test_metricas_coherentes():
    """Comprueba que las métricas sean calculadas correctamente."""
    resultado = busqueda_profundidad()

    assert resultado["nodos_visitados"] > 0
    assert resultado["maximo_pila"] > 0

    assert (
        resultado["costo_total"]
        == resultado["costo_busqueda"] + resultado["costo_ruta"]
    )
