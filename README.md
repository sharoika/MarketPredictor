## MarketPredictor
A TensorFlow machine learning algorithm using YFinance (yahoo finance) data alongside scraped Twitter data that has been run thru a sentient analyzer (textblob) to attempt to predict stock movements.

## AI Generated Logo
[<img src="https://github.com/sharoika/MarketPredictor/blob/85f43fefb32074d8b13eb722f46238ae54159dfc/logo.jpg" width="300">]

## Installation and Setup Instructions
1. Ensure that you have Python 3 installed on your system.
2. Clone the project repository from GitHub.
3. Navigate to the project directory.
4. Run "pip install -r requirements.txt" in the root directory to install all the dependencies.
5. Create a .env file with the following format (all twitter information):
    - TW_EMAIL=
    - TW_USERNAME=
    - TW_PASSWORD=
7. Once the dependencies are installed successfully and the .env file is created, you are ready to use the project by running "Python3 MarketPredictor.py" in the root directory and following the prompts. [HINT: Use AAPL as the first ticker for testing]

## File Overview
- /MarketPredictionModel
    - The TensorFlow model, this was created an uploaded so people don't need to train their own with my data.
- /analyzed
    - The tweets with sentiment values already attached to them. 
- /finances
    - The financial data the YFinanace provides us. 
- /scraped
    - The raw tweets scraped straight from twitter. 
- /scripts
    - FinanaceScraper.py
        - This is the script that request data from YFinance.
    - SentimentAnalyzer.py
        - This is the script that analyzes the sentiment of the Twitter data.
    - TweetScraper.py
        - This is the script that scrapes tweets off of Twitter.  
- /training
    - MarketTrainer.py
        - This is the script that created, and saves the model; it grabs the existing data in the training folder and also request from YFinanace.
- MarketPredictor.py
    - This is the main drivers of the predictor, this should be the file you call.  
      
## Training Data
- Tweet Dataset:
    - https://www.kaggle.com/datasets/equinxx/stock-tweets-for-sentiment-analysis-and-prediction
- Stock Information Dataset:
    - Grabbed using YFinance for the maximal date range of the Kaggle dataset. 
