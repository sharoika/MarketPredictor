from tensorflow.keras.models import load_model
import numpy as np

features = []

open_price = 182.8
close_price = 182.31
low_price = 182.44
high_price = 184.15
volume = 51703670

polarity = 0.9
subjectivity = 1.0

features.append([open_price, close_price, high_price, low_price, polarity, subjectivity])

features = np.array(features)


# Load the saved model
model = load_model("my_model_test")

predictions = model.predict(features)

print(predictions)