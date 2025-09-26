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
st.set_page_config(page_title="Portfolio Luis Caballero Ramos", layout="wide")

# Hero section
st.markdown(
    """
    <div style="text-align: center; padding: 2em; background-color: var(--background-color); border-radius: 12px; margin-bottom: 2em;">
        <h1 style="color: var(--text-color); margin-bottom: 0.2em;">Luis Caballero Ramos</h1>
        <p style="color: var(--secondary-text-color); font-size: 1.2em;">Structural Engineer • Developer</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# --- Apps grouped into categories ---
ENGINEERING_UTILITIES = {
    "Unit Converter": {
        "path": "pages/app_unit_converter.py",
        "desc": "Convert engineering units for different magnitudes",
    },
    "Steel Section Properties": {
        "path": "pages/app_steel_section.py",
        "desc": "Cross-section properties for standard steel profiles",
    },
}
STRUCTURAL_TOOLS = {
    "Beam Model": {
        "path": "pages/app_beam.py",
        "desc": "Structural beam analysis and visualization with Bernoulli Beam Model (V & M)",
    },
    "Pile Model": {
        "path": "pages/app_pile.py",
        "desc": "Design and calculation of a single pile including geotechnical layers",
    },
}


def render_app_cards(apps):
    cols = st.columns(2)
    for i, (appName, app) in enumerate(apps.items()):
        with cols[i % 2]:
            st.page_link(app["path"], label=appName, use_container_width=True)
            # Improved CSS for perfect horizontal centering
            st.markdown(
                f"""
            <style>
            div[data-testid^="stPageLink"] > div {{
                border: 2px solid var(--text-color);
                border-radius: 16px;
                background-color: var(--background-color);
                color: inherit;
                display: flex;
                align-items: center;
                justify-content: center;
                text-align: center;
                height: 40px;
                font-size: 1.5em;
                font-weight: bold;
                transition: transform 0.2s, box-shadow 0.2s;
            }}
            div[data-testid^="stPageLink"] > div > span {{
                margin: auto;
                width: 100%;
                text-align: center;
                color: inherit;
                display: flex !important;
                align-items: center !important;
                justify-content: center !important;
            }}
            </style>
            """,
                unsafe_allow_html=True,
            )


# --- Display apps ---
st.subheader("📐 Engineering utilities")
render_app_cards(ENGINEERING_UTILITIES)

st.subheader("🛠️ Structural Tools")
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
#                     runpy.run_path(app["path"])
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
