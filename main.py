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

def main():

    '''
    Main analysis function which manages the execution of the analysis program.
    '''

    while True: # Run the analysis program on an infinite loop.

    
        print("Executing.")
        
        # Call the stock price prediction program.
        main_stock_prediction_function()

        # Wait for 5 minutes before performing URL analysis again.
        time.sleep(5 * 60) 

if __name__ == "__main__":
    main()

# ============================================================
# END OF PROGRAM
# ============================================================