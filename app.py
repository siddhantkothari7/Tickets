#Streamlit app
import streamlit as st
import pandas as pd
import time
from sqlalchemy.orm import sessionmaker
from database import Session
from models import Stubhub

# Set up the session
session = Session()

# Streamlit app title
st.title("Stubhub Prices Tracker")

# Function to fetch data from the database
@st.cache_data(ttl=60)  # Cache data for 60 seconds
def fetch_data():
    entries = session.query(Stubhub).all()
    return pd.DataFrame([{
        "Time": entry.time,
        "Raw Price": entry.raw_price,
        "Fees": entry.fees,
        "Total Price": entry.total_price,
        "Lowest Price Time": entry.lowest_price_time,
        "Lowest Price": entry.lowest_price
    } for entry in entries]).sort_index(ascending=False)

# Display entries in the database
st.header("Current Entries in Database")
df = fetch_data()
if not df.empty:
    st.dataframe(df)

    # Basic Visualizations
    st.subheader("Basic Visualizations")

    st.line_chart(df.set_index("Time")[["Total Price", "Lowest Price"]])
    st.bar_chart(df.set_index("Time")[["Total Price", "Lowest Price"]])

    # Using Matplotlib for Custom Visualization
    st.subheader("Matplotlib Visualization")
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots()
    df.set_index("Time")[["Total Price", "Lowest Price"]].plot(kind='line', ax=ax)
    ax.set_ylabel("Price")
    ax.set_title("Total Price and Lowest Price Over Time")
    st.pyplot(fig)

else:
    st.write("No entries found in the database.")

# Add a delay and refresh the app
time.sleep(60)
st.experimental_rerun()