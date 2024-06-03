# Personal Finance Dashboard 

The goal of this Personal Finance Dashboard is to have a better understanding of spending habits and predict future spending on a monthly basis. As a result, the aim of this insight is to have more realistic budgets and reduce spending where possible.

## Background Info

I have created a Python based web application dashboard on Streamlit to gain better insight of my spending habits. This web app is using personal spending data that I have collected for 9 months to analyze and visualize spending patterns, as well as predict future spending. This dashboard connects to a database in MongoDB which manages historical and new inputted data. As well, it predicts average spending per month based on a time series Prophet model, which allows the user to know if their spending is predicted to be too high in a specific category.   

https://financialdash.streamlit.app/

## References 

Some Python codes and project structure was inspired by the resources below: 
https://www.statsmodels.org/dev/examples/notebooks/generated/exponential_smoothing.html
https://www.bounteous.com/insights/2020/09/15/forecasting-time-series-model-using-python-part-one/
