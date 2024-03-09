# =============================================================================================================================================
#
# FILE:         main.py
# DESCRIPTION:  This file runs the analysis program, which performs URL analysis.
# AUTHORS:      Nishanth Dhinakaran, Yifan Xu, Changpei Yuan
# CREATED:      02/03/2024
# VERSION:      1.0
#
# =============================================================================================================================================

import time #Import the time module.
from URL_Analysis.url_analysis import url_analysis_function  # Import the function from url_analysis.py
from supabase import (
    create_client,
    Client
)  # Import Supabase client for interacting with the Supabase database

# Makes the connection to the Supabase client.
SUPABASE_URL = "https://irendefjtnvixqkiehya.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImlyZW5kZWZqdG52aXhxa2llaHlhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MDUwNzcxNTUsImV4cCI6MjAyMDY1MzE1NX0.IaTi8UJP4JCcjP35RUNu2gLE3qd_CzQcHgy2y3UTaew"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ============================================================
# START OF PROGRAM
# ============================================================

def main():

    '''
    Main analysis function which manages the execution of the analysis program.
    '''

    while True: # Run the analysis program on an infinite loop.

        # Call the URL analysis program.
        print("Executing URL analysis.")
        authentication = supabase.auth.sign_in_with_password({"email": "tudor0404@gmail.com", "password": "test123"})
        url_analysis_function(supabase)
        supabase.auth.sign_out() 
        # Wait for 5 minutes before performing URL analysis again.
        print("Waiting for 5 minutes.")
        time.sleep(5 * 60) 
        
    

if __name__ == "__main__":
    main()

# ============================================================
# END OF PROGRAM
# ============================================================
