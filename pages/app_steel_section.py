import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches

from examplesportfolio.profileproperties import propiedades_ipe
from examplesportfolio.steelprofilesection import profiles


st.title("Selector de perfiles metálicos")

# Desplegable tipo de perfil
col1, col2, col3 = st.columns(3)
with col1:
    tipo = st.selectbox("Tipo de perfil", list(profiles.keys()))
    # Desplegable subtipo basado en tipo seleccionado
    subtipo = st.selectbox("Subtipo de perfil", list(profiles[tipo].keys()))
with col2:
    # Mostrar dimensiones en formato lista, sin alineación especial
    dim = profiles[tipo][subtipo]
    st.subheader("Dimensiones")
    for k, v in dim.items():
        st.text(f"{str(k).rjust(20)}: {v}")
    st.subheader("Propiedades")
    if tipo == "I":
        A, Ixx = propiedades_ipe(dim["h"], dim["b"], dim["tw"], dim["tf"])
        st.write(f"A: {A:.1f} mm²")
        st.write(f"Ixx: {Ixx:.1f} mm⁴")


def draw_ipe(h, b, tw, tf, r):
    fig, ax = plt.subplots()
    color = "lightgrey"
    # web
    ax.add_patch(
        plt.Rectangle(
            (b / 2 - tw / 2, tf), tw, h - 2 * tf, facecolor=color, edgecolor="none"
        )
    )
    # flanges
    ax.add_patch(plt.Rectangle((0, 0), b, tf, facecolor=color, edgecolor="none"))
    ax.add_patch(plt.Rectangle((0, h - tf), b, tf, facecolor=color, edgecolor="none"))
    # radius corners
    # bottom left
    ax.add_patch(
        plt.Rectangle((b / 2 - tw / 2 - r, tf), r, r, facecolor=color, edgecolor="none")
    )
    ax.add_patch(
        patches.Wedge(
            center=(b / 2 - tw / 2 - r, tf + r),
            r=r,
            theta1=0,
            theta2=360,
            facecolor="white",
            edgecolor="none",
        )
    )
    # bottom right
    ax.add_patch(
        plt.Rectangle((b / 2 + tw / 2, tf), r, r, facecolor=color, edgecolor="none")
    )
    ax.add_patch(
        patches.Wedge(
            center=(b / 2 + tw / 2 + r, tf + r),
            r=r,
            theta1=0,
            theta2=360,
            facecolor="white",
            edgecolor="none",
        )
    )
    # top left
    ax.add_patch(
        plt.Rectangle(
            (b / 2 - tw / 2 - r, h - tf - r), r, r, facecolor=color, edgecolor="none"
        )
    )
    ax.add_patch(
        patches.Wedge(
            center=(b / 2 - tw / 2 - r, h - tf - r),
            r=r,
            theta1=0,
            theta2=360,
            facecolor="white",
            edgecolor="none",
        )
    )
    # top right
    ax.add_patch(
        plt.Rectangle(
            (b / 2 + tw / 2, h - tf - r), r, r, facecolor=color, edgecolor="none"
        )
    )
    ax.add_patch(
        patches.Wedge(
            center=(b / 2 + tw / 2 + r, h - tf - r),
            r=r,
            theta1=0,
            theta2=360,
            facecolor="white",
            edgecolor="none",
        )
    )

    # Cotas básicas
    ax.annotate(
        f"h={h}mm\ntw={tw}mm",
        xy=(b / 2 + tw, h / 2),
        # xytext=(b + 10, h / 2),
        # arrowprops=dict(arrowstyle="-["),
    )
    ax.annotate(
        f"b={b}mm\ntw={tw}mm",
        xy=(0, tf),
        # xytext=(b / 2, -10),
        # arrowprops=dict(arrowstyle="->"),
    )
    ax.set_xlim(-20, b + 30)
    ax.set_ylim(-20, h + 20)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig


with col3:
    if tipo == "I":
        r = dim.get("r", 0)
        fig = draw_ipe(dim["h"], dim["b"], dim["tw"], dim["tf"], r)
        st.pyplot(fig)
    elif tipo == "U":
        st.warning("Dibujo para perfil UPN aún no implementado.")
    elif tipo == "L":
        st.warning("Dibujo para perfil ángulo aún no implementado.")
    else:
        st.write("Dibujo no disponible para este tipo aún.")
