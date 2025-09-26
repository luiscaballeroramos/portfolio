import streamlit as st
from dataclasses import dataclass
import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches

from main import STRUCTURAL_TOOLS

appName = "Pile Model"
app = STRUCTURAL_TOOLS[appName]
st.set_page_config(page_title=appName, page_icon="🛠️")


# --- DATACLASSES ---
@dataclass
class SteelProperties:
    fy: float  # yield strength [MPa]
    fu: float  # ultimate strength [MPa]
    gamma_M0: float = 1.0
    gamma_M1: float = 1.1


@dataclass
class PileGeometry:
    length: float  # [m]
    diameter: float  # [m]
    thickness: float  # [m]

    @property
    def area(self):
        return math.pi * (
            (self.diameter / 2) ** 2 - ((self.diameter - 2 * self.thickness) / 2) ** 2
        )


@dataclass
class SoilLayer:
    thickness: float  # [m]
    cu: float  # undrained cohesion [Pa]
    alpha: float  # adhesion factor


# --- STRUCTURAL ---
def axial_resistance(steel: SteelProperties, geo: PileGeometry):
    return steel.fy * 1e6 * geo.area / steel.gamma_M0


def buckling_resistance(steel: SteelProperties, geo: PileGeometry, K=2.0, E=210e9):
    A = geo.area
    Do = geo.diameter
    t = geo.thickness
    I = math.pi / 64 * (Do**4 - (Do - 2 * t) ** 4)
    Lcr = geo.length * K
    slenderness = Lcr * math.sqrt(steel.fy * 1e6 / (E * math.pi**2)) / math.sqrt(I / A)
    alpha = 0.49  # curve c for tubes
    phi = 0.5 * (1 + alpha * (slenderness - 0.2) + slenderness**2)
    chi = 1 / (phi + math.sqrt(phi**2 - slenderness**2))
    chi = min(1.0, chi)
    return chi * steel.fy * 1e6 * A / steel.gamma_M1


def plastic_moment_resistance(steel: SteelProperties, geo: PileGeometry):
    Do = geo.diameter
    Di = Do - 2 * geo.thickness
    W_pl = (math.pi / 4) * ((Do / 2) ** 3 - (Di / 2) ** 3)
    return steel.fy * 1e6 * W_pl / steel.gamma_M0


# --- GEOTECHNICAL ---
def compute_geotechnical_capacity(layers: list[SoilLayer], geo: PileGeometry, Nc=9):
    Q_s = 0
    depth_accum = 0
    for layer in layers:
        depth_in_layer = min(layer.thickness, geo.length - depth_accum)
        if depth_in_layer <= 0:
            break
        perimeter = math.pi * geo.diameter
        Q_s += layer.alpha * layer.cu * perimeter * depth_in_layer
        depth_accum += depth_in_layer
    A_b = math.pi * (geo.diameter / 2) ** 2
    cu_tip = layers[-1].cu  # Last = deepest
    Q_b = cu_tip * Nc * A_b
    return Q_s + Q_b


# --- EVALUATION ---
def evaluate_pile_full(steel, geo, soil_layers, K=2.0):
    N_Rd = axial_resistance(steel, geo)
    N_b_Rd = buckling_resistance(steel, geo, K)
    M_Rd = plastic_moment_resistance(steel, geo)
    Q_geo = compute_geotechnical_capacity(soil_layers, geo)
    return {
        "Axial resistance [kN]": N_Rd / 1e3,
        "Buckling resistance [kN]": N_b_Rd / 1e3,
        "Moment resistance [kNm]": M_Rd / 1e3,
        "Geotechnical capacity [kN]": Q_geo / 1e3,
        "Governing axial capacity [kN]": min(N_Rd, N_b_Rd, Q_geo) / 1e3,
    }


# --- PLOT FUNCTION ---
def plot_pile_and_soil(geo: PileGeometry, soil_layers: list[SoilLayer]):
    fig, ax = plt.subplots(figsize=(3, 6))
    depth = 0
    n = len(soil_layers)
    for i, layer in enumerate(soil_layers):
        h = min(layer.thickness, geo.length - depth)
        # if h <= 0:
        #     break
        # Capa desde profundidad "depth" hasta "depth + h"
        cmap_val = 0.2 + 0.6 * (i / max(1, n - 1))  # entre 0.2 y 0.8 del colormap
        rect = patches.Rectangle(
            (0.6, depth),  # x, y (y = profundidad actual)
            0.8,
            depth + layer.thickness,
            linewidth=1,
            edgecolor=None,
            alpha=0.5,
            facecolor=plt.cm.terrain(cmap_val),
        )
        ax.add_patch(rect)
        ax.text(
            1.5,
            depth + layer.thickness / 2,
            f"Layer {i+1}\ncu={layer.cu/1e3:.0f} kPa",
            va="center",
            fontsize=8,
        )
        depth += layer.thickness
    # Dibujo del pilote
    ax.plot([1.0, 1.0], [0, geo.length], color="grey", linewidth=None, label="Pile")
    ax.set_xlim(0, 3)
    maxDepth = sum(layer.thickness for layer in soil_layers)
    ax.set_ylim(0, max(geo.length + 0.5, maxDepth + 0.5))
    ax.set_title("Pile and Soil Stratigraphy")
    ax.set_ylabel("Depth [m]")
    ax.invert_yaxis()  # ahora sí, sentido físico: profundidad va hacia abajo
    ax.axis("off")
    st.pyplot(fig)


# --- STREAMLIT APP ---

if st.button("⬅️ Back to Home"):
    st.switch_page("main.py")
st.title(appName)
st.write(app["desc"])
st.markdown("---")

st.sidebar.header("Pile Geometry")
L = st.sidebar.number_input("Length [m]", 1.0, 50.0, 10.0, step=0.5)
D = st.sidebar.number_input("Diameter [m]", 0.1, 2.0, 0.3, step=0.05)
t = st.sidebar.number_input("Wall thickness [m]", 0.005, 0.05, 0.012, step=0.01)

st.sidebar.header("Steel Properties")
fy = st.sidebar.number_input("Yield strength fy [MPa]", 100, 1000, 355)
fu = st.sidebar.number_input("Ultimate strength fu [MPa]", 100, 1200, 510)

geo = PileGeometry(L, D, t)
steel = SteelProperties(fy, fu)

st.sidebar.header("Soil Stratigraphy")
num_layers = st.sidebar.number_input("Number of layers", 1, 10, 3)
layers = []
for i in range(num_layers):
    cols = st.columns(4)
    with cols[0]:
        st.subheader(f"Layer {i+1}")
    with cols[1]:
        thickness = st.number_input(
            f"Thickness [m] - Layer {i+1}", 0.1, 50.0, 5.0, key=f"t{i}", step=1.0
        )
    with cols[2]:
        cu = st.number_input(
            f"Cohesion cu [kPa] - Layer {i+1}", 1.0, 500.0, 50.0, key=f"cu{i}", step=5.0
        )
    with cols[3]:
        alpha = st.number_input(
            f"Alpha - Layer {i+1}", 0.1, 1.0, 0.5, key=f"a{i}", step=0.05
        )
        layers.append(SoilLayer(thickness, cu * 1e3, alpha))

col1, col2 = st.columns([1, 2])
with col1:
    if st.button("Run Design"):
        results = evaluate_pile_full(steel, geo, layers)
        st.success("Design complete")
        for k, v in results.items():
            st.write(f"**{k}**:")
            st.write(f"{v:.2f}")
with col2:
    st.subheader("Visualization")
    plot_pile_and_soil(geo, layers)
