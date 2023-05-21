# Import nltk and download data
import string
import nltk
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('stopwords')

# Define a function to calculate sentence score


# def sentence_score(sentence):
#     # Tokenize by word and by sentence
#     words = nltk.word_tokenize(sentence)
#     sentences = nltk.sent_tokenize(sentence)
#     # Initialize score
#     score = 0
#     # Parameter 1: ratio of proper nouns
#     tags = nltk.pos_tag(words)
#     proper_nouns = [word for word,
#                     tag in tags if tag == 'NNP' or tag == 'NNPS']
#     ratio_1 = len(proper_nouns) / len(words)
#     score += ratio_1
#     # Parameter 2: ratio of numerical data
#     numerical_data = [word for word in words if word.isdigit()]
#     ratio_2 = len(numerical_data) / len(words)
#     score += ratio_2
#     # Parameter 3: ratio of connected nodes
#     # Define a similarity threshold
#     threshold = 5
#     # Define a function to measure similarity between sentences

#     def similarity(sent1, sent2):
#         return nltk.edit_distance(sent1, sent2)
#     # Count how many nodes are connected by similarity
#     connected_nodes = 0
#     total_nodes = len(sentences) * (len(sentences) - 1) / 2  # n choose 2
#     for i in range(len(sentences)):
#         for j in range(i + 1, len(sentences)):
#             if similarity(sentences[i], sentences[j]) <= threshold:
#                 connected_nodes += 1
#     ratio_3 = connected_nodes / total_nodes
#     score += ratio_3
#     # Parameter 4: ratio of words in title
#     # Assume we have access to the title of the document
#     title = "Natural Language Processing with Python"
#     # Tokenize the title by word
#     title_words = nltk.word_tokenize(title)
#     # Remove stopwords from title words
#     stopwords = nltk.corpus.stopwords.words('english')
#     title_words = [word for word in title_words if word not in stopwords]
#     # Count how many words in title are in sentence
#     matching_words = [word for word in words if word in title_words]
#     ratio_4 = len(matching_words) / len(words)
#     score += ratio_4
#     # Parameter 5: ratio of theme words
#     # Assume we have access to the whole document as a list of sentences
#     document = ["Natural Language Processing with Python", "This is a tutorial on how to use NLTK for NLP.",
#                 "You will learn how to tokenize, filter, stem, tag, chunk, and analyze text.", "You will also create visualizations based on your analysis."]

#     # Join all sentences into one text
#     text = " ".join(document)
#     # Tokenize the text by word
#     text_words = nltk.word_tokenize(text)
#     # Remove stopwords from text words
#     text_words = [word for word in text_words if word not in stopwords]
#     # Calculate the frequency distribution of words in text
#     freq_dist = nltk.FreqDist(text_words)
#     # Create a text collection object from text words
#     text_collection = nltk.TextCollection(text_words)
#     # Calculate the tf-idf value of each word in text collection
#     tf_idf = {word: text_collection.tf_idf(
#         word, text_words) for word in text_words}
#     # Sort the words by their tf-idf values and select the top 10 percent as theme words
#     sorted_tf_idf = sorted(tf_idf.items(), key=lambda x: x[1], reverse=True)
#     top_10_percent = int(len(sorted_tf_idf) * 0.1)
#     theme_words = [word for word, value in sorted_tf_idf[:top_10_percent]]
#     print(theme_words)


def sentence_score(sentence):
    # Tokenize by word and by sentence
    words = nltk.word_tokenize(sentence)
    sentences = nltk.sent_tokenize(sentence)
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

    # # Parameter 3: ratio of connected nodes
    # # Define a similarity threshold
    # threshold = 5
    # # Define a function to measure similarity between sentences

    # def similarity(sent1, sent2):
    #     return nltk.edit_distance(sent1, sent2)
    # # Count how many nodes are connected by similarity
    # connected_nodes = 0
    # total_nodes = len(sentences) * (len(sentences) - 1) / 2  # n choose 2
    # for i in range(len(sentences)):
    #     for j in range(i + 1, len(sentences)):
    #         if similarity(sentences[i], sentences[j]) <= threshold:
    #             connected_nodes += 1
    # ratio_3 = connected_nodes / total_nodes
    # score += ratio_3

    # Parameter 4: ratio of words in title
    # Assume we have access to the title of the document
    title = "Natural Language Processing with Python"
    title = title.lower()
    # Tokenize the title by word
    title_words = nltk.word_tokenize(title)
    # Remove stopwords from title words
    stopwords = nltk.corpus.stopwords.words('english')
    title_words = [word for word in title_words if word not in stopwords]
    # Count how many words in title are in sentence
    matching_words = [word for word in words if word in title_words]
    ratio_4 = len(matching_words) / len(words)
    print("params4:", ratio_4)
    score += ratio_4

    # Parameter 5: ratio of theme words
    # Assume we have access to the whole document as a list of sentences
    document = ["Natural Language Processing tutorial Language with  filter Python", "This Language is a tutorial on how analyze to use NLTK for NLP.",
                "You will learn Language   how to tokenize, filter, stem, tag, chunk, and analyze text."]

    stopwords_punctuation = set(stopwords + list(string.punctuation))
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

    # Print the frequencies
    for word, frequency in freq_dist.items():
        print(word, frequency)
    # Create a text collection object from text words
    text_collection = nltk.TextCollection(text_words)

    # Calculate the tf-idf value of each word in text collection
    tf_idf = {word: text_collection.tf_idf(
        word, text_words) for word in text_words}
    # Sort the words by their tf-idf values and select the top 10 percent as theme words
    sorted_tf_idf = sorted(tf_idf.items(), key=lambda x: x[1], reverse=True)
    print(sorted_tf_idf)
    top_10_percent = int(len(sorted_tf_idf) * 0.1)
    theme_words = [word for word, value in sorted_tf_idf[:top_10_percent]]
    print(theme_words)

    return score


# Define a sentence to test the function
sentence = "This tutorial will teach you how to use NLTK for natural language processing."
# Call the function and print the result
result = sentence_score(sentence)
print(result)
