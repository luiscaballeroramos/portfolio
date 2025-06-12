import streamlit as st
import subprocess
import sys
import requests

st.set_page_config(page_title="main", layout="centered")
st.title("Portfolio Luis Caballero Ramos")
st.write("Select an app to run")
col1, col2 = st.columns(2)
with col1:
    st.page_link("pages/app_multiply.py", label="Multiply")
with col2:
    st.page_link("pages/app_2.py", label="None")
