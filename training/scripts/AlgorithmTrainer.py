import json
import math
import numpy as np
import tensorflow as tf

def AlgorithmTrainer(masterTrainerFilePath, modelFilePath):

    # Load the JSON data
    with open(masterTrainerFilePath) as inputData:
        masterTrainerData = json.load(inputData)

    masterTrainerData = sorted(masterTrainerData , key=lambda item: item["date"])

    # Extract the features and labels from the data
    features = []
    labels = []

    polarityList = []
    subjectivityList = []

    for today, nextDay in zip(masterTrainerData, masterTrainerData[1:]):
        for stock, stockNextDay in zip(today["stocks"], nextDay["stocks"]):
            
            stockData = stock["stock"]
            stockNextDayData = stockNextDay["stock"]
            
            ticker = stockData["ticker"]

            openPrice = float(stockData["open"])
            closePrice = float(stockData["close"] / stockData["open"])
            highPrice = float(stockData["high"] / stockData["open"])
            lowPrice = float(stockData["low"] / stockData["open"])

            tommorowChange = float(stockNextDayData["close"] / stockData["close"])
            
            # Filter tweets for the current ticker
            tweets = [tweet["tweet"] for tweet in today["tweets"] if tweet["tweet"]["ticker"] == ticker]

            # Calculate average polarity and subjectivity
            polarity = float(np.mean([tweet["polarity"] for tweet in tweets]))
            subjectivity = float(np.mean([tweet["subjectivity"] for tweet in tweets]))

            if math.isnan(polarity) or math.isnan(subjectivity):
                polarity = float(sum(polarityList)) / float(len(polarityList))
                subjectivity =  float(sum(subjectivityList)) / float(len(subjectivityList))
            else:
                polarityList.append(polarity)
                subjectivityList.append(subjectivity)

            features.append([closePrice, highPrice, lowPrice, polarity, subjectivity])
            labels.append(tommorowChange)

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
        tf.keras.layers.Dense(64, activation='relu', input_shape=(5,)),
        tf.keras.layers.Dense(1)
    ])

    # Compile the model
    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.0001), loss='mean_squared_error')

    # Train the model
    model.fit(train_features, train_labels, epochs=100, batch_size=32)

    # Evaluate the model
    mse = model.evaluate(test_features, test_labels)
    print("Mean Squared Error:", mse)

    model.save(modelFilePath)