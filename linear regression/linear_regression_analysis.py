




import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder


# Read data from the CSV file
csv_file_path = 'baby_names.csv'
df = pd.read_csv(csv_file_path)


# Encode names from the Name column
label_encoder = LabelEncoder()
df['Name_encoded'] = label_encoder.fit_transform(df['Name'])


# Extract features (Popularity Rank) and target variable (Name_encoded)
X = df['Popularity Rank'].values.reshape(-1, 1)
y = df['Name_encoded'].values


# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create a linear regression model
model = LinearRegression()

# Train the model
model.fit(X_train, y_train)

# Make predictions on the test set
y_pred = model.predict(X_test)

# Calculate and print the mean squared error
mse = mean_squared_error(y_test, y_pred)
print(f'Mean Squared Error: {mse}')

# Plot the data and the regression line
plt.scatter(X, y, color='blue')
plt.plot(X, model.predict(X), color='red', linewidth=2)
plt.xlabel('Popularity Rank')
plt.ylabel('Name')
plt.title('Linear Regression Analysis')
plt.show()
