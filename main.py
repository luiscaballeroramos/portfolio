import streamlit as st
import subprocess
import sys
import requests

# Leer token desde secrets
token = st.secrets["GITHUB_TOKEN"]

# Instalar repo privado si no está presente
repo_url = f"https://{token}@github.com/luiscaballeroramos/lcr_code.git"
try:
    import lcr_code
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", f"git+{repo_url}"])
    import lcr_code

# Verificar autenticación
headers = {"Authorization": f"token {token}"}
response = requests.get("https://api.github.com/user", headers=headers)
if response.status_code == 200:
    user_data = response.json()
    st.success(f"Authenticated as: {user_data['login']}")
else:
    st.error(f"GitHub API error: {response.status_code}")

# Continúa con tu app
st.set_page_config(page_title="main", layout="centered")
st.title("Portfolio Luis Caballero Ramos")
st.write("Select an app to run")
col1, col2 = st.columns(2)
with col1:
    st.page_link("pages/app_multiply.py", label="Multiply")
with col2:
    st.page_link("pages/app_2.py", label="None")
