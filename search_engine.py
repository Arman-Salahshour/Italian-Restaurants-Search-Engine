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
    
    
def create_vocab_indexer(df, column):
    # Initialize an empty set to store unique tokens
    vocab = set()
    
    # Convert the specified column of the DataFrame to a NumPy array
    corpus = df[column].to_numpy()
    
    # Tokenize each text in the corpus and update the vocabulary set
    for text in corpus:
        tokens = word_tokenize(text)
        vocab.update(tokens)
    
    # Convert the vocabulary set into a DataFrame with a 'token' column
    vocab_df = pd.DataFrame(vocab, columns=['token'])  
    
    # Return the DataFrame containing unique tokens
    return vocab_df



def create_inverted_indexer(vocab_df, restaurants_df):
    # Initialize an empty dictionary to store the inverted index
    vocab_documents_dict = dict()
    
    # Iterate over each token in the vocabulary DataFrame
    for i, vocab in tqdm(enumerate(vocab_df.to_numpy())):
        # Find indices of rows in the DataFrame where the token appears in the 'cleaned_description' column
        indices = list(restaurants_df[restaurants_df['cleaned_description'].str.contains(vocab[0])].index)
        
        # Map the token's index in the vocabulary to the list of document indices
        vocab_documents_dict[i] = indices
    
    # Return the inverted index dictionary
    return vocab_documents_dict



