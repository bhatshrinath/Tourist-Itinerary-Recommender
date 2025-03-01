import streamlit as st
import pandas as pd
import numpy as np


# Custom CSS for background and other styles
def add_custom_css():
    """
    Add custom CSS to the Streamlit app to improve the overall look and feel.

    This function uses Streamlit's `st.markdown` function to inject the CSS code
    into the app. The CSS rules are written inside a multi-line string with
    triple quotes and wrapped in `<style>` tags.

    The CSS rules target specific elements in the Streamlit app by using their
    data-testid attribute. This attribute is unique to each Streamlit element
    and can be found by inspecting the app in the browser.

    The CSS rules in this function style the main app background, sidebar, and
    other elements to create a clean and modern look.
    """
    st.markdown(
        """
        <style>
        /* Main app background */
        div[data-testid="stAppViewContainer"] {
            background-color: #fdfaf1; /* Slightly green cream */
            color: #3b3b3b; /* Dark gray for text */
            font-family: 'Roboto', sans-serif; /* Clean and modern font */
        }

        /* Sidebar background */
        section[data-testid="stSidebar"] {
            background-color: #d1e7d0; /* Slightly darker light green */
            border-right: 3px solid #a3cfa1; /* Subtle green border */
        }

        /* Headings styled with a natural color */
        h1, h2, h3 {
            color: #2d6a4f; /* Deep green */
            font-family: 'Poppins', sans-serif; /* Modern and sleek */
            text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.1); /* Subtle shadow for depth */
        }

        /* Buttons with a soft hover effect */
        .stButton > button {
            background: linear-gradient(45deg, #6a11cb, #2575fc);
            color: #ffffff;
            border: none;
            border-radius: 12px;
            padding: 0.6em 1.2em;
            font-size: 1em;
            font-weight: bold;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0px 8px 20px rgba(0, 0, 0, 0.2);
        }

        /* Input fields styling */
        .stTextInput > div > div > input {
            background-color: #ffffff; /* White */
            border: 2px solid #b5d3b6; /* Soft green border */
            border-radius: 8px;
            padding: 0.6em;
            font-size: 0.9em;
            transition: border-color 0.3s;
        }
        .stTextInput > div > div > input:focus {
            border-color: #74c69d; /* Green focus effect */
            outline: none;
        }

        /* Dataframe styling */
        .stDataFrame {
            background-color: #ffffff; /* White for clarity */
            border: 2px solid #b5d3b6; /* Green border */
            border-radius: 8px;
            padding: 10px;
        }

        /* Sidebar menu text */
        .sidebar .sidebar-content {
            color: #3b3b3b;
            font-size: 0.95em;
            font-weight: 500;
        }

        </style>
        """,
        unsafe_allow_html=True,
    )
