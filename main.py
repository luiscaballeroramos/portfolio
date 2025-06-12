import streamlit as st
import requests

# Leer token desde secrets
token = st.secrets["github"]["token"]
# Opcional: hacer una llamada a la API de GitHub para demostrar autenticación
headers = {"Authorization": f"token {token}"}
response = requests.get("https://api.github.com/user", headers=headers)
if response.status_code == 200:
    user_data = response.json()
    st.success(f"Authenticated as: {user_data['login']}")
else:
    st.error(f"GitHub API error: {response.status_code}")





st.set_page_config(page_title="main", layout="centered")
st.title("PortfolioLuis Caballero Ramos")
st.write("select an app to run")
col1, col2 = st.columns(2)
with col1:
    st.page_link("pages/app_multiply.py", label="Multiply")
with col2:
    st.page_link("pages/app_2.py", label="None")





# Mostrar token parcialmente (solo los primeros 4 caracteres como demo)
st.write(f"Token starts with: {token[:4]}...")
