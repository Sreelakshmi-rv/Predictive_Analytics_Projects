# -*- coding: utf-8 -*-
"""Predictive_Analytics_Project_1.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1chKG5raIsZu0AMG8X2gUrHMrcnpj2xbK

# Multiple Linear Regression

**1. Loading and exploring data:**
"""

import pandas as pd

df= pd.read_csv('/content/cars.csv')
df.head()

df.info()

df.describe()

"""Rows & Columns: 5,076 entries, 18 columns.

Numeric Features: Dimensions (Height, Length, Width), Number of Forward Gears,
City & Highway MPG, Horsepower, Torque, Year.

Categorical Features: Driveline, Engine Type, Transmission, Fuel Type, Classification, Make, Model Year, ID.

Potential Target Variables: City MPG, Highway MPG, or Horsepower.

**2. Handle missing and unique values:**
"""

# Check for missing values
missing_values = df.isnull().sum()

missing_values

# Check unique values in categorical columns
categorical_cols = df.select_dtypes(include=['object', 'bool']).columns
unique_values = {col: df[col].nunique() for col in categorical_cols}

unique_values

"""Missing values: None

Categorical variables with high cardinalities: Engine Information.Engine Type(535), Identification.ID(5030), Identification.Model Year(918)

**3. Handle Duplicate rows:**
"""

# Check for duplicate rows
duplicate_rows = df.duplicated().sum()
duplicate_rows

df = df.drop_duplicates()
df.reset_index(drop=True, inplace=True)

"""**4. Encode Categorical Variables:**"""

# Dropping ID and Model Year since they are the mostly unique identifiers
df_cleaned = df.drop(columns=["Identification.ID", "Identification.Model Year"])

# One-hot encode categorical variables with low cardinality
cols_to_encode = ["Engine Information.Driveline", "Engine Information.Transmission",
                              "Fuel Information.Fuel Type", "Identification.Classification"]

df_encoded = pd.get_dummies(df_cleaned, columns=cols_to_encode, drop_first=True)

# Display the first few rows after encoding
df_encoded.head()

# Identify columns with object (string) data types
categorical_cols = df_encoded.select_dtypes(include=['object']).columns
print("Categorical Columns:", categorical_cols)

from sklearn.preprocessing import LabelEncoder

# Apply Label Encoding to all categorical columns
label_encoders = {}
for col in categorical_cols:
    le = LabelEncoder()
    df_encoded[col] = le.fit_transform(df_encoded[col])
    label_encoders[col] = le  # Store encoders for reference

print("Categorical columns successfully encoded.")

"""**5. Feature Selection:**

Possible Target Variables: Fuel Information.City mpg, Fuel Information.Highway mpg, Engine Information.Engine Statistics.Horsepower.
"""

import seaborn as sns
import matplotlib.pyplot as plt

# Compute correlation matrix
corr_matrix = df_encoded.corr()

# Plot heatmap
plt.figure(figsize=(12, 8))
sns.heatmap(corr_matrix, cmap="coolwarm", annot=False, linewidths=0.5)
plt.title("Feature Correlation Heatmap")
plt.show()

"""*From the heat map we can identify strongly correlated variables:*

Fuel Information.City mpg and Fuel Information.Highway mpg

Engine Information.Engine Statistics.Horsepower and Engine Information.Engine Statistics.Torque

**Selected Target variable:** Fuel Information.Highway mpg

**6. Feature Scaling:**
"""

from sklearn.preprocessing import StandardScaler

# Selecting numerical features for scaling
numerical_features = [
    "Engine Information.Engine Statistics.Horsepower",
    "Engine Information.Engine Statistics.Torque",
    "Dimensions.Height",
    "Dimensions.Length",
    "Dimensions.Width",
    "Engine Information.Number of Forward Gears",
    "Fuel Information.City mpg",
    "Fuel Information.Highway mpg",
    "Identification.Year"
]

# Applying StandardScaler (Z-score normalization)
scaler = StandardScaler()
df_scaled = df.copy()
df_scaled[numerical_features] = scaler.fit_transform(df[numerical_features])

# Display the first few rows of the scaled dataset
df_scaled.head()

"""**7. Handling Outliers:**"""

import numpy as np

# Define numerical features
numerical_features = [
    "Engine Information.Engine Statistics.Horsepower",
    "Engine Information.Engine Statistics.Torque",
    "Dimensions.Height",
    "Dimensions.Length",
    "Dimensions.Width",
    "Engine Information.Number of Forward Gears",
    "Fuel Information.City mpg",
    "Fuel Information.Highway mpg",
    "Identification.Year"
]

# Remove outliers using IQR method
Q1 = df[numerical_features].quantile(0.25)
Q3 = df[numerical_features].quantile(0.75)
IQR = Q3 - Q1

df_no_outliers = df[~((df[numerical_features] < (Q1 - 1.5 * IQR)) |
                      (df[numerical_features] > (Q3 + 1.5 * IQR))).any(axis=1)]

# Compare dataset size before and after outlier removal
print("Original dataset shape:", df.shape)
print("Dataset shape after outlier removal:", df_no_outliers.shape)

"""**8. Data splitting:**"""

from sklearn.model_selection import train_test_split

# Define target variable
target = "Fuel Information.Highway mpg"

# Define features (excluding the target variable)
X = df_encoded.drop(columns=[target])
y = df_encoded[target]

# Split data into training (80%) and testing (20%) sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Display shapes of the datasets
X_train.shape, X_test.shape, y_train.shape, y_test.shape

"""Training Set: 4,060 samples

Testing Set: 1,016 samples

Feature Count: 28

**9. Building the Multiple linear regression model:**
"""

#building multiple linear regression model
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np

# Initialize and train the model
model = LinearRegression()
model.fit(X_train, y_train)

# Predictions
y_train_pred = model.predict(X_train)
y_test_pred = model.predict(X_test)

"""**10. Evaluating Model Performance:**"""

# Model Evaluation
train_mae = mean_absolute_error(y_train, y_train_pred)
test_mae = mean_absolute_error(y_test, y_test_pred)

train_mse = mean_squared_error(y_train, y_train_pred)
test_mse = mean_squared_error(y_test, y_test_pred)

train_rmse = np.sqrt(train_mse)
test_rmse = np.sqrt(test_mse)

train_r2 = r2_score(y_train, y_train_pred)
test_r2 = r2_score(y_test, y_test_pred)

# Display evaluation metrics
(train_mae, test_mae, train_rmse, test_rmse, train_r2, test_r2)

"""**11. Check assumptions of Linear Regression:**"""

import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats

# Calculate residuals
train_residuals = y_train - y_train_pred
test_residuals = y_test - y_test_pred

# --- HOMOSCEDASTICITY CHECK ---
plt.scatter(y_train_pred, train_residuals, alpha=0.5)
plt.axhline(y=0, color='red', linestyle='dashed')
plt.xlabel("Predicted Values")
plt.ylabel("Residuals")
plt.title("Residuals vs Predicted (Homoscedasticity Check)")
plt.show()

# --- NORMALITY CHECK ---
sns.histplot(train_residuals, kde=True, bins=30)
plt.title("Histogram of Residuals (Normality Check)")
plt.show()

stats.probplot(train_residuals, dist="norm", plot=plt)
plt.title("Q-Q Plot (Normality Check)")
plt.show()

"""**12. Visulaizations:**"""

#actual vs predicted plot
import matplotlib.pyplot as plt

plt.figure(figsize=(8, 5))
plt.scatter(y_test, y_test_pred, color='blue', alpha=0.5, label="Predictions")
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r', lw=2, label="Perfect Fit")  # 45-degree line
plt.xlabel("Actual Highway MPG")
plt.ylabel("Predicted Highway MPG")
plt.title("Actual vs Predicted Highway MPG")
plt.legend()
plt.show()

#Residual plot
import seaborn as sns

residuals = y_test - y_test_pred  # Compute residuals

plt.figure(figsize=(8, 5))
sns.scatterplot(x=y_test_pred, y=residuals, alpha=0.5, color='blue')
plt.axhline(y=0, color='red', linestyle='--', lw=2)  # Zero line
plt.xlabel("Predicted Highway MPG")
plt.ylabel("Residuals")
plt.title("Residual Plot")
plt.show()

"""**Final Model Evaluation:**

Mean Absolute Error (MAE)-
Training Set: 1.1223,
Test Set: 1.0700

Mean Squared Error(MSE)-
Training Set: 3.3773,
Test Set: 1.4415

Root Mean Squared Error (RMSE)-
Training Set: 3.3773,
Test Set: 1.4415

R² Score-
Training Set: 0.7406,
Test Set: 0.9407

***The R² score of 0.94 on the test set suggests that the model explains 94% of the variance in the target variable (Fuel Information.Highway mpg).***

***The low RMSE on the test set indicates that predictions are relatively close to actual values, suggesting a well-fitting model.***

***The model seems to generalize well, as the test R² is higher than the training R², which might indicate that the model performs slightly better on unseen data.***
"""