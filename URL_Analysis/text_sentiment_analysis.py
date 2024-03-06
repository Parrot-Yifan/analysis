from transformers import (
    pipeline,
    AutoModelForSeq2SeqLM,
    AutoTokenizer,
)  # Import transformers from Hugging Face for summarization/sentiment analysis.
import re
from db_interaction import * #Import database interaction functions.

# ============================================================
# START OF PROGRAM
# ============================================================

def sentiment_analysis_article(sentences):
    # Maximum length for the sentiment analysis.
    max_length = 128

    # Initialize variables for accumulating scores/labels.
    total_score = 0.0
    total_sentences = len(sentences)

    # Load the sentiment analysis model.
    model_name = "finiteautomata/bertweet-base-sentiment-analysis"
    sentiment_analysis = pipeline(model=model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    # Conduct sentiment analysis on each sentence in the list.
    for sentence in sentences:

        # If the number of words in the sentence exceeds the maximum length the model can handle, skip it.
        if len(tokenizer.tokenize(sentence)) > max_length:
            continue

        # Perform sentiment analysis on the sentence.
        result = sentiment_analysis(sentence)

        # Map the sentiment score using the label and accumulate to find the final score.
        mapped_score = map_sentiment_to_number(result[0]["label"], result[0]["score"])
        total_score += mapped_score

    # Calculate the average score.
    average_score = total_score / total_sentences

    return average_score


def sentiment_analysis_company(sentences, supabase):

    """
    Performs sentiment analysis on a list of sentences.
    Returns an average score, plus sentences that need to be modified.
    """ 

    max_length = 128

    # Initialize variables for accumulating scores/labels.
    total_score = 0.0
    total_sentences = len(sentences)

    # Load the sentiment analysis model.
    model_name = "finiteautomata/bertweet-base-sentiment-analysis"
    sentiment_analysis = pipeline(model=model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    modified_sentences = []

    # Conduct sentiment analysis on each sentence in the list.
    for sentence in sentences:

        # If the number of words in the sentence exceeds the maximum length the model can handle, skip it.
        if len(tokenizer.tokenize(sentence)) >= max_length:
            continue

        # Perform sentiment analysis on the sentence.
        result = sentiment_analysis(sentence)

        # Map the sentiment score using the label and accumulate to find the final score.
        mapped_score = map_sentiment_to_number(result[0]["label"], result[0]["score"])
        total_score += mapped_score
        
        tickers = find_mentioned_tickers(sentence, supabase)
        # Modify the sentence that was analysed for sentiment analysis and add to a list of modified sentences.
        modified_sentence = wrap_sentence_with_html(
            sentence, map_sentiment_to_number(result[0]["label"], result[0]["score"]), tickers
        )
        modified_sentences.append(modified_sentence)

    # Calculate the average score.
    average_score = total_score / total_sentences

    return average_score, modified_sentences


def map_sentiment_to_number(sentiment_label, score):

    """
    Map the sentiment scores to a value that can be interpreted.
    Used as a helper function for sentiment analysis.
    """

    if sentiment_label == "NEU":  # If the label is neutral, map to 0.
        return 0.0
    elif (
        sentiment_label == "POS"
    ):  # If the label is positive, map to its positive score directly.
        return score
    elif (
        sentiment_label == "NEG"
    ):  # If the label is negative, map to the negative score by inverting the sign.
        return -1 * score
    else:
        return None


def wrap_sentence_with_html(sentence, score, tickers):

    """
    Modifies the sentence to include the <span> tag.
    Used as a helper function for sentiment analysis.
    """

    # Modify the sentence to HTML.
    html_structure = f'<span score="{score}" tickers="{tickers}">{sentence}</span>'
    return html_structure

def find_mentioned_tickers(sentence, supabase):

    '''
    Finds all the tickers of companies mentioned in a sentence.
    '''

    #Instead retrieve any aliases too and append to list.
    db_data = retrieve_DB_data(supabase)
    company_names = db_data["company_names"]

    mentioned_companies = [
            # company for company in company_names if {company} in sentence
            company for company in company_names if f'{company}' in sentence
        ]
    
    tickers = get_tickers(mentioned_companies, supabase)

    return tickers




# ============================================================
# END OF PROGRAM
# ============================================================
