# Stock Price Prediction program

This Python program leverages the power of Facebook Prophet to predict stock prices 5 minutes into the future. It uses Yfinance to retrieve historical market data and then applies Prophet's time series forecasting capabilities to make informed predictions.

## Key Features

-   Future-Looking Insights: Predict stock prices for various companies with a 5-minute time horizon.
-   Data-Driven Decisions: Integrate with your workflow by storing and managing the analysed data using the included database interaction module (configuration required).

## Program Structure

For improved maintainability and readability, the program is modularised into several Python scripts:

-   Main Program (main.py): The central hub, orchestrating the entire process by calling subprograms for prediction and data management at regular intervals (default: 5 minutes).
-   Stock Price Prediction (stock_prediction.py): Employs Prophet to forecast future stock prices using historical data obtained from Yfinance.
-   Database Interaction Module (db_interaction.py): Provides methods for interacting with a database, allowing you to store and manage the predicted values (requires separate configuration).

Note: This program uses external libraries including `supabase`, `pandas`, `yfinance` and `prophet`. Install the latest versions for all.

## Usage Instructions

1.  Prerequisites:

    -   Python version 3.10 or later
    -   Installation of required libraries:

        Bash

        ```
        pip install supabase pandas yfinance prophet    
        ```

2.  Running the Program:

    -   Clone the repository from GitHub.
    -   Run the main program using:

        Bash

        ```
        python main.py
        ```

3.  Customisation:

    -   Modify the configuration within `db_interaction.py` to connect to your preferred database for storing predicted data (optional).
