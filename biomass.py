import streamlit as st

# Biomass generation ratios (in percentage of FFB weight)
BIOMASS_RATIOS = {
    'Empty Fruit Bunches (EFB)': 0.22,    # 22% of FFB
    'Palm Kernel Shell (PKS)': 0.055,      # 5.5% of FFB
    'Mesocarp Fibre': 0.135,               # 13% of FFB
    'Palm Oil Mill Effluent (POME)': 0.67 # 67% of FFB
}

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
ffb_mt = st.number_input('Enter the amount of Fresh Fruit Bunches (FFB) in Metric Tons (MT):', min_value=0.0, value=10.0)

# Biomass calculation
if ffb_mt > 0:
    st.write(f"### Biomass Generated for {ffb_mt} MT of FFB:")
    biomass_results = calculate_biomass(ffb_mt)
    
    # Display results
    for biomass_type, biomass_amount in biomass_results.items():
        st.write(f"**{biomass_type}:** {biomass_amount:.2f} MT")

    st.write("---")
    st.markdown("""
    **Biomass Components**:
    - **Empty Fruit Bunches (EFB):** Residual bunches after oil extraction.
    - **Palm Kernel Shell (PKS):** Shell fragments from palm kernels.
    - **Mesocarp Fibre:** Fibrous residue from the palm fruit.
    - **Palm Oil Mill Effluent (POME):** Liquid waste by-product from palm oil mills.
    """)
else:
    st.warning("Please enter a valid amount of FFB to calculate biomass.")

# Optional Footer Information
st.sidebar.title("About the App")
st.sidebar.info("""
This app calculates the potential biomass produced from processing palm oil fresh fruit bunches (FFB).
Biomass such as Empty Fruit Bunches (EFB), Palm Kernel Shell (PKS), Mesocarp Fibre, and Palm Oil Mill Effluent (POME) 
are valuable by-products for energy generation and other applications.
""")
