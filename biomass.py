import streamlit as st

# Biomass generation ratios (in percentage of FFB weight)
BIOMASS_RATIOS = {
    'Empty Fruit Bunches (EFB)': 0.21,    # 21% of FFB
    'Palm Kernel Shell (PKS)': 0.055,     # 5.5% of FFB
    'Mesocarp Fibre': 0.144,              # 14.4% of FFB
    'Decanter Cake': 0.035,               # 3.5% of FFB
    'Palm Oil Mill Effluent (POME)': 0.583 # 58.3% of FFB
    
}

# Constants for frond and trunk production
FROND_MT_PER_HA = 14.47
TRUNK_MT_PER_HA = 74.48

# Function to calculate biomass
def calculate_biomass(ffb_mt):
    biomass = {}
    for biomass_type, ratio in BIOMASS_RATIOS.items():
        biomass[biomass_type] = ffb_mt * ratio
    return biomass

# Streamlit App UI
st.title("Palm Oil Biomass Calculator")

st.markdown("""
### Estimate the amount of biomass generated from processing Fresh Fruit Bunches (FFB)
Enter the amount of FFB in metric tons (MT) and the app will calculate the projected biomass output.
""")

# User input for FFB in MT
ffb_mt = st.number_input('Enter the amount of Fresh Fruit Bunches (FFB) in Metric Tons (MT):', min_value=0.0, value=100.0)

# Biomass calculation
if ffb_mt > 0:
    st.write(f"### Biomass Generated for {ffb_mt} MT of FFB:")
    biomass_results = calculate_biomass(ffb_mt)
    
    # Display results
    for biomass_type, biomass_amount in biomass_results.items():
        st.write(f"**{biomass_type}:** {biomass_amount:.2f} MT")

# User input for plantation area in hectares
st.markdown("""
---
### Estimate Biomass from Plantation Area
Enter the plantation area in hectares to estimate the amount of frond and trunk biomass produced.
""")

plantation_area_ha = st.number_input('Enter the plantation area in hectares (ha):', min_value=0.0, value=100.0)

# Calculation of frond and trunk biomass based on plantation area
if plantation_area_ha > 0:
    frond_biomass = plantation_area_ha * FROND_MT_PER_HA
    trunk_biomass = plantation_area_ha * TRUNK_MT_PER_HA
    
    st.write(f"### Biomass Produced from Plantation Area of {plantation_area_ha} ha:")
    st.write(f"**Oil Palm Frond (OPF):** {frond_biomass:.2f} MT")
    st.write(f"**Oil Palm Trunk (OPT):** {trunk_biomass:.2f} MT")

st.write("---")
st.markdown("""
**Biomass Components**:
- **Empty Fruit Bunches (EFB):** Residual bunches after oil extraction.
- **Palm Kernel Shell (PKS):** Shell fragments from palm kernels.
- **Mesocarp Fibre:** Fibrous residue from the palm fruit.
- **Palm Oil Mill Effluent (POME):** Liquid waste by-product from palm oil mills.
- **Oil Palm Frond (OPF):** The leaves of the palm, often used as animal feed or compost.
- **Oil Palm Trunk (OPT):** The trunk of the palm, commonly used as a source of biomass for energy or as a raw material in wood-based industries.
""")

st.write("---")
st.markdown("""
**References**:
Cheah, W. Y., Siti-Dina, R. P., Leng, S. T. K., Er, A. C., & Show, P. L. (2023). Circular bioeconomy in palm oil industry: Current practices and future perspectives. Environmental Technology & Innovation, 30, 103050. https://doi.org/10.1016/j.eti.2023.103050
Abioye, K. J., Harun, N. Y., Umar, H. A., & Kolawole, A. H. (2023). Study of Physicochemical Properties of Palm Oil Decanter Cake for Potential Syngas Generation. Chemical Engineering Transactions, 99, 709–714. https://doi.org/10.3303/CET2399119
""")

st.write("---")
st.markdown("""

**Developed by**:
Mohd Rafizan Samian, Jabatan Perancangan Strategi dan Transformasi, FELDA
""")

# Optional Footer Information
st.sidebar.title("About the App")
st.sidebar.info("""
This app calculates the potential biomass produced from processing palm oil fresh fruit bunches (FFB) and estimates the additional biomass generated from oil palm fronds (OPF) and trunks (OPT) based on plantation area in hectares. Biomass by-products, such as Empty Fruit Bunches (EFB), Palm Kernel Shell (PKS), Mesocarp Fibre, Palm Oil Mill Effluent (POME), as well as OPF and OPT, play crucial roles in a circular economy. They contribute to sustainable energy production, soil enrichment, animal feed, and even wood-based materials, maximizing resource use and minimizing waste in the palm oil industry.
""")
