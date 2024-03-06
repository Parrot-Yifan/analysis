from unittest import TestCase, mock
from url_scraping import scrape, scrape_cnbc
import unittest
import html2text
from bs4 import BeautifulSoup
from requests.exceptions import HTTPError

class TestScrape(TestCase):

    def setUp(self):
        self.converter = html2text.HTML2Text()
        self.converter.ignore_links = True
        self.converter.ignore_images = True
        self.converter.ignore_emphasis = True

        # fake html structure from the news_site
        self.mock_html = """
        <html>
        <body>
            <h1>Test Article Title</h1>
            <div class="ArticleBody-articleBody">
                <p>Paragraph 1</p>
                <p>Paragraph 2</p>
            </div>
        </body>
        </html>
        """
        self.mock_soup = BeautifulSoup(self.mock_html, 'html.parser')
    
    @mock.patch('url_scraping.requests.get')
    def test_scrape_cnbc(self, mock_get):
        # simulate 'requests.get' return value
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.content = self.mock_html.encode('utf-8')

        mock_get.return_value = mock_response

        # use scrape function
        result = scrape_cnbc(self.mock_soup, self.converter)

        # check the result
        # self.assertIsNone(result)
        self.assertIn('title', result)
        self.assertIn('body', result)
        self.assertEqual(result['title'], '# Test Article Title\n\n')
        self.assertEqual(result['body'], 'Paragraph 1\n\nParagraph 2\n\n')

    
    '''
    TEST 'TRY EXCEPT'
    '''
    @mock.patch('requests.get')
    def test_fetch_data_http_error(self, mock_get):
        mock_get.side_effect = HTTPError("Error occurred")

        result = scrape("http://example.com", "cndc")
        self.assertIsNone(result) 



    '''
    TEST RESPONSE_STATUS ERROR_HANDLE
    '''

    @mock.patch('requests.get')
    def test_error_handle_response_status(self, mock_get):
        # set the request status
        mock_response = mock.Mock()

        '''
        wrtong 'response.status'
        '''
        mock_response.status_code = 404
        mock_response.content = self.mock_html.encode('utf-8')
        mock_get.return_value = mock_response

        # call 'scrape' function and check whether the return is 'None'
        result = scrape("http://example.com", "cndc")
        self.assertIsNone(result)
        mock_get.assert_called_once_with("http://example.com")


    '''
    TEST SITE_VAILED ERROR_HANDLE
    '''
    @mock.patch('requests.get')
    def test_error_handle_site_vailed(self, mock_get):
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.content = self.mock_html.encode('utf-8')
        mock_get.return_value = mock_response

        # wrong news_site input
        result = scrape("http://example.com", "ddd")
        self.assertIsNone(result)
        mock_get.assert_called_once_with("http://example.com")
        

if __name__ == "__main__":
    unittest.main()
