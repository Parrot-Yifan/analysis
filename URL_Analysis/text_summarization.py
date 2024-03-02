from transformers import (
    pipeline,
    AutoModelForSeq2SeqLM,
    AutoTokenizer,
)  # Import transformers from Hugging Face for summarization.

# ============================================================
# START OF PROGRAM
# ============================================================

def word_count(text, tokenizer):

    """
    Counts the number of words in a given article text.
    Used as a helper function for summarization.
    """

    # Tokenize the text and return the count of tokens (words).
    tokens = tokenizer(text)["input_ids"]

    return len(tokens)

def summarize_text(text):

    """
    Summarizes the article text and returns a sumamry.
    """

    # Load the distilbart-cnn-12-6 model and tokenizer.
    model_name = "sshleifer/distilbart-cnn-12-6"
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    # Calculate the total number of tokens in the text.
    total_tokens = word_count(text, tokenizer)

    # Define the summarization pipeline.
    summarizer = pipeline("summarization", model=model, tokenizer=tokenizer)

    if total_tokens > 1024:
        # Split the text into chunks of reasonable size based on the number of tokens.
        chunk_length = max(total_tokens // 4, 1)
        chunks = [text[i * chunk_length : (i + 1) * chunk_length] for i in range(4)]

        # Summarize the input text for each chunk.
        summarized_texts = [
            summarizer(
                chunk,
                max_length=max(chunk_length // 2, 1),
                min_length=0,
                length_penalty=2.0,
                num_beams=4,
                early_stopping=True,
            )[0]["summary_text"]
            for chunk in chunks
        ]

        final_summary = " ".join(summarized_texts)
    else:
        # If the text is shorter than or equal to 1024 characters, summarize directly.
        summarised_text = summarizer(
            text,
            max_length= max(total_tokens // 4, 1),
            min_length=0,
            length_penalty=2.0,
            num_beams=4,
            early_stopping=True,
        )[0]["summary_text"]
        final_summary = summarised_text

    final_summary = format_summary(final_summary)
    return final_summary

def format_summary(final_summary):
    
    '''
    Formats the summary into an appropriate format.
    '''

    # Initialize formatted_summary with the original final_summary.
    formatted_summary = final_summary

    # Ensure the summary ends with a full stop.
    if not formatted_summary.endswith("."):
        # Find the last occurrence of a full stop and truncate the text.
        last_full_stop = formatted_summary.rfind(".")
        if last_full_stop != -1:
            formatted_summary = formatted_summary[: last_full_stop + 1]

    # Remove any space before full stops.
    formatted_summary = formatted_summary.replace(" .", ".")

    return formatted_summary

# ============================================================
# END OF PROGRAM
# ============================================================

