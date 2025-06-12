import streamlit as st
from lcr_code.operaciones import duplicar

# Slider de 0 a 100
valor = st.slider("Selecciona un valor", min_value=0, max_value=100, value=50)

# Llamar a la función del otro archivo
resultado = duplicar(valor)

# Mostrar el resultado en un cuadro de texto
st.text_input("Resultado (valor * 10)", value=str(resultado), disabled=True)
