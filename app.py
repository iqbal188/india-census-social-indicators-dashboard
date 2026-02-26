import streamlit as st
import pandas as pd
import plotly.express as px


# Load Data
df = pd.read_csv("india.csv")

# Page Title
st.title("India Census 2011 Dashboard")
st.markdown("Geospatial analysis of literacy, gender ratio and infrastructure")


# Sidebar Controls
st.sidebar.title("Dashboard Controls")

# State Selection
list_of_states = list(df["State"].unique())
list_of_states.insert(0, "Overall India")

selected_state = st.sidebar.selectbox(
    "Select State",
    list_of_states,
    index=0
)

# Indicator Selection
metric_dict = {
    "Literacy Rate": "literacy_rate",
    "Sex Ratio": "sex_ratio",
    "Internet Access": "Households_with_Internet",
    "Electric Lighting": "Housholds_with_Electric_Lighting"
}

st.sidebar.subheader("Select Indicator")
indicator = st.sidebar.radio("Choose Metric", list(metric_dict.keys()))
column = metric_dict[indicator]


# Filtering Logic
if selected_state == "Overall India":
    filtered_df = df.copy()
else:
    filtered_df = df[df["State"] == selected_state]


# KPI Section

st.subheader(f"{selected_state} Overview")

avg_value = filtered_df[column].mean()
max_value = filtered_df[column].max()
highest_row = filtered_df.loc[filtered_df[column].idxmax()]
highest_district = highest_row["District"]

# Smart formatting
if indicator == "Literacy Rate":
    avg_display = f"{avg_value:.2f}%"
    max_display = f"{max_value:.2f}%"

elif indicator == "Sex Ratio":
    avg_display = f"{avg_value:.0f}"
    max_display = f"{max_value:.0f}"

else:
    avg_display = f"{avg_value:,.0f}"
    max_display = f"{max_value:,.0f}"

col1, col2 = st.columns(2)

with col1:
    st.metric(f"Average {indicator}", avg_display)

with col2:
    st.metric(
        f"Highest {indicator}",
        max_display,
        delta=f"{highest_district}"
    )

# Dynamic Zoom Logic
if selected_state == "Overall India":
    zoom_level = 3.8
    center_lat = df["Latitude"].mean()
    center_lon = df["Longitude"].mean()
else:
    zoom_level = 6
    center_lat = filtered_df["Latitude"].mean()
    center_lon = filtered_df["Longitude"].mean()

# Map Visualization
fig = px.scatter_mapbox(
    filtered_df,
    lat="Latitude",
    lon="Longitude",
    color=column,
    size=column,
    size_max=30,
    hover_name="District",
    hover_data={
        "State": True,
        column: True,
        "Latitude": False,
        "Longitude": False
    },
    labels={
        "literacy_rate": "Literacy Rate",
        "sex_ratio": "Sex Ratio",
        "Households_with_Internet": "Internet Access",
        "Housholds_with_Electric_Lighting": "Electric Lighting"
    },
    color_continuous_scale="Viridis",
    zoom=zoom_level,
    height=650
)

fig.update_layout(
    mapbox_style="open-street-map",
    mapbox=dict(center=dict(lat=center_lat, lon=center_lon)),
    margin={"r": 0, "t": 0, "l": 0, "b": 0},
    coloraxis_colorbar_title=indicator
)
st.plotly_chart(fig)

# Top 5 Ranking Section
st.subheader("Top 5 Districts")

ranked = filtered_df.sort_values(column, ascending=False).head(5)

display_df = ranked[["District", column]].copy()
display_df = display_df.rename(columns={column: indicator})

st.dataframe(
    display_df.reset_index(drop=True),
    width='stretch',
    hide_index=True
)
# Footer
st.markdown("---")

st.markdown(
    "<div style='text-align:center; font-size:14px;'>"
    "Data Source: Census of India 2011 | Dashboard built using Streamlit & Plotly"
    "</div>",
    unsafe_allow_html=True
)