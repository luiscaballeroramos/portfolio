import streamlit as st
from lcr_code.operaciones import sqrt

# Slider de 0 a 100
valor = st.slider("Selecciona un valor", min_value=0, max_value=100, value=64)

# Llamar a la función del otro archivo
resultado = sqrt(valor)

# Mostrar el resultado en un cuadro de texto
st.text_input("Squared root of value", value=str(resultado), disabled=True)
