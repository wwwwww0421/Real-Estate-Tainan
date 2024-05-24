import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from data_preprocessing import data_processing_land, data_processing_house

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
    data = pd.read_csv("./台南土地.csv")
    processed_data = data_processing_land(data)


if land_or_house == "House":
    data = pd.read_csv("./房地王.csv")
    processed_data = data_processing_house(data)

st.subheader("Raw Data")
st.write(data.head())

# Data Processing
st.subheader("Data Processing")

# Selecting columns
columns = st.sidebar.multiselect(
    "Select columns to include",
    data.columns.tolist(),
    default=data.columns.tolist(),
)

# Display processed data
st.write("Processed Data")
st.write(processed_data.head())

st.subheader("Average Price")
if land_or_house == "Land":
    st.write(f'{round(processed_data["price"].mean())}K')

if land_or_house == "House":
    col1, col2 = st.columns(2)
    with col1:
        st.write("Max Price")
        st.write(f'{round(processed_data["max_price"].mean())}K')
    with col2:
        st.write("Min Price")
        st.write(f'{round(processed_data["min_price"].mean())}K')


# Handling missing values
if st.sidebar.checkbox("Handle Missing Values"):
    missing_value_strategy = st.sidebar.selectbox(
        "Select strategy",
        ["Drop rows", "Fill with mean", "Fill with median", "Fill with mode"],
    )

    if missing_value_strategy == "Drop rows":
        processed_data = processed_data.dropna()
    elif missing_value_strategy == "Fill with mean":
        processed_data = processed_data.fillna(processed_data.mean())
    elif missing_value_strategy == "Fill with median":
        processed_data = processed_data.fillna(processed_data.median())
    elif missing_value_strategy == "Fill with mode":
        processed_data = processed_data.fillna(processed_data.mode().iloc[0])

    st.write("Processed Data after handling missing values")
    st.write(processed_data.head())

# Interactive Widgets for Data Visualization
st.subheader("Data Visualization")

# Scatter plot
st.sidebar.header("Scatter Plot")
x_axis = st.sidebar.selectbox("Select X-axis", columns)
y_axis = st.sidebar.selectbox("Select Y-axis", columns)
if st.sidebar.button("Generate Scatter Plot"):
    st.write(f"Scatter Plot of {x_axis} vs {y_axis}")
    fig, ax = plt.subplots()
    ax.scatter(processed_data[x_axis], processed_data[y_axis])
    ax.set_xlabel(x_axis)
    ax.set_ylabel(y_axis)
    st.pyplot(fig)

# Histogram
st.sidebar.header("Histogram")
hist_column = st.sidebar.selectbox("Select column for histogram", columns)
if st.sidebar.button("Generate Histogram"):
    st.write(f"Histogram of {hist_column}")
    fig, ax = plt.subplots()
    ax.hist(processed_data[hist_column], bins=20)
    ax.set_xlabel(hist_column)
    ax.set_ylabel("Frequency")
    st.pyplot(fig)

# Correlation heatmap
st.sidebar.header("Correlation Heatmap")
if st.sidebar.button("Generate Correlation Heatmap"):
    st.write("Correlation Heatmap")
    corr = processed_data.corr()
    fig, ax = plt.subplots()
    sns.heatmap(corr, annot=True, ax=ax, cmap="coolwarm")
    st.pyplot(fig)

# If no file is uploaded
else:
    st.write("Please upload a CSV file to proceed.")

# Run the app: Save this script as app.py and run `streamlit run app.py` in your terminal.
