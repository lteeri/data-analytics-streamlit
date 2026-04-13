import streamlit as st
import pandas as pd

# importing the up to date data
@st.cache_data
def load_data():
    # the data had this weird ï»¿"Month" in front of the first column, which gets fixed when using encoding="utf-8-sig"
    return pd.read_csv("https://pxdata.stat.fi/PxWeb/sq/11627403-779b-42c0-91fa-0cfc3a81c048", encoding="utf-8-sig")

df_raw = load_data()

df = df_raw.rename(columns={
    
    "Espoo Domestic nights": "Domestic nights",
    "Espoo Foreign nights": "Foreign nights",
    "Espoo Average room price": "Average room price",
    "Espoo Average price per night": "Average price per night",
    "Espoo Nights spent": "Nights spent",
})

st.markdown(''' # Overnight stays in Espoo
On this Streamlit page I will display data about monthly hotel capacity and nights spent in Espoo, 
from year 1995 to the current time.

''')

st.divider()

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

st.divider()

# diaplaying the average room price by month
st.markdown('''### Graph of selected data
Here you can choose which data you would like to see as a line chart.''')
option = st.selectbox(
    "Chosen data from Espoo",
    ("Domestic nights", "Foreign nights", "Average room price", "Average price per night", "Nights spent"),
)
# drawing the line chart based on chosen option
st.line_chart(df, x="Month", y=option)


st.divider()

# making a new table that has years summed together

# extracting just the night spent
df_nights_spent_by_year = df[["Month", "Nights spent"]]
# now the row has values in a form of 1995M01

# we must split with M. That created a list and we want the first value of that [0]
df_nights_spent_by_year["Month"] = df_nights_spent_by_year["Month"].str.split("M").str[0]

# generated with chatgpt
df_nights_spent_by_year = (
    df_nights_spent_by_year.groupby("Month", as_index=False)["Nights spent"]
      .sum()
      .rename(columns={"Month": "Year"})
)

# drawing a bar chart of year totals
st.markdown('''### Yearly total of nights spent
This graph displays the sum of the nights spent by year. The data shows a slight increase
over the years, but there is a lot of variation. 2020 is has the smallest amout since that year travelling was
very restricted. The newest year is still waiting for data of the whole year.''')
st.bar_chart(df_nights_spent_by_year, x="Year", y="Nights spent", horizontal=True)


st.divider()

# Domestic vs Foreign: datatable and small line chart.

# extracting the domestic and foreign night from the table
df_domestic_and_foreign = df[["Month", "Domestic nights", "Foreign nights"]]

st.markdown('''### Datatable of just the domestic and foreign nights
These columns are the people who are staying overnight at an accommondation. From this line chart we can see that
the trends follow each other quite well. There are a bit more of domestic stays. In the recent years this gap has
widened and it seems that domestic stays have increased while foreign stays have stayed quite the same.''')
# drawing the table and graph
st.dataframe(df_domestic_and_foreign)

st.markdown('''### Line chart of domestic and foreign nights
This describes the domestic and foreign stays as a linechart.''')
st.line_chart(df_domestic_and_foreign, x="Month", y=["Domestic nights", "Foreign nights"], color=["#FF8C00", "#0041C2"])



