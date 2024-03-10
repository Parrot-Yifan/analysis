import unittest

from nltk import sent_tokenize

from URL_Analysis.text_sentiment_analysis import sentiment_analysis_article
from URL_Analysis.url_analysis import format_body
from URL_Analysis.url_scraping import scrape

url_dict = {
    'https://www.theverge.com': 'https://www.theverge.com/2024/3/6/24091367/semiconductor-manufacturing-us-electricity-consumption-renewable-energy-report',
    'https://www.cnbc.com': 'https://www.cnbc.com/2024/03/06/microsoft-ai-engineer-says-copilot-designer-creates-disturbing-images.html',
    'https://www.foxbusiness.com': 'https://www.foxbusiness.com/markets/googles-gemini-debacle-make-break-moment-analyst'
}

articlebody = []

for site, url in url_dict.items():
    scrape_result = scrape(url, site)
    body = scrape_result["body"]
    body = format_body(body)
    sentences = sent_tokenize(body)

    articlebody.append(sentences)


class TestSentimentAnalysisCompany(unittest.TestCase):
    def setUp(self):
        self.expected_result = [-0.143, -0.155, -0.291]  # expected result

    def test_tickers_mentioned(self):
        actual_results = []

        # actual result
        for article in articlebody:
            sentiment_score = sentiment_analysis_article(article)
            actual_results.append(sentiment_score)

        for expected_result, actual_result in zip(self.expected_result, actual_results):
            self.assertAlmostEquals(expected_result, actual_result, delta=0.005)


if __name__ == '__main__':
    unittest.main()