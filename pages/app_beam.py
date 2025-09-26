import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

from main import STRUCTURAL_TOOLS
from structuralelement.beam2d import Beam2D

appName = "Beam Model"
app = STRUCTURAL_TOOLS[appName]
st.set_page_config(page_title=appName, page_icon="🛠️")

# Aumentar el grosor de líneas del hatch
plt.rcParams["hatch.linewidth"] = 2.0


def reset_variable(variableName, default_value):
    """Reset the specified variable to the default value."""
    st.session_state[variableName] = default_value


# --- Beam Parameters ---
if st.button("⬅️ Back to Home"):
    st.switch_page("main.py")
st.title(appName)
st.write(app["desc"])
st.markdown("---")

st.title("Bernoulli Beam Model (V & M)")
with st.expander("Beam Parameters"):
    default_E_GPa = "210.0"  # default young modulus in GPa
    default_I_mm4 = "8000000"  # default moment of inertia in mm⁴
    if "young_modulus" not in st.session_state:
        st.session_state.young_modulus = default_E_GPa
    if "inertia" not in st.session_state:
        st.session_state.inertia = default_I_mm4
    length = st.slider(
        "Beam Length (m)", min_value=2.0, max_value=20.0, value=10.0, step=2.0
    )
    col1, col2, col3, col4 = st.columns([4, 1, 4, 1])
    with col1:
        st.text_input(label="Young Modulus (GPa)", key="young_modulus")
    with col2:
        if st.button(
            "🔄",
            key="reset_E",
            on_click=reset_variable,
            args=("young_modulus", default_E_GPa),
        ):
            st.rerun()
    with col3:
        st.text_input(label="Moment of Inertia (mm⁴)", key="inertia")
    with col4:
        if st.button(
            "🔄",
            key="reset_I",
            on_click=reset_variable,
            args=("inertia", default_I_mm4),
        ):
            st.rerun()
    # unit conversion
    try:
        E = float(st.session_state.young_modulus) * 1e9  # GPa → Pa
    except ValueError:
        st.error("Please enter a valid number for the Young Modulus.")
        E = None
    try:
        I = float(st.session_state.inertia) * 1e-12  # mm⁴ → m⁴
    except ValueError:
        st.error("Please enter a valid number for the Moment of Inertia.")
        I = None
# --- Supports ---
with st.expander("Supports"):
    col1, col2, col3 = st.columns([1, 3, 1])
    with col1:
        left_support = st.selectbox("Left Support", ["Fixed", "Simple", "Free"])
    with col2:
        use_middle_support = st.checkbox("Include Middle Support")
    with col3:
        right_support = st.selectbox("Right Support", ["Fixed", "Simple", "Free"])
    col1, col2, col3 = st.columns([1, 5, 1])
    with col2:
        if use_middle_support:
            middle_support_position = st.slider(
                "Middle Support Position (m)",
                min_value=1.0,
                max_value=length - 1.0,
                value=length / 2,
                step=0.5,
            )
# --- Point Loads ---
with st.expander("Point Loads"):
    use_point_load = st.checkbox("Include Point Load")
    if use_point_load:
        point_load_magnitude = st.slider(
            "Point Load Magnitude (kN)",
            min_value=1,
            max_value=100,
            value=10,
            step=1,
        )
        col1, col2, col3 = st.columns([1, 16, 1])
        with col2:
            point_load_position = st.slider(
                "Point Load Position (m)",
                min_value=0.0,
                max_value=length,
                value=length / 2,
                step=0.5,
            )
# --- Distributed Loads ---
with st.expander("Distributed Loads"):
    use_distributed = st.checkbox("Include Distributed Load")
    if use_distributed:
        st.markdown("Coeficientes del polinomio w(x) = a₀ + a₁·x + a₂·x²")
        col1, col2, col3 = st.columns(3)
        with col1:
            a0 = st.number_input("a₀", value=50.0, step=0.5)
        with col2:
            a1 = st.number_input("a₁", value=0.0, step=0.5)
        with col3:
            a2 = st.number_input("a₂", value=0.0, step=0.5)
        if use_distributed:
            col1, col2, col3 = st.columns([1, 16, 1])
            with col2:
                x1, x2 = st.slider(
                    "Intervalo de carga (m)",
                    0.0,
                    length,
                    (length * 0.2, length * 0.8),
                    step=0.5,
                )
# --- Plot ---
fig, ax = plt.subplots(figsize=(8, 2))
ax.set_xlim(-length * 0.1, length * 1.1)
ax.set_ylim(-1, 2)
ax.axis("off")
# --- Beam ---
ax.plot([0, length], [0, 0], color="black", linewidth=3)
# --- Dibujar apoyos ---
# Escala constante para los apoyos (en metros, relativo)
support_height = 0.8
support_width = 0.05


def draw_support(x, kind):
    if kind == "Fixed":
        # Rectángulo vertical con hachurado (empotramiento)
        rect = patches.Rectangle(
            (x - support_width * length / 2, -support_height),
            support_width * length,
            2 * support_height,
            hatch="///",
            facecolor="none",
            edgecolor="black",
            linewidth=0,
        )
        ax.add_patch(rect)
    elif kind == "Simple":
        # Triángulo isósceles
        triangle = [
            [x - support_width * length / 2, -support_height],
            [x, 0],
            [x + support_width * length / 2, -support_height],
        ]
        ax.add_patch(plt.Polygon(triangle, closed=True, color="black"))


# left support
if left_support != "Free":
    draw_support(0, left_support)
# right support
if right_support != "Free":
    draw_support(length, right_support)
# middle support (optional)
if use_middle_support:
    draw_support(middle_support_position, "Simple")
# --- Plot Point Load ---
if use_point_load:
    # arrow plot
    ax.annotate(
        "",  # sin texto
        xy=(point_load_position, 0),  # punta de flecha
        xytext=(point_load_position, 2.5),  # inicio de flecha
        arrowprops=dict(arrowstyle="->", color="red", lw=2),
    )
    # value label
    ax.text(
        point_load_position + 0.1,
        0.6,
        f"{point_load_magnitude} kN",
        color="red",
        fontsize=10,
    )
# --- Plot Distributed Load ---
if use_distributed:
    # load function
    # q(x) = a0 + a1*x + a2*x²
    num_points = max(10, int(25 * (x2 - x1) / length))
    x_vals = np.linspace(x1, x2, num=num_points)
    q_vals = a0 + a1 * x_vals + a2 * x_vals**2
    max_q = np.max(np.abs(q_vals))
    if max_q == 0:
        max_q = 1  # avoid division by zero
    scale = 1.5 / max_q  # scale arrows
    for xi, qi in zip(x_vals, q_vals):
        arrow_len = qi * scale
        ax.annotate(
            "",
            xy=(xi, 0),
            xytext=(xi, arrow_len),
            arrowprops=dict(arrowstyle="->", color="blue", lw=1.5),
        )
    # value label
    ax.text((x1 + x2) / 2, 1.2, "q(x)", color="blue", fontsize=10)
# show figure
st.pyplot(fig)
# --- Calculate reactions and efforts ---
# create the beam model and calculate reactions and efforts
st.markdown("### Calculations")


def calculate_beam():
    # supports
    supports = []
    supports.append((0, left_support.lower()))
    supports.append((length, right_support.lower()))
    if use_middle_support:
        supports.insert(1, (middle_support_position, "simple"))
    # point loads
    point_loads = []
    if use_point_load:
        point_loads.append((point_load_position, point_load_magnitude))
    # distributed loads
    distributed_loads = []
    if use_distributed:
        distributed_loads.append(((x1, x2), f"{a0} + {a1}*x + {a2}*x**2"))

    beam = Beam2D(
        youngModulus=float(st.session_state.young_modulus) * 1e9,  # GPa to Pa
        inertia=float(st.session_state.inertia) * 1e-12,  # mm⁴ to m⁴
        length=length,
        supports=supports,
        pointLoads=point_loads,
        pointMoments=[],
        distributedLoads=distributed_loads,
    )
    try:
        beam.solve()
        return beam
    except Exception as e:
        st.error(f"Error al calcular la viga: {e}")
        return None


# button to calculate the beam
if st.button("Calculate Beam"):
    # Crear el modelo de la viga
    calculatedBeam = calculate_beam()
    if calculatedBeam:
        # data plot from beam
        xVals, wVals, thetaVals, vVals, mVals = calculatedBeam.data_plot()
        fig2, axs = plt.subplots(2, 1, figsize=(6, 5))
        # Combined Deflection (w) and Slope (θ)
        ax0 = axs[0]
        ax0_2 = ax0.twinx()
        # common limits
        wMax = np.nanmax(np.abs(wVals))
        thetaMax = np.nanmax(np.abs(thetaVals))
        wLims = (-wMax, wMax)
        thetaLims = (-thetaMax, thetaMax)
        ax0.fill_between(
            xVals,
            0,
            wVals,
            where=~np.isnan(wVals),
            color="skyblue",
            alpha=0.25,
            label="Deflection (w)",
        )
        ax0.set_ylabel("Deflection (m)", color="skyblue")
        ax0.tick_params(axis="y", labelcolor="skyblue")
        ax0.set_ylim(wLims)
        ax0_2.fill_between(
            xVals,
            0,
            thetaVals,
            where=~np.isnan(thetaVals),
            color="peachpuff",
            alpha=0.5,
            label="Slope (θ)",
        )
        ax0_2.set_ylabel("Slope (rad)", color="peru")
        ax0_2.tick_params(axis="y", labelcolor="peru")
        ax0_2.set_ylim(thetaLims)
        # common title and x_labels
        ax0.set_title("Deflection (w) and Slope (θ)")
        ax0.set_xlabel("x (m)")
        # Combined Shear (V) and Bending Moment (M)
        axs1 = axs[1]
        axs1_2 = axs1.twinx()
        # common limits
        vMax = np.nanmax(np.abs(vVals))
        mMax = np.nanmax(np.abs(mVals))
        vLims = (-vMax, vMax)
        mLims = (-mMax, mMax)
        axs1.fill_between(
            xVals,
            0,
            vVals,
            where=~np.isnan(vVals),
            color="lightgreen",
            alpha=0.5,
            label="Shear force (V)",
        )
        axs1.set_ylabel("Shear force (N)", color="lightgreen")
        axs1.tick_params(axis="y", labelcolor="lightgreen")
        axs1.set_ylim(vLims)
        axs1_2.fill_between(
            xVals,
            0,
            mVals,
            where=~np.isnan(mVals),
            color="lightcoral",
            alpha=0.25,
            label="Bending Moment (M)",
        )
        axs1_2.set_ylabel("Bending Moment (N·m)", color="lightcoral")
        axs1_2.tick_params(axis="y", labelcolor="lightcoral")
        axs1_2.set_ylim(mLims)
        # common title and x_labels
        axs1.set_title("Shear (V) and Moment (M)")
        axs1.set_xlabel("x (m)")
        # general settings for all subplots
        plt.tight_layout(rect=[0, 0.05, 1, 1])
        st.pyplot(fig2)

        # reactions
        st.markdown("### Reactions")

        def reactions_text(reactions, xRef):
            has_support = any(
                xSupport == xRef for xSupport, _, vReaction, mReaction in reactions
            )
            if not has_support:
                return None
            else:
                for xSupport, _, vReaction, mReaction in reactions:
                    if xSupport == xRef:
                        vReaction = 0 if vReaction is None else vReaction
                        mReaction = 0 if mReaction is None else mReaction
                        return vReaction, mReaction

        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            vReaction, mReaction = reactions_text(calculatedBeam.reactions, 0)
            st.markdown(f"V (0): {vReaction:.2f} N")
            st.markdown(f"M (0): {mReaction:.2f} Nm")
        with col2:
            if use_middle_support:
                vReaction, mReaction = reactions_text(
                    calculatedBeam.reactions, middle_support_position
                )
                st.markdown(f"V ({middle_support_position:.2f} m): {vReaction:.2f} N")
                st.markdown(f"M ({middle_support_position:.2f} m): {mReaction:.2f} Nm")
        with col3:
            vReaction, mReaction = reactions_text(calculatedBeam.reactions, length)
            st.markdown(f"V ({length:.2f} m): {vReaction:.2f} N")
            st.markdown(f"M ({length:.2f} m): {mReaction:.2f} Nm")

        # # efforts formulas
        # st.markdown("### Efforts Formulas")
        # # Print LaTeX function of w(x)
        # st.markdown("#### Deflection function $w(x)$")
        # latex_formula = calculatedBeam.latex_function(calculatedBeam.wSpans)
        # latex_formula = latex_formula.replace(r"inertia", "I")
        # latex_formula = latex_formula.replace(r"e", "E")
        # st.latex(latex_formula)

        # efforts formulas
        st.markdown("### Max / Min Values")
        minmax = calculatedBeam.get_minmax()
        col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
        for i, (key, value) in enumerate(minmax.items()):
            maxPos, maxVal = value["max"]
            minPos, minVal = value["min"]
            # format positions as lists of floats with 2 decimals
            maxPosStr = (
                [f"{float(p):.2f}" for p in maxPos]
                if isinstance(maxPos, list)
                else f"{float(maxPos):.2f}"
            )
            minPosStr = (
                [f"{float(p):.2f}" for p in minPos]
                if isinstance(minPos, list)
                else f"{float(minPos):.2f}"
            )
            # Format values with 2 decimals
            try:
                maxValStr = f"{float(maxVal):.2f}"
            except Exception:
                maxValStr = str(maxVal)
            try:
                minValStr = f"{float(minVal):.2f}"
            except Exception:
                minValStr = str(minVal)
            col = (
                col1
                if i % 4 == 0
                else col2 if i % 4 == 1 else col3 if i % 4 == 2 else col4
            )
            col.markdown(f"{key} max: {maxValStr}")
            col.markdown(f"{key} min: {minValStr}")
