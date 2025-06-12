import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Configuración
st.set_page_config(page_title="Esfuerzos en Viga Biapoyada", layout="wide")
st.title("🧱 Viga Biapoyada con Carga Puntual Variable")

# Parámetros de la viga
L = 10.0  # Longitud de la viga (m)
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
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6), sharex=True)

# Cortante
ax1.plot(x, Vn, label="Cortante V(x)/P", color="orange")
ax1.axvline(a, color="gray", linestyle="--", label="Carga puntual")
ax1.set_ylabel("Cortante normalizado")
ax1.grid(True)
ax1.legend()

# Momento
ax2.plot(x, Mn, label="Momento M(x)/(P·L)", color="blue")
ax2.axvline(a, color="gray", linestyle="--")
ax2.set_xlabel("x [m]")
ax2.set_ylabel("Momento normalizado")
ax2.grid(True)
ax2.legend()

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
