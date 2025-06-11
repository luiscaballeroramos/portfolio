import streamlit as st

st.set_page_config(page_title="main", layout="centered")
st.title("PortfolioLuis Caballero Ramos")
st.write("select an app to run")
col1, col2 = st.columns(2)
with col1:
    st.page_link("app_multiply.py", label="Multiply")
with col2:
    st.page_link("app_2.py", label="None")
