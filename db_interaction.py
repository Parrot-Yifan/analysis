from supabase import (
    create_client,
    Client,
)  # Import Supabase client for interacting with the Supabase database

# ============================================================
# START OF PROGRAM
# ============================================================

def get_tickers(supabase):

    '''
    Given a list of companies, it converts the list into a list of tickers.
    '''

    tickers = []

    # Retrieve tickers.
    ticker_name_query = supabase.table('company').select('ticker').execute()

    # Extract the 'ticker' value from the dictionary and append it to the tickers list.
    if ticker_name_query.data:
        for ticker in ticker_name_query.data:
            ticker_value = ticker.get('ticker')
            if ticker_value:
                tickers.append(ticker_value)

    return tickers

def remove_existing_company_stock(ticker,supabase):

    '''
    Deletes the existing entry of a company's stock predictions.
    '''

    # Retrieve company_id using the company name.
    company_id_query = supabase.table('company').select('id').eq('ticker', ticker).execute()
    # Assuming only one entry should match each condition.
    if len(company_id_query.data) == 1:
        company_id = company_id_query.data[0]['id']
        print(company_id)
        data, count = supabase.table('company_stock').delete().eq('company_id', company_id).execute()
        print(data)


def insert_company_stock(ticker, stock, supabase):

    '''
    Inserts an entry into the company_stock table.
    '''
    
     # Retrieve company_id using the company name.
    company_id_query = supabase.table('company').select('id').eq('ticker', ticker).execute()

    # Assuming only one entry should match each condition.
    if len(company_id_query.data) == 1:
        company_id = company_id_query.data[0]['id']

        # Insert company_news entry into the 'company_news' table.
        data, count = supabase.table('company_stock').insert({
            "company_id": company_id,
            "stock_impact": stock
        }).execute()

# ============================================================
# END OF PROGRAM
# ============================================================
