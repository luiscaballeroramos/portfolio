import streamlit as st
from install_private_packages import install_all_packages

if "packages_installed" not in st.session_state:
    local = False
    try:
        install_all_packages(local=local, force_reinstall=False)
    except Exception as e:
        st.error(f"⚠️ Could not install private packages: {e}")
    st.session_state["packages_installed"] = True


# Page config
st.set_page_config(page_title="Portfolio Luis Caballero Ramos", layout="centered")

# Hero section
st.markdown(
    """
    <div style="
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 1.5em;
        padding: 2em;
        background-color: var(--background-color);
        border-radius: 12px;
        margin-bottom: 2em;
    ">
        <img src="https://github.com/luiscaballeroramos.png"
             alt="Luis Caballero Ramos"
             style="width:120px; height:120px; border-radius:50%; box-shadow:0px 3px 10px rgba(0,0,0,0.15);">
        <div style="text-align: left;">
            <h1 style="color: var(--text-color); margin-bottom: 0.2em;">Luis Caballero Ramos</h1>
            <p style="color: var(--secondary-text-color); font-size: 1.2em;">Structural Engineer • Developer</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# --- Apps grouped into categories ---
ENGINEERING_UTILITIES = {
    "Unit Converter": {
        "page": "pages/app_unit_converter.py",
        "desc": "Convert engineering units for different magnitudes",
    },
    "Steel Section Properties": {
        "page": "pages/app_steel_section.py",
        "desc": "Cross-section properties for standard steel profiles",
    },
}
STRUCTURAL_TOOLS = {
    "Beam Model": {
        "page": "pages/app_beam.py",
        "desc": "Structural beam analysis and visualization with Bernoulli Beam Model (V & M)",
    },
    "Pile Model": {
        "page": "pages/app_pile.py",
        "desc": "Design and calculation of a single pile including geotechnical layers",
    },
}


def render_app_cards(apps):
    cols = st.columns(2)
    for i, (appName, app) in enumerate(apps.items()):
        with cols[i % 2]:
            st.page_link(app["page"], label=appName, use_container_width=True)

    # CSS centrado, limpio y estable
    st.markdown(
        """
        <style>
        /* Estilo general de las tarjetas de enlace */
        div[data-testid^="stPageLink"] {
            display: flex;
            justify-content: center;
            align-items: center;
            text-align: center;
            border: 2px solid var(--text-color, #bbb);
            border-radius: 16px;
            background-color: var(--background-color);
            color: inherit;
            height: 35px;
            font-size: 1.3em;
            font-weight: 600;
            transition: all 0.2s ease;
            box-shadow: 0px 1px 3px rgba(0,0,0,0.1);
        }

        /* Efecto hover */
        div[data-testid^="stPageLink"]:hover {
            transform: translateY(-3px);
            box-shadow: 0px 4px 10px rgba(0,0,0,0.15);
        }

        /* Centrado perfecto del texto dentro del enlace */
        div[data-testid^="stPageLink"] a {
            width: 100%;
            height: 100%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: inherit;
            text-decoration: none;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


# --- Display apps ---
st.markdown(
    '<h2 style="text-align: center;">📐 Engineering utilities</h2>',
    unsafe_allow_html=True,
)
render_app_cards(ENGINEERING_UTILITIES)

st.markdown(
    '<h2 style="text-align: center;">🛠️ Structural Tools</h2>',
    unsafe_allow_html=True,
)
render_app_cards(STRUCTURAL_TOOLS)

# # Combine everything into one list of categories
# categories = {
#     "📐 Engineering utilities": utilities,
#     "🛠️ Structural Tools": structuralTools,
# }

# # --- Tabs for categories ---
# cat_tabs = st.tabs(list(categories.keys()))

# for cat_tab, (cat_name, apps) in zip(cat_tabs, categories.items()):
#     with cat_tab:
#         # Create one tab per app inside each category
#         app_tabs = st.tabs([appName for app in apps])
#         for i, app in enumerate(apps):
#             with app_tabs[i]:
#                 st.markdown(f"### {appName}")
#                 st.caption(app["desc"])
#                 # Run the page inline
#                 try:
#                     runpy.run_path(app["page"])
#                 except Exception as e:
#                     st.error(f"⚠️ Could not load {appName}: {e}")

# --- Footer ---
st.markdown("---")
# Centered subheader and footer links
st.markdown(
    """
    <div style="text-align: center;">
        <h3 style="margin-bottom: 0.5em;">🔗 Stay Connected</h3>
        <ul style="list-style: none; padding-left: 0;">
            <li style="margin-bottom: 0.5em;">
                💼 <a href="https://www.linkedin.com/in/luiscaballeroramos/" target="_blank">LinkedIn</a>
            </li>
            <li style="margin-bottom: 0.5em;">
                📧 <a href="mailto:luiscaballeroramos@gmail.com">Email me</a>
            </li>
            <li>
                💻 <a href="https://github.com/luiscaballeroramos" target="_blank">GitHub</a>
            </li>
        </ul>
    </div>
    """,
    unsafe_allow_html=True,
)
