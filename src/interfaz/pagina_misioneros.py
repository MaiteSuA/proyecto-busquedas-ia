"""Interfaz del problema de Misioneros y Caníbales."""

import time

import streamlit as st

from src.algoritmos.profundidad import busqueda_profundidad
from src.problemas.misioneros.visualizacion import (
    preparar_metricas,
    preparar_pasos,
)


def mostrar_pagina_misioneros():
    """Muestra la solución obtenida mediante profundidad."""

    st.title("Misioneros y Caníbales")

    st.write(
        """
        El problema consiste en trasladar tres misioneros y tres
        caníbales desde la orilla izquierda hasta la orilla derecha.
        La canoa puede transportar como máximo dos personas.
        """
    )

    st.write("Método utilizado: búsqueda en profundidad")
    st.write("Estado inicial: (3, 3, I)")
    st.write("Estado meta: (0, 0, D)")

    mostrar_animacion = st.checkbox("Mostrar animación")

    velocidad = 0.8

    if mostrar_animacion:
        velocidad = st.slider(
            "Tiempo entre movimientos (segundos)",
            min_value=0.2,
            max_value=2.0,
            value=0.8,
            step=0.2,
        )

    if st.button("Ejecutar búsqueda"):
        resultado = busqueda_profundidad()

        if resultado["encontrado"]:
            st.success("Se encontró una solución.")
        else:
            st.error("No se encontró una solución.")
            return

        metricas = preparar_metricas(resultado)

        st.subheader("Resultados")

        tabla_metricas = [
            {
                "Parámetro": nombre,
                "Resultado": valor,
            }
            for nombre, valor in metricas.items()
        ]

        st.table(tabla_metricas)

        pasos = preparar_pasos(
            resultado["ruta"],
            resultado["movimientos"],
        )

        if mostrar_animacion:
            st.subheader("Animación de la solución")

            espacio_animacion = st.empty()
            progreso = st.progress(0)

            for indice, paso in enumerate(pasos):
                with espacio_animacion.container():
                    st.write(
                        f"Paso {paso['numero']}: "
                        f"{paso['accion']}"
                    )

                    st.write(
                        "Orilla izquierda: "
                        f"{paso['misioneros_izquierda']}M, "
                        f"{paso['canibales_izquierda']}C"
                    )

                    st.write(
                        f"Canoa: {paso['canoa']}"
                    )

                    st.write(
                        "Orilla derecha: "
                        f"{paso['misioneros_derecha']}M, "
                        f"{paso['canibales_derecha']}C"
                    )

                    st.code(str(paso["estado"]))

                progreso.progress(
                    (indice + 1) / len(pasos)
                )

                time.sleep(velocidad)

            st.success("Animación finalizada.")

        st.subheader("Ruta solución")

        tabla_ruta = []

        for paso in pasos:
            tabla_ruta.append(
                {
                    "Paso": paso["numero"],
                    "Acción": paso["accion"],
                    "Estado": str(paso["estado"]),
                    "Orilla izquierda": (
                        f"{paso['misioneros_izquierda']}M, "
                        f"{paso['canibales_izquierda']}C"
                    ),
                    "Orilla derecha": (
                        f"{paso['misioneros_derecha']}M, "
                        f"{paso['canibales_derecha']}C"
                    ),
                    "Canoa": paso["canoa"],
                }
            )

        st.table(tabla_ruta)


if __name__ == "__main__":
    mostrar_pagina_misioneros()