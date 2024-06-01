import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

from Dashboard import res
from functions import seasonal_decompose, test_stationarity, ADF_test


st.header("📈 Data Exploration")
st.markdown("We will now further explore the data in preparation for time series modelling.")
st.subheader("Total Monthly Spending with Monthly Mean Resample")
# This is monthly spending and mean resampling on monthly basis
fig, ax = plt.subplots(figsize=(20, 6))
ax.plot(res['Amount Spent '],marker='.', linestyle='-', linewidth=0.5, label='Monthly')
ax.plot(res['2021-07-01':'2022-05-30'].resample('M').mean(),marker='o', markersize=8, linestyle='-', label='Monthly Mean Resample')
ax.set_ylabel('Total Spent')
ax.legend()
st.pyplot(fig)
with st.expander("Read more"):
    st.markdown("this plot allows us to visualize the spending on a monthly basis in comparison to the average amount spent that month. It is important to check time series data for patterns that may affect the results, and can inform which forecasting model to use. Depending on the stability of the mean line we can judge to volatility of an individuals spending")

st.subheader("Decomposition")
st.markdown("First I start by looking for patterns in the model. I do this by decomposing the data using the seasonal_decompose function, within the 'statsmodel' package, to view more of the complexity behind the linear visualization. This function helps to decompose the data into the four common time series data patterns; Observed, Trended, Seasonal, Residual.")

df = pd.DataFrame(res['Amount Spent '])
seasonal_decompose(df)

# %% 
# Stationarity - must check if data is stationary 
### plot for Rolling Statistic for testing Stationarity

st.subheader("Stationarity")
st.markdown("Next I check the data for stationarity. Data is statinary when its statistical properties do not change much over time. It is important to have stationary data when building a time series forecasting model to make accurate predictions. I check stationarity using isualization and the Augmented Dickey-Fuller (ADF) Test.")

test_stationarity(df['Amount Spent '],'raw data')
with st.expander("Read more"):
    st.markdown("Using the test_stationarity function we can see the rolling statistics (mean and variance) at a glance to determine how drastically the standard deviation over time. Since both mean and standard deviation do not change much over time we can assume they are stationary, but can further use the ADF for more confidence")
# %%
# Augmented Dickey-Fuller Test

st.subheader("Augmented Dickey-Fuller Test")
ADF_test(df,'raw data')
with st.expander("Read more"):
    st.markdown("Using the ADF test we can be confident the data is stationary ")