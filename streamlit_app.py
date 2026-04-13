import streamlit as st
import pandas as pd
import numpy as np

# importing the up to date data
@st.cache_data
def load_espoo_data():
    # the data had this weird ï»¿"Month" in front of the first column, which gets fixed when using encoding="utf-8-sig"
    return pd.read_csv("https://pxdata.stat.fi/PxWeb/sq/11627403-779b-42c0-91fa-0cfc3a81c048", encoding="utf-8-sig")

@st.cache_data
def load_rovaniemi_data():
    # for some reason this didn't have the character problem that the espoo data has
    return pd.read_csv("https://pxdata.stat.fi/PxWeb/sq/40290d49-8cb4-43ba-acc8-750d0fa8bac0")

# loading the datas
df_raw_espoo = load_espoo_data()
df_raw_rovaniemi = load_rovaniemi_data()

df = df_raw_espoo.rename(columns={
    "Espoo Domestic nights": "Domestic nights",
    "Espoo Foreign nights": "Foreign nights",
    "Espoo Average room price": "Average room price",
    "Espoo Average price per night": "Average price per night",
    "Espoo Nights spent": "Nights spent",
})

st.markdown(''' # Overnight stays in Espoo
On this Streamlit page I will display data about accommondation capacity and nights spent in Espoo, 
from year 1995 to the current time. The data is divided into months. At the end of the page
I am comparing the Espoo data to Rovaniemi data. This comparison data can be exported.
''')

st.divider()

# displaying the raw data by using the streamlit's dataframe
st.markdown('''### Raw data of Espoo
This is the raw data about the overnight stays in Espoo that I will be working with.''')
st.dataframe(df_raw_espoo)

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
These columns are the people who are staying overnight at an accommondation. Below is a line chart of this data.''')
# drawing the table and graph
st.dataframe(df_domestic_and_foreign)

st.markdown('''### Line chart of domestic and foreign nights
This describes the domestic and foreign stays as a linechart. From this line chart we can see that
the trends follow each other quite well. There are a bit more of domestic stays. In the recent years this gap has
widened and it seems that domestic stays have increased while foreign stays have stayed quite the same.''')
st.line_chart(df_domestic_and_foreign, x="Month", y=["Domestic nights", "Foreign nights"], color=["#FF8C00", "#0041C2"])


# comparing espoo and rovaniemi
st.divider()

st.markdown('''# Comparing Espoo and Rovaniemi
I thought it would be interesting to see the difference betweeh a northern and southern cities.
Also, Espoo is not really a tourism city and Rovaniemi is. How do they compare? Let's see.''')

# first I will create a table that has both of rovaniemi's and espoo's data
# left join makes the values follow the espoo table and the rovaniemi values might get null
# this way I make sure that at least all the espoo values are the original ones
df_combined = df_raw_espoo.merge(df_raw_rovaniemi, how="left", on="Month")

# next I will create a dropdown menu that the user can choose what they compare
st.markdown('''### Comparison between Espoo and Rovaniemi
Here you can choose which data you would like to compare as a line chart. This data shows clearly how much
more popular Rovaniemi is at high season times.
            
Rovaniemi has around 70 000 residents whereas Espoo has well over 300 000 (2025). Therefore the difference is quite amazing.''')
comparison_column = st.selectbox(
    "Chosen data to compare",
    ("Domestic nights", "Foreign nights", "Average room price", "Average price per night", "Nights spent"),
)
# drawing the line chart based on chosen option
st.line_chart(df_combined, x="Month", y=["Espoo " + comparison_column, "Rovaniemi " + comparison_column])


# this base is copied form the streamlit documentation
# https://docs.streamlit.io/develop/api-reference/widgets/st.download_button
@st.cache_data
def convert_for_download(comparison_column):

    # turning the comparison data into a table. Here we will take into account 
    # what the user has chosen from the drop down menu
    df_export = df_combined[["Month", "Espoo " + comparison_column, "Rovaniemi " + comparison_column]]
    
    # then I will change the column name to have a _ instead of space
    # this will be used in the export name
    export_column_name = comparison_column.replace(" ", "_")

    return df_export.to_csv().encode("utf-8"), export_column_name

csv, export_column_name = convert_for_download(comparison_column)

st.download_button(
    label="Download Comparison as CSV",
    data=csv,
    file_name=f"espoo_rovaniemi_comparison_{export_column_name}.csv",
    mime="text/csv",
    icon=":material/download:",
)

st.markdown('''
You can export this displayed data as a CSV. The file will have the Month column and the columns of the
selected data. The file will be named by the comparison column name.''')
