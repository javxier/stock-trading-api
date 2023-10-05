# CPSC-362 - Automated ETF Trading System

Welcome to the CPSC-362 project. In this venture, we aim to develop an automated trading system tailored to handle two particular Exchange-Traded Funds (ETFs): **FNGU** and **FNGD**. These ETFs are exciting due to their high volatility brought about by their 3x leverage. 

The main holdings of these ETFs are primarily the FANG companies, along with others like META (Facebook), AMZN, AAPL, NFLX, GOOGL, MSFT, TSLA, NVDA, AMD, and SNOW. The interesting aspect is the inverse relationship between FNGU and FNGD: if most holdings rise, FNGU goes up while FNGD drops, and vice versa. This correlation allows for profitable buying and selling actions based on any market direction without short-selling.

## Project Features

Our trading system targets to provide:

1. **Data Management:** Fetch and store the historical data for FNGU and FNGD, spanning from 01/01/2020 till yesterday. Any data source can be used for this purpose, such as Yahoo Finance. The stored data should include Date, Open, High, Low, Close, and Volume details. It will be kept in a JSON format locally. Please note that the data source may be subject to change in the future.

2. **User Interface:** We need to develop an intuitive GUI or command-line interface that allows users to view the stored data. This feature should also enable drawing a graph for a chosen symbol (FNGU or FNGD) over a specific date range.

3. **Trading Strategies:** The system should implement at least two trading strategies: the Moving Average Cross-over and the Bollinger Band Bounce. However, creativity is welcomed - feel free to add or merge different strategies to optimize returns.

4. **Backtesting & Performance Evaluation:** We'll start with an initial trading account balance of $100,000. Your task involves implementing a basic backtesting method to compute the total gain or loss from each trade over the chosen period. The system should then display the final performance of each trading strategy in terms of total $ return and % return. For simplicity, we'll assume a zero trading fee.

Do note, these requirements may change as we progress through the project lifecycle. You can expect multiple assignments geared towards the successful completion of this project.

## Recommended Tools

Although we recommend Python or JavaScript (TypeScript) for this project, you're free to choose the programming language that you're most comfortable with.

Enjoy trading!
