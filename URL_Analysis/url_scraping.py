from bs4 import BeautifulSoup  # Import BeautifulSoup for web scraping
import requests  # Import requests to make GET requests
import html2text  # Import html2text to allow markdown conversion

# ============================================================
# START OF PROGRAM
# ============================================================

from bs4 import BeautifulSoup
import requests
import html2text

def scrape_cnbc(soup, converter):
    article = {'title': '', 'body': ''}
    segment = ''  # use to store article

    # get the title
    articleTitle = str(soup.find('h1'))

    # find the news body
    articleBody = soup.find_all('div', class_='ArticleBody-articleBody')
    articleBody1 = soup.find_all('div', class_='group')

    # scrape the body
    if articleBody:
        for paragraph in articleBody:
            body = paragraph.find_all(['p', 'li', 'h2'])
            for Body in body:
                segment += str(Body)

    elif not articleBody:
        if articleBody1:
            for Body in articleBody1:
                body = Body.find_all(['p', 'li', 'h2'])
                for paragraph in body:
                    segment += str(paragraph)

    # Error handling
    else:
        articleTitle = "<h1>can't get the article</h1>"

    # result
    article['title'] = articleTitle
    article['body'] = segment

    # transfer to markdown
    article['title'] = converter.handle(article['title'])
    article['body'] = converter.handle(article['body'])

    return article


def scrape_foxbusiness(soup, converter):
    article = {'title': '', 'body': ''}
    segment = ''  # use to store article

    # get the title
    articleTitle = str(soup.find('h1'))

    # filter the messages don't require
    unwanted_div = soup.find('div', class_='featured featured-video video-ct')
    unwanted_pi = soup.find_all('div', class_='inline image-ct')
    unwanted_ti = soup.find_all('div', class_='info')
    if unwanted_ti:
        for ti in unwanted_ti:
            ti.decompose()

    if unwanted_pi:
        for pi in unwanted_pi:
            pi.decompose()

    if unwanted_div:
        unwanted_div.decompose()

    articleBody = soup.find_all('div', class_='article-body')
    for Body in articleBody:
        body = Body.find_all(['p', 'h2'])
        for paragraph in body:
            segment += str(paragraph)

    # result
    article['title'] = articleTitle
    article['body'] = segment

    # transfer to markdown
    article['title'] = converter.handle(article['title'])
    article['body'] = converter.handle(article['body'])

    return article


def scrape_aljazeera(soup, converter):
    article = {'title': '', 'body': ''}
    segment = ''  # use to store article

    # get the title
    articleTitle = str(soup.find('h1'))

    articleBody = soup.find_all('div', class_='wysiwyg wysiwyg--all-content css-ibbk12')
    unwanted_pd = soup.find('p', class_='site-footer__social-section-title dark')
    unwanted_p = soup.find('p', class_='site-footer__social-section-title')
    unwanted_pi = soup.find_all('img')
    unwanted_rm = soup.find('h2', 'more-on__heading')

    if unwanted_rm:
        unwanted_rm.decompose()

    if unwanted_pi:
        for pi1w in unwanted_pi:
            pi1w.decompose()

    if articleBody:
        for Body in articleBody:
            body = Body.find_all(['p', 'h2', 'li'])
            for paragraph in body:
                segment += str(paragraph)

    else:
        articleTitle = "<h1>can't get the article</h1>"

    article['title'] = articleTitle
    article['body'] = segment

    # transfer to markdown
    article['title'] = converter.handle(article['title'])
    article['body'] = converter.handle(article['body'])

    return article


def scrape_cnn(soup, converter):
    article = {'title': '', 'body': ''}
    segment = ''  # use to store article

    # get the title
    articleTitle = str(soup.find('h1'))

    articleBody = soup.find_all('div', class_='article__content')
    unwanted_p = soup.find('div', class_='layout__bottom layout-with-rail__bottom')
    unwanted_rd = soup.find_all('div', class_='related-content related-content--article')

    if unwanted_rd:
        for rd in unwanted_rd:
            rd.decompose()

    if unwanted_p:
        unwanted_p.decompose()

    if articleBody:
        for Body in articleBody:
            body = Body.find_all(['p', 'h2'])
            for paragraph in body:
                segment += str(paragraph)

    else:
        articleTitle = "<h1>can't get the article</h1>"

    article['title'] = articleTitle
    article['body'] = segment

    # transfer to markdown
    article['title'] = converter.handle(article['title'])
    article['body'] = converter.handle(article['body'])

    return article


def scrape_businessinsider(soup, converter):
    article = {'title': '', 'body': ''}
    segment = ''  # use to store article

    # get the title
    articleTitle = str(soup.find('h1'))

    articleBody = soup.find_all('article')
    if articleBody:
        for Body in articleBody:
            body = Body.find_all(['p', 'h2', 'li', 'h3'])
            for text in body:
                segment += str(text)

    else:
        articleTitle = "<h1>can't get the article</h1>"

    article['title'] = articleTitle
    article['body'] = segment

    # transfer to markdown
    article['title'] = converter.handle(article['title'])
    article['body'] = converter.handle(article['body'])

    return article


def scrape_kiplinger(soup, converter):
    article = {'title': '', 'body': ''}
    segment = ''  # use to store article

    # get the title
    articleTitle = str(soup.find('h1'))

    unwanted = soup.find_all('div', id='blueconic-article-kiplinger')
    unwanted_pi = soup.find_all('p', class_='vanilla-image-block')

    if unwanted:
        for unwanted_ad in unwanted:
            unwanted_ad.decompose()

    if unwanted_pi:
        for pi in unwanted_pi:
            pi.decompose()

    articleBody = soup.find_all('div', class_='article__body')
    if articleBody:
        for Body in articleBody:
            body = Body.find_all(['p', 'h2', 'li', 'h3', {'table': {'class': 'table__wrapper '
                                                                             'table__wrapper--inbodyContent '
                                                                             'table__wrapper--sticky '
                                                                             'table__wrapper--divider'}}])
            for article in body:
                segment += str(article)

    else:
        articleTitle = "<h1>can't get the article</h1>"

    article['title'] = articleTitle
    article['body'] = segment

    # transfer to markdown
    article['title'] = converter.handle(article['title'])
    article['body'] = converter.handle(article['body'])

    return article


def scrape_motley_fool(soup, converter):
    article = {'title': '', 'body': ''}
    segment = ''  # use to store article

    # get the title
    articleTitle = str(soup.find('h1'))

    articleBody = soup.find_all('div', class_='article-body')
    articlest = soup.find('h2', class_='font-light leading-10 text-h3 text-gray-1100 mb-32px')

    if articlest:
        segment += str(articlest)

    if articleBody:
        for Body in articleBody:
            body = Body.find_all(['p', 'h2'])
            for paragraph in body:
                segment += str(paragraph)

    else:
        articleTitle = "<h1>can't get the article</h1>"

    article['title'] = articleTitle
    article['body'] = segment

    # transfer to markdown
    article['title'] = converter.handle(article['title'])
    article['body'] = converter.handle(article['body'])

    return article


def scrape_benzinga(soup, converter):
    article = {'title': '', 'body': ''}
    segment = ''  # use to store article

    # get the title
    articleTitle = str(soup.find('h1'))

    articleBody = soup.find_all('div', id='article-body')
    unwanted_ad = soup.find_all('div', class_='ad-container')
    if unwanted_ad:
        for ad in unwanted_ad:
            ad.decompose()

    if articleBody:
        for Body in articleBody:
            body = Body.find_all(['p', 'h3', 'li'])
            for paragraph in body:
                segment += str(paragraph)

    else:
        articleTitle = "<h1>can't get the article</h1>"

    article['title'] = articleTitle
    article['body'] = segment

    # transfer to markdown
    article['title'] = converter.handle(article['title'])
    article['body'] = converter.handle(article['body'])

    return article


def scrape_guardian(soup, converter):
    article = {'title': '', 'body': ''}
    segment = ''  # use to store article

    # get the title
    articleTitle = str(soup.find('h1'))

    articleBody = soup.find_all('div', class_='dcr-lw02qf')
    unwanted_si = soup.find_all('figure')
    if unwanted_si:
        for si in unwanted_si:
            si.decompose()

    if articleBody:
        for Body in articleBody:
            body = Body.find_all(['p', 'h2'])
            for paragraph in body:
                segment += str(paragraph)

    else:
        articleTitle = "<h1>can't get the article</h1>"

    article['title'] = articleTitle
    article['body'] = segment

    # transfer to markdown
    article['title'] = converter.handle(article['title'])
    article['body'] = converter.handle(article['body'])

    return article


# ======================================================================================= has test: print(soup)
def scrape_yahoo(soup, converter):
    article = {'title': '', 'body': ''}
    segment = ''  # use to store article

    # get the title
    articleTitle = str(soup.find('h1'))

    articleBody = soup.find_all('div', class_='caas-body')
    unwanted_td = soup.find('div', id='module-dynamicRR')

    if unwanted_td:
        unwanted_td.decompose()

    # articleBody2 = soup.find_all('div')
    if articleBody:
        for Body in articleBody:
            body = Body.find_all(['p', 'h2'])
            for paragraph in body:
                segment += str(paragraph)

    else:
        print(soup)
        articleTitle = "<h1>can't get the article</h1>"

    article['title'] = articleTitle
    article['body'] = segment

    # transfer to markdown
    article['title'] = converter.handle(article['title'])
    article['body'] = converter.handle(article['body'])

    return article


def scrape_verge(soup, converter):
    article = {'title': '', 'body': ''}
    segment = ''  # use to store article

    # get the title
    articleTitle = str(soup.find('h1'))

    articleBody = soup.find_all('div', class_='clearfix')
    articleBody2 = soup.find_all('div', class_='md:flex lg:justify-between')
    # ad = soup.find_all('div', role='button')
    # unwanted_bt = soup.find('div', class_='mx-auto max-w-container-lg')
    # unwanted_bt1 = soup.find_all('div', class_='flex-auto')
    unwanted_si = soup.find_all('div', class_='duet--article--article-body-component clear-both block')
    ad1 = soup.find_all('p', class_='mr-8 inline pt-6 font-polysans-mono text-12 font-medium tracking-1 '
                                    'dark:text-gray-bd')

    # if unwanted_bt1:
    #     for signin in unwanted_bt1:
    #         signin.decompose()
    #
    # if unwanted_bt:
    #     unwanted_bt.decompose()

    # if ad:
    #     for unwanted_ad in ad:
    #         unwanted_ad.decompose()
    if unwanted_si:
        for si in unwanted_si:
            si.decompose()

    if ad1:
        for unwanted_a1 in ad1:
            unwanted_a1.decompose()

    if articleBody:

        for Body in articleBody:
            body = Body.find_all(['p', 'h4', 'h3', 'li'])
            for paragraph in body:
                segment += str(paragraph)

    # elif articleBody2:
    #     for Body in articleBody2:
    #         body = Body.find_all(['p', 'li', 'front'])
    #         for Text in body:
    #             segment += str(Text)

    else:
        articleTitle = "<h1>can't get the article</h1>"

    article['title'] = articleTitle
    article['body'] = segment

    # transfer to markdown
    article['title'] = converter.handle(article['title'])
    article['body'] = converter.handle(article['body'])

    return article


def scrape_bbc(soup, converter):
    article = {'title': '', 'body': ''}
    segment = ''  # use to store article

    # get the title
    articleTitle = str(soup.find('h1'))

    articleBody = soup.find_all('main')
    unwanted_vd = soup.find('figure')
    unwanted_rl = soup.find('section', {'data-component': 'related-internet-links'})
    unwanted_ab = soup.find('section', {'data-component': 'around-the-bbc'})
    unwanted_rt = soup.find('div', {'data-component': 'topic-list'})
    unwanted_ms = soup.find('div', {'data-component': 'links-block'})
    # unwanted_md = soup.find('div', class_='ssrcss-1l5yt4e-ComponentWrapper-SocialComponentWrapper ehp21060')

    # if unwanted_md:
    #     unwanted_md.decompose()

    if unwanted_rl:
        unwanted_rl.decompose()

    if unwanted_ab:
        unwanted_ab.decompose()

    if unwanted_ms:
        unwanted_ms.decompose()

    if unwanted_rt:
        unwanted_rt.decompose()

    if unwanted_vd:
        unwanted_vd.decompose()

    if articleBody:
        for Text in articleBody:
            body = Text.find_all(['p', 'h2', 'li'])
            for Body in body:
                segment += str(Body)

    else:
        articleTitle = "<h1>can't get the article</h1>"

    # result
    article['title'] = articleTitle
    article['body'] = segment

    # transfer to markdown
    article['title'] = converter.handle(article['title'])
    article['body'] = converter.handle(article['body'])

    return article


def scrape_politicoeu(soup, converter):
    article = {'title': '', 'body': ''}
    segment = ''  # use to store article

    # get the title
    articleTitle = str(soup.find('h1'))

    articleBody = soup.find_all('div', class_='sidebar-grid sidebar-grid--is-narrow')

    if articleBody:
        for Body in articleBody:
            body = Body.find_all(['p', 'h2', 'h3'])
            for text in body:
                segment += str(text)

    else:
        articleTitle = "<h1>can't get the article</h1>"

    article['title'] = articleTitle
    article['body'] = segment

    # transfer to markdown
    article['title'] = converter.handle(article['title'])
    article['body'] = converter.handle(article['body'])

    return article


def scrape_techcrunch(soup, converter):
    article = {'title': '', 'body': ''}
    segment = ''  # use to store article

    # get the title
    articleTitle = str(soup.find('h1'))

    unwanted_ad = soup.find_all('div', class_='wp-caption aligncenter')
    unwanted_ct = soup.find_all('blockquote', class_='text-post-media')

    if unwanted_ct:
        for ct in unwanted_ct:
            ct.decompose()

    if unwanted_ad:
        for text in unwanted_ad:
            text.decompose()

    articleBody = soup.find_all('div', class_='article-content')

    if articleBody:
        for Body in articleBody:
            segment += str(Body)
    else:
        articleTitle = "<h1>can't get the article</h1>"

    article['title'] = articleTitle
    article['body'] = segment

    article['title'] = converter.handle(article['title'])
    article['body'] = converter.handle(article['body'])

    return article


def scrape_scmp(soup, converter):
    article = {'title': '', 'body': ''}
    segment = ''  # use to store article

    # get the title
    articleTitle = str(soup.find('h2'))

    article['title'] = articleTitle

    return article


# scrape dictionary
news_sites = {
    'cnbc.com': scrape_cnbc,
    'foxbusiness.com': scrape_foxbusiness,
    'aljazeera.com': scrape_aljazeera,
    'cnn.com': scrape_cnn,
    'businessinsider.com': scrape_businessinsider,
    'kiplinger.com': scrape_kiplinger,
    'fool.com': scrape_motley_fool,
    'benzinga.com': scrape_benzinga,
    'theguardian.com': scrape_guardian,
    'finance.yahoo.com': scrape_yahoo,
    'theverge.com': scrape_verge,
    'bbc.co.uk': scrape_bbc,
    'politico.eu': scrape_politicoeu,
    'techcrunch.com': scrape_techcrunch,
    'scmp.com': scrape_scmp
}


def scrape(url, site):
    # transform to markdown
    converter = html2text.HTML2Text()
    converter.ignore_links = True  # want link, set False
    converter.ignore_images = True  # don't want picture, set True
    converter.ignore_emphasis = True  # keep Font, such as bold, set False

    try:
        response = requests.get(url)
        if response.status_code == 200:
            # Get the html
            soup = BeautifulSoup(response.content, 'html.parser')

            # Check if any source key is present in the lowercase site URL
            for source, scrape_function in news_sites.items():
                if source in site.lower():
                    return scrape_function(soup, converter)

            print(f'No scraping strategy for: {site}')
            return None

        else:
            print(f'Error fetching {url}: {response.status_code}')
            return None

    except requests.exceptions.RequestException as e:
        print(f'Error fetching {url}: {e}')
        return None

# ------------------------------------------------------------

# These are the sites that cannot be scraped:

# ------------------------------------------------------------
# Cannot use Beautiful Soup
# ------------------------------------------------------------
# Reuters
# barrons
# ------------------------------------------------------------


# ------------------------------------------------------------
# Request denied
# ------------------------------------------------------------
# Investors Business Daily
# ------------------------------------------------------------


# ------------------------------------------------------------
# Requires money
# ------------------------------------------------------------
# The Atlantic
# Marketwatch
# Forbes
# The Economist
# South China Morning Post
# Bloomberg
# The Week
# ------------------------------------------------------------

# ------------------------------------------------------------
# Some articles cannot be retrieved
# ------------------------------------------------------------
# yahoo finance (some problems: some articles can't get)
# ------------------------------------------------------------

# ------------------------------------------------------------
# No response
# ------------------------------------------------------------
# Nasdag
# ------------------------------------------------------------

# ============================================================
# END OF PROGRAM
# ============================================================
