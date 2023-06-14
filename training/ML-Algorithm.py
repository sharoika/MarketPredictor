import json
import numpy as np
import tensorflow as tf

# Load the JSON data
with open("master_tainer.json") as inputData:
    data = json.load(inputData)

data = sorted(data, key=lambda item: item["date"])

# Extract the features and labels from the data
features = []
labels = []

for item, next_day_item in zip(data, data[1:]):
    for stock, next_day_stock in zip(item["stocks"], next_day_item["stocks"]):
        
        stock_data = stock["stock"]
        next_dat_stock_data = next_day_stock["stock"]
        
        ticker = stock_data["ticker"]


        open_price = float(stock_data["open"])

        if np.isnan(open_price):
            print("Missing or NaN value found for open_price")

        close_price = float(stock_data["close"])

        if np.isnan(close_price):
            print("Missing or NaN value found for close_price")

        high_price = float(stock_data["high"])

        if np.isnan(high_price):
            print("Missing or NaN value found for high_price")

        low_price = float(stock_data["low"])

        if np.isnan(low_price):
            print("Missing or NaN value found for low_price")

        volume = float(stock_data["volume"])

        if np.isnan(volume):
            print("Missing or NaN value found for volume")

        tommorow_price_change = float(next_dat_stock_data["close"] - stock_data["close"])
        print(tommorow_price_change)

        if np.isnan(tommorow_price_change):
            print("Missing or NaN value found for tommorow_price_change")

        # Filter tweets for the current ticker
        tweets = [tweet["tweet"] for tweet in item["tweets"] if tweet["tweet"]["ticker"] == ticker]

        # Calculate average polarity and subjectivity
        polarity = float(np.mean([tweet["polarity"] for tweet in tweets]))
        subjectivity = float(np.mean([tweet["subjectivity"] for tweet in tweets]))

        if ticker == "NVDA":
            polarity = 0
            subjectivity = 0

        if np.isnan(polarity):
            print("Missing or NaN value found for polarity" + ticker)
        
        if np.isnan(subjectivity):
            print("Missing or NaN value found for subjectivity" + ticker)

        features.append([open_price, close_price, high_price, low_price, polarity, subjectivity])
        labels.append(tommorow_price_change)

# Convert the lists to numpy arrays
features = np.array(features)
labels = np.array(labels)

# normalized_features = (features - np.mean(features, axis=0)) / np.std(features, axis=0)

# Split the data into training and testing sets
train_size = int(0.8 * len(features))
train_features, test_features = features[:train_size], features[train_size:]
train_labels, test_labels = labels[:train_size], labels[train_size:]

# Create a TensorFlow model
model = tf.keras.models.Sequential([
    tf.keras.layers.Dense(64, activation='relu', input_shape=(6,)),
    tf.keras.layers.Dense(1)
])

# Compile the model
model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.0001), loss='mean_squared_error')

# Train the model
model.fit(train_features, train_labels, epochs=1000, batch_size=32)

# Evaluate the model
mse = model.evaluate(test_features, test_labels)
print("Mean Squared Error:", mse)

model.save("my_model_test")