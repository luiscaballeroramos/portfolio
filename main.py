import install_private_packages

import streamlit as st

st.set_page_config(page_title="main", layout="centered")
st.title("Portfolio Luis Caballero Ramos\n🚧 Portfolio Under Construction")
st.write("Select an app to run")
col1, col2 = st.columns(2)
with col1:
    st.page_link("pages/app_multiply.py", label="Squared Root Calculator")
with col2:
    st.page_link("pages/app_beam_forces.py", label="Beam Forces Calculator")
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
