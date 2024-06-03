# %%
import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

from Dashboard import collection
from functions import seasonal_decompose, test_stationarity, ADF_test


st.header("📈 Data Exploration")
st.markdown("We will now further explore the data in preparation for time series modelling.")
st.subheader("Total Monthly Spending with Monthly Mean Resample")
# This is monthly spending and mean resampling on monthly basis

# %% 
# retrieve data 
data = collection.find()
df = pd.DataFrame(data)
df['date'] = pd.to_datetime(df['date'])

# daily sum 
daily = df.groupby(df['date'].dt.to_period('D'))['amount_spent'].sum()
daily = daily.to_frame()
daily['date'] = daily.index

# monthly resample 
monthly = df.resample('M', on='date')['amount_spent'].sum()
monthly = monthly.to_frame()
monthly['date'] = monthly.index

# Streamlit line plot 
st.line_chart(monthly, x='date', y='amount_spent', use_container_width=True)
# %%
# Display the plot in Streamlit
with st.expander("Read more"):
    st.markdown("this plot allows us to visualize the spending on a monthly basis in comparison to the average amount spent that month. It is important to check time series data for patterns that may affect the results, and can inform which forecasting model to use. Depending on the stability of the mean line we can judge to volatility of an individuals spending")

st.subheader("Decomposition")
st.markdown("First I start by looking for patterns in the model. I do this by decomposing the data using the seasonal_decompose function, within the 'statsmodel' package, to view more of the complexity behind the linear visualization. This function helps to decompose the data into the four common time series data patterns; Observed, Trended, Seasonal, Residual.")

seasonal_decompose(df['amount_spent'])

# %% 
# Stationarity - must check if data is stationary 
### plot for Rolling Statistic for testing Stationarity

st.subheader("Stationarity")
st.markdown("Next I check the data for stationarity. Data is statinary when its statistical properties do not change much over time. It is important to have stationary data when building a time series forecasting model to make accurate predictions. I check stationarity using isualization and the Augmented Dickey-Fuller (ADF) Test.")

test_stationarity(df['amount_spent'],'raw data')
with st.expander("Read more"):
    st.markdown("Using the test_stationarity function we can see the rolling statistics (mean and variance) at a glance to determine how drastically the standard deviation over time. Since both mean and standard deviation do not change much over time we can assume they are stationary, but can further use the ADF for more confidence")
# %%
# Augmented Dickey-Fuller Test

st.subheader("Augmented Dickey-Fuller Test")
ADF_test(df['amount_spent'],'raw data')
with st.expander("Read more"):
    st.markdown("Using the ADF test we can be confident the data is stationary ")