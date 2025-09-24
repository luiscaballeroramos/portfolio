import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches

from section.ipe import ipeDict

# from section.hd import hdDict
# from section.he import heDict
# from section.hea import heaDict
# from section.heaa import heaaDict
# from section.heb import hebDict
# from section.hem import hemDict
# from section.hl import hlDict
# from section.hlz import hlzDict

typesDict = {
    "IPE": ipeDict,
}

if st.button("⬅️ Back to Home"):
    st.switch_page("main.py")
st.title("Steel profile selector")

col1, col2, col3 = st.columns(3)
with col1:
    # select type of steel profile
    typeProfile = st.selectbox("Steel profile type", list(typesDict.keys()))
    # list of items corresponding to type selected
    profileName = st.selectbox(
        "Steel profile item", list(typesDict[typeProfile].keys())
    )
with col2:
    # show dimensions and properties
    profile = typesDict[typeProfile][profileName]
    # for k, v in dim.items():
    #     st.text(f"{str(k).rjust(20)}: {v}")
    st.subheader("Properties")
    xCentroid, yCentroid = profile.centroid()
    area = profile.area()
    inertiaxxTotal, inertiayyTotal, inertiaxyTotal = profile.inertia()
    ix, iy = profile.radii_of_gyration()
    st.write(f"x centroid: {xCentroid:.2f} mm")
    st.write(f"y centroid: {yCentroid:.2f} mm")
    st.write(f"A: {area:.2f} mm²")
    st.write(f"Ixx: {inertiaxxTotal:.0f} mm⁴")
    st.write(f"Iyy: {inertiayyTotal:.0f} mm⁴")
    st.write(f"ix: {ix:.2f} mm")
    st.write(f"iy: {iy:.2f} mm")

with col3:
    st.subheader("Dimensions (mm)")
    fig, ax = profile.plot(show=False)
    st.pyplot(fig)
