import streamlit as st
from unit.convert import length, area, volume, force, mass, time, angle

converters = {
    "Length": length,
    "Area": area,
    "Volume": volume,
    "Force": force,
    "Mass": mass,
    "Time": time,
    "Angle": angle,
}

st.title("Dynamic Multi-Unit Converter")

# magnitude, input_unit, input_value
magnitude = st.selectbox("Select magnitude", list(converters.keys()))
converter = converters[magnitude]
units = list(converter.units.keys())
col_val, col_unit = st.columns([4, 2])
with col_unit:
    input_unit = st.selectbox("Input unit", units)
with col_val:
    input_value = st.number_input(
        f"Value in {input_unit}", format="%.6f", value=1.0, step=1.0
    )

# Convertir valor base para todas las unidades
# Primero convertimos input_value de input_unit a base
base_value = input_value * converter.units[input_unit]

# Luego convertimos base_value a todas unidades disponibles
converted_values = {}
for u in units:
    converted_values[u] = base_value / converter.units[u]
# Ordenar las unidades por valor convertido en orden descendente
converted_values = dict(
    sorted(converted_values.items(), key=lambda item: item[1], reverse=True)
)
# Mostrar resultados en dos columnas: unidades | valores
col1, col2 = st.columns([4, 2])
with col1:
    st.write("Values")
    for u in converted_values.keys():
        st.write(f"{converted_values[u]:.6f}")
with col2:
    st.write("Units")
    for u in converted_values.keys():
        st.write(u)
