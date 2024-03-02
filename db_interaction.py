from supabase import (
    create_client,
    Client,
)  # Import Supabase client for interacting with the Supabase database

# ============================================================
# START OF PROGRAM
# ============================================================

# Makes the connection to the Supabase client.
SUPABASE_URL = "https://irendefjtnvixqkiehya.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImlyZW5kZWZqdG52aXhxa2llaHlhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MDUwNzcxNTUsImV4cCI6MjAyMDY1MzE1NX0.IaTi8UJP4JCcjP35RUNu2gLE3qd_CzQcHgy2y3UTaew"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def retrieve_DB_data():

    '''
    Retrieves all the company names and news source names from the database.
    '''
    
    # Authenticate with Supabase using email and password.
    authentication = supabase.auth.sign_in_with_password({"email": "tudor0404@gmail.com", "password": "test123"})

    # Get lists of company names and news site names from the database.
    company_names = get_company_names()
    news_sites = get_news_sites()

    # Create a dictionary to store the retrieved data.
    data_dict = {
        "company_names": company_names,
        "news_sites": news_sites
    }

    # Sign out from Supabase authentication.
    supabase.auth.sign_out()

    # Return the dictionary containing company names and news site names.
    return data_dict

def get_company_names():

    '''
    Gets all the company names from the database.
    '''

    # Retrieve data from the "company" table in the database, selecting only the "name" column.
    data = supabase.table("company").select("name").execute()

    # Extract company names from the retrieved data.
    company_names = [company['name'] for company in data.data]

    # Return the list of company names.
    return company_names


def get_news_sites():

    '''
    Gets all the news site names from the database.
    '''

    # Retrieve data from the "news_site" table in the database, selecting only the "url" column.
    data = supabase.table("news_site").select("url").execute()

    # Extract news site names from the retrieved data.
    news_site_names = [news_site['url'].rstrip('\n') for news_site in data.data]

    # Return the list of news site names.
    return news_site_names


def insert_news(current_datetime, title, news_date, url, body, source_url, summary, sentiment_score):
    
    '''
    Inserts an entry into the 'news' table.
    '''

    # Authenticate with Supabase using email and password.
    authentication = supabase.auth.sign_in_with_password({"email": "tudor0404@gmail.com", "password": "test123"})

    print(f"Inserting article: {title} from {source_url}")

    # Remove "https://" from the start of the source URL.
    source_url = source_url.lstrip("https://")

    # Retrieve news_site_id using the source URL.
    news_site_id_query = supabase.table('news_site').select('id').eq('url', source_url).execute()

    # Assuming only one entry should match the condition.
    if len(news_site_id_query.data) == 1:
        news_site_id = news_site_id_query.data[0]['id']

        # Insert news entry into the 'news' table.
        data, count = supabase.table('news').insert({
            "created": current_datetime,
            "title": title,
            "published": news_date,
            "url": url,
            "text": body,
            "news_site_id": news_site_id,  # Assuming a default value for news_site_id.
            "summary": summary,
            "overall_sentiment": sentiment_score
        }).execute()

    # Sign out from Supabase authentication.
    supabase.auth.sign_out()


def insert_company_news(url, company, average_score):

    '''
    Inserts an entry into the company_news table.
    '''

    # Authenticate with Supabase using email and password.
    authentication = supabase.auth.sign_in_with_password({"email": "tudor0404@gmail.com", "password": "test123"})
    print(f"Inserting company news: {company} = {average_score}")

    # Retrieve news_id using the news URL.
    news_id_query = supabase.table('news').select('id').eq('url', url).execute()

    # Retrieve company_id using the company name.
    company_id_query = supabase.table('company').select('id').eq('name', company).execute()

    # Assuming only one entry should match each condition.
    if len(news_id_query.data) == 1 and len(company_id_query.data) == 1:
        news_id = news_id_query.data[0]['id']
        company_id = company_id_query.data[0]['id']

        # Insert company_news entry into the 'company_news' table.
        data, count = supabase.table('company_news').insert({
            "news_id": news_id,
            "company_id": company_id,
            "public_impact": average_score
        }).execute()

    # Sign out from Supabase authentication.
    supabase.auth.sign_out()

def update_text(url, body):

    '''
    Updates the 'text' field of the relevant entry (using the URL as an identifier) in the 'news' table of the database.
    '''
    
    # Authenticate with Supabase using email and password.
    authentication = supabase.auth.sign_in_with_password({"email": "tudor0404@gmail.com", "password": "test123"})

    # Retrieve news_id using the news URL.

    news_id_query = supabase.table('news').select('id').eq('url', url).execute()

    # Assuming only one entry should match the condition.
    if len(news_id_query.data) == 1:
        news_id = news_id_query.data[0]['id']
        # Update the 'text' field of the relevant news entry in the 'news' table.
        data, count = supabase.table('news').update({"text": body}).eq('id', news_id).execute()

    # Sign out from Supabase authentication.
    supabase.auth.sign_out()

def get_tickers(mentioned_companies):

    '''
    Given a list of companies, it converts the list into a list of tickers.
    '''

    # Authenticate with Supabase using email and password.
    authentication = supabase.auth.sign_in_with_password({"email": "tudor0404@gmail.com", "password": "test123"})
    tickers = []

    # Retrieve ticker using the company name.
    for company in mentioned_companies:
        ticker_name_query = supabase.table('company').select('ticker').eq('name', company).execute()

         # Extract the 'ticker' value from the dictionary and append it to the tickers list.
        if ticker_name_query.data:
            ticker_value = ticker_name_query.data[0]['ticker']
            tickers.append(ticker_value)

    # Sign out from Supabase authentication.
    supabase.auth.sign_out()

    return tickers

def get_news_source_name(source_url):
    
    '''
    Given a source URL, find its source name.
    '''

    # Authenticate with Supabase using email and password.
    authentication = supabase.auth.sign_in_with_password({"email": "tudor0404@gmail.com", "password": "test123"})

    news_source_name_query = supabase.table('news_site').select('name').eq('url', source_url).execute()

    if len(news_source_name_query.data) == 1:
    
        # Sign out from Supabase authentication.
        supabase.auth.sign_out()

        return news_source_name_query.data[0]['name']

    supabase.auth.sign_out()

    return None

# ============================================================
# END OF PROGRAM
# ============================================================