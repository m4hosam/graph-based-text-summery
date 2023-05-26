import matplotlib.pyplot as plt
import pprint
import numpy as np
import networkx as nx
# from transformers import DistilBertModel, DistilBertTokenizer
from scipy.spatial.distance import cosine
from visualize_graph import visualize_graph
from embedding import sentence_vector_bert, sentence_vector_glove

# import warnings
# import logging
# warnings.simplefilter('ignore')
# logging.disable(logging.WARNING)

# model_name = "distilbert-base-uncased"
# model = DistilBertModel.from_pretrained(model_name)
# tokenizer = DistilBertTokenizer.from_pretrained(model_name)


# def sentence_vector_bert(sentence, model, tokenizer):
#     inputs = tokenizer(sentence, return_tensors="pt")
#     outputs = model(**inputs)
#     return outputs.last_hidden_state.mean(dim=1).detach().numpy()


def compute_sentence_similarity_graph(sentences, model, tokenizer, method='bert'):
    # Create an empty graph
    G = nx.Graph()

    # Add sentence nodes to the graph
    for sentence in sentences:
        G.add_node(sentence)

    # Compute similarity matrix
    n_sentences = len(sentences)
    similarity_matrix = np.zeros((n_sentences, n_sentences))

    for i in range(n_sentences):
        for j in range(n_sentences):
            if i == j:
                similarity_matrix[i, j] = 1
            elif i < j:
                sentence1 = sentences[i]
                sentence2 = sentences[j]

                if method == "bert":
                    # Get or compute sentence embeddings
                    if "bert_embedding" not in G.nodes[sentence1]:
                        G.nodes[sentence1]["bert_embedding"] = sentence_vector_bert(
                            sentence1, model, tokenizer).reshape(-1)
                    if "bert_embedding" not in G.nodes[sentence2]:
                        G.nodes[sentence2]["bert_embedding"] = sentence_vector_bert(
                            sentence2, model, tokenizer).reshape(-1)

                    # Compute similarity
                    similarity = round(1 -
                                       cosine(G.nodes[sentence1]["bert_embedding"],
                                              G.nodes[sentence2]["bert_embedding"]), 4)

                elif method == "glove":
                    # Get or compute sentence embeddings
                    if "glove_embedding" not in G.nodes[sentence1]:
                        G.nodes[sentence1]["glove_embedding"] = sentence_vector_glove(
                            sentence1, model)
                    if "glove_embedding" not in G.nodes[sentence2]:
                        G.nodes[sentence2]["glove_embedding"] = sentence_vector_glove(
                            sentence2, model)

                    # Compute similarity
                    similarity = round(1 -
                                       cosine(G.nodes[sentence1]["glove_embedding"],
                                              G.nodes[sentence2]["glove_embedding"]), 4)

                similarity_matrix[i, j] = similarity_matrix[j, i] = similarity

                # Add edge with similarity score as an attribute
                G.add_edge(sentence1, sentence2, similarity=similarity)
    # print(G.edges)

    return similarity_matrix, G


'''
sentences = ['The cat sits outside',
             'A man is playing guitar',
             'I love pasta',
             'The new movie is awesome',
             'The cat plays in the garden',
             'A woman watches TV',
             'The new movie is so great',
             'Do you like pizza?']

similarity_matrix, graph = compute_sentence_similarity_graph(
    sentences, model, tokenizer, method='bert')


# Print similarity scores
print("Similarity Matrix:")
pprint.pprint(similarity_matrix)
# print(similarity_matrix)

# Print graph nodes and their attributes
# print("\nGraph Nodes:")
# for node in graph.nodes(data=True):
#     print(node)

visualize_graph(graph, 0.8)
'''

'''
# Draw the graph with node labels
pos = nx.spring_layout(graph, seed=42)
nx.draw(graph, pos, with_labels=True, font_weight='bold',
        node_color='skyblue', font_size=8, node_size=1000)

# Draw edge labels with similarity scores
edge_labels = nx.get_edge_attributes(graph, 'similarity')
nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_size=6)

plt.show()
'''
