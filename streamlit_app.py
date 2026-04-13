import streamlit as st
import pandas as pd

# importing the up to date data
@st.cache_data
def load_data():
    # the data had this weird ï»¿"Month" in front of the first column, which gets fixed when using encoding="utf-8-sig"
    return pd.read_csv("https://pxdata.stat.fi/PxWeb/sq/11627403-779b-42c0-91fa-0cfc3a81c048", encoding="utf-8-sig")

df_raw = load_data()

df = df_raw

st.markdown(''' # Overnight stays in Espoo
On this Streamlit page I will display data about monthly hotel capacity and nights spent in Espoo, 
from year 1995 to the current time.

''')

# displaying the raw data by using the streamlit's dataframe
st.markdown('''### Raw data of Espoo
This is the raw data about the overnight stays in Espoo that I will be working with.''')
st.dataframe(df_raw)

# column cheatsheet
# "Month"
# "Espoo Domestic nights"
# "Espoo Foreign nights"
# "Espoo Average room price"
# "Espoo Average price per night"
# "Espoo Nights spent"

# diaplaying the average room price by month
st.markdown('''### Graph of selected data
Here you can choose which data you would like to see as a line chart.''')
option = st.selectbox(
    "Chosen data",
    ("Espoo Domestic nights", "Espoo Foreign nights", "Espoo Average room price", "Espoo Average price per night", "Espoo Nights spent"),
)
# drawing the line chart based on chosen option
st.line_chart(df, x="Month", y=option)



