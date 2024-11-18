import nltk
import string
from constants import *
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer

nltk.download('stopwords')
nltk.download('punkt')


stemmer = PorterStemmer()
stop_words = set(stopwords.words('english'))

def clean_text(text, stop_words=stop_words, stemmer=stemmer, tokenized=False):
    
    # Convert text to lowercase
    text = text.lower()
    
    # Remove punctuation
    text = text.translate(str.maketrans("", "", string.punctuation))
    
    # Tokenize the text 
    tokens = word_tokenize(text)
    
    # Remove stopwords
    tokens = [token for token in tokens if token not in stop_words]
    
    # Apply stemming
    stemmed_tokens = [stemmer.stem(word) for word in tokens]
    
    if tokenized:
        return stemmed_tokens
    else:
        # Join tokens back into a single string
        cleaned_text = " ".join(stemmed_tokens)
        return cleaned_text
    
 