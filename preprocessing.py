import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import PorterStemmer, WordNetLemmatizer, SnowballStemmer
import string

# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('wordnet')


def preprocess_text(text, tokenize=True, remove_stopwords=True, remove_punctuation=True, stemming=True, lemmatize=False):
    # Tokenization
    if tokenize:
        sentences = sent_tokenize(text)
        print("SENTENCE TOKENIZER: ")
        print(sentences)
        words = [word_tokenize(sentence) for sentence in sentences]
        print("WORD TOKENIZER: ")
        print(words)
    else:
        words = text

    # Stop-word elimination
    if remove_stopwords:
        stop_words = set(stopwords.words("english"))
        words = [[word for word in sentence if word.lower() not in stop_words]
                 for sentence in words]
        print("STOPWORD: ")
        print(words)

    # Punctuation removal
    if remove_punctuation:
        words = [[word for word in sentence if word not in string.punctuation]
                 for sentence in words]
        print("PUNC: ")
        print(words)

    # Stemming
    if stemming:
        stemmer = PorterStemmer()
        # stemmer = SnowballStemmer("english")
        words = [[stemmer.stem(word) for word in sentence]
                 for sentence in words]
        print("STEMMER: ")
        print(words)

    # Lemmatization
    if lemmatize:
        lemmatizer = WordNetLemmatizer()
        words = [[lemmatizer.lemmatize(word)
                  for word in sentence] for sentence in words]
        print("LEMMATIZER: ")
        print(words)
    return words


# Example usage:
# text = "A Christmas tree that can receive text messages has been unveiled at London's Tate Britain art gallery."
# preprocessed_text = preprocess_text(text)
# print(preprocessed_text)
