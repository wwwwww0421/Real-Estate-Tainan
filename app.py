import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff
import plotly.express as px
from data_preprocessing import (
    data_processing_land,
    data_processing_house,
    get_plotable_range,
    district_lst,
)

# Set the title of the app
st.title("Tainan Real Estate Trading Dashboard")

# Sidebar for user inputs
st.sidebar.header("User Input Parameters")

land_or_house = st.sidebar.selectbox(
    "Which one info are you interested in?", ("Land", "House")
)

# File uploader
# uploaded_file = st.sidebar.file_uploader("Upload your CSV file", type=["csv"])

if land_or_house == "Land":
    data = pd.read_csv("./Output/台南土地.csv")
    processed_data = data_processing_land(data)


if land_or_house == "House":
    data = pd.read_csv("./Output/房地王.csv")
    processed_data = data_processing_house(data)


# Data Processing
st.subheader("Data Preview")

test = processed_data[processed_data.district != 0]

district = st.selectbox("Select the district:", sorted(test.district.unique()))
processed_data = processed_data[processed_data["district"] == district].reset_index(
    drop=True
)

plotable_data = get_plotable_range(processed_data)

processed_columns = [
    "min_price",
    "max_price",
    "avg_price",
    "min_size",
    "max_size",
    "avg_size",
]

# Display processed data
st.write("Processed Data")
st.write(processed_data.head())

st.subheader("Average Price")
try:
    if land_or_house == "Land":
        st.markdown(
            f"<h3 style='text-align: center; color: yellow;'>{round(processed_data['avg_price'].mean())}K</h3>",
            unsafe_allow_html=True,
        )
    if land_or_house == "House":
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(
                "<h3 style='text-align: center; color: white;'>Max Price</h3>",
                unsafe_allow_html=True,
            )
            st.markdown(
                f"<h3 style='text-align: center; color: yellow;'>{round(processed_data['max_price'].max())}K</h3>",
                unsafe_allow_html=True,
            )
        with col2:
            st.markdown(
                "<h3 style='text-align: center; color: white;'>Min Price</h3>",
                unsafe_allow_html=True,
            )
            st.markdown(
                f"<h3 style='text-align: center; color: yellow;'>{round(processed_data[processed_data['min_price']>0]['min_price'].min())}K</h3>",
                unsafe_allow_html=True,
            )

except ValueError:
    st.markdown(
        "<h1 style='text-align: center; color: grey;'>Oops.. No data for this district..</h1>",
        unsafe_allow_html=True,
    )

# Histogram
st.sidebar.header("Histogram")
hist_column = st.sidebar.selectbox("Select column for histogram", processed_columns)
if st.sidebar.button("Generate Histogram"):
    st.subheader(f"{district} Histogram")
    # fig, ax = plt.subplots()
    fig = px.histogram(
        processed_data[(processed_data["district"] == f"{district}")],
        x=hist_column,
    )
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    st.plotly_chart(fig)


colour_scale = [
    "#66C3F4",
    "#3EB3F2",
    "#0E89CB",
    "#08527A",
    "#063751",
    "#031B29",
]
# Correlation heatmap
st.subheader(f"{district} Map")
try:
    fig = ff.create_hexbin_mapbox(
        data_frame=plotable_data[
            (plotable_data["district"] == f"{district}")
            & (plotable_data["avg_price"] > 0)
        ],
        lat="latitude",
        lon="longitude",
        color="avg_price",
        min_count=1,
        nx_hexagon=30,
        opacity=0.8,
        labels={"color": "avg_price"},
        show_original_data=False,
        color_continuous_scale=colour_scale,
        agg_func=np.mean,
    )

    fig.update_layout(
        mapbox_style="open-street-map",
        mapbox=dict(
            layers=[
                dict(
                    sourcetype="raster",
                    source=["https://a.tile.openstreetmap.org/{z}/{x}/{y}.png"],
                    below="traces",
                    opacity=0.5,
                )
            ]
        ),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
    )
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    st.plotly_chart(fig)
except ValueError:
    st.markdown(
        "<h1 style='text-align: center; color: grey;'>Oops.. No data for this district..</h1>",
        unsafe_allow_html=True,
    )
