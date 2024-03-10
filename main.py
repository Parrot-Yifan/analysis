# =============================================================================================================================================
#
# FILE:         main.py
# DESCRIPTION:  This file runs the analysis program, which performs stock price predictions.
# AUTHORS:      Nishanth Dhinakaran, Yifan Xu, Changpei Yuan
# CREATED:      27/02/2024
# VERSION:      1.0
#
# =============================================================================================================================================

import time #Import the time module.
from stock_prediction import *  # Import the function from url_analysis.py
# from stock_prediction import stock_prediction_function # Import the function from stock_prediction.py
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

def main():

    '''
    Main analysis function which manages the execution of the analysis program.
    '''

    while True: # Run the analysis program on an infinite loop.

    
        print("Executing.")
        
        # Authenticate with Supabase using email and password.
        authentication = supabase.auth.sign_in_with_password({"email": "tudor0404@gmail.com", "password": "test123"})
        # Call the stock price prediction program.
        main_stock_prediction_function(supabase)
        # Sign out from Supabase authentication.
        supabase.auth.sign_out()

        print("Waiting for 5 minutes.")
        # Wait for 5 minutes before performing URL analysis again.
        time.sleep(5 * 60) 

if __name__ == "__main__":
    main()

# ============================================================
# END OF PROGRAM
# ============================================================
