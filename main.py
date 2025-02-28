import streamlit as st
import pandas as pd
import os
from io import BytesIO

# Set up app
st.set_page_config(page_title="Data sweeper", layout="wide")
st.title("Data sweeper")
st.write("Transform your files between CSV and Excel formats.")

uploaded_files = st.file_uploader("Upload your files (CSV or Excel):", type=["csv", "xlsx"], accept_multiple_files=True)

# Working with uploaded files
if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"Unsupported file type: {file_ext}")
            continue

        # Display file info
        st.write(f"**File Name:** {file.name}")

        st.write("Preview")
        st.dataframe(df.head())

        st.subheader("Data cleaning Options")
        if st.checkbox(f"Clean data for file {file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"Remove duplicates from {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("Duplicates Removed!")

            with col2:
                if st.button(f"Fill missing values for {file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("Missing values have been Filled!")


        st.write("Select columns to convert.")
        columns = st.multiselect(f"Choose columns for {file.name}", df.columns, default=df.columns)
        df = df[columns]

