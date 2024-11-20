import streamlit as st

# Default biomass generation ratios (in percentage of FFB weight)
DEFAULT_BIOMASS_RATIOS = {
    'Empty Fruit Bunches (EFB)': 0.21,    # 21% of FFB
    'Palm Kernel Shell (PKS)': 0.055,     # 5.5% of FFB
    'Mesocarp Fibre': 0.144,              # 14.4% of FFB
    'Decanter Cake': 0.035,               # 3.5% of FFB
    'Palm Oil Mill Effluent (POME)': 0.583 # 58.3% of FFB
}

# Constants for frond and trunk production
DEFAULT_FROND_MT_PER_HA = 14.47
DEFAULT_TRUNK_MT_PER_HA = 74.48

# Function to calculate biomass with custom ratios
def calculate_biomass(ffb_mt, biomass_ratios):
    biomass = {}
    for biomass_type, ratio in biomass_ratios.items():
        biomass[biomass_type] = ffb_mt * ratio
    return biomass

# Streamlit App UI
st.set_page_config(page_title="Biomass Calculator", page_icon="🌴", layout="wide")
st.title("Palm Oil Biomass Calculator")

# Add a tab selection at the top
tab1, tab2 = st.tabs(["Default Ratios", "Custom Ratios"])

with tab1:
    st.markdown("""
    ### Estimate the amount of biomass generated using default ratios
    Enter the amount of FFB in metric tons (MT) and the app will calculate the projected biomass output using standard ratios.
    """)

    # Display default ratios
    st.write("**Default Biomass Ratios:**")
    for biomass_type, ratio in DEFAULT_BIOMASS_RATIOS.items():
        st.write(f"- {biomass_type}: {ratio*100:.1f}%")

    # User input for FFB in MT (Default tab)
    ffb_mt_default = st.number_input('Enter the amount of Fresh Fruit Bunches (FFB) in Metric Tons (MT):', 
                                    min_value=0.0, value=100.0, key='ffb_default')

    # Biomass calculation with default ratios
    if ffb_mt_default > 0:
        st.write(f"### Biomass Generated for {ffb_mt_default} MT of FFB:")
        biomass_results = calculate_biomass(ffb_mt_default, DEFAULT_BIOMASS_RATIOS)
        
        # Display results
        for biomass_type, biomass_amount in biomass_results.items():
            st.write(f"**{biomass_type}:** {biomass_amount: ,.2f} MT")

    # Default plantation area calculation
    st.markdown("""
    ---
    ### Estimate Biomass from Plantation Area
    Enter the plantation area in hectares to estimate the amount of frond and trunk biomass produced.
    """)

    plantation_area_ha_default = st.number_input('Enter the plantation area in hectares (ha):', 
                                               min_value=0.0, value=100.0, key='area_default')

    if plantation_area_ha_default > 0:
        frond_biomass = plantation_area_ha_default * DEFAULT_FROND_MT_PER_HA
        trunk_biomass = plantation_area_ha_default * DEFAULT_TRUNK_MT_PER_HA
        
        st.write(f"### Biomass Produced from Plantation Area of {plantation_area_ha_default} ha:")
        st.write(f"**Oil Palm Frond (OPF):** {frond_biomass: ,.2f} MT")
        st.write(f"**Oil Palm Trunk (OPT):** {trunk_biomass: ,.2f} MT")

with tab2:
    st.markdown("""
    ### Customize biomass generation ratios
    Enter your own ratios for each biomass component (as percentages). The total should sum to 100%.
    """)

    # Create columns for better layout
    col1, col2 = st.columns([2, 1])

    with col1:
        # Create a dictionary to store custom ratios
        custom_ratios = {}
        total_percentage = 0

        # Input fields for custom ratios
        for biomass_type in DEFAULT_BIOMASS_RATIOS.keys():
            default_percentage = DEFAULT_BIOMASS_RATIOS[biomass_type] * 100
            custom_percentage = st.number_input(
                f"{biomass_type} (%)", 
                min_value=0.0, 
                max_value=100.0, 
                value=default_percentage,
                step=0.1,
                key=f"custom_{biomass_type}"
            )
            custom_ratios[biomass_type] = custom_percentage / 100
            total_percentage += custom_percentage

        # Display total percentage and warning if not 100%
        st.write(f"**Total Percentage: {total_percentage:.1f}%**")
        if abs(total_percentage - 100) > 0.1:  # Allow for small floating-point differences
            st.warning("⚠️ The total percentage should be 100%")

    with col2:
        # Show the default values for reference
        st.write("**Default Values (for reference):**")
        for biomass_type, ratio in DEFAULT_BIOMASS_RATIOS.items():
            st.write(f"- {biomass_type}: {ratio*100:.1f}%")
    
    # User input for FFB in MT (Custom tab)
    ffb_mt_custom = st.number_input('Enter the amount of Fresh Fruit Bunches (FFB) in Metric Tons (MT):', 
                                   min_value=0.0, value=100.0, key='ffb_custom')

    # Biomass calculation with custom ratios
    if ffb_mt_custom > 0:
        st.write(f"### Biomass Generated for {ffb_mt_custom} MT of FFB:")
        biomass_results = calculate_biomass(ffb_mt_custom, custom_ratios)
        
        # Display results
        for biomass_type, biomass_amount in biomass_results.items():
            st.write(f"**{biomass_type}:** {biomass_amount: ,.2f} MT")

    # Custom plantation area calculation
    st.markdown("""
    ---
    ### Customize Plantation Biomass Estimates
    Enter your own values for frond and trunk biomass production per hectare.
    """)

    # Create columns for custom plantation inputs
    col3, col4 = st.columns(2)

    with col3:
        custom_frond_mt_per_ha = st.number_input(
            'Oil Palm Frond (OPF) production (MT/ha/year):',
            min_value=0.0,
            value=DEFAULT_FROND_MT_PER_HA,
            step=0.01,
            help=f"Default value is {DEFAULT_FROND_MT_PER_HA} MT/ha/year"
        )

        custom_trunk_mt_per_ha = st.number_input(
            'Oil Palm Trunk (OPT) production (MT/ha/year):',
            min_value=0.0,
            value=DEFAULT_TRUNK_MT_PER_HA,
            step=0.01,
            help=f"Default value is {DEFAULT_TRUNK_MT_PER_HA} MT/ha/year"
        )

    with col4:
        plantation_area_ha_custom = st.number_input(
            'Plantation area (ha):',
            min_value=0.0,
            value=100.0,
            key='area_custom'
        )

    if plantation_area_ha_custom > 0:
        custom_frond_biomass = plantation_area_ha_custom * custom_frond_mt_per_ha
        custom_trunk_biomass = plantation_area_ha_custom * custom_trunk_mt_per_ha
        
        st.write(f"### Custom Biomass Produced from Plantation Area of {plantation_area_ha_custom} ha:")
        st.write(f"**Oil Palm Frond (OPF):** {custom_frond_biomass: ,.2f} MT")
        st.write(f"**Oil Palm Trunk (OPT):** {custom_trunk_biomass: ,.2f} MT")

        # Show comparison with default values
        st.write("#### Comparison with Default Calculations:")
        default_frond_biomass = plantation_area_ha_custom * DEFAULT_FROND_MT_PER_HA
        default_trunk_biomass = plantation_area_ha_custom * DEFAULT_TRUNK_MT_PER_HA
        
        frond_diff = ((custom_frond_biomass - default_frond_biomass) / default_frond_biomass) * 100
        trunk_diff = ((custom_trunk_biomass - default_trunk_biomass) / default_trunk_biomass) * 100
        
        st.write(f"**OPF Difference:** {frond_diff:+.1f}% from default")
        st.write(f"**OPT Difference:** {trunk_diff:+.1f}% from default")

# Original footer content and sidebar remain the same...

st.write("---")
st.markdown("""
**Biomass Components**:
- **Empty Fruit Bunches (EFB):** Residual bunches after oil extraction.
- **Palm Kernel Shell (PKS):** Shell fragments from palm kernels.
- **Mesocarp Fibre:** Fibrous residue from the palm fruit.
- **Decanter Cake:** Solid waste produced from the three phase separation step of crude palm oil process.
- **Palm Oil Mill Effluent (POME):** Liquid waste by-product from palm oil mills.
- **Oil Palm Frond (OPF):** The leaves of the palm, often used as animal feed or compost.
- **Oil Palm Trunk (OPT):** The trunk of the palm, commonly used as a source of biomass for energy or as a raw material in wood-based industries.
""")

st.write("---")
st.markdown("""
**References**:
- Cheah, W. Y., Siti-Dina, R. P., Leng, S. T. K., Er, A. C., & Show, P. L. (2023). Circular bioeconomy in palm oil industry: Current practices and future perspectives. Environmental Technology & Innovation, 30, 103050. https://doi.org/10.1016/j.eti.2023.103050
- Abioye, K. J., Harun, N. Y., Umar, H. A., & Kolawole, A. H. (2023). Study of Physicochemical Properties of Palm Oil Decanter Cake for Potential Syngas Generation. Chemical Engineering Transactions, 99, 709–714. https://doi.org/10.3303/CET2399119
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
