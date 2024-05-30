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
st.title("Interactive Data Processing and Dashboard")

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


# st.subheader("Raw Data")
# st.write(data.head())

# Data Processing
st.subheader("Top 5 rows of Processed Data")

# Selecting columns
# columns = st.sidebar.multiselect(
#     "Select columns to include",
#     data.columns.tolist(),
#     default=data.columns.tolist(),
# )

# print(processed_data.district.unique().tolist())
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


# Handling missing values
# if st.sidebar.checkbox("Handle Missing Values"):
#     missing_value_strategy = st.sidebar.selectbox(
#         "Select strategy",
#         ["Drop rows", "Fill with mean", "Fill with median", "Fill with mode"],
#     )

#     if missing_value_strategy == "Drop rows":
#         processed_data = processed_data.dropna()
#     elif missing_value_strategy == "Fill with mean":
#         processed_data = processed_data.fillna(processed_data.mean())
#     elif missing_value_strategy == "Fill with median":
#         processed_data = processed_data.fillna(processed_data.median())
#     elif missing_value_strategy == "Fill with mode":
#         processed_data = processed_data.fillna(processed_data.mode().iloc[0])

#     st.write("Processed Data after handling missing values")
#     st.write(processed_data.head())


# Interactive Widgets for Data Visualization
# st.subheader("Data Visualization")

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
    # ax.hist(
    #     processed_data[(processed_data["district"] == f"{district}")][hist_column],
    #     bins=20,
    # )
    # ax.set_xlabel(hist_column)
    # ax.set_ylabel("Frequency")
    # st.pyplot(fig)


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
        nx_hexagon=50,
        opacity=0.9,
        labels={"color": "avg_price"},
        show_original_data=False,
        agg_func=np.mean,
    )

    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    st.plotly_chart(fig)
except ValueError:
    st.markdown(
        "<h1 style='text-align: center; color: grey;'>Oops.. No data for this district..</h1>",
        unsafe_allow_html=True,
    )
# fig.show()
# if st.sidebar.button("Generate Correlation Heatmap"):
#     pass
# st.write("Correlation Heatmap")
# corr = processed_data.corr()
# fig, ax = plt.subplots()
# sns.heatmap(corr, annot=True, ax=ax, cmap="coolwarm")
# st.pyplot(fig)

# If no file is uploaded
# else:
#     st.write("Please upload a CSV file to proceed.")

# Run the app: Save this script as app.py and run `streamlit run app.py` in your terminal.
