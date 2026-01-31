import re
import string
from typing import List

# A simple tokenizer/cleaner. 
# in a real prod scenario with spaCy:
# import spacy
# nlp = spacy.load("en_core_web_sm")

def clean_text(text: str) -> str:
    """
    Cleans the input text by:
    1. Lowercasing
    2. Removing special characters and numbers
    3. removing extra whitespace
    """
    if not text:
        return ""
    
    # Lowercase
    text = text.lower()
    
    # Remove punctuation and numbers (keep only letters and spaces)
    text = re.sub(r'[^a-z\s]', '', text)
    
    # Collapse multiple spaces
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def preprocess_story(text: str) -> str:
    """
    Full preprocessing pipeline for a user story.
    Returns the cleaned string ready for vectorization.
    """
    # 1. Cleaning
    cleaned = clean_text(text)
    
    # 2. Lemmatization could happen here if we used spaCy
    # doc = nlp(cleaned)
    # return " ".join([token.lemma_ for token in doc if not token.is_stop])
    
    return cleaned
