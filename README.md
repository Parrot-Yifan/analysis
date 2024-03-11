# Stock Price Prediction program

This Python program performs stock price predictions 5 minutes into the future for companies using data from Yfinance and time series forecasting using Prophet API. 

## Key Features

-   Stock Price Prediction: Predicts stock prices of companies 5 minutes into the future.
-   Database Interaction: Provides methods for interacting with a database to store and manage the analysed data.

## Program Structure

The program is modularized into several Python scripts for improved maintainability and readability:

1.  Main Program (main.py): Orchestrates the overall workflow by calling subprograms for URL analysis at regular intervals (default: 5 minutes).
2.  Stock Price Prediction (stock_prediction.py): Predicts future stock price of companies using Prophet API.
3.  Database Interaction Module (db_interaction.py): Provides methods for database interactions (configuration required for specific usage).

Note: This program uses external libraries including `supabase`, `BeautifulSoup4` (`bs4`), `html2text`, `requests`, and `textwrap`.

## Usage Instructions

1.  Prerequisites:

    -   Python version 3.10 or later
    -   Installation of required libraries:

        Bash

        ```
        pip install supabase    
        ```

2.  Running the Program:

    -   Clone the repository from GitHub.
    -   Run the main program using:

        Bash

        ```
        python main.py
        ```
