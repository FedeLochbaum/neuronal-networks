import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import random
from sklearn.utils import shuffle
from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score

housing = shuffle(pd.read_csv("housing.csv"))

# Only a feature (total_rooms)
x = pd.DataFrame(housing['total_rooms'])

# Goal (median_house_value)
y = pd.DataFrame(housing['median_house_value'])

housing_x_train = x[:-20]
housing_x_test = x[-20:]

housing_y_train = y[:-20]
housing_y_test = y[-20:]

# Create an instance of linear model
linear_modal = linear_model.LinearRegression()

# Train and fit the model
linear_modal.fit(housing_x_train, housing_y_train)

# Check the  predictions
housing_y_pred = linear_modal.predict(housing_x_test)


print('Coefficients: \n', linear_modal.coef_)

print("Mean squared error: %.2f"
      % mean_squared_error(housing_y_test, housing_y_pred))

print('Variance score: %.2f' % r2_score(housing_y_test, housing_y_pred))

# Plot outputs
plt.scatter(housing_x_test, housing_y_test,  color='black')
plt.plot(housing_x_test, housing_y_pred, color='blue', linewidth=3)

plt.xticks(())
plt.yticks(())

plt.show()