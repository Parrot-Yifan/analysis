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
    max_length = 128  # Maximum length for the sentiment analysis model.
    total_score = 0.0  # Initialize the total score.

    # Load the sentiment analysis model and tokenizer.
    model_name = "finiteautomata/bertweet-base-sentiment-analysis"
    sentiment_analysis = pipeline("sentiment-analysis", model=model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    # Filter out or truncate sentences that exceed the maximum token length.
    processed_sentences = []
    for sentence in sentences:
        tokens = tokenizer.encode(sentence, add_special_tokens=True, truncation=False, max_length=max_length)
        
        # Check if token length, including special tokens, exceeds max_length
        if len(tokens) < max_length: 
            # If within the limit, decode tokens back to text for sentiment analysis
            processed_sentences.append(sentence)

    # Update total_sentences to consider only processed sentences.
    total_sentences = len(processed_sentences)

    # Conduct sentiment analysis on each filtered or truncated sentence.
    for sentence in processed_sentences:
        result = sentiment_analysis(sentence)
        mapped_score = map_sentiment_to_number(result[0]["label"], result[0]["score"])
        total_score += mapped_score

    # Calculate the average score.
    average_score = total_score / total_sentences if total_sentences > 0 else 0

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
    processed_sentences = []
    for sentence in sentences:
        tokens = tokenizer.encode(sentence, add_special_tokens=True, truncation=False, max_length=max_length)
        
        # Check if token length, including special tokens, exceeds max_length
        if len(tokens) < max_length:
            # If it's too long, you can choose to truncate manually or skip the sentence
            # continue  # Skipping here; you can also truncate manually if needed
            # tokens = tokens[:max_length]
            # continue
            processed_sentences.append(sentence)
        
    # Update total_sentences to consider only processed sentences.
    total_sentences = len(processed_sentences)

    # Conduct sentiment analysis on each sentence in the list.
    for sentence in processed_sentences:

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

    # print(modified_sentences)
    # Calculate the average score.
    average_score = total_score / total_sentences if total_sentences > 0 else 0

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
           company_name 
           for company_entry in company_names 
           for company_name in company_entry['names'] 
           if f'{company_name}' in sentence
    ]
    
    tickers = get_tickers(mentioned_companies, supabase)

    return tickers


# ============================================================
# END OF PROGRAM
# ============================================================
