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
    page_title = 'Financial Dashboard',
    layout = 'wide'
)

st.title('Financial Dashboard')
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

# %%
### Importing Data
# must update total months and new dataset name 

path = '/Users/rashmipanse/Documents/Projects/FinancialDash/data.csv'

# for filename in os.listdir(path):
#     if filename.endswith('.csv'):
#         filepath = os.path.join(path, filename)
#         monthly_list.append(pd.read_csv(filepath))

# # Concatenate all dataframes in the list into a single dataframe
# monthly = pd.concat(monthly_list, ignore_index=True)
data = pd.read_csv(path)

#%%
### Cleaning Dataframes 

# drop columns
data.dropna(inplace=True)

# %% 
# reformat date column to date datatype
data['Date '] = pd.to_datetime(data['Date '], errors='coerce')



# %%
### Combine monthly datasets, convert to datetime, set date as index 

res = data.set_index('Date ').sort_index()

if st.checkbox('Show model data'):
    st.subheader('Model data')
    st.write(res)

# %% 
# Plots  
st.subheader('Summary Plots')

col1, col2 = st.columns(2)

with col1:
    st.subheader("Total Amount Spent Over Time")
    st.line_chart(res['Amount_Spent'], use_container_width=True)

with col2:
    st.header("Total Spending by Type")
    ty_plot = res['Type'].value_counts()
    st.bar_chart(ty_plot)


# %% 
### Selecting time period for monthly aggregation and reducing dataframe to df to prepare for time series model
spent_by_month = res.resample('M').sum()

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

# graphs to show seasonal_decompose
# Examined model for patterns:
# Level (avg value in series) - increases and then drops  after a peak, seen pattern twice
# Trend (increases, decreases, stays same over time)
# Seasonal/Periodic
# Cyclical (increase/decrease non-seasonal related, like business cycles)
# Random/Irregular variations
# %% 

# add section to input csv 
st.title("CSV File Uploader")

# File uploader
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    # Read the CSV file
    newdata = pd.read_csv(uploaded_file)

    # Display the DataFrame
    st.write(newdata)

    # Process the DataFrame as needed
    # Example: Display the first few rows
    st.write("First 5 rows of the DataFrame:")
    st.write(newdata.head())

# %% 

# New data inputs 
st.title("New Entry")

# Date input widget
selected_date = st.date_input(
    "Select a date",
    value=datetime.date.today(),
    min_value=datetime.date(2020, 1, 1),
    max_value=datetime.date.today()
)

st.write(f"Selected date: {selected_date}")

# Type of spending input dropdown 
type_spending = st.selectbox("Type of spending", ['Groceries', 'Motives', 'Takeout', 'School', 'Misc.', 'Shopping', 'Gifts', 'Subscriptions', 'Travel'])
st.write(f"Type of spending: {type_spending}")

# Amount spent input 
amount_spent = st.number_input("Amount spent", min_value=0.00, max_value=10000.00, value=0.00, step=0.01)
st.write(f"Amount spent: ${amount_spent}")

# toggle between credit or debit 
payment_type = st.radio("Payment type", ['Credit', 'Debit'])
st.write(f"Payment type: {payment_type}")

# %% 
# Add new entry to the database

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

# Retrieve data from MongoDB
data = list(collection.find())

# Convert data to Pandas DataFrame
df = pd.DataFrame(data)

# Streamlit app
st.title("Data Visualization")

# Display the DataFrame
st.write("Data from MongoDB:")
st.write(df)

# Plotting
st.title("Graph")

# Example plot using Matplotlib
st.write("Example plot using Matplotlib:")
plt.bar(df["type_spending"], df["amount_spent"])
plt.xlabel("Type of Spending")
plt.ylabel("Amount Spent")
plt.title("Amount Spent by Type")
st.set_option('deprecation.showPyplotGlobalUse', False)
st.pyplot()