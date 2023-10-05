import requests
import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from abc import ABC, abstractmethod

def data_decorator(func):
    def wrapper(self, data):
        print("---- Start of Data ----")
        func(self, data)
        print("---- End of Data ----")
    return wrapper

def calculate_moving_average_signals(filename):
    # Load data from json file
    with open(filename, 'r') as f:
        data = json.load(f)

    # Convert the data to pandas DataFrame
    df = pd.DataFrame(data).T
    df.index = pd.to_datetime(df.index)
    df = df.sort_index(ascending=True)

    # Convert the 'close' column to numeric type
    df['close'] = pd.to_numeric(df['close'])

    # Calculate the 5-day moving average
    df['5_day_ma'] = df['close'].rolling(window=5).mean()

    # Calculate the 10-day moving average
    df['10_day_ma'] = df['close'].rolling(window=10).mean()

    # Create an 'order' column to record the "buy" and "sell" signals
    df['order'] = 'N/A'
    # If the 5-day moving average is larger than the 10-day moving average, set order as 'buy'
    df.loc[df['5_day_ma'] > df['10_day_ma'], 'order'] = 'buy'
    # If the 5-day moving average is less than the 10-day moving average, set order as 'sell'
    df.loc[df['5_day_ma'] < df['10_day_ma'], 'order'] = 'sell'
    df['balance'] = 100000.0
    df['stock'] = 0.0

    for i in range(1, len(df)):
        if df.iloc[i]['order'] == 'buy' and df.iloc[i - 1]['balance'] > 0:
            df.loc[df.index[i], 'stock'] = df.iloc[i - 1]['balance'] / df.loc[df.index[i], 'close']
            df.loc[df.index[i], 'balance'] = 0.0
        elif df.iloc[i]['order'] == 'sell' and df.iloc[i - 1]['stock'] > 0:
            df.loc[df.index[i], 'balance'] = df.iloc[i - 1]['stock'] * df.loc[df.index[i], 'close']
            df.loc[df.index[i], 'stock'] = 0.0
        else:
            df.loc[df.index[i], 'balance'] = df.iloc[i - 1]['balance']
            df.loc[df.index[i], 'stock'] = df.iloc[i - 1]['stock']

    # print the DataFrame
    print(df.to_string())
    print()

    # Calculate final portfolio value
    df['portfolio_value'] = df['balance'] + df['stock']*df['close']

    # Get final portfolio value
    final_portfolio_value = df['portfolio_value'].iloc[-1]

    # Display final balance
    print(f"Final Balance in Dollar Amount: ${final_portfolio_value:.2f}")

    # Calculate the percentage gain or loss
    percentage_change = ((final_portfolio_value - 100000) / 100000) * 100
    print(f"Percentage Change in Balance: {percentage_change:.2f}%")

    print()

def bollinger_bands_strategy(json_file_path):
    # Load data from json file
    with open(json_file_path, 'r') as f:
        data = json.load(f)

    # Convert the data to pandas DataFrame
    df = pd.DataFrame(data).T
    df.index = pd.to_datetime(df.index)
    df = df.sort_index(ascending=True)

    # Convert the 'close' column to numeric type
    df['close'] = pd.to_numeric(df['close'])

    # Calculate the 20-day moving average
    df['20_day_ma'] = df['close'].rolling(window=20).mean()

    # Calculate the standard deviation for Bollinger Bands
    df['std'] = df['close'].rolling(window=20).std()

    # Calculate upper and lower Bollinger Bands
    df['upper_band'] = df['20_day_ma'] + 2 * df['std']
    df['lower_band'] = df['20_day_ma'] - 2 * df['std']

    # Create an 'order' column to record the "buy" and "sell" signals based on Bollinger Band Bounce strategy
    df['order'] = 'N/A'
    # If the closing price crosses above the upper Bollinger Band, set order as 'sell'
    df.loc[df['close'] > df['upper_band'], 'order'] = 'sell'
    # If the closing price crosses below the lower Bollinger Band, set order as 'buy'
    df.loc[df['close'] < df['lower_band'], 'order'] = 'buy'
    # Create 'balance' column and initialize it with a balance of $100,000
    df['balance'] = 100000.0
    # Create 'stock' column to store the number of stocks bought
    df['stock'] = 0.0

    for i in range(1, len(df)):
        if df.iloc[i]['order'] == 'buy' and df.iloc[i - 1]['balance'] > 0:
            df.loc[df.index[i], 'stock'] = df.iloc[i - 1]['balance'] / df.loc[df.index[i], 'close']
            df.loc[df.index[i], 'balance'] = 0.0
        elif df.iloc[i]['order'] == 'sell' and df.iloc[i - 1]['stock'] > 0:
            df.loc[df.index[i], 'balance'] = df.iloc[i - 1]['stock'] * df.loc[df.index[i], 'close']
            df.loc[df.index[i], 'stock'] = 0.0
        else:
            df.loc[df.index[i], 'balance'] = df.iloc[i - 1]['balance']
            df.loc[df.index[i], 'stock'] = df.iloc[i - 1]['stock']
    
    print(df.to_string())
    print()

    # Calculate final portfolio value
    df['portfolio_value'] = df['balance'] + df['stock']*df['close']

    # Get final portfolio value
    final_portfolio_value = df['portfolio_value'].iloc[-1]

    # Display final balance
    print(f"Final Balance in Dollar Amount: ${final_portfolio_value:.2f}")

    # Calculate the percentage gain or loss
    percentage_change = ((final_portfolio_value - 100000) / 100000) * 100
    print(f"Percentage Change in Balance: {percentage_change:.2f}%")

    print()

def plot_closing_prices(json_file_path):
    # read the JSON file
    with open(json_file_path) as f:
        data = json.load(f)

    # turn the dictionary into a DataFrame with dates as index
    df = pd.DataFrame.from_dict(data, orient='index')

    # convert index to datetime
    df.index = pd.to_datetime(df.index)

    # convert closing prices to float
    df['close'] = df['close'].astype(float)

    # plot the data
    plt.figure(figsize=(10,6))
    plt.scatter(df.index, df['close'])
    plt.xlabel('Date')
    plt.ylabel('Closing Price')
    plt.ylim([0, 100])
    start, end = plt.ylim()  
    stepsize = 5.0  
    plt.yticks(np.arange(start, end, stepsize))
    plt.xticks(rotation = 45)
    plt.title('Closing Stock Prices Over Time')
    plt.show()

    print()

class StockDataModel:
    API_KEY = '1JA77LS8UJHMNV19'

    def __init__(self):
        self.symbol = None
        self.start_date = None
        self.end_date = None

    def set_data(self, symbol, start_date, end_date):
        self.symbol = symbol
        self.start_date = start_date
        self.end_date = end_date

    def download_stock_data(self):
        if not self.symbol or not self.start_date or not self.end_date:
            raise ValueError("Missing symbol, start date, or end date.")
        
        base_url = 'https://www.alphavantage.co/query'
        url_params = {
            'function': 'TIME_SERIES_DAILY',
            'outputsize': 'full',
            'symbol': self.symbol,
            'apikey': self.API_KEY
        }

        response = requests.get(base_url, params=url_params)
        if response.status_code == 200:
            data = response.json()
            daily_prices = data['Time Series (Daily)']

            filtered_data = {}
            for date, values in daily_prices.items():
                if self.start_date <= date <= self.end_date:
                    filtered_data[date] = {
                        'open': values['1. open'],
                        'high': values['2. high'],
                        'low': values['3. low'],
                        'close': values['4. close'],
                        'volume': values['5. volume']
                    }

            return filtered_data
        else:
            print(f"Error fetching data: {response.status_code}")
            return None

    def save_data_as_json(self, data, filename):
        with open(filename, 'w') as file:
            json.dump(data, file)

    def load_data_from_json(self, filename):
        try:
            with open(filename, 'r') as file:
                data = json.load(file)
                return data
        except FileNotFoundError:
            return None
        except json.JSONDecodeError:
            return None


class StockDataView:
    @data_decorator
    def display_data(self, data):
        if data:
            print("Data:")
            for date, values in data.items():
                print(f"Date: {date}")
                print(f"Open: {values['open']}")
                print(f"High: {values['high']}")
                print(f"Low: {values['low']}")
                print(f"Close: {values['close']}")
                print(f"Volume: {values['volume']}")
                print("-" * 20)
        else:
            print("Data download failed.")

    def get_input(self, prompt):
        return input(prompt)

    def display_message(self, message):
        print(message)

# Adapter pattern implementation

class StockDataAdapter:
    def __init__(self, model):
        self.model = model

    def request_data(self, symbol, start_date, end_date):
        self.model.set_data(symbol, start_date, end_date)
        raw_data = self.model.download_stock_data()
        # Here you can manipulate raw_data if needed
        # to conform to the interface expected by the model
        return raw_data
    
# Strategy pattern implementation

class Strategy(ABC):
    @abstractmethod
    def execute(self, filename):
        pass

class BollingerBandsStrategy(Strategy):
    def execute(self, filename):
        bollinger_bands_strategy(filename)

class MovingAverageCrossoverStrategy(Strategy):
    def execute(self, filename):
        calculate_moving_average_signals(filename)

class StockDataController:
    def __init__(self, model, view, strategy: Strategy):
        self.model = model
        self.view = view
        self.strategy = strategy

    def set_strategy(self, strategy: Strategy):
        self.strategy = strategy

    def run(self):
        symbol = self.view.get_input(f'Enter a ticker symbol (either FNGU or FNGD): ').upper()
        start_date = self.view.get_input(f'Enter a start date (YYYY-MM-DD): ')
        end_date = self.view.get_input(f'Enter an end date (YYYY-MM-DD): ')
        self.model.set_data(symbol, start_date, end_date)

        stock_data = self.model.download_stock_data()

        if stock_data:
            filename = f'{symbol}_stock_data.json'
            self.model.save_data_as_json(stock_data, filename)
            self.view.display_message(f"Data saved as {filename}\n")
        else:
            self.view.display_message("Data download failed.")
            exitPrompt = input('Press enter to exit')
            exit()

        loaded_data = self.model.load_data_from_json(filename)
        displayPrompt = input('Display data stock data from JSON file? (Y/N): ').upper()
        if displayPrompt == 'Y':
            self.view.display_data(loaded_data)
        
        graphPrompt = input('Display graph of data? (Y/N): ').upper()
        if graphPrompt == 'Y':
            plot_closing_prices(filename)

        print('Which of the following strategies would you like to implement?')
        print('1. Bollinger Bounce\n2. Moving Average Crossover')
        strategyPrompt = input('Enter 1 or 2 and press Enter: ')
        if strategyPrompt == '1':
            self.strategy = BollingerBandsStrategy()
        elif strategyPrompt == '2':
            self.strategy = MovingAverageCrossoverStrategy()
        self.strategy.execute(filename)
        otherStrategyPrompt = input('Would you like to see the second strategy (Y/N): ').upper()
        if strategyPrompt == '2':
            self.strategy = BollingerBandsStrategy()
        elif strategyPrompt == '1':
            self.strategy = MovingAverageCrossoverStrategy()
        self.strategy.execute(filename)

        finalExitPrompt = input('Press enter to exit program')


if __name__ == "__main__":
    model = StockDataModel()
    view = StockDataView()
    controller = StockDataController(model, view, Strategy)
    controller.run()
