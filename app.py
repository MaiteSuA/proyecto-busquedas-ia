
import streamlit as st

from src.interfaz.pagina_pacman import mostrar_pagina_pacman
from src.interfaz.pagina_misioneros import mostrar_pagina_misioneros


st.set_page_config(
    page_title="Sistema de Búsquedas IA",
    page_icon="🧠",
    layout="wide",
)

st.sidebar.title("Inteligencia Artificial")

problema = st.sidebar.radio(
    "Selecciona un problema",
    ["Pac-Man", "Misioneros y Caníbales"],
)

if problema == "Pac-Man":
    mostrar_pagina_pacman()
else:
    mostrar_pagina_misioneros()
