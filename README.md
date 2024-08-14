## Pairs Trading Model Implementation and Backtesting
This repository offers a detailed implementation of a pairs trading strategy using Python. The project includes various functions and methodologies to identify, analyze, and backtest cointegrated pairs within a dataset of commodities. The models included are:

1. **Pairs Trading Strategy**
   - `PairsTradingMain.ipynb`: Contains the implementation of the built Pairs Trading Strategy.

    This project implements a pairs trading strategy using historical commodities data, with a focus on identifying and exploiting the relationship between two highly correlated assets. The process begins with importing and preparing data from the yfinance library, ensuring that the dataset is clean and free from anomalies such as NaN values. This initial step is crucial, as it ensures that subsequent analyses are based on accurate and reliable data. <br/>

    The core of the strategy involves calculating the spread between two selected commodities. This is done using an Ordinary Least Squares (OLS) regression model, which quantifies the relationship between the two assets. The spread is defined as the residuals from this regression, capturing the deviations from the expected relationship. These deviations are central to the pairs trading strategy, as they represent potential opportunities for profit. <br/>

    To determine whether the spread is suitable for trading, the project employs the Augmented Dickey-Fuller (ADF) test. This test checks for stationarity in the spread, which is a key condition for the pairs trading strategy. A stationary spread indicates that it is mean-reverting, making the pair of assets suitable for trading. This step ensures that only pairs with a statistically valid spread are selected for trading, adding robustness to the strategy. <br/>

    The project then calculates the Z-score of the spread, which standardizes the spread and helps identify potential trading opportunities. The Z-score measures how far the spread is from its mean in terms of standard deviations. Trading signals are generated based on predefined Z-score thresholds, which trigger long or short positions. This systematic approach ensures that trades are made based on quantifiable criteria rather than subjective judgment. <br/>

    Initially, the strategy is rigorously backtested to evaluate its performance over historical data. This backtesting process simulates the strategy in a controlled environment, allowing for an assessment of its potential profitability. The results of the backtesting are visualized, providing a clear view of the strategy's performance over time and helping to identify trends or areas that may require further refinement. The project provides a robust framework for deploying a systematic pairs trading strategy in the commodities markets, grounded in statistical rigor and data-driven decision-making.

   - `GetTestPairs.ipynb`: Contains the project to get the test pairs with statistical refinement.

    This project focuses on identifying cointegrated pairs of commodities from a larger dataset, and filtering them based on statistical significance. The process begins by importing historical price data for a range of commodities and generating all possible unique pairs. Each pair is then tested for cointegration using statistical methods to determine whether a long-term equilibrium relationship exists between them. <br/>

    Only pairs with a p-value of less than 0.05, indicating a strong cointegration, are selected for further analysis. This filtering ensures that the strategy is based on pairs with a statistically significant relationship, increasing the likelihood of successful trades. The project allows us to streamline the approach of handling a larger datasets to identify viable pairs to apply the mean reversion pairs trading strategy to.

   - `StockPairsTradingCHECK.ipynb`: Contains the implementation of an existing python function to test the outputs of my implemented model.

    This project leverages the `stock-pairs-trading` Python package to validate and analyze a pairs trading strategy using our created historical commodity data. The script begins by initializing a StockPairsTrading object, and specifying the time frame over which the data will be analyzed. These pairs filtered in the `GetTestPairs.ipynb` project are then subjected to a backtest, which simulates trading to evaluate the effectiveness of the strategy. The results of the backtest are printed, providing insights into the historical performance of the strategy for the selected pairs. <br/>

    In addition to backtesting, the script also retrieves the latest trading signal for a specific pair, offering a real-time recommendation based on the strategy. This functionality allows for the practical application of the strategy in live trading scenarios, ensuring that the strategy is not only historically sound but also actionable in current market conditions. <br/>

    Citation:
    StockPairsTrading. (n.d.). Stock pairs trading. PyPI. Retrieved August 14, 2024, from https://pypi.org/project/stock-pairs-trading/

2. **Archive**
   - Contains unused/unrefined implementations and non-finished projects


