import unittest

from URL_Analysis.url_analysis import format_body
from url_scraping import scrape
from supabase import create_client, Client
from text_sentiment_analysis import sentiment_analysis_company, find_mentioned_tickers

url_dict = {
    'https://www.theverge.com': 'https://www.theverge.com/2024/3/6/24091367/semiconductor-manufacturing-us-electricity-consumption-renewable-energy-report',
    'https://www.cnbc.com': 'https://www.cnbc.com/2024/03/06/microsoft-ai-engineer-says-copilot-designer-creates-disturbing-images.html',
    'https://www.foxbusiness.com': 'https://www.foxbusiness.com/markets/googles-gemini-debacle-make-break-moment-analyst'
}

company_mentioned = {
    '0': ['TSM', 'INTC', 'AAPL', 'META', 'GOOG'],
    '1': ['TSLA', 'MSFT', 'META', 'GOOG'],
    '2': ['GOOG']
}

articlebody = []

for site, url in url_dict.items():
    scrape_result = scrape(url, site)

    body = scrape_result["body"]

    body = format_body(body)

    articlebody.append(body)

SUPABASE_URL = "https://irendefjtnvixqkiehya.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImlyZW5kZWZqdG52aXhxa2llaHlhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MDUwNzcxNTUsImV4cCI6MjAyMDY1MzE1NX0.IaTi8UJP4JCcjP35RUNu2gLE3qd_CzQcHgy2y3UTaew"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

authentication = supabase.auth.sign_in_with_password({"email": "tudor0404@gmail.com", "password": "test123"})


class TestSentimentAnalysisCompany(unittest.TestCase):
    def setUp(self):
        # self.expected_result = company_mentioned['0']  # first article expected result
        # self.expected_result = company_mentioned['1']  # second article expected result
        self.expected_result = company_mentioned['2']  # third article expected result

    def test_tickers_mentioned(self):

        # actual_results = find_mentioned_tickers(articlebody[0], supabase)  # first article actual result
        # actual_results = find_mentioned_tickers(articlebody[1], supabase)  # second article actual result
        actual_results = find_mentioned_tickers(articlebody[2], supabase)  # third article actual result

        self.assertEquals(self.expected_result, actual_results)


if __name__ == '__main__':
    unittest.main()

supabase.auth.sign_out()
