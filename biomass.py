import streamlit as st
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd

# Default biomass generation ratios (in percentage of FFB weight)
DEFAULT_BIOMASS_RATIOS = {
    'Empty Fruit Bunches (EFB)': 0.21,    # 21% of FFB
    'Palm Kernel Shell (PKS)': 0.055,     # 5.5% of FFB
    'Mesocarp Fibre': 0.144,              # 14.4% of FFB
    'Decanter Cake': 0.035,               # 3.5% of FFB
    'Palm Oil Mill Effluent (POME)': 0.583, # 58.3% of FFB
    'Sludge Palm Oil (SPO)': 0.01,        # 1.0% of FFB
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

# Enhanced Streamlit App UI
st.set_page_config(
    page_title="Palm Biomass Calculator", 
    page_icon="🌴", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for improved styling
st.markdown("""
<style>
    .stApp {
        background-color: #f0f2f6;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 10px 15px;
        background-color: #ffffff;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #e6f2ff;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background-color: #007bff;
        color: white;
    }
    .metric-card {
        background-color: white;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
    }
    .metric-card:hover {
        transform: scale(1.05);
    }
</style>
""", unsafe_allow_html=True)

# Main Title with Subtitle
st.title("🌴 Palm Oil Biomass Calculator")
st.markdown("### Sustainable Biomass Estimation for Palm Oil Production")

# Sidebar with Detailed Information
st.sidebar.image("https://via.placeholder.com/250x150.png?text=Palm+Oil+Biomass", use_column_width=True)
st.sidebar.title("About the Calculator")
st.sidebar.info("""
This advanced tool helps you:
- Estimate biomass from Fresh Fruit Bunches (FFB)
- Customize biomass generation ratios
- Calculate plantation-level biomass production
- Visualize biomass distribution
""")

# Add tabs for different calculation methods
tab1, tab2, tab3 = st.tabs([
    "🔢 Default Ratios", 
    "🛠️ Custom Ratios", 
    "📊 Biomass Insights"
])

with tab1:
    st.markdown("### Biomass Estimation Using Standard Ratios")
    
    # Create columns for input and default ratios
    #col1, col2 = st.columns([2, 1])
    
    #with col1:
    ffb_mt_default = st.number_input(
        'Enter Fresh Fruit Bunches (FFB) in Metric Tons:', 
        min_value=0.0, 
        value=100.0, 
        key='ffb_default',
        help="Amount of Fresh Fruit Bunches processed"
    )
    
    #with col2:
    st.markdown("#### Default Biomass Ratios")
    cols = st.columns(len(DEFAULT_BIOMASS_RATIOS.item))
        for i, (biomass_type, biomass_amount) in enumerate(DEFAULT_BIOMASS_RATIOS.item()):
            with cols[i]:
                st.markdown(f"<div class='metric-card'><h4>{biomass_type}</h4><p>{biomass_amount:,.2f} MT</p></div>", unsafe_allow_html=True)
   
        #for biomass_type, ratio in DEFAULT_BIOMASS_RATIOS.items():
            #st.metric(label=biomass_type, value=f"{ratio*100:.1f}%")
        
       
   
    
    # Biomass calculation and visualization
    if ffb_mt_default > 0:
        biomass_results = calculate_biomass(ffb_mt_default, DEFAULT_BIOMASS_RATIOS)
        
        # Bar Chart instead of Pie Chart
        df_biomass = pd.DataFrame.from_dict(biomass_results, orient='index', columns=['Quantity'])
        df_biomass.index.name = 'Biomass Type'
        df_biomass = df_biomass.reset_index().sort_values('Quantity', ascending=False)
        
        fig = px.bar(
            df_biomass, 
            x='Biomass Type', 
            y='Quantity', 
            title=f'Biomass Distribution for {ffb_mt_default} MT of FFB',
            color='Biomass Type',
            text_auto=True
        )
        fig.update_traces(texttemplate='%{y:,.2f} MT', textposition='outside')
        fig.update_layout(
            xaxis_title='Biomass Type',
            yaxis_title='Quantity (MT)',
            height=500
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Detailed Results
        st.markdown("### Detailed Biomass Breakdown")
        cols = st.columns(len(biomass_results))
        for i, (biomass_type, biomass_amount) in enumerate(biomass_results.items()):
            with cols[i]:
                st.markdown(f"<div class='metric-card'><h4>{biomass_type}</h4><p>{biomass_amount:,.2f} MT</p></div>", unsafe_allow_html=True)

with tab2:
    st.markdown("### Customize Biomass Generation Ratios")
    
    # Custom Ratio Inputs
    col1, col2 = st.columns([2, 1])
    
    with col1:
        custom_ratios = {}
        total_percentage = 0
        
        for biomass_type in DEFAULT_BIOMASS_RATIOS.keys():
            default_percentage = DEFAULT_BIOMASS_RATIOS[biomass_type] * 100
            custom_percentage = st.slider(
                f"{biomass_type} (%)", 
                min_value=0.0, 
                max_value=100.0, 
                value=default_percentage,
                step=0.1,
                help=f"Adjust the percentage for {biomass_type}"
            )
            custom_ratios[biomass_type] = custom_percentage / 100
        
    with col2:
        st.markdown("#### Ratio Guidelines")
        st.info("""
        - Adjust sliders freely
        - Percentages don't need to sum to 100%
        - Use regional or specific mill data
        """)
    
    # FFB Input and Calculation
    ffb_mt_custom = st.number_input(
        'Enter Fresh Fruit Bunches (FFB) in Metric Tons:', 
        min_value=0.0, 
        value=100.0, 
        key='ffb_custom'
    )
    
    if ffb_mt_custom > 0:
        biomass_results_custom = calculate_biomass(ffb_mt_custom, custom_ratios)
        
        # Bar Chart for Custom Ratios
        df_biomass_custom = pd.DataFrame.from_dict(biomass_results_custom, orient='index', columns=['Quantity'])
        df_biomass_custom.index.name = 'Biomass Type'
        df_biomass_custom = df_biomass_custom.reset_index().sort_values('Quantity', ascending=False)
        
        fig_custom = px.bar(
            df_biomass_custom, 
            x='Biomass Type', 
            y='Quantity', 
            title=f'Custom Biomass Distribution for {ffb_mt_custom} MT of FFB',
            color='Biomass Type',
            text_auto=True
        )
        fig_custom.update_traces(texttemplate='%{y:,.2f} MT', textposition='outside')
        fig_custom.update_layout(
            xaxis_title='Biomass Type',
            yaxis_title='Quantity (MT)',
            height=500
        )
        st.plotly_chart(fig_custom, use_container_width=True)

        # Detailed Results
        st.markdown("### Detailed Biomass Breakdown")
        cols = st.columns(len(biomass_results_custom))
        for i, (biomass_type, biomass_amount) in enumerate(biomass_results_custom.items()):
            with cols[i]:
                st.markdown(f"<div class='metric-card'><h4>{biomass_type}</h4><p>{biomass_amount:,.2f} MT</p></div>", unsafe_allow_html=True)


with tab3:
    st.markdown("### Plantation Biomass Insights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Frond Biomass")
        custom_frond_mt_per_ha = st.number_input(
            'Oil Palm Frond (OPF) production (MT/ha/year):',
            min_value=0.0,
            value=DEFAULT_FROND_MT_PER_HA,
            step=0.01,
            help=f"Default value is {DEFAULT_FROND_MT_PER_HA} MT/ha/year"
        )
    
    with col2:
        st.markdown("#### Trunk Biomass")
        custom_trunk_mt_per_ha = st.number_input(
            'Oil Palm Trunk (OPT) production (MT/ha/year):',
            min_value=0.0,
            value=DEFAULT_TRUNK_MT_PER_HA,
            step=0.01,
            help=f"Default value is {DEFAULT_TRUNK_MT_PER_HA} MT/ha/year"
        )
    
    plantation_area_ha = st.number_input(
        'Plantation area (hectares):',
        min_value=0.0,
        value=100.0,
        key='area_insights'
    )
    
    if plantation_area_ha > 0:
        custom_frond_biomass = plantation_area_ha * custom_frond_mt_per_ha
        custom_trunk_biomass = plantation_area_ha * custom_trunk_mt_per_ha
        
        # Comparison Bar Chart
        df_comparison = pd.DataFrame({
            'Biomass Type': ['Oil Palm Frond (OPF)', 'Oil Palm Trunk (OPT)'],
            'Default Biomass (MT)': [
                plantation_area_ha * DEFAULT_FROND_MT_PER_HA, 
                plantation_area_ha * DEFAULT_TRUNK_MT_PER_HA
            ],
            'Custom Biomass (MT)': [custom_frond_biomass, custom_trunk_biomass]
        })
        
        fig_comparison = go.Figure(data=[
            go.Bar(name='Default', x=df_comparison['Biomass Type'], y=df_comparison['Default Biomass (MT)'], marker_color='blue'),
            go.Bar(name='Custom', x=df_comparison['Biomass Type'], y=df_comparison['Custom Biomass (MT)'], marker_color='green')
        ])
        fig_comparison.update_layout(
            title='Frond and Trunk Biomass Comparison',
            xaxis_title='Biomass Type',
            yaxis_title='Biomass (MT)'
        )
        
        st.plotly_chart(fig_comparison, use_container_width=True)
        
        # Percentage Difference Calculation
        frond_diff = ((custom_frond_biomass - (plantation_area_ha * DEFAULT_FROND_MT_PER_HA)) / (plantation_area_ha * DEFAULT_FROND_MT_PER_HA)) * 100
        trunk_diff = ((custom_trunk_biomass - (plantation_area_ha * DEFAULT_TRUNK_MT_PER_HA)) / (plantation_area_ha * DEFAULT_TRUNK_MT_PER_HA)) * 100
        
        st.markdown("### Biomass Insights")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("OPF Difference", f"{frond_diff:+.1f}%")
        with col2:
            st.metric("OPT Difference", f"{trunk_diff:+.1f}%")
            

# Final sections about references, developer info, etc.
st.write("---")
st.markdown("""
**References**:
1. Cheah et al. (2023). Circular bioeconomy in palm oil industry.
2. Abioye et al. (2023). Physicochemical Properties of Palm Oil Decanter Cake.
""")

# Sidebar Additional Information
st.sidebar.markdown("### Biomass Components")
st.sidebar.info("""
- **EFB:** Residual bunches after oil extraction
- **PKS:** Shell fragments from palm kernels
- **Mesocarp Fibre:** Fibrous residue 
- **Decanter Cake:** Solid waste from oil separation
- **POME:** Liquid mill waste
- **SPO:** Oil-rich liquid waste
""")

st.sidebar.markdown("### Developer")
st.sidebar.info("Mohd Rafizan Samian\nFELDA Strategic Planning and Transformation")
