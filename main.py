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
# from stock_prediction import stock_prediction_function # Import the function from stock_prediction.py

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
        url_analysis_function()

        # Wait for 5 minutes before performing URL analysis again.
        time.sleep(5 * 60) 

if __name__ == "__main__":
    main()

# ============================================================
# END OF PROGRAM
# ============================================================