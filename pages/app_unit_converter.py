import streamlit as st
from main import ENGINEERING_UTILITIES
from unit.convert import (
    length,
    area,
    volume,
    force,
    mass,
    time,
    angle,
    pressure,
    energy,
    power,
    speed,
    density,
)

appName = "Unit Converter"
app = ENGINEERING_UTILITIES[appName]
st.set_page_config(page_title=appName, page_icon="📐")
converters = {
    "Length": length,
    "Area": area,
    "Volume": volume,
    "Mass": mass,
    "Density": density,
    "Force": force,
    "Pressure": pressure,
    "Time": time,
    "Speed": speed,
    "Angle": angle,
    "Energy": energy,
    "Power": power,
}

if st.button("⬅️ Back to Home"):
    st.switch_page("main.py")

st.title(appName)
st.write(app["desc"])
st.markdown("---")

# select magnitude
magnitude = st.selectbox("Select magnitude", list(converters.keys()))
# track magnitude change
if "magnitude" not in st.session_state:
    st.session_state.magnitude = magnitude
    st.session_state.base_value = 1.0
    st.session_state.input_unit = list(converters[magnitude].units.keys())[0]
if st.session_state.magnitude != magnitude:
    st.session_state.magnitude = magnitude
    st.session_state.base_value = 1.0
    st.session_state.input_unit = list(converters[magnitude].units.keys())[0]
converter = converters[magnitude]
units = list(converter.units.keys())

# Initialize session state
if "base_value" not in st.session_state:
    st.session_state.base_value = 1.0
if "input_unit" not in st.session_state:
    st.session_state.input_unit = units[0]

# Columns for unit & value
col_val, col_unit = st.columns([4, 2])

with col_unit:
    selected_unit = st.selectbox(
        "Input unit", units, index=units.index(st.session_state.input_unit)
    )
    # If unit changes, recalc base_value to keep numeric value consistent
    if selected_unit != st.session_state.input_unit:
        # Convert current input_value in old unit to base_value
        st.session_state.base_value *= (
            converter.units[st.session_state.input_unit]
            / converter.units[selected_unit]
        )
        st.session_state.input_unit = selected_unit


with col_val:
    # Show value corresponding to selected unit
    input_value = st.number_input(
        f"Value in {st.session_state.input_unit}",
        format="%.3f",
        value=st.session_state.base_value,
        step=1.0,
    )
    # Update base_value when user edits input
    st.session_state.base_value = (
        input_value * converter.units[st.session_state.input_unit]
    )

# Convert base_value to all units
converted_values = {u: st.session_state.base_value / converter.units[u] for u in units}
converted_values = dict(
    sorted(converted_values.items(), key=lambda item: item[1], reverse=True)
)

# Display results
col1, col2 = st.columns([4, 2])
with col1:
    st.write("Values")
    for u in converted_values.keys():
        st.write(f"{converted_values[u]:.3f}")
with col2:
    st.write("Units")
    for u in converted_values.keys():
        st.write(u)
