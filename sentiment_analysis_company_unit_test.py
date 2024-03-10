import unittest

from URL_Analysis.url_analysis import format_body
from url_scraping import scrape
from supabase import create_client, Client
from text_sentiment_analysis import sentiment_analysis_company
from url_analysis import get_relevant_sentences

url_dict = {
    'https://www.theverge.com': 'https://www.theverge.com/2024/3/6/24091367/semiconductor-manufacturing-us-electricity-consumption-renewable-energy-report',
    'https://www.cnbc.com': 'https://www.cnbc.com/2024/03/06/microsoft-ai-engineer-says-copilot-designer-creates-disturbing-images.html',
    'https://www.foxbusiness.com': 'https://www.foxbusiness.com/markets/googles-gemini-debacle-make-break-moment-analyst'
}

company_mentioned = {
    '0': ['TSM', 'INTC', 'AAPL', 'META', 'GOOG'],
    '1': ['MSFG', 'GOOG'],
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
        # self.expected_scores = [-0.166, -0.155, 0.051, -0.091, 0.021]  # first article
        # self.expected_scores = [-0.133, -0.126] # second article
        self.expected_scores = [-0.311] # third article

    def test_sentiment_analysis_company(self):

        actual_scores = []
        
        for name in company_mentioned['2']:
            relevant_sentences = get_relevant_sentences(articlebody[2], name)
            actual_scores.append(sentiment_analysis_company(relevant_sentences, supabase)[0])

        for expected_score, actual_score in zip(self.expected_scores, actual_scores):
            self.assertAlmostEqual(expected_score, actual_score, delta=0.005)


if __name__ == '__main__':
    unittest.main()

supabase.auth.sign_out()
