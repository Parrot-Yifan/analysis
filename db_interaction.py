from supabase import (
    create_client,
    Client
)  # Import Supabase client for interacting with the Supabase database

# ============================================================
# START OF PROGRAM
# ============================================================


def retrieve_DB_data(supabase):

    '''
    Retrieves all the company names and news source names from the database.
    '''
    
    # Get lists of company names and news site names from the database.
    company_names = get_company_names(supabase)
    news_sites = get_news_sites(supabase)

    # Create a dictionary to store the retrieved data.
    data_dict = {
        "company_names": company_names,
        "news_sites": news_sites
    }

    # Return the dictionary containing company names and news site names.
    return data_dict

def get_company_names(supabase):

    '''
    Gets all the company names from the database.
    '''

    # Retrieve data from the "company" table in the database, selecting only the "name" column.
    data = supabase.table("company").select("name, aliases").execute()

    # Extract company names from the retrieved data.
    company_data = []

    for company in data.data:
        company_name = company['name']
        aliases = [alias.strip() for alias in (company['aliases'].split(',') if company['aliases'] and ',' in company['aliases'] else [company['aliases']]) if company['aliases']]
        combined_names = [company_name] + aliases
        company_data.append({'names': combined_names})

    # data = supabase.table("company").select("aliases").execute()

    # Return the list of company names.
    return company_data


def get_news_sites(supabase):

    '''
    Gets all the news site names from the database.
    '''

    # Retrieve data from the "news_site" table in the database, selecting only the "url" column.
    data = supabase.table("news_site").select("url").execute()

    # Extract news site names from the retrieved data.
    news_site_names = [news_site['url'].rstrip('\n') for news_site in data.data]

    # Return the list of news site names.
    return news_site_names


def insert_news(current_datetime, title, news_date, url, body, source_url, summary, sentiment_score, supabase):
    
    '''
    Inserts an entry into the 'news' table.
    '''

    print(f"Inserting article: {title} from {source_url}")

    # Remove "https://" from the start of the source URL.
    source_url = source_url.replace("http://", "").replace("https://", "")

    # Retrieve news_site_id using the source URL.
    news_site_id_query = supabase.table('news_site').select('id').eq('url', source_url).execute()
    print(news_site_id_query)
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


def insert_company_news(url, companies, average_score, supabase):

    '''
    Inserts an entry into the company_news table.
    '''

    print(f"Inserting company news: {companies} = {average_score}")

    # First gather all company names and a list.

    # Retrieve news_id using the news URL.
    news_id_query = supabase.table('news').select('id').eq('url', url).execute()

    # # Query to get company_id based on the name
    # company_id_query = supabase.table('company').select('id').eq('name', company).execute()

    # # Query to get company_id based on the aliases - is this case sensitive?
    # company_id_alias_query = supabase.table('company').select('id').like('aliases', f'%{company}%').execute()

    # Assuming only one entry should match each condition.
    if len(news_id_query.data) == 1:
        news_id = news_id_query.data[0]['id']

        for company in companies:
            # Query to get company_id based on the name
            company_id_query = supabase.table('company').select('id').eq('name', company).execute()

            if len(company_id_query.data) == 1:
                company_id = company_id_query.data[0]['id']
                break

        supabase.table('company_news').insert({
            "news_id": news_id,
            "company_id": company_id,
            "public_impact": average_score
        }).execute()


def update_text(url, body, supabase):

    '''
    Updates the 'text' field of the relevant entry (using the URL as an identifier) in the 'news' table of the database.
    '''

    # Retrieve news_id using the news URL.

    news_id_query = supabase.table('news').select('id').eq('url', url).execute()

    # Assuming only one entry should match the condition.
    if len(news_id_query.data) == 1:
        news_id = news_id_query.data[0]['id']
        # Update the 'text' field of the relevant news entry in the 'news' table.
        data, count = supabase.table('news').update({"text": body}).eq('id', news_id).execute()


def get_tickers(mentioned_companies, supabase):

    '''
    Given a list of companies, it converts the list into a list of tickers.
    '''

    tickers = []
    seen_tickers = set()  # Keep track of seen tickers to avoid duplicates.

    # Retrieve ticker using the company name and aliases.
    for company in mentioned_companies:
        # Retrieve ticker for the company name.

        # Query to get ticker based on the name
        ticker_name_query = supabase.table('company').select('ticker').eq('name', company).execute()

        # Query to get ticker based on the aliases
        ticker_name_alias_query = supabase.table('company').select('ticker').like('aliases', f'%{company}%').execute()

        # Extract the 'ticker' value from the dictionary and append it to the tickers list.
        if ticker_name_query.data:
            ticker_value = ticker_name_query.data[0]['ticker']
        elif ticker_name_alias_query.data:
            ticker_value = ticker_name_alias_query.data[0]['ticker']

        # Check if the ticker or its aliases are already in the seen_tickers set.
        if ticker_value not in seen_tickers:
            tickers.append(ticker_value)
            seen_tickers.add(ticker_value)


    return tickers

# ============================================================
# END OF PROGRAM
# ============================================================
