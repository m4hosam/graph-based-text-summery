from embedding import get_model
from graph import compute_sentence_similarity_graph
from visualize_graph import visualize_graph

# model, tokenizer = get_model('bert', 'models/bert')
model, tokenizer = get_model('glove', 'models/glove.6B.50d.word2vec.txt')

sentences = ['I am playing football',
             'My brother reads some books',
             'I love pasta',
             'The weather yesterday was bad',
             'The cat likes milk',
             'My manager is a nice guy',
             'My mother bought Pizza yesterday',
             'Thank you for your email']

similarity_matrix, G = compute_sentence_similarity_graph(
    sentences, model, tokenizer, method='glove')

visualize_graph(G, 0.8)

# from gensim.summarization import summarize

# input_text = """
# Gallery unveils interactive tree

# A Christmas tree that can receive text messages has been unveiled at London's Tate Britain art gallery.

# The spruce has an antenna which can receive Bluetooth texts sent by visitors to the Tate. The messages will be "unwrapped" by sculptor Richard Wentworth, who is responsible for decorating the tree with broken plates and light bulbs. It is the 17th year that the gallery has invited an artist to dress their Christmas tree. Artists who have decorated the Tate tree in previous years include Tracey Emin in 2002.

# The plain green Norway spruce is displayed in the gallery's foyer. Its light bulb adornments are dimmed, ordinary domestic ones joined together with string. The plates decorating the branches will be auctioned off for the children's charity ArtWorks. Wentworth worked as an assistant to sculptor Henry Moore in the late 1960s. His reputation as a sculptor grew in the 1980s, while he has been one of the most influential teachers during the last two decades. Wentworth is also known for his photography of mundane, everyday subjects such as a cigarette packet jammed under the wonky leg of a table.
# """

# summary = summarize(input_text, ratio=0.2)
# print(summary)


# from preprocessing import preprocess_text

# # Example of text preprocessing:
# text = "The plain green Norway spruce is displayed in the gallery's foyer."
# preprocessed_text = preprocess_text(text)
# print(preprocessed_text)
