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
        elif file_ext == "xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"Unsupported file type: {file_ext}")
            continue

        # Display file info
        st.write(f"**File Name:** {file.name}")
