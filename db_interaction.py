from supabase import (
    create_client,
    Client,
)  # Import Supabase client for interacting with the Supabase database

# ============================================================
# START OF PROGRAM
# ============================================================

SUPABASE_URL = "https://irendefjtnvixqkiehya.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImlyZW5kZWZqdG52aXhxa2llaHlhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MDUwNzcxNTUsImV4cCI6MjAyMDY1MzE1NX0.IaTi8UJP4JCcjP35RUNu2gLE3qd_CzQcHgy2y3UTaew"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_tickers():

    '''
    Given a list of companies, it converts the list into a list of tickers.
    '''

    # Authenticate with Supabase using email and password.
    authentication = supabase.auth.sign_in_with_password({"email": "tudor0404@gmail.com", "password": "test123"})

    tickers = []

    # Retrieve tickers.
    ticker_name_query = supabase.table('company').select('ticker').execute()

    # Extract the 'ticker' value from the dictionary and append it to the tickers list.
    if ticker_name_query.data:
        for ticker in ticker_name_query.data:
            ticker_value = ticker.get('ticker')
            if ticker_value:
                tickers.append(ticker_value)

    # Sign out from Supabase authentication.
    supabase.auth.sign_out()

    return tickers

def remove_existing_company_stock(ticker):

    '''
    Deletes the existing entry of a company's stock predictions.
    '''

    # Authenticate with Supabase using email and password.
    authentication = supabase.auth.sign_in_with_password({"email": "tudor0404@gmail.com", "password": "test123"})


    # Retrieve company_id using the company name.
    company_id_query = supabase.table('company').select('id').eq('ticker', ticker).execute()

    # Assuming only one entry should match each condition.
    if len(company_id_query.data) == 1:
        company_id = company_id_query.data[0]['id']

        data, count = supabase.table('company_stock').delete().eq('id', company_id).execute()

    # Sign out from Supabase authentication.
    supabase.auth.sign_out()


def insert_company_stock(ticker, date, stock):

    '''
    Inserts an entry into the company_stock table.
    '''

    # Authenticate with Supabase using email and password.
    authentication = supabase.auth.sign_in_with_password({"email": "tudor0404@gmail.com", "password": "test123"})

     # Retrieve company_id using the ticker.
    company_id_query = supabase.table('company').select('id').eq('ticker', ticker).execute()

    # Assuming only one entry should match each condition.
    if len(company_id_query.data) == 1:
        company_id = company_id_query.data[0]['id']

        # Insert company_news entry into the 'company_news' table.
        data, count = supabase.table('company_stock').insert({
            "created_at": date,
            "company_id": company_id,
            "stock_impact": stock
        }).execute()

    # Sign out from Supabase authentication.
    supabase.auth.sign_out()

# ============================================================
# END OF PROGRAM
# ============================================================
