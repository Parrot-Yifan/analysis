import requests  # Import requests for making HTTP requests
from requests.exceptions import RequestException
import re  # Import re for regular expressions
from datetime import datetime, timezone  # Import datetime for handling date and time

# ============================================================
# START OF PROGRAM
# ============================================================

TIME_WINDOW = 26000

def url_fetch_googlerss(query_term):

    """
    Fetch recent news from the Google News RSS Feed for a specific company and news site.
    """

    # Initialize the variable with a default value.
    fetched_url = ""

    # Generate the URL with a keyword search for a specific company.
    url = "https://news.google.com/rss/search?q={}+when:1y&hl=en-GB&gl=GB&ceid=GB:en&orderby=published".format(
        query_term
    )

    try:
        # Make an HTTP GET request to the generated URL.
        # response = requests.get(url)
        response = requests.get(url)

        # Check if the request was successful (status code 200).
        if response.status_code == 200:

            # Convert the response into string.
            fetched_url = response.text
        else:

            # Print an error message if the request was unsuccessful.
            print(
                f"Error: Unable to fetch the web page. Status code: {response.status_code}"
            )
    except RequestException as e:
        # Handle connection-related exceptions.
        print(f"An error occurred during the request: {e}")

    # Return the fetched URL content.
    return fetched_url


def extract_google_data(fetched_url):

    """
    Method to get relevant data from the Google News API.
    """
    result = []  # Initialize an empty list to store extracted data.

    # Use regular expressions to find all occurrences of '<item>' tags in the fetched URL.
    items = re.findall(r"<item>(.*?)</item>", fetched_url, re.DOTALL)

    # Iterate through each '<item>' found in the fetched content.
    for item in items:

        # Use regular expressions to extract data (title, link, source URL, and publication date) from each '<item>'.
        title_match = re.search(r"<title>(.*?)</title>", item)
        link_match = re.search(r"<link>(.*?)</link>", item)
        source_match = re.search(r'<source url="(.*?)">', item)
        pub_date_match = re.search(r"<pubDate>(.*?)</pubDate>", item)

        # Check if all required data is found.
        if title_match and link_match and source_match and pub_date_match:

            # Extract data from the regex matches.
            title = title_match.group(1)
            link = link_match.group(1)
            source_url = source_match.group(1)
            pub_date_str = pub_date_match.group(1)

            # Convert the input string to a datetime object.
            input_datetime = datetime.strptime(pub_date_str, "%a, %d %b %Y %H:%M:%S %Z")

            # Convert the datetime object to the desired format (UTC ISO 8601 format).
            output_datetime_str = input_datetime.replace(
                tzinfo=timezone.utc
            ).isoformat()

            # Create a dictionary with extracted data and append it to the result list.
            data = {
                "title": title,
                "url": link, # Use the final URL after following the redirection.
                "source_url": source_url,
                "pub_date": output_datetime_str,
            }
            result.append(data)

    # Return the list of extracted data.
    return result

def valid_check(entries, site):

    """
    Check if the entries are valid, by filtering out news articles that aren't in the list of news_sites.
    Also filter out articles that are within 5 minutes from the time now.
    """

    valid_entries = []  # Initialize an empty list to store valid entries.

    # Get the current time.
    current_time = datetime.now(timezone.utc)
    
    # Iterate through each entry in the provided list of entries.
    for entry in entries:

        source_url = entry.get("source_url", "")  # Get the source URL from the entry.
        pub_date_str = entry.get("pub_date", "")  # Get the publication date string from the entry.
        
        # Convert the publication date string to a datetime object.
        pub_date = pub_date = datetime.strptime(pub_date_str, "%Y-%m-%dT%H:%M:%S%z")

        # Calculate the time difference between the current time and the publication date.
        time_difference = current_time - pub_date

        # Check if the specified news sites is  present in the source URL and if the site is published within 5 minutes of the time now.
        if site.lower() in source_url and time_difference.total_seconds() <= TIME_WINDOW:
        # if site.lower() in source_url and time_difference.days <= 0.2:
            
            # If the source URL contains any of the specified news sites, consider it a valid entry.
            # Fetch the final URL after following any redirections.
            response = requests.head(entry["url"], allow_redirects=True)
            final_url = response.url
            
            # Update the url in the entry with the final_url.
            entry["url"] = final_url
            print(final_url)

            # If the source URL contains any of the specified news sites, consider it a valid entry.
            valid_entries.append(entry)

    # Return the list of valid entries.
    return valid_entries


# ============================================================
# END OF PROGRAM
# ============================================================
