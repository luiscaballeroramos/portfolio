import install_private_packages

import streamlit as st

# Configuración inicial
st.set_page_config(page_title="main", layout="centered")

# Estilo global para botones (afecta también a st.page_link)
st.markdown(
    """
    <style>
    /* Afecta botones en general, incluyendo los de st.page_link */
    button[kind="link"] {
        border: 2px solid #777777 !important;  /* Gris medio */
        border-radius: 8px;
        padding: 0.5em 1em;
        margin: 0.3em 0;
        color: #fafafa;
        background-color: #0e1117;
    }

    button[kind="link"]:hover {
        border-color: #aaaaaa;
        background-color: #222222;
    }
    </style>
""",
    unsafe_allow_html=True,
)

st.title("Portfolio Luis Caballero Ramos")
st.title("🚧 under construction🚧")
st.write(
    "<div style='text-align: center;'>Select an app to run</div>",
    unsafe_allow_html=True,
)
st.markdown("---")
col1, col2 = st.columns(2)
with col1:
    st.page_link(
        "pages/app_beam.py",
        label="Beam Model",
        use_container_width=True,
    )
    st.page_link(
        "pages/app_pile.py",
        label="Pile Design",
        use_container_width=True,
    )
    st.page_link(
        "pages/app_steel_section.py",
        label="Steel Section Calculator",
        use_container_width=True,
    )
    st.page_link(
        "pages/app_unit_converter.py",
        label="Unit Converter",
        use_container_width=True,
    )
with col2:
    st.markdown(
        "<div style='text-align: center;'>More apps (Coming Soon)</div>",
        unsafe_allow_html=True,
    )

st.markdown("---")
st.subheader("🔗 Stay Connected")
st.markdown(
    """
    - 💼 [LinkedIn](https://www.linkedin.com/in/luiscaballeroramos/)  
    - 📧 [Email me](mailto:luiscaballeroramos@gmail.com)  
    - 🧑‍💻 [GitHub](https://github.com/luiscaballeroramos)  
    """,
    unsafe_allow_html=True,
)
