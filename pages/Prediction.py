import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from statsmodels.tsa.api import SimpleExpSmoothing 
from statsmodels.tsa.api import ExponentialSmoothing
from sklearn.model_selection import train_test_split
from prophet import Prophet
from Dashboard import collection

data = collection.find()
df = pd.DataFrame(data)
df['date'] = pd.to_datetime(df['date'])

# use train_test_split to split the data into training and validation sets by date
df = df.sort_values(by='date')
train_df, validation_df = train_test_split(df, test_size=0.2, random_state=42, shuffle=False)

# Prepare the training data for Prophet
train_prophet = train_df[['date', 'amount_spent']].rename(columns={'date': 'ds', 'amount_spent': 'y'})

# Initialize and fit the Prophet model
model = Prophet()
model.fit(train_prophet)

# Make future dataframe for the next 12 months
future = model.make_future_dataframe(periods=12, freq='M')

# Make predictions
forecast = model.predict(future)

# Plot the forecast
fig1 = model.plot(forecast)
fig2 = model.plot_components(forecast)

# Display the plot in Streamlit
st.header("Prophet Model Forecast")
st.pyplot(fig1)
st.pyplot(fig2)

# Optionally, you can compare with validation data
validation_prophet = validation_df[['date', 'amount_spent']].rename(columns={'date': 'ds', 'amount_spent': 'y'})
validation_prophet = validation_prophet.set_index('ds')
forecast.set_index('ds', inplace=True)

# Plot the actual validation data against the forecast
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(train_prophet['ds'], train_prophet['y'], label='Training Data')
ax.plot(validation_prophet.index, validation_prophet['y'], label='Validation Data', color='orange')
ax.plot(forecast.index, forecast['yhat'], label='Forecast', color='green')
ax.fill_between(forecast.index, forecast['yhat_lower'], forecast['yhat_upper'], color='lightgreen', alpha=0.5)
ax.set_title('Training, Validation and Forecast')
ax.legend()

st.pyplot(fig)