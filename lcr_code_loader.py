import subprocess
import sys
import streamlit as st

def ensure_lcr_code():
    try:
        import lcr_code
    except ImportError:
        token = st.secrets["github"]["token"]
        repo_url = f"https://{token}@github.com/luiscaballeroramos/lcr_code.git"
        subprocess.check_call([sys.executable, "-m", "pip", "install", f"git+{repo_url}"])
        import lcr_code
    return lcr_code
