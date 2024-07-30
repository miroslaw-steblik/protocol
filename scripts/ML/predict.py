

# ----------------- PREDICT WITH API ----------------- #
# import requests

# url = 'http://127.0.0.1:5000/predict'

# value = 100
# data = {'features': [value]}  # Replace with actual feature values

# response = requests.post(url, json=data)
# print(response.json())

# ----------------- PREDICT MANUAL ----------------- #
import pickle

"""
`pickle` is a Python module used for serializing and deserializing Python object 
structures, also known as "pickling" and "unpickling." Serialization 
refers to the process of converting an object into a byte stream, 
and deserialization is the reverse process, where the byte stream is 
converted back into an object.

Here's a brief overview of how `pickle` is used:

- Pickling: Convert a Python object into a byte stream and save it to a file.
- Unpickling: Load the byte stream from a file and convert it back into a Python object.
"""

# List of values to predict
values = [14.5, 20.0, 25.5, 30.0]  # Replace with your actual values

# Load the trained model
with open('model.pkl', 'rb') as file:
    model = pickle.load(file)

# Predict for each value in the list
predictions = model.predict([[value] for value in values])

# Print the prediction results
for value, prediction in zip(values, predictions):
    print(f'\nValue: {value}, Prediction: {prediction}')


