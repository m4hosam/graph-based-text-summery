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
    tags = nltk.pos_tag(sentence_words)
    proper_nouns = [word for word,
                    tag in tags if tag == 'NNP' or tag == 'NNPS']
    ratio_1 = len(proper_nouns) / len(sentence_words)
    # print(proper_nouns)
    print("params1:", ratio_1)
    score += ratio_1

    # Parameter 2: ratio of numerical data
    numerical_data = [word for word in sentence_words if word.isdigit()]
    ratio_2 = len(numerical_data) / len(sentence_words)
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
    matching_words = [word for word in sentence_words if word in title_words]
    ratio_4 = len(matching_words) / len(sentence_words)
    print("params4:", ratio_4)
    score += ratio_4

    # Parameter 5: ratio of theme words
    print("sentence: ", sentence_words)
    similar_to_theme_words = 0
    for word in theme_words_arr:
        similar_to_theme_words += sentence.count(word)
    print("Inside: ", theme_words_arr)
    ratio_5 = similar_to_theme_words/len(sentence_words)
    score += ratio_5
    print("ratio5: ", ratio_5)

    score = score/5

    return score


def separate_title_and_paragraph(text):
    # Split the text into lines
    lines = text.split('\n')

    # Find the first non-empty line as the title
    title = ""
    for line in lines:
        line = line.strip()
        if line != "":
            title = line.strip()
            break

    # Split the paragraph into an array of sentences
    # Join the remaining lines after the title
    paragraph = "\n".join(lines[lines.index(title)+1:])
    sentences = paragraph.split('.')

    document = []
    for sentence in sentences:
        if (sentence.strip() != ""):
            document.append(sentence.strip())

    # Return the title and array of sentences
    return title, document


def calculate_document_score(text):
    # Split the text into lines
    title, document = separate_title_and_paragraph(text)

    print("Title:", title)
    print("Sentences:", document)
    theme_words_arr = theme_words(document)
    print("Theme Words: ", theme_words_arr)

    for sentence in document:
        score = sentence_score(sentence, theme_words_arr,
                               title, 1)
        print(f"\n\nScore[{sentence}]: ", score, "\n\n")


# Example usage
text = '''
Gallery unveils interactive tree

A Christmas tree that can receive text messages has been unveiled at London's Tate Britain art gallery.

The spruce has an antenna which can receive Bluetooth texts sent by visitors to the Tate. The messages will be "unwrapped" by sculptor Richard Wentworth, who is responsible for decorating the tree with broken plates and light bulbs. It is the 17th year that the gallery has invited an artist to dress their Christmas tree. Artists who have decorated the Tate tree in previous years include Tracey Emin in 2002.

The plain green Norway spruce is displayed in the gallery's foyer. Its light bulb adornments are dimmed, ordinary domestic ones joined together with string. The plates decorating the branches will be auctioned off for the children's charity ArtWorks. Wentworth worked as an assistant to sculptor Henry Moore in the late 1960s. His reputation as a sculptor grew in the 1980s, while he has been one of the most influential teachers during the last two decades. Wentworth is also known for his photography of mundane, everyday subjects such as a cigarette packet jammed under the wonky leg of a table.
'''

calculate_document_score(text)


# title, document = separate_title_and_paragraph(text)

# print("Title:", title.strip())
# print("Sentences:", document)
# for sentence in document:
#     print("***", sentence)


# # Define a sentence to test the function
# sentence = "Its light bulb adornments are dimmed, ordinary domestic ones joined together with string"
# # Call the function and print the result

# theme_words_arr = theme_words(document)
# print("Theme Words: ", theme_words_arr)

# score = sentence_score(sentence, theme_words_arr,
#                        title.strip(), 1)
# print("Score: ", score)
