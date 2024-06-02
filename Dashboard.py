# %%
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime as dt
import streamlit as st
import plotly.graph_objects as go
import os
import datetime
import pymongo 
from pymongo.server_api import ServerApi

# %% 
# Page Configuration 
st.set_page_config(
    page_title = 'Dashboard',
    layout = 'wide'
)

st.title('💸 Financial Dashboard')
st.sidebar.success('Selection Panel')

# %% 
# Connect to MongoDB

@st.cache_resource
def connect_db():
    client = pymongo.MongoClient(
        st.secrets["mongo"]["connection_url"],
        server_api=ServerApi('1'))
    db = client["spending_data"]
    return db.financial_dash

collection = connect_db()

st.write("Connected to MongoDB")

# %% 

# New data inputs 
st.subheader("New Entry")

col1, col2, col3, col4 = st.columns(4)

with col1:
    # Date input widget
    selected_date = st.date_input(
        "Select a date",
        value=datetime.date.today(),
        min_value=datetime.date(2020, 1, 1),
        max_value=datetime.date.today()
)

with col2:  
    # Type of spending input dropdown 
    type_spending = st.selectbox("Type of spending", ['Groceries', 'Motives', 'Takeout', 'School', 'Misc.', 'Shopping', 'Gifts', 'Subscriptions', 'Travel'])

with col3: 
    # Amount spent input 
    amount_spent = st.number_input("Amount spent", min_value=0.00, max_value=10000.00, value=0.00, step=0.01)

with col4:
    # toggle between credit or debit 
    payment_type = st.radio("Payment type", ['Credit', 'Debit'])

# Save data to MongoDB
if st.button("Save Entry"):
    data = {
        "date": selected_date.isoformat(),
        "type_spending": type_spending,
        "amount_spent": amount_spent,
        "payment_type": payment_type
    }
    collection.insert_one(data)
    st.success("Entry saved to the database!")

# %% 

# add section to input csv 
st.subheader("CSV File Uploader")

# File uploader
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    # Read the CSV file
    newdata = pd.read_csv(uploaded_file)
    # Example: Display the first few rows
    if st.button("Save CSV to MongoDB"):
        data = []
        for index, row in newdata.iterrows():
            data.append({
                "date": row[0],
                "description": row[1],
                "type_spending": row[2],
                "amount_spent": row[3],
                "payment_type": row[4]
            })
        collection.insert_many(data)
        st.success("Entry saved to the database!")

# %% 

# Retrieve data from MongoDB
data = collection.find()

# Convert data to Pandas DataFrame
df = pd.DataFrame(data)

st.title("Data Visualization")

# Display the DataFrame
if st.checkbox('Show data:'):
    st.subheader('MongoDB data')
    st.write(df.head())

col1, col2 = st.columns(2)

with col1:  
    # Example plot using Matplotlib
    st.write("Total Amount Spent Over Time")
    st.line_chart(df, x= 'date', y='amount_spent', use_container_width=True)
with col2:
    st.write("Total Spending by Type")
    type_plot = df['type_spending'].value_counts()
    st.bar_chart(type_plot, use_container_width=True)

st.set_option('deprecation.showPyplotGlobalUse', False)
st.pyplot()

# %% 
### Selecting time period for monthly aggregation and reducing dataframe to df to prepare for time series model

# %%
# df = res.reset_index()

# df2 = df.groupby(['Date ','Type'], as_index=False)['Amount Spent '].sum()
# df2.groupby([df2['Date '].dt.to_period('M'), 'Type']).sum().reset_index()

# st.subheader("Spending Type Comparison")
# clist = df2["Type"].unique().tolist()
# types = st.multiselect("Select the types of spending you would like to compare", clist)
# st.header("You selected: {}".format(", ".join(types)))      

# dfs = {type: df2[df2["Type"] == type] for type in types}

# fig = go.Figure()
# for type, df2 in dfs.items():
#     fig = fig.add_trace(go.Scatter(x=df2["Date "], y=df2["Amount Spent "], name=type))

# st.plotly_chart(fig, use_container_width=True)
