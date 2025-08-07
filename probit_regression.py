#!/usr/bin/env python
# coding: utf-8

# # 📈 Probit Regression Analysis with 95% Confidence Interval Plot
# 
# This notebook demonstrates how to perform a **probit regression** to model the probability of a positive detection based on antibody concentration. We also visualize the predicted probabilities along with their 95% confidence intervals.
# 
# ---
# 
# ## 📥 1. Import Libraries and Load Data

# In[2]:


import pandas as pd

url = "https://raw.githubusercontent.com/WKPhang/probit-regression-plot/main/pseudodata_diagnostic_performance.csv"
df = pd.read_csv(url)
print(df.head())


# # 🧮 2. Fit Probit Regression Model
# We use the statsmodels library to fit a probit regression model:
# 
# Predictor: antibody_conc
# 
# Response: binary variable positive (1 = positive detection, 0 = negative)

# In[3]:


import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt

# Fit model
X = sm.add_constant(df['antibody_conc'])
y = df['positive']
model = sm.Probit(y, X)
result = model.fit()
print(result.summary())


# # 3. 📈 Predict Probabilities and 95% Confidence Intervals
# We generate predictions across a range of antibody concentrations (0 to 10, step of 0.5) and extract:
# - Predicted probabilities
# - Lower and upper bounds of 95% confidence intervals

# In[4]:


# Generate new values for prediction
newdf = pd.DataFrame({'antibody_conc': np.arange(0, 10.5, 0.5)})
X_new = sm.add_constant(newdf['antibody_conc'])

# Predict probabilities + get 95% confidence intervals
pred = result.get_prediction(X_new)
pred_summary = pred.summary_frame(alpha=0.05)

print(pred_summary.head())  # See actual column names



# # 4. 📊 Visualization of Predicted Probabilities with 95% CI
# We plot:
# - The predicted probability curve (blue line)
# - The 95% confidence interval (shaded region)

# In[5]:


newdf['p'] = pred_summary['predicted']
newdf['lwr'] = pred_summary['ci_lower']
newdf['upr'] = pred_summary['ci_upper']

# Plot
plt.figure(figsize=(8, 5))
plt.plot(newdf['antibody_conc'], newdf['p'], label='Probit predicted probability', color='blue')
plt.fill_between(newdf['antibody_conc'], newdf['lwr'], newdf['upr'], color='blue', alpha=0.4, label='95% CI')
plt.xlabel('Antibody concentration')
plt.ylabel('Probability of positive detection')
plt.legend()
plt.title('Probit Regression: Predicted Probability with 95% CI')
plt.show()

