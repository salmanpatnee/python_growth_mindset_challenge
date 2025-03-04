import streamlit as st
import pandas as pd
import os
from io import BytesIO
import time

# Set page config with favicon and title
st.set_page_config(page_title="Data Sweeper - File Transformer", page_icon="🔄", layout="wide")

# Custom CSS for styling
st.markdown("""
    <style>
    /* Background and fonts */
    body {
        font-family: Arial, sans-serif;
    }

    /* Custom header */
    .main-header {
        text-align: center;
        font-size: 32px;
        font-weight: bold;
        color: #4CAF50;
        margin-bottom: 10px;
    }

    /* Custom buttons */
    div.stButton > button {
        background-color: #4CAF50;
        color: white;
        padding: 10px 20px;
        border-radius: 8px;
        border: none;
    }

    /* File uploader styling */
    div.stFileUploader {
        border: 2px dashed #4CAF50;
        padding: 10px;
        border-radius: 8px;
    }

    /* Section headers */
    .section-header {
        font-size: 20px;
        color: #4CAF50;
        font-weight: bold;
        margin-top: 20px;
    }

    /* Dataframe styling */
    .dataframe-container {
        margin-top: 10px;
        margin-bottom: 20px;
    }

    </style>
""", unsafe_allow_html=True)

# Sidebar navigation
with st.sidebar:
    st.image("assets/data-collection.png", width=100)  # Replace with your logo URL
    # st.title("📂 Navigation")
    page = st.radio("Go to", ["Home", "Upload & Process", "About"])

# Home Page
if page == "Home":
    st.title("🔄 Data Sweeper")
    st.write("""
        Welcome to **Data Sweeper**, your friendly tool for cleaning, transforming, and converting files!

        🚀 Upload CSV or Excel files  
        🧹 Clean data (remove duplicates, fill missing values)  
        📊 Visualize key insights  
        💾 Convert files between formats
    """)
    st.write("Use the **sidebar** to navigate.")

# About Page
elif page == "About":
    st.title("ℹ️ About Data Sweeper")
    st.write("""
        **Data Sweeper** was built using **Streamlit** to simplify file processing for data enthusiasts.  
        This app supports:
        - CSV and Excel file handling
        - Data cleaning options
        - Interactive visualizations
        - Format conversion
    """)
    st.write("💡 *Styled creatively to showcase growth mindset and UX focus.*")

# Upload & Process Page
elif page == "Upload & Process":
    st.markdown('<div class="main-header">📊 Data Sweeper - File Processor</div>', unsafe_allow_html=True)
    st.write("Transform your files between CSV and Excel formats with data cleaning and visualization options.")

    uploaded_files = st.file_uploader("📤 Upload your files (CSV or Excel)", type=["csv", "xlsx"],
                                      accept_multiple_files=True)

    if uploaded_files:
        for file in uploaded_files:
            file_ext = os.path.splitext(file.name)[-1].lower()

            if file_ext == ".csv":
                df = pd.read_csv(file)
            elif file_ext == ".xlsx":
                df = pd.read_excel(file)
            else:
                st.error(f"❌ Unsupported file type: {file_ext}")
                continue

            st.markdown(f'<div class="section-header">📂 File: {file.name}</div>', unsafe_allow_html=True)

            st.write("🔎 **Preview**")
            st.dataframe(df.head())

            # Data Cleaning Section
            st.markdown('<div class="section-header">🧹 Data Cleaning Options</div>', unsafe_allow_html=True)
            if st.checkbox(f"Enable cleaning options for **{file.name}**"):
                col1, col2 = st.columns(2)

                with col1:
                    if st.button(f"🗑️ Remove Duplicates from {file.name}"):
                        df.drop_duplicates(inplace=True)
                        st.success("✅ Duplicates Removed!")

                with col2:
                    if st.button(f"🩺 Fill Missing Values for {file.name}"):
                        numeric_cols = df.select_dtypes(include=['number']).columns
                        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                        st.success("✅ Missing values filled with column mean!")

            # Column selection
            st.markdown('<div class="section-header">📊 Column Selection</div>', unsafe_allow_html=True)
            columns = st.multiselect(f"Choose columns to keep for **{file.name}**", df.columns, default=df.columns)
            df = df[columns]

            # Data Visualization Section
            st.markdown('<div class="section-header">📈 Data Visualization</div>', unsafe_allow_html=True)
            if st.checkbox(f"Show Visualization for **{file.name}**"):
                numeric_cols = df.select_dtypes(include=['number']).columns
                if len(numeric_cols) < 2:
                    st.warning("⚠️ Not enough numeric columns for visualization.")
                else:
                    st.bar_chart(df[numeric_cols].iloc[:, :2])

            # Conversion Section
            st.markdown('<div class="section-header">💾 File Conversion</div>', unsafe_allow_html=True)
            conversion_type = st.radio(f"Convert **{file.name}** to:", ["CSV", "Excel"], key=file.name)

            if st.button(f"🔄 Convert {file.name}"):
                progress_bar = st.progress(0)
                for i in range(100):
                    time.sleep(0.01)  # Simulate processing
                    progress_bar.progress(i + 1)

                buffer = BytesIO()
                if conversion_type == 'CSV':
                    df.to_csv(buffer, index=False)
                    file_name = file.name.replace(file_ext, ".csv")
                    mime_type = "text/csv"
                elif conversion_type == 'Excel':
                    df.to_excel(buffer, index=False)
                    file_name = file.name.replace(file_ext, ".xlsx")
                    mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

                buffer.seek(0)
                st.success(f"✅ {file.name} successfully converted to {conversion_type}")

                st.download_button(
                    label=f"⬇️ Download {file.name} as {conversion_type}",
                    data=buffer,
                    file_name=file_name,
                    mime=mime_type
                )
