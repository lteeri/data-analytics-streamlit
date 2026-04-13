import streamlit as st
import pandas as pd

# importing the up to date data
df = pd.read_csv("https://pxdata.stat.fi/PxWeb/sq/11627403-779b-42c0-91fa-0cfc3a81c048", encoding="latin-1")

# displaying the data by using the streamlit's dataframe
st.dataframe(df)

