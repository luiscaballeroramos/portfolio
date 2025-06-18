import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Configuración
st.set_page_config(page_title="Esfuerzos en Viga Biapoyada", layout="wide")
st.title("🧱 Viga Biapoyada con Carga Puntual Variable")

# Parámetros de la viga
L = 1.0  # Longitud de la viga (m)
P = 1.0  # Valor de la carga (N), para normalización

# Slider para posición de la carga puntual
a = st.slider(
    "📍 Posición de la carga puntual (m)",
    min_value=0.0,
    max_value=L,
    value=L / 2,
    step=0.1,
)

# Cálculo de reacciones en apoyos
RA = P * (L - a) / L
RB = P * a / L

# Coordenadas
x = np.linspace(0, L, 500)

# Cortante V(x) y momento M(x)
V = np.piecewise(x, [x < a, x >= a], [lambda x: RA, lambda x: RA - P])
M = np.piecewise(x, [x < a, x >= a], [lambda x: RA * x, lambda x: RA * x - P * (x - a)])

# Normalización
Vn = V / P
Mn = M / (P * L)

# Plotting
fig, ax = plt.subplots(figsize=(10, 6), sharex=True)
# Cortante
ax.plot(x, Vn, label="Cortante V(x)/P", color="orange")
# Momento
ax.plot(x, Mn, label="Momento M(x)/(P·L)", color="blue")
# Línea vertical en x = a
ax.axvline(a, color="gray", linestyle="--")
# Línea horizontal en y = 0
ax.axhline(0, color="black", linestyle="--", linewidth=0.8)
# Ejes y etiquetas
ax.set_xlabel("")
ax.set_ylabel("")
ax.set_xticks([])
ax.set_yticks([])
ax.legend()


# Mostrar gráfico
st.pyplot(fig)

# Mostrar fórmulas de esfuerzo
st.markdown("### 🧮 Ecuaciones")
st.latex(
    r"""
V(x) = \begin{cases}
R_A = P \cdot \frac{L - a}{L} & \text{si } x < a \\
R_A - P & \text{si } x \geq a
\end{cases}
"""
)

st.latex(
    r"""
M(x) = \begin{cases}
R_A \cdot x & \text{si } x < a \\
R_A \cdot x - P \cdot (x - a) & \text{si } x \geq a
\end{cases}
"""
)
