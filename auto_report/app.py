# ------------------------------------------------------------
# app.py
# Streamlit UI for AutoReport AI
# 
# This module handles:
#   1. File uploads (CSV / JSON / SQL / SQLite)
#   2. Data preview and sanity checks
#   3. Triggering AI insights and report generation
#   4. Downloading PPTX/PDF outputs
# 
# The goal of this layer is to stay thin and focus only on:
#   1. User input handling
#   2. Displaying results
#   3. Passing data to processing modules
# ------------------------------------------------------------

import os
import streamlit as st
from ingest import ingest_csv, ingest_sql, ingest_sqlite, ingest_json
from processor import generate_summary, generate_plots
from insights import generate_insights
from report import create_ppt, create_pdf

st.title("📊 AI-Powered Automated Analytics Engine (Groq + Python)")

source = st.selectbox(
    "Choose Data Source",
    ["CSV", "JSON", "SQL Query", "SQLite"]
)

df = None

# CSV Upload
if source == "CSV":
    file = st.file_uploader("Upload CSV", type=["csv"])
    if file:
        df = ingest_csv(file)

# JSON Upload
elif source == "JSON":
    file = st.file_uploader("Upload JSON", type=["json"])
    if file:
        df = ingest_json(file)

# SQL Query
elif source == "SQL Query":
    connection = st.text_input("SQLAlchemy Connection String (e.g. sqlite:///mydb.db)")
    query = st.text_area("Enter SQL Query")
    if connection and query:
        try:
            df = ingest_sql(query, connection)
        except Exception as e:
            st.error(f"SQL Error: {e}")

# SQLite Query
elif source == "SQLite":
    db_file = st.file_uploader("Upload SQLite DB", type=["db", "sqlite"])
    query = st.text_area("Enter SQL Query")
    if db_file and query:
        try:
            df = ingest_sqlite(query, db_file)
        except Exception as e:
            st.error(f"SQLite Error: {e}")

# If data loaded
if df is not None:
    st.subheader("Data Preview")
    st.dataframe(df)

    # Generate summary
    summary = generate_summary(df)

    # Generate plots
    plots = generate_plots(df)


    # Generate AI Insights
    st.subheader("AI Insights (Groq)")
    insights = generate_insights(summary)
    st.write(insights)

    st.subheader("Download Reports")

    # Create folder based on filename
    if source == "CSV":
        dataset_name = file.name.split(".")[0]
    else:
        dataset_name = "dataset"

    output_folder = os.path.join(os.path.dirname(__file__), "..", "output", dataset_name)
    os.makedirs(output_folder, exist_ok=True)

    # Download PPTX
    pptx_path = create_ppt(summary, insights, plots, df, output_folder, filename=f"{dataset_name}_report.pptx")
    with open(pptx_path, "rb") as f:
        st.download_button("Download PPTX Report", f, f"{dataset_name}_report.pptx")

    # Download PDF
    pdf_path = create_pdf(summary, insights, plots, df, output_folder, filename=f"{dataset_name}_report.pdf")
    with open(pdf_path, "rb") as f:
        st.download_button("Download PDF Report", f, f"{dataset_name}_report.pdf")

