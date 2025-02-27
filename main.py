import streamlit as st
import pandas as pd
import os
from io import BytesIO

# Set up app
st.set_page_config(page_title="Data sweeper", layout="wide")
st.title("Data sweeper")
st.write("Transform your files between CSV and Excel formats.")

st.file_uploader("Upload your files (CSV or Excel):", type=["csv", "xlsx"], accept_multiple_files=True)