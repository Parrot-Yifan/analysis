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
title_lock = threading.Lock() # Initialize threading lock for title.
MAX_WORKERS = 3  # Set the maximum number of threads in the thread pool here.


def url_analysis_function(supabase):

    """
    Main URL analysis function which handles main logic.
    """

    try:
        all_google_rss_entries = []

        # Retrieve DB data.
        db_data = retrieve_DB_data(supabase)
        company_names = db_data["company_names"] #Include alias names too.
        news_sites = db_data["news_sites"]

        # Fetch news articles (from Google News), querying each company.

        for company_entry in company_names:
            for company_name in company_entry['names']:  # Iterate through each name in the list.
                for site in news_sites:
                    query_term = f"{company_name} {site}"  # Concatenate company and site into a single query term.

                    google_rss = url_fetch_googlerss(query_term)

                    # Extract the relevant data needed.
                    google_rss_entries = extract_google_data(google_rss)

                    google_rss_entries = valid_check(google_rss_entries, site)

                    all_google_rss_entries.extend(google_rss_entries)

        all_google_rss_entries.sort(
            key=lambda x: x["pub_date"], reverse=False
        )  # Sort the entries from oldest to newest.

        # all_google_rss_entries = [{'title': 'How much energy will new semiconductor factories burn through in the US? - The Verge', 'url': 'https://www.theverge.com/2024/3/6/24091367/semiconductor-manufacturing-us-electricity-consumption-renewable-energy-report', 'source_url': 'https://www.theverge.com', 'pub_date': '2024-03-06T13:00:00+00:00'}, {'title': "Microsoft engineer warns company's AI tool creates violent, sexual images, ignores copyrights - CNBC", 'url': 'https://www.cnbc.com/2024/03/06/microsoft-ai-engineer-says-copilot-designer-creates-disturbing-images.html', 'source_url': 'https://www.cnbc.com', 'pub_date': '2024-03-06T13:30:01+00:00'}]
        # all_google_rss_entries = [{'title': "Google's Gemini debacle a make-or-break moment, analyst says - Fox Business", 'url': 'https://www.foxbusiness.com/markets/googles-gemini-debacle-make-break-moment-analyst', 'source_url': 'https://www.foxbusiness.com', 'pub_date': '2024-03-06T20:36:00+00:00'}]
        print(all_google_rss_entries)

        # Process each filtered entry concurrently using ThreadPoolExecutor.
        with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:

            # Create a dictionary of futures, where each future corresponds to processing an entry with the 'process_entry' function.
            futures = {
                executor.submit(process_entry, entry, company_names, supabase): entry
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


def process_entry(entry, company_names, supabase):

    """
    Processes each filtered entry.
    """

    # Extract relevant information from each entry.
    title = entry["title"]
    url = entry["url"]
    source_url = entry["source_url"]
    news_date = entry["pub_date"]

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
        handle_article(title, url, source_url, news_date, company_names, supabase)


def handle_article(title, url, source_url, news_date, company_names, supabase):

    """
    Processes each article's information.
    """

    # Scrape each URL for the main article content.
    scrape_result = scrape(url, source_url)

    if scrape_result:

        # Store the article body here.
        body = scrape_result["body"]

        # Format the body into the appropriate format.
        body = format_body(body)

        # Gather all the mentioned companies in the article, including aliases. 
        # mentioned_companies = [
        #     company_name 
        #     for company_entry in company_names 
        #     for company_name in company_entry['names'] 
        #     if f'{company_name}' in body
        # ]

        mentioned_companies = [
            company_entry['names']
            for company_entry in company_names
            if any(company_name in body for company_name in company_entry['names'])
        ]

        #If there are no mentioned companies, find a way to exit and move onto the next URL.
        if not mentioned_companies:
            print(f"No mentioned companies in the article at URL: {url}. Skipping.")
            return

        # Summarize the article body.
        summary = summarize_text(body)
        sentences = sent_tokenize(body)
        sentiment_score = sentiment_analysis_article(sentences)

        # Retrieve the current date-time with the time-zone.
        current_datetime = (
            datetime.now(timezone.utc).replace(tzinfo=timezone.utc).isoformat()
        )

        # Insert the main article information into the 'news' table of the DB.
        insert_news(current_datetime, title, news_date, url, body, source_url, summary, sentiment_score, supabase)

        # Initialise a set of unique modified sentences that mention all companies.
        total_modified_sentences = set()

        for company in mentioned_companies:
            # For each company, gather relevant sentences about it in the article.
            relevant_sentences = get_relevant_sentences(body, company)

            if relevant_sentences:
                # Perform sentiment analysis on these sentences for the specific company.
                average_score, modified_sentences = sentiment_analysis_company(
                    relevant_sentences, supabase
                )

                # Update the set with the modified sentences for the company.
                total_modified_sentences.update(modified_sentences)

                # Insert the entry into the 'company_news' table in the DB.
                insert_company_news(url, company, average_score, supabase)

        # Modify the body with the modified sentences.
        body = modify_body(body, list(total_modified_sentences))

        # Update the relevant 'news' table entry with this body, using the URL as an indentifier.
        update_text(url, body, supabase)


def get_relevant_sentences(text, target_companies):
    """
    Takes an article's text and a list of company names and returns all sentences in the article that mention any of those companies.
    """
    
    # Use NLTK to split the entire text into sentences.
    sentences = sent_tokenize(text)

    # Iterate over each sentence and remove "\n" characters.
    cleaned_sentences = [sentence.replace("\n", " ") for sentence in sentences]

    # # Gather sentences that mention any of the target companies. Include aliases!
    # relevant_sentences = [
    #     sentence.strip()
    #     for sentence in cleaned_sentences
    #     for company_name in target_companies
    #     if company_name in sentence
    # ]

    # print(relevant_sentences)
    # return relevant_sentences

    # Use a set to gather unique sentences that mention any of the target companies. Include aliases!
    relevant_sentences_set = {
        sentence.strip()
        for sentence in cleaned_sentences
        for company_name in target_companies
        if company_name in sentence
    }

    # Convert the set back to a list if you need to maintain some form of order or work with the list type
    relevant_sentences = list(relevant_sentences_set)

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
    # print("Modified")
    # print(modified_sentences)

   # Iterate through each modified sentence
    for modified in modified_sentences:
        # Check if the original sentence is a substring of the modified sentence
        for original in original_sentences:
            cleaned_original = original.replace("\n", " ").strip()
            # cleaned_original = re.sub(r'\n+', ' ', original)
            # print(cleaned_original)
            #INVESTIGATE ISSUE OF INCORRECT REPLACEMENTS!

            if cleaned_original in modified:
                # Replace the original sentence with the modified sentence and update body
                body = body.replace(original, modified, 1)
                break
    
    return body

# ============================================================
# END OF PROGRAM
# ============================================================
