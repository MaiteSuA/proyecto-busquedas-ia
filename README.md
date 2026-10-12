# Proyecto de Búsquedas en Inteligencia Artificial

## Descripción del proyecto

Este proyecto tiene como objetivo implementar y comparar diferentes algoritmos de búsqueda utilizados en Inteligencia Artificial mediante la resolución de dos problemas: **Misioneros y Caníbales** y **Pac-Man**.

El sistema fue desarrollado en Python y utiliza Streamlit para proporcionar una interfaz gráfica interactiva que permite visualizar la ejecución de los algoritmos, los resultados obtenidos y diferentes métricas de rendimiento.

## Problemas implementados

### 1. Misioneros y Caníbales

Consiste en trasladar tres misioneros y tres caníbales de una orilla del río a otra utilizando una embarcación con capacidad máxima para dos personas.

Durante el traslado se debe garantizar que los caníbales nunca superen en número a los misioneros en una orilla donde haya misioneros.

**Algoritmos implementados:**

- Búsqueda en anchura (BFS).
- Búsqueda en profundidad (DFS).

El sistema permite encontrar y visualizar una secuencia válida de cruces hasta alcanzar el estado objetivo.

### 2. Pac-Man

Se implementó una versión simplificada del videojuego Pac-Man, donde un agente inteligente debe recolectar los puntos distribuidos en un laberinto mientras evita a un fantasma adversario.

**Características principales:**

- Laberinto bidimensional de 20 × 19 posiciones.
- Un fantasma adversario.
- Tres vidas iniciales.
- Recolección de puntos.
- Evaluación heurística para seleccionar movimientos.
- Profundidades de búsqueda configurables de 1 a 4.

**Algoritmos implementados:**

- Minimax.
- Minimax con poda alfa-beta.

El agente analiza posibles movimientos futuros y selecciona acciones según la evaluación de los estados. La poda alfa-beta permite reducir la cantidad de nodos explorados sin modificar la decisión de Minimax bajo las mismas condiciones.

## Tecnologías utilizadas

- **Python:** lenguaje principal de programación.
- **Streamlit:** desarrollo de la interfaz gráfica.
- **Git:** control de versiones.
- **GitHub:** almacenamiento del repositorio y colaboración entre integrantes.
- **Visual Studio Code:** entorno de desarrollo.

## Instalación y ejecución

### 1. Clonar el repositorio

```bash
git clone https://github.com/MaiteSuA/proyecto-busquedas-ia.git
```

### 2. Ingresar al proyecto

```bash
cd proyecto-busquedas-ia
```

### 3. Crear un entorno virtual

```bash
python -m venv .venv
```

### 4. Activar el entorno virtual

En Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 5. Instalar las dependencias

Si el proyecto dispone de un archivo `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 6. Ejecutar la aplicación

```bash
python -m streamlit run app.py
```

Una vez iniciado Streamlit, abrir la dirección local que aparece en la terminal, generalmente:

`http://localhost:8501`

## Funcionamiento del sistema

Al iniciar la aplicación se presenta una interfaz desde la cual es posible seleccionar uno de los dos problemas.

**Misioneros y Caníbales:** permite ejecutar BFS o DFS y visualizar los estados de la solución, los movimientos de la embarcación y el costo de la ruta.

**Pac-Man:** permite seleccionar Minimax o poda alfa-beta, configurar la profundidad de búsqueda y observar los movimientos del agente, la puntuación, las vidas disponibles y las métricas de exploración.

## Comparación de algoritmos

El proyecto permite analizar las diferencias entre las metodologías implementadas.

| Problema | Algoritmos | Tipo de búsqueda |
|---|---|---|
| Misioneros y Caníbales | BFS y DFS | No informada |
| Pac-Man | Minimax y poda alfa-beta | Adversarial |

Los resultados permiten estudiar aspectos como los estados explorados, el costo de búsqueda, la cantidad de movimientos y la eficiencia computacional.

## Objetivo académico

Aplicar los fundamentos de búsqueda en Inteligencia Artificial mediante la implementación de algoritmos en problemas prácticos, analizando sus características, ventajas, limitaciones y comportamiento durante la ejecución.

## Integrantes

Proyecto académico desarrollado en equipo para la asignatura de Inteligencia Artificial.

## Repositorio

https://github.com/MaiteSuA/proyecto-busquedas-ia