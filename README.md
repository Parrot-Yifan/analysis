# URL Analysis program

This Python program performs comprehensive analysis of URLs related to companies and news sources. It uses various functionalities to extract and analyse relevant information from the web.

## Key Features

-   URL Fetching: Retrieves relevant URLs based on company and news source, ensuring they are recently published (within a customizable time window).
-   URL Scraping: Extracts the main body of the article content from the scraped webpage.
-   URL Sentiment Analysis: Analyses the overall sentiment of the article and identifies sentiment towards specific companies mentioned within the text.
-   URL Summarization: Creates a concise summary of the extracted article content.
-   Database Interaction: Provides methods for interacting with a database to store and manage the analysed data.

## Program Structure

The program is modularized into several Python scripts for improved maintainability and readability:

1.  Main Program (main.py): Orchestrates the overall workflow by calling subprograms for URL analysis at regular intervals (default: 5 minutes).
2.  URL Fetching Program (url_fetching.py): Fetches URLs based on predefined criteria and validates their publication time.
3.  URL Scraping Program (url_scraping.py): Extracts the relevant article body content from the scraped webpage.
4.  URL Analysis Program (url_analysis.py): Handles the core logic of URL analysis, including sentiment analysis and summarization.
5.  Database Interaction Module (db_interaction.py): Provides methods for database interactions (configuration required for specific usage).

Note: This program uses external libraries including `supabase`, `BeautifulSoup4` (`bs4`), `html2text`, `requests`, and `textwrap`. Install the latest verions for all.

## Usage Instructions

1.  Prerequisites:

    -   Python version 3.10 or later
    -   Installation of required libraries:

        Bash

        ```
        pip install supabase bs4 html2text requests textwrap
        ```

2.  Running the Program:

    -   Clone the repository from GitHub.
    -   Run the main program using:

        Bash

        ```
        python main.py
        ```

3.  Customization:

    -   Modify the configuration within `db_interaction.py` to connect to your preferred database for storing predicted data (optional).

    -   Modify the `TIME_WINDOW` constant within `url_fetching.py` to adjust the time window for fetching recent articles.

