from transformers import (
    pipeline,
    AutoModelForSeq2SeqLM,
    AutoTokenizer,
)  # Import transformers from Hugging Face for summarization.
import textwrap

# ============================================================
# START OF PROGRAM
# ============================================================


def chunk_text(text, tokenizer, max_token_length=1024):
    """
    Splits the text into chunks where each chunk is as close to the max_token_length as possible
    while respecting sentence boundaries.
    """
    # Convert to tokens and determine where to split them into chunks
    tokens = tokenizer(text, truncation=True, max_length=max_token_length)["input_ids"]
    chunked_text = textwrap.wrap(text, width=1000, break_long_words=False, break_on_hyphens=False)
    return chunked_text

def summarize_chunks(chunks, summarizer):
    """
    Summarizes each text chunk and combines them into a final summary.
    """
    summaries = [summarizer(chunk)[0]["summary_text"] for chunk in chunks]
    final_summary = " ".join(summaries)
    return final_summary

def summarize_text(text, model_name="sshleifer/distilbart-cnn-12-6"):
    """
    Summarizes the text ensuring each chunk is within the token limit.
    """
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    summarizer = pipeline("summarization", model=model, tokenizer=tokenizer)

    chunks = chunk_text(text, tokenizer)
    final_summary = summarize_chunks(chunks, summarizer)
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

