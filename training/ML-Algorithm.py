import pandas as pd
import numpy as np

np.set_printoptions(precision=3, suppress=True)

import tensorflow as tf
from tensorflow.keras import layers

tweets = pd.read_json("stock_tweets_analyzed.json")
stock_info = pd.read_json("")

tweets_features = np.copy(tweets)
abalone_labels = tweets_features.pop('Age')

print(tweets.head())