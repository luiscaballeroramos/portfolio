import streamlit as st
import matplotlib.pyplot as plt
from steel_calculation.steelprofilesection import profiles
from steel_calculation.profileproperties import propiedades_ipe


st.title("Selector de perfiles metálicos")

# Desplegable tipo de perfil
tipo = st.selectbox("Tipo de perfil", list(profiles.keys()))

# Desplegable subtipo basado en tipo seleccionado
subtipo = st.selectbox("Subtipo de perfil", list(profiles[tipo].keys()))

# Mostrar dimensiones
dim = profiles[tipo][subtipo]
st.write(f"Dimensiones del perfil {subtipo}:")
for k, v in dim.items():
    st.write(f"{k} = {v} mm")


def draw_ipe(h, b, tw, tf):
    fig, ax = plt.subplots()
    # Dibujar alma
    ax.add_patch(plt.Rectangle((b / 2 - tw / 2, 0), tw, h, color="grey"))
    # Dibujar alas
    ax.add_patch(plt.Rectangle((0, h - tf), b, tf, color="grey"))
    ax.add_patch(plt.Rectangle((0, 0), b, tf, color="grey"))
    # Cotar (sólo ejemplo básico)
    ax.annotate(
        f"h={h}mm",
        xy=(b, h / 2),
        xytext=(b + 10, h / 2),
        arrowprops=dict(arrowstyle="->"),
    )
    ax.annotate(
        f"b={b}mm", xy=(b / 2, 0), xytext=(b / 2, -10), arrowprops=dict(arrowstyle="->")
    )
    ax.set_xlim(-10, b + 30)
    ax.set_ylim(-20, h + 20)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig


if tipo == "I":
    fig = draw_ipe(dim["h"], dim["b"], dim["tw"], dim["tf"])
    st.pyplot(fig)
else:
    st.write("Dibujo no disponible para este tipo aún.")


if tipo == "I":
    A, Ixx = propiedades_ipe(dim["h"], dim["b"], dim["tw"], dim["tf"])
    st.write(f"Área: {A:.1f} mm²")
    st.write(f"Momento de inercia Ixx: {Ixx:.1f} mm⁴")
