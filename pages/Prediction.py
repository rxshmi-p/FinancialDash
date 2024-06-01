import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from statsmodels.tsa.api import SimpleExpSmoothing 
from statsmodels.tsa.api import ExponentialSmoothing
from Dashboard import spent_by_month


y_to_train = spent_by_month['2021-07-01':'2022-01-01'] # dataset to train
y_to_val = spent_by_month['2022-01-02':'2022-05-30'] # last X months for test  
predict_date = len(spent_by_month) - len(spent_by_month['2022-01-02':'2022-05-30']) # the number of data points for the test set


st.header("Predicting Future Spending")

st.subheader("Choosing a Model: Simple Exponential Smoothing (SES)")

ses_fit = SimpleExpSmoothing(spent_by_month, initialization_method="estimated").fit(
    smoothing_level=0.8, optimized=False
)
ses_forecast = ses_fit.forecast(4).rename(r"$\alpha=0.8$")
fig, ax = plt.subplots(figsize=(8, 3))
(line3,) = plt.plot(ses_forecast, marker="o", color="red")
ax.plot(spent_by_month, marker="o", color="black")
ax.plot(ses_fit.fittedvalues, marker="o", color="red")
ax.legend([line3], [ses_forecast.name])
st.pyplot(fig)

st.text(ses_forecast)
st.expander("This model is not a good fit because the forecast is linear so this is an inaccurate prediction for our model")
# %%
st.subheader("Choosing a Model: Holt - Winters")


hw_add = ExponentialSmoothing(
    spent_by_month,
    seasonal_periods=4,
    trend="add",
    seasonal="add",
    use_boxcox=True,
    initialization_method="estimated",
).fit()
hw_mul = ExponentialSmoothing(
    spent_by_month,
    seasonal_periods=4,
    trend="mul",
    seasonal="mul",
    use_boxcox=True,
    initialization_method="estimated",
).fit()
ax = spent_by_month.plot(
    figsize=(8, 3),
    marker="o",
    color="black",
    title="Forecasts from Holt-Winters'",
)
ax.set_ylabel("Amount Spent ($)")
ax.set_xlabel("Month")
hw_add.fittedvalues.plot(ax=ax, style="--", color="red")
hw_mul.fittedvalues.plot(ax=ax, style="--", color="green")
hw_add.forecast(12).rename("Holt-Winters (add-add-seasonal)").plot(
    ax=ax, style="--", marker="o", color="red", legend=True
)
hw_mul.forecast(12).rename("Holt-Winters (add-mul-seasonal)").plot(
    ax=ax, style="--", marker="o", color="green", legend=True
)

st.set_option('deprecation.showPyplotGlobalUse', False)
st.pyplot()


# %%

st.markdown("Taking a look at the model metrics we can compare the HW Additive method vs the HW Multiplicative Method")

results = pd.DataFrame(
    index=[r"$\alpha$", r"$\beta$", r"$\phi$", r"$\gamma$", r"$l_0$", "$b_0$", "SSE"]
)
params = [
    "smoothing_level",
    "smoothing_trend",
    "damping_trend",
    "smoothing_seasonal",
    "initial_level",
    "initial_trend",
]
results["Additive"] = [hw_add.params[p] for p in params] + [hw_add.sse]
results["Multiplicative"] = [hw_mul.params[p] for p in params] + [hw_mul.sse]
st.dataframe(results) 

st.markdown("Since multiplicative has the lowest sum of squared estimate of error, we will using this method.")

# %%

with st.container():
    m = st.slider('How many months would you like to forecast?', 5, 10, 5)
    st.subheader("Forecast - Multiplicative Method")
    mul_forecast = hw_mul.forecast(m)
    st.dataframe(mul_forecast)
