# Import nltk and download data
import string
import nltk
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('stopwords')
stopwords = nltk.corpus.stopwords.words('english')
punctuation = list(string.punctuation)
stopwords_punctuation = set(stopwords + punctuation)


def theme_words(document):
    # Join all sentences into one text
    text = " ".join(document)
    # Tokenize the text by word
    text_words = nltk.word_tokenize(text)
    # print(text_words)
    # Remove stopwords from text words
    text_words = [
        word for word in text_words if word not in stopwords_punctuation]
    print(text_words)
    # Calculate the frequency distribution of words in text
    freq_dist = nltk.FreqDist(text_words)

    # # Print the frequencies
    # for word, frequency in freq_dist.items():
    #     print(word, frequency)
    # Create a text collection object from text words
    text_collection = nltk.TextCollection(text_words)

    # Calculate the tf-idf value of each word in text collection
    tf_idf = {word: text_collection.tf_idf(
        word, text_words) for word in text_words}
    # Sort the words by their tf-idf values and select the top 10 percent as theme words
    sorted_tf_idf = sorted(tf_idf.items(), key=lambda x: x[1], reverse=True)
    # print(sorted_tf_idf)
    top_10_percent = int(len(sorted_tf_idf) * 0.1)
    theme_words_arr = [word for word, value in sorted_tf_idf[:top_10_percent]]
    return theme_words_arr


def sentence_score(sentence, theme_words_arr, title, ratio_3):
    # Tokenize by word and by sentence
    words = nltk.word_tokenize(sentence)
    sentence_words = [
        word for word in words if word not in stopwords_punctuation]

    print("without punc", sentence_words)
    # Initialize score
    score = 0

    # Parameter 1: ratio of proper nouns
    tags = nltk.pos_tag(words)
    proper_nouns = [word for word,
                    tag in tags if tag == 'NNP' or tag == 'NNPS']
    ratio_1 = len(proper_nouns) / len(words)
    # print(proper_nouns)
    print("params1:", ratio_1)
    score += ratio_1

    # Parameter 2: ratio of numerical data
    numerical_data = [word for word in words if word.isdigit()]
    ratio_2 = len(numerical_data) / len(words)
    print("params2:", ratio_2)
    score += ratio_2

    # Taken from Similarity code
    score += ratio_3

    # Parameter 4: ratio of words in title
    # Assume we have access to the title of the document

    title = title.lower()
    # Tokenize the title by word
    title_words = nltk.word_tokenize(title)
    # Remove stopwords from title words

    title_words = [word for word in title_words if word not in stopwords]
    # Count how many words in title are in sentence
    matching_words = [word for word in words if word in title_words]
    ratio_4 = len(matching_words) / len(words)
    print("params4:", ratio_4)
    score += ratio_4

    # Parameter 5: ratio of theme words
    print("sentence: ", words)
    count = 0
    for word in theme_words_arr:
        count += sentence.count(word)
    print("Inside: ", theme_words_arr)
    print("ratio5: ", count/len(words))

    return score


# Assume we have access to the whole document as a list of sentences
document = ["Natural Language Processing tutorial Language with  filter Python", "This Language is a tutorial on how analyze to use NLTK for NLP.",
            "You will learn Language   how to tokenize, filter, stem, tag, chunk, and analyze text."]

# Define a sentence to test the function
sentence = "This tutorial will teach you how to use NLTK for natural Language processing."
# Call the function and print the result

theme_words_arr = theme_words(document)
print("Theme Words: ", theme_words_arr)

score = sentence_score(sentence, theme_words_arr,
                       "Natural Language Processing with Python", 2)
print("Score: ", score)
