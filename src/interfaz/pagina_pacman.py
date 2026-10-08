
"""Interfaz Streamlit de Pac-Man con movimiento automático."""

import time

import streamlit as st

from src.algoritmos.minimax import buscar_minimax
from src.algoritmos.alfa_beta import buscar_alfa_beta
from src.problemas.pacman.problema import ProblemaPacman
from src.problemas.pacman.visualizacion import generar_svg


def ejecutar_turno(juego, estado, algoritmo, profundidad):
    """Calcula una decisión de IA y mueve a los personajes."""

    inicio = time.perf_counter()

    if algoritmo == "Minimax":
        resultado = buscar_minimax(juego, estado, profundidad)
    else:
        resultado = buscar_alfa_beta(juego, estado, profundidad)

    tiempo_ms = (time.perf_counter() - inicio) * 1000

    if resultado.movimiento is not None:
        estado = juego.mover_pacman(estado, resultado.movimiento)

        if not estado.terminado:
            movimientos = juego.movimientos_fantasma(estado)

            if movimientos:
                # El fantasma persigue a Pac-Man.
                direccion_fantasma = min(
                    movimientos,
                    key=lambda direccion: (
                        abs(movimientos[direccion][0] - estado.pacman[0])
                        + abs(movimientos[direccion][1] - estado.pacman[1])
                    ),
                )

                estado = juego.mover_fantasma(
                    estado, direccion_fantasma
                )

    metricas = {
        "algoritmo": algoritmo,
        "movimiento": resultado.movimiento,
        "valor": resultado.valor,
        "nodos": resultado.nodos_explorados,
        "tiempo_ms": tiempo_ms,
        "podas": getattr(resultado, "podas", 0),
    }

    return estado, metricas


def mostrar_pagina_pacman():
    st.title("🟡 Pac-Man — Inteligencia Artificial")
    st.caption("Búsqueda adversarial: Minimax y poda alfa-beta")

    if "pacman_juego" not in st.session_state:
        st.session_state.pacman_juego = ProblemaPacman()
        st.session_state.pacman_estado = (
            st.session_state.pacman_juego.estado_inicial()
        )
        st.session_state.pacman_ultima_decision = None
        st.session_state.pacman_reproduciendo = False

    juego = st.session_state.pacman_juego

    col1, col2 = st.columns(2)

    with col1:
        algoritmo = st.selectbox(
            "Algoritmo de búsqueda",
            ["Minimax", "Poda alfa-beta"],
        )

    with col2:
        profundidad = st.slider(
            "Profundidad",
            min_value=1,
            max_value=4,
            value=2,
        )

    velocidad = st.slider(
        "Velocidad (milisegundos por turno)",
        min_value=100,
        max_value=1000,
        value=350,
        step=50,
    )

    col_iniciar, col_pausar, col_reiniciar, col_paso = st.columns(4)

    with col_iniciar:
        if st.button("▶ Iniciar", use_container_width=True):
            if not st.session_state.pacman_estado.terminado:
                st.session_state.pacman_reproduciendo = True

    with col_pausar:
        if st.button("⏸ Pausar", use_container_width=True):
            st.session_state.pacman_reproduciendo = False

    with col_reiniciar:
        if st.button("↻ Reiniciar", use_container_width=True):
            st.session_state.pacman_estado = juego.estado_inicial()
            st.session_state.pacman_ultima_decision = None
            st.session_state.pacman_reproduciendo = False
            st.rerun()

    with col_paso:
        avanzar = st.button(
            "⏭ Un turno",
            use_container_width=True,
            disabled=st.session_state.pacman_reproduciendo,
        )

    if avanzar and not st.session_state.pacman_estado.terminado:
        nuevo_estado, metricas = ejecutar_turno(
            juego,
            st.session_state.pacman_estado,
            algoritmo,
            profundidad,
        )
        st.session_state.pacman_estado = nuevo_estado
        st.session_state.pacman_ultima_decision = metricas
        st.rerun()

    @st.fragment(run_every=velocidad / 1000)
    def actualizar_juego():
        estado = st.session_state.pacman_estado

        if st.session_state.pacman_reproduciendo and not estado.terminado:
            nuevo_estado, metricas = ejecutar_turno(
                juego, estado, algoritmo, profundidad
            )
            st.session_state.pacman_estado = nuevo_estado
            st.session_state.pacman_ultima_decision = metricas
            estado = nuevo_estado

        if estado.terminado:
            st.session_state.pacman_reproduciendo = False

        col_puntos, col_vidas, col_turnos = st.columns(3)

        col_puntos.metric("Puntuación", estado.puntuacion)
        col_vidas.metric("Vidas", estado.vidas)
        col_turnos.metric("Turnos", estado.turnos)

        svg = generar_svg(juego.laberinto, estado)

        st.markdown(
            f"""
            <div style="
                display:flex;
                justify-content:center;
                padding:15px;
                background:#050509;
                border:2px solid #235BFF;
                border-radius:12px;
                overflow-x:auto;
            ">
                {svg}
            </div>
            """,
            unsafe_allow_html=True,
        )

        if estado.terminado:
            if estado.victoria:
                st.success("¡Pac-Man ganó!")
            else:
                st.error("Pac-Man perdió todas sus vidas.")

        if st.session_state.pacman_reproduciendo:
            st.caption("🟢 Juego en ejecución")
        else:
            st.caption("⏸ Juego pausado")

        ultima = st.session_state.pacman_ultima_decision

        if ultima:
            st.subheader("Última decisión de la IA")
            st.write("**Algoritmo:**", ultima["algoritmo"])
            st.write("**Movimiento:**", ultima["movimiento"])

            met1, met2, met3 = st.columns(3)

            met1.metric("Nodos explorados", ultima["nodos"])
            met2.metric("Tiempo", f'{ultima["tiempo_ms"]:.2f} ms')
            met3.metric("Podas", ultima["podas"])

            st.write(
                "**Valor de evaluación:**",
                ultima["valor"],
            )

    actualizar_juego()
