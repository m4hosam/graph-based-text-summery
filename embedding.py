import numpy as np
from gensim.models import KeyedVectors
from transformers import AutoModel, AutoTokenizer
from preprocessing import preprocess_text
# from transformers import DistilBertModel, DistilBertTokenizer, BertModel, BertTokenizer
# from nltk.tokenize import word_tokenize
# import torch


import warnings
import logging
warnings.simplefilter('ignore')
logging.disable(logging.WARNING)


# Load the model

def get_model(model_type, path):
    if model_type == "glove":
        return load_glove_model(path), None
    elif model_type == "bert":
        return load_bert_model(path)
    elif model_type == "distilbert":
        return load_bert_model(model_directory="models/distilbert", model_name='distilbert-base-uncased')
    else:
        raise ValueError(
            "Invalid model type. Please use 'glove', 'bert', or 'distilbert'.")


def load_glove_model(file_path='models/glove.6B.50d.word2vec.txt'):
    # model = KeyedVectors.load_word2vec_format('glove.6B.50d.txt', no_header=True)
    return KeyedVectors.load_word2vec_format(file_path, binary=False)


def load_bert_model(model_directory="models/bert", model_name="bert-base-uncased"):
    # Load BERT model and tokenizer
    bert_model = AutoModel.from_pretrained(model_name)
    # local_files_only=True
    # bert_model.eval()
    bert_tokenizer = AutoTokenizer.from_pretrained(model_name)
    return bert_model, bert_tokenizer


'''
def load_distilbert_model(model_directory="models/distilbert", model_name="distilbert-base-uncased"):
    # Load DistilBERT model and tokenizer
    distilbert_model = AutoModel.from_pretrained(model_directory)
    distilbert_tokenizer = AutoTokenizer.from_pretrained(model_directory)
    return distilbert_model, distilbert_tokenizer
'''


def sentence_vector_glove(sentence, embeddings):
    # words = word_tokenize(sentence)
    words = preprocess_text(sentence)[0]
    word_vectors = [embeddings[word] for word in words if word in embeddings]
    # print(word_vectors)
    if not word_vectors:
        return np.zeros(embeddings.vector_size)

    return np.mean(word_vectors, axis=0)


def sentence_vector_bert(sentence, model, tokenizer):
    # print(tokenizer(sentence))
    inputs = tokenizer(sentence, return_tensors="pt")
    # print("inputs: ")
    # print(inputs)
    outputs = model(**inputs)
    # for i, token_str in enumerate(outputs):
    #     print(i, token_str)
    return outputs.last_hidden_state.mean(dim=1).detach().numpy()


def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def sentence_similarity(sentence1, sentence2, method="glove", embeddings=None, bert_model=None, bert_tokenizer=None):
    if method == "glove":
        vec1 = sentence_vector_glove(sentence1, embeddings)
        vec2 = sentence_vector_glove(sentence2, embeddings)
    elif method == "bert":
        vec1 = sentence_vector_bert(
            sentence1, bert_model, bert_tokenizer).reshape(-1)
        vec2 = sentence_vector_bert(
            sentence2, bert_model, bert_tokenizer).reshape(-1)
    else:
        raise ValueError("Invalid method. Choose either 'glove' or 'bert'.")

    return cosine_similarity(vec1, vec2)

# The codes below are just for testing


'''
# Load GloVe word embeddings
embeddings = load_glove_model('models/glove.6B.50d.word2vec.txt')
# print(embeddings.similarity('night', 'day'))
'''

'''
# Load BERT model and tokenizer
model_directory = "models/bert"
model_name = "bert-base-uncased"

bert_model = AutoModel.from_pretrained(model_name)  # local_files_only=True
# bert_model.eval()
bert_tokenizer = AutoTokenizer.from_pretrained(model_name)
'''

'''
# Load DistilBERT model and tokenizer from the Hugging Face Model Hub
# model_name = "distilbert-base-uncased"
# distilbert_model = DistilBertModel.from_pretrained(model_name)
# distilbert_tokenizer = DistilBertTokenizer.from_pretrained(model_name)

# Save DistilBERT model and tokenizer to a local directory
# local_directory = "my_distilbert_model"
# distilbert_model.save_pretrained(local_directory)
# distilbert_tokenizer.save_pretrained(local_directory)
'''

'''
# Example usage
sentence1 = "A Christmas tree that can receive text messages has been unveiled at London's Tate Britain art gallery."
# sentence2 = "An interactive Christmas tree capable of receiving text messages was revealed at the Tate Britain gallery in London."
sentence2 = "It is the 17th year that the gallery has invited an artist to dress their Christmas tree."

similarity_glove = sentence_similarity(
    sentence1, sentence2, method="glove", embeddings=embeddings)
similarity_bert = sentence_similarity(
    sentence1, sentence2, method="bert", bert_model=bert_model, bert_tokenizer=bert_tokenizer)

print("Sentence similarity using GloVe:", similarity_glove)
print("Sentence similarity using BERT:", similarity_bert)
'''

# word1 = "apple"
# word2 = "juice"
# print(sentence_similarity(
#     word1, word2, method="glove", embeddings=embeddings))

# # List of sentences
# sentences = [
#     "This is a sample sentence.",
#     "Another example sentence.",
#     "One more sentence to process.",
#     "The final sentence in the list."
# ]

# # Compute sentence embeddings with progress bar
# sentence_vectors = []
# for sentence in tqdm.tqdm(sentences, desc="Computing sentence embeddings"):
#     vector = sentence_vector_bert(sentence, bert_model, bert_tokenizer)

#     sentence_vectors.append(vector)

# sentence_vectors = np.vstack(sentence_vectors)
# print(sentence_vectors)

'''
# Import GloVe Model with progress animation

def load_word_embeddings(file_path):
    import tqdm
    embeddings = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in tqdm.tqdm(file, desc="Loading word embeddings"):
            values = line.strip().split()
            word = values[0]
            vector = np.asarray(values[1:], dtype='float32')
            embeddings[word] = vector
    return embeddings
'''
