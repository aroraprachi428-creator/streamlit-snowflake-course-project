# import packages
import streamlit as st
import pandas as pd
import re
import os
import string



# Helper function to get dataset path
def get_dataset_path():
    # Get the current script directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Construct the path to the CSV file
    csv_path = os.path.join(current_dir, "..", "..", "data", "customer_reviews.csv")
    return csv_path
st.title("Hello, GenAI!")


def clean_text(text):
    """
    Clean input text by removing punctuation, lowercasing, and stripping whitespace.
    Non-string inputs are converted to string.
    """
    if not isinstance(text, str):
        text = str(text)
    # strip leading/trailing whitespace and lowercase
    text = text.strip().lower()
    # remove punctuation characters
    translator = str.maketrans('', '', string.punctuation)
    return text.translate(translator)


st.write("This is your GenAI-powered data processing app.")

col1, col2 = st.columns(2)

with col1:
    if st.button("Ingest Dataset"):
        try:
            csv_path = get_dataset_path()
            st.session_state["df"] = pd.read_csv(csv_path)
            st.success("Dataset ingested successfully!")
        except FileNotFoundError:
            st.error("Dataset file not found. Please check the path and try again.")

with col2:
    if st.button("Parse Reviews"):
        if "df" in st.session_state:
            st.session_state["df"]["CLEANED_SUMMARY"] = st.session_state["df"]["SUMMARY"].apply(clean_text)
            st.success("Reviews parsed and cleaned successfully!")
        else:
            st.error("Please ingest the dataset first before parsing reviews.")

# Display data if it exists in session state
if "df" in st.session_state:
    st.subheader("🔍 Filter by Product")
    product = st.selectbox("Choose a product", ["All Products"] + list(st.session_state["df"]["PRODUCT"].unique()))

    st.subheader(f"Dataset Preview")

    if product != "All Products":
        filtered_df = st.session_state["df"][st.session_state["df"]["PRODUCT"] == product]
    else:
        filtered_df = st.session_state["df"]
    st.dataframe(filtered_df)

    st.subheader("Sentiment score by product")
    grouped = st.session_state["df"].groupby("PRODUCT")["SENTIMENT_SCORE"].mean()
    st.bar_chart(grouped)



