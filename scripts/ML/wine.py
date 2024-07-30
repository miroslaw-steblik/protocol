import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.datasets import load_wine
import pickle

# ----------------- LOAD DATA ----------------- #
wine = load_wine()
print(wine.DESCR)
print(wine.feature_names)
print('Three types of wine', wine.target_names) # Three types of wine ['class_0' 'class_1' 'class_2']

df = pd.DataFrame(wine.data, columns=wine.feature_names)
print(df.head())

X = df['alcohol'].values.reshape(-1, 1) 
y = df['proline'].values

"""
X: The feature matrix X is reshaped to be a 2D array with one column 
because scikit-learn's LinearRegression model expects the input features 
to be in a 2D array format, where each row is a sample and each column is a feature.

y: The target variable y is a 1D array, which is the expected format for the 
target values in scikit-learn. The LinearRegression model can handle y as a 1D array 
directly.
"""

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

"""
X_train:
- Description: This variable contains the training data for the features (input variables).
- Usage: It is used to train the machine learning model.
- Shape: Typically a 2D array where rows represent samples and columns represent features.

X_test:
- Description: This variable contains the testing data for the features.
- Usage: It is used to evaluate the performance of the trained model.
- Shape: Similar to X_train, it is a 2D array with the same number of columns (features) but fewer rows (samples).

y_train:
- Description: This variable contains the training data for the target variable (output variable).
- Usage: It is used along with X_train to train the machine learning model.
- Shape: Typically a 1D array where each element corresponds to the target value for the respective row in X_train.

y_test:
- Description: This variable contains the testing data for the target variable.
- Usage: It is used along with X_test to evaluate the performance of the trained model.
- Shape: Similar to y_train, it is a 1D array where each element corresponds to the target value for the respective row in X_test.
"""

# ----------------- TRAIN MODEL ----------------- #
model = LinearRegression()
model.fit(X_train, y_train)

# ----------------- EVALUATE MODEL ----------------- #
score = model.score(X_test, y_test)
print('R2 Score:', score)


# ----------------- SAVE MODEL ----------------- #
# Save the model
with open('model.pkl', 'wb') as file:
    pickle.dump(model, file)

# ----------------- LOAD MODEL - FLASK ----------------- #
# from flask import Flask, request, jsonify

# app = Flask(__name__)

# # Load the trained model
# with open('model.pkl', 'rb') as file:
#     model = pickle.load(file)

# # Endpoint API to predict
# @app.route('/predict', methods=['POST'])
# def predict():
#     data = request.get_json(force=True)
#     prediction = model.predict([data['features']])
#     return jsonify({'prediction': prediction.tolist()})

# if __name__ == '__main__':
#     app.run(debug=True)

# ----------------- PLot ----------------- #
import matplotlib.pyplot as plt

y_pred = model.predict(X_test)

plt.scatter(X_test, y_test, color='black')
plt.plot(X_test, y_pred, color='blue', linewidth=3)
plt.xlabel('Alcohol')
plt.ylabel('Proline')
plt.show()




