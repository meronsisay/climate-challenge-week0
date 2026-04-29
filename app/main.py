
import streamlit as st
import pandas as pd
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from utils import (
    load_all_data, filter_data, get_summary_statistics,
    plot_temperature_trend, plot_precipitation_boxplot,
    plot_extreme_heat, plot_drought, plot_correlation_heatmap,
    COUNTRIES
)

# Page config
st.set_page_config(
    page_title="African Climate Dashboard",
    page_icon="🌍",
    layout="wide"
)

st.markdown("""
<style>

/* Global font + size */
html, body, [class*="css"]  {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    font-size: 14px;
    color: #222;
}

/* Slightly tighter spacing */
p {
    margin-bottom: 0.5rem;
}

</style>
""", unsafe_allow_html=True)

# Header
st.title("🌍 African Climate Trends Dashboard")
st.markdown("*NASA POWER Data Analysis (2015-2026) | Ethiopia, Kenya, Nigeria, Sudan, Tanzania*")
st.markdown("---")

# Load data
@st.cache_data
def load_cached_data():
    return load_all_data()

with st.spinner("Loading climate data..."):
    df = load_cached_data()

if df.empty:
    st.error("""
     **No data found!**
    
    Please ensure:
    1. Cleaned CSV files are in the `data/` directory
    2. Files are named: `ethiopia_clean.csv`, `kenya_clean.csv`, etc.
    3. You have run the EDA notebooks to generate these files
    """)
    st.stop()

# Sidebar filters
st.sidebar.header("🔧 Filter Controls")
st.sidebar.markdown("---")

countries = st.sidebar.multiselect(
    "**Select Countries**",
    options=COUNTRIES,
    default=COUNTRIES,
    help="Select one or more countries to compare"
)

min_year, max_year = int(df['Year'].min()), int(df['Year'].max())
year_range = st.sidebar.slider(
    "**Select Year Range**",
    min_value=min_year, max_value=max_year,
    value=(min_year, max_year),
    help="Drag the handles to filter data by year"
)

st.sidebar.markdown("---")
st.sidebar.markdown(f"**Records loaded:** {len(df):,}")
st.sidebar.markdown(f"**After filters:** {len(filter_data(df, countries, year_range)):,}")

# Filter data
filtered_df = filter_data(df, countries, year_range)

# Key metrics
st.subheader("Key Metrics")

if not filtered_df.empty:
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Countries Selected", len(countries))
    col2.metric("Years", f"{year_range[0]} - {year_range[1]}")
    col3.metric("Avg Temperature", f"{filtered_df['T2M'].mean():.1f}°C")
    col4.metric("Avg Precipitation", f"{filtered_df['PRECTOTCORR'].mean():.1f} mm/day")
else:
    st.warning("No data available for selected filters. Please adjust your selection.")

st.markdown("---")

# Summary Statistics
if not filtered_df.empty:
    st.subheader("Summary Statistics by Country")
    temp_stats, precip_stats = get_summary_statistics(filtered_df)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Temperature Statistics**")
        st.dataframe(temp_stats, width='stretch')  
    with col2:
        st.markdown("**Precipitation Statistics**")
        st.dataframe(precip_stats, width='stretch')  

# Temperature Trend
if not filtered_df.empty and len(countries) > 0:
    st.subheader("Temperature Trends Over Time")
    fig_temp = plot_temperature_trend(filtered_df)
    st.pyplot(fig_temp)
    
    with st.expander("📖 Interpretation"):
        st.markdown("""
        - **Sudan** shows the highest temperatures with dramatic seasonal variation (σ = 4.68)
        - **Ethiopia** maintains the coolest temperatures year-round due to high elevation (16.1°C mean)
        - **Clear separation** exists between lowland countries (Sudan, Nigeria, Tanzania) and highland countries (Ethiopia, Kenya)
        - The 12.7°C gap between Sudan and Ethiopia is statistically significant (ANOVA p < 0.001)
        """)
    st.markdown("---")

# Precipitation Distribution
if not filtered_df.empty and len(countries) > 0:
    st.subheader("Precipitation Distribution by Country")
    fig_precip = plot_precipitation_boxplot(filtered_df)
    st.pyplot(fig_precip)
    
    with st.expander("📖 Interpretation"):
        st.markdown("""
        - **Nigeria** has highest mean precipitation (4.21 mm/day) with extreme outliers → flood risk
        - **Tanzania** shows most variability (σ = 8.0 mm/day) → unpredictable rainfall
        - **Sudan** is extremely dry (median = 0 mm/day) → chronic drought risk
        - **Ethiopia** has moderate, bimodal rainfall patterns → reliable for agriculture
        """)
    st.markdown("---")

# Extreme Events
if not filtered_df.empty and len(countries) > 0:
    st.subheader("Extreme Events Analysis")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Extreme Heat Days (>35°C)**")
        fig_heat = plot_extreme_heat(filtered_df)
        st.pyplot(fig_heat)
        st.caption("Note: Only Sudan recorded extreme heat days across the entire dataset")
    
    with col2:
        st.markdown("**Consecutive Dry Days (<1mm)**")
        fig_drought = plot_drought(filtered_df)
        st.pyplot(fig_drought)
    
    with st.expander("📖 Interpretation"):
        st.markdown("""
        **Extreme Heat Days:**
        - **Only Sudan** recorded extreme heat days throughout 2015-2026
        - Peak: 275 days in 2015 | Lowest: 40 days in 2026
        - Ethiopia, Kenya, Nigeria, and Tanzania recorded **zero days** above 35°C
        
        **Consecutive Dry Days:**
        - **Sudan** faces most severe drought (240-277 days max dry spells)
        - **Ethiopia & Kenya** have shortest dry spells (29-63 days)
        - **Nigeria & Tanzania** maintain 120-170 dry days annually
        
        **Compound Risk:** Sudan faces extreme heat AND prolonged drought simultaneously — a severe humanitarian risk.
        """)
    st.markdown("---")

# Vulnerability Ranking
st.subheader("Climate Vulnerability Ranking for COP32")

vulnerability_data = {
    'Rank': [1, 2, 3, 4, 5],
    'Country': ['Sudan', 'Nigeria', 'Tanzania', 'Kenya', 'Ethiopia'],
    'Temperature Risk': ['Extreme', 'Moderate', 'Low-Moderate', 'Low', 'Low'],
    'Precipitation Risk': ['Extreme (Drought)', 'High (Flood)', 'High (Variable)', 'Low', 'Low-Moderate'],
    'Heat Risk': ['Extreme (200+ days)', 'None', 'None', 'None', 'None'],
    'Drought Risk': ['Extreme (240+ days)', 'High', 'High', 'Low', 'Low']
}

st.dataframe(pd.DataFrame(vulnerability_data), use_container_width=True, hide_index=True)


# Raw Data Preview
with st.expander("📄 View Raw Data"):
    st.dataframe(filtered_df.head(100), use_container_width=True)
    st.caption(f"Showing first 100 rows of {len(filtered_df):,} total records")

# Footer
st.markdown("---")
st.caption("📊 Data Source: NASA POWER | 👤 Created by: Meron Sisay | 🎯 Purpose: 10 Academy Climate Challenge Week 0 - COP32 Vulnerability Assessment")