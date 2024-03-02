from URL_Analysis.url_fetching import *  # Import functions from url_fetching.py - Fetching URL's
from URL_Analysis.url_scraping import *  # Import functions from url_scraping.py - Scraping URL's

from URL_Analysis.text_summarization import *  # Import functions from text_summarization.py - Summarization
from URL_Analysis.text_sentiment_analysis import *  # Import functions from text_sentiment_analysis.py - Sentiment Analysis

from db_interaction import *  # Import functions from db_interaction.py - Interacting with the DB

from datetime import datetime, timezone  # Import datetime.
from collections import deque  # Import a double ended queue for cache.

import threading, concurrent.futures  # Import threading/thread pooling.
import sys #Import sys module for system-specific parameters and functions.
import re # Import regular expressions for string searching.
import signal #Import signal module for signal handling in the program.

import nltk
nltk.download('punkt')  # Download the Punkt tokenizer models

from nltk.tokenize import sent_tokenize

# ============================================================
# START OF PROGRAM
# ============================================================

url_cache = deque(maxlen=100)  # Initiliaze a 100 URL length cache.
url_cache_lock = threading.Lock()  # Set a thread lock for this shared structure.
title_lock = threading.Lock()
MAX_WORKERS = 3  # Set the maximum number of threads in the thread pool here.


def url_analysis_function():

    """
    Main URL analysis function which handles main logic.
    """

    try:
        all_google_rss_entries = []

        # Retrieve DB data.
        db_data = retrieve_DB_data()
        company_names = db_data["company_names"]
        news_sites = db_data["news_sites"]

        # Fetch news articles (from Google News), querying each company.

        for company in company_names:
            for site in news_sites:
                query_term = f"{company} {site}"  # Concatenate company and site into a single query term.
                google_rss = url_fetch_googlerss(query_term)

                # Extract the relevant data needed.
                google_rss_entries = extract_google_data(google_rss)

                google_rss_entries = valid_check(google_rss_entries, site)

                all_google_rss_entries.extend(google_rss_entries)

        all_google_rss_entries.sort(
            key=lambda x: x["pub_date"], reverse=False
        )  # Sort the entries from oldest to newest.

        print(all_google_rss_entries)

        # Process each filtered entry concurrently using ThreadPoolExecutor.
        with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:

            # Create a dictionary of futures, where each future corresponds to processing an entry with the 'process_entry' function.
            futures = {
                executor.submit(process_entry, entry, company_names, ): entry
                for entry in all_google_rss_entries
            }

            # Install a signal handler for Ctrl+C
            signal.signal(signal.SIGINT, signal_handler)

            try:
                # Iterate through completed futures as they finish execution.
                for future in concurrent.futures.as_completed(futures):
                    try:

                        # Retrieve and propagate the result to handle any exceptions raised during entry processing.
                        future.result()  # Retrieve the result to propagate exceptions.

                    except Exception as e:

                        # Handle exceptions raised during processing (e.g., log, notify, or take appropriate action).
                        print(f"Error processing entry: {e}")

            except KeyboardInterrupt:

                print("\nCtrl+C detected. Cancelling remaining tasks...")

                for future in futures:
                    future.cancel()

                # Wait for tasks to be cancelled.
                concurrent.futures.wait(futures)

                print("Remaining tasks cancelled.")

                sys.exit(0)

    except KeyboardInterrupt:

        print("\nProgram terminated by user.")

        # Exiting the program after Ctrl+C.
        sys.exit(0)


def signal_handler(sig, frame):

    """
    Signal handler function for Ctrl+C.
    """

    print("\nCtrl+C detected. Stopping the program...")

    # Exiting the program after Ctrl+C.
    sys.exit(0)


def process_entry(entry, company_names, ):

    """
    Processes each filtered entry.
    """

    # Extract relevant information from each entry.
    title = entry["title"]
    url = entry["url"]
    source_url = entry["source_url"]
    news_date = entry["pub_date"]

    #Modify the title to not include the news source if it exists.
    title = modify_title(title, source_url)

    # Convert URL to lower case for comparison.
    url_lower = url.lower()

    # Use a lock to ensure thread-safe access to the URL cache.
    with url_cache_lock:

        # Check if URL already exists in cache to avoid redundant processing.
        if url_lower in (cached_url.lower() for cached_url in url_cache):
            print(f"URL {url} already processed. Skipping.")
            return

        # Add URl to cache to mark it as having been processed.
        url_cache.append(url)

        # Analyze the article content.
        handle_article(title, url, source_url, news_date, company_names)


def handle_article(title, url, source_url, news_date, company_names):

    """
    Processes each article's information.
    """

    # #Remove https://www. from the beginning.
    # source_url = source_url.replace("https://www.", "")

    # Scrape each URL for the main article content.
    scrape_result = scrape(url, source_url)

    if scrape_result:

        # Store the article body here.
        body = scrape_result["body"]

        # Format the body into the appropriate format.
        body = format_body(body)

        # Summarize the article body.
        summary = summarize_text(body)

        #Conduct sentiment analysis on the entire article.
        # sentences = re.split(r"(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.)\s*(?=\S)", body)

        sentences = sent_tokenize(body)
        sentiment_score = sentiment_analysis_article(sentences)

        # Retrieve the current date-time with the time-zone.
        current_datetime = (
            datetime.now(timezone.utc).replace(tzinfo=timezone.utc).isoformat()
        )

        # Insert the main article information into the 'news' table of the DB.
        insert_news(current_datetime, title, news_date, url, body, source_url, summary, sentiment_score, )

        # Gather all the mentioned companies in the article.
        mentioned_companies = [
            company for company in company_names if  f' {company}' in body #MODIFIED TO ENSURE CORRECT COMPANY SEARCH!
        ]


        # Initialise a set of unique modified sentences that mention all companies.
        total_modified_sentences = set()

        for company in mentioned_companies:
            # For each company, gather relevant sentences about it in the article.
            relevant_sentences = get_relevant_sentences(body, company)
            
            
            if relevant_sentences:
                # Perform sentiment analysis on these sentences for the specific company.
                average_score, modified_sentences = sentiment_analysis_company(
                    relevant_sentences, 
                )

                # Update the set with the modified sentences for the company.
                total_modified_sentences.update(modified_sentences)

                # Insert the entry into the 'company_news' table in the DB.

                insert_company_news(url, company, average_score, )

        # Modify the body with the modified sentences.
        body = modify_body(body, list(total_modified_sentences))

        # Update the relevant 'news' table entry with this body, using the URL as an indentifier.
        update_text(url, body, )


def get_relevant_sentences(text, target_company):
    """
    Takes an article's text and a company name and returns all sentences in the article that mention that company.
    """
    
    # Use NLTK to split the entire text into sentences.
    sentences = sent_tokenize(text)

    # # Iterate over each sentence and remove "\n" characters.
    cleaned_sentences = [sentence.replace("\n", " ") for sentence in sentences]

    # Gather sentences that mention the target company.
    relevant_sentences = [
        sentence.strip()
        for sentence in cleaned_sentences 
        if target_company.lower() in sentence.lower()
    ]

    print(relevant_sentences)
    return relevant_sentences


def format_body(body):

    '''
    Formats the body into the desired format (by removing 'In this article').
    '''

    # Remove the starting phrase "In this article" if it exists.
    body = body.replace("In this article", "").lstrip()
    return body

def modify_body(body, modified_sentences):

    """
    Modifies the article body using the list of modified sentences.
    """

    # Split the body into sentences
    original_sentences = sent_tokenize(body)
    
   # Iterate through each modified sentence
    for modified in modified_sentences:
        # Check if the original sentence is a substring of the modified sentence
        for original in original_sentences:
            
            cleaned_original = original.replace("\n", " ")

            if cleaned_original in modified:
                # Replace the original sentence with the modified sentence and update body
                body = body.replace(original, modified, 1)
                break
    
    return body


def modify_title(title, source_url, ):

    '''
    Modifies the news headline to remove the news source if it is present.
    '''

    # Strip "https://" from the front of the source_url
    source_url = source_url.replace("https://", "")
    source_name = get_news_source_name(source_url, )

    domain = source_name

    # Check if the domain is present in the title
    if domain and domain.lower() in title.lower():

        # Remove the domain and any characters before it
        index = title.lower().find(domain.lower())
        if index != -1:
            title = title[:index] + title[index + len(domain):]

        # Remove any leading or trailing dashes or spaces
        title = title.strip("- ")

    return title.strip()

# ============================================================
# END OF PROGRAM
# ============================================================