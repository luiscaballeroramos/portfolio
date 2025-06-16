import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from lcr_code.steel_calculation.steelprofilesection import profiles
from lcr_code.steel_calculation.profileproperties import propiedades_ipe


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


def draw_ipe(h, b, tw, tf, r, r1):
    fig, ax = plt.subplots()
    color = "lightgrey"

    # Alma
    ax.add_patch(plt.Rectangle((b / 2 - tw / 2, r), tw, h - 2 * r, color=color))

    # Alas
    ax.add_patch(
        plt.Rectangle((0, h - tf), b, tf - r1, color=color)
    )  # ala superior sin redondeo
    ax.add_patch(
        plt.Rectangle((0, 0 + r1), b, tf - r1, color=color)
    )  # ala inferior sin redondeo

    # Radios internos (esquinas entre alma y ala)
    ax.add_patch(
        patches.Arc(
            (b / 2 - tw / 2, tf), 2 * r, 2 * r, theta1=180, theta2=270, color=color
        )
    )
    ax.add_patch(
        patches.Arc(
            (b / 2 + tw / 2, tf), 2 * r, 2 * r, theta1=270, theta2=360, color=color
        )
    )
    ax.add_patch(
        patches.Arc(
            (b / 2 - tw / 2, h - tf), 2 * r, 2 * r, theta1=90, theta2=180, color=color
        )
    )
    ax.add_patch(
        patches.Arc(
            (b / 2 + tw / 2, h - tf), 2 * r, 2 * r, theta1=0, theta2=90, color=color
        )
    )

    # Radios externos (en las esquinas de las alas)
    ax.add_patch(
        patches.Arc((0, r1), 2 * r1, 2 * r1, theta1=180, theta2=270, color=color)
    )
    ax.add_patch(
        patches.Arc((b, r1), 2 * r1, 2 * r1, theta1=270, theta2=360, color=color)
    )
    ax.add_patch(
        patches.Arc((0, h - r1), 2 * r1, 2 * r1, theta1=90, theta2=180, color=color)
    )
    ax.add_patch(
        patches.Arc((b, h - r1), 2 * r1, 2 * r1, theta1=0, theta2=90, color=color)
    )

    # Cotas básicas
    ax.annotate(
        f"h={h}mm",
        xy=(b, h / 2),
        xytext=(b + 10, h / 2),
        arrowprops=dict(arrowstyle="->"),
    )
    ax.annotate(
        f"b={b}mm", xy=(b / 2, 0), xytext=(b / 2, -10), arrowprops=dict(arrowstyle="->")
    )

    ax.set_xlim(-20, b + 30)
    ax.set_ylim(-20, h + 20)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig


if tipo == "I":
    fig = draw_ipe(dim["h"], dim["b"], dim["tw"], dim["tf"], dim["r"], dim["r1"])
    st.pyplot(fig)
else:
    st.write("Dibujo no disponible para este tipo aún.")


if tipo == "I":
    A, Ixx = propiedades_ipe(dim["h"], dim["b"], dim["tw"], dim["tf"])
    st.write(f"Área: {A:.1f} mm²")
    st.write(f"Momento de inercia Ixx: {Ixx:.1f} mm⁴")
