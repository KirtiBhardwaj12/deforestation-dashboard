import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(page_title="Deforestation Dashboard", layout="wide")

# -------------------------------
# LOAD DATA
# -------------------------------
df = pd.read_csv("IndianForestNDVI_10Years.csv")
results_df = pd.read_csv("final_dashboard_data.csv")

# -------------------------------
# TITLE
# -------------------------------
st.title("🌳 AI-Based Deforestation Monitoring Dashboard")
st.markdown("Analyze forest health, environmental factors, and deforestation risk")

# -------------------------------
# SIDEBAR FILTER
# -------------------------------
st.sidebar.header("🔍 Filter Data")

regions = st.sidebar.multiselect(
    "Select Region",
    df["Regions"].unique(),
    default=df["Regions"].unique()
)

df = df[df["Regions"].isin(regions)]
results_df = results_df[results_df["Regions"].isin(regions)]

# -------------------------------
# KPI CARDS
# -------------------------------
st.subheader("📊 Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Avg NDVI", round(df["NDVI"].mean(), 3))
col2.metric("Avg Rainfall", round(df["Rainfall_mm"].mean(), 2))
col3.metric("Avg Temperature", round(df["Average_Temperature_C"].mean(), 2))
col4.metric("Avg Risk Score", round(results_df["Risk_Score"].mean(), 2))

# -------------------------------
# NDVI + RISK (SIDE BY SIDE)
# -------------------------------
col5, col6 = st.columns(2)

with col5:
    st.subheader("📈 NDVI Trend")
    fig_ndvi = px.line(
        df,
        x="Year",
        y="NDVI",
        color="Regions",
        markers=True
    )
    st.plotly_chart(fig_ndvi, use_container_width=True)

with col6:
    st.subheader("🔥 Risk Trend")
    fig_risk = px.line(
        results_df,
        x="Year",
        y="Risk_Score",
        color="Regions",
        markers=True
    )
    st.plotly_chart(fig_risk, use_container_width=True)

# -------------------------------
# CORRELATION + REGION RISK
# -------------------------------
col7, col8 = st.columns(2)

with col7:
    st.subheader("🌧️ Rainfall vs NDVI")
    fig_corr = px.scatter(
        df,
        x="Rainfall_mm",
        y="NDVI",
        color="Regions"
    )
    st.plotly_chart(fig_corr, use_container_width=True)

with col8:
    st.subheader("🌍 Region-wise Risk")
    region_risk = results_df.groupby("Regions")["Risk_Score"].mean().reset_index()

    fig_bar = px.bar(
        region_risk,
        x="Regions",
        y="Risk_Score",
        color="Risk_Score"
    )
    st.plotly_chart(fig_bar, use_container_width=True)

# -------------------------------
# RISK DISTRIBUTION
# -------------------------------
st.subheader("📉 Risk Distribution")

fig_hist = px.histogram(
    results_df,
    x="Risk_Score",
    nbins=20
)

st.plotly_chart(fig_hist, use_container_width=True)

# -------------------------------
# INSIGHTS SECTION (VERY IMPRESSIVE)
# -------------------------------
st.subheader("💡 Key Insights")

st.markdown("""
- Regions with decreasing NDVI indicate possible deforestation  
- Higher rainfall generally improves vegetation health  
- High risk scores highlight areas needing conservation attention  
- Machine learning helps predict future vegetation conditions  
""")

# -------------------------------
# FOOTER
# -------------------------------
st.markdown("---")
st.markdown("Developed using Python, Machine Learning, and Streamlit 🌍")
# -------------------------------
# MAP VISUALIZATION (NEW)
# -------------------------------
st.subheader("🌍 Deforestation Risk Map")

# Add approximate coordinates for regions
region_coords = {
    "Aravalli": [27.0, 75.0],
    "Central Forest": [23.0, 80.0],
    "Eastern Ghats": [17.0, 82.0],
    "North Eastern Rainforest": [26.0, 92.0],
    "Odisha Forest": [20.0, 85.0],
    "Western Ghats": [10.0, 76.0],
    "Western Himalayas": [32.0, 77.0]
}

# Convert to dataframe
coords_df = pd.DataFrame([
    {"Regions": k, "lat": v[0], "lon": v[1]}
    for k, v in region_coords.items()
])

# Merge with risk data
map_df = results_df.groupby("Regions")["Risk_Score"].mean().reset_index()
map_df = map_df.merge(coords_df, on="Regions")

# Plot map
fig_map = px.scatter_geo(
    map_df,
    lat="lat",
    lon="lon",
    size="Risk_Score",
    color="Risk_Score",
    hover_name="Regions",
    title="Deforestation Risk by Region",
    projection="natural earth"
)

fig_map.update_geos(
    scope="asia",
    showcountries=True,
    showland=True,
    landcolor="lightgray"
)

st.plotly_chart(fig_map, use_container_width=True)