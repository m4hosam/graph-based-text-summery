import random
import networkx as nx
import matplotlib.pyplot as plt
from scoreFunctions import *

from pyvis.network import Network


def extract_summary(G, min_score):
    # Filter nodes based on score
    high_score_nodes = [(node, data["score"]) for node, data in G.nodes(
        data=True) if data["score"] > min_score]

    # Sort nodes based on score in descending order
    high_score_nodes = sorted(
        high_score_nodes, key=lambda x: x[1], reverse=True)

    # Extract node names (sentences) from the list
    sentences = [node for node, _ in high_score_nodes]

    # Combine sentences into a summary
    summary = '. '.join(sentences)

    return summary


def visualize_graph(G, similarityThreshold, min_score, theme_words_arr,title):

    # Add edge_count attribute to the nodes

    for node in G.nodes():
        edge_count = sum(1 for _, _, data in G.edges(
            node, data=True) if data['similarity'] > similarityThreshold)
        G.nodes[node]['edge_count'] = edge_count
        G.nodes[node]['score'] = round(sentence_score(node, theme_words_arr,
                                                      title, edge_count/G.number_of_nodes()), 4)

    for node in G.nodes():
        if G.nodes[node]['score'] >= 0.4:
            print(G.nodes[node]['score'])
            print(node)

    # Create node labels with edge_count information
    # node_labels = {
    #     node: f"{node}\nCount: {data['edge_count']}" for node, data in G.nodes(data=True)}

    node_labels = {node: ' '.join(
        node.split()[:5]) + f"...\nCount: {data['edge_count']}\nScore: {data['score']}" for node, data in G.nodes(data=True)}

    # nx.draw_networkx_labels(graph, pos, labels=labels, font_weight='bold', font_size=8)

    pos = nx.spring_layout(G, seed=43)

    # Get the edges with similarity scores greater than min_score
    green_edges = [(u, v) for (u, v, d) in G.edges(
        data=True) if d["similarity"] >= similarityThreshold]
    gray_edges = [(u, v) for (u, v, d) in G.edges(
        data=True) if d["similarity"] < similarityThreshold]

    # Draw nodes
    nx.draw_networkx_nodes(G, pos, node_color='skyblue', node_size=1000)

    # Draw edges
    nx.draw_networkx_edges(G, pos, edgelist=green_edges,
                           edge_color="g", width=2)
    nx.draw_networkx_edges(G, pos, edgelist=gray_edges,
                           edge_color="gray", width=0.5)

    # Draw node labels with edge_count information
    nx.draw_networkx_labels(G, pos, labels=node_labels,
                            font_weight='bold', font_size=8)

    # Draw edge labels with similarity scores
    edge_labels = nx.get_edge_attributes(G, 'similarity')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=6)

    # edge_labels = nx.get_edge_attributes(G, 'similarity')
    # formatted_edge_labels = {k: f"Similarity: {v:.2f}\nScore: {G.nodes[k[0]]['score']:.2f}"
    #                          for k, v in edge_labels.items()}
    # nx.draw_networkx_edge_labels(
    #     G, pos, edge_labels=formatted_edge_labels, font_size=6)

    # plt.axis('off')

    # # Choose a node to highlight
    # highlighted_text = node_labels["The plain green Norway spruce is displayed in the gallery's foyer."]

    # # Get the position of the node
    # x, y = pos["The plain green Norway spruce is displayed in the gallery's foyer."]

    # # Add highlighted text
    # plt.text(x, y, highlighted_text, bbox=dict(facecolor='red', alpha=0.5))

    # print(extract_summary(G, 0.6))

    # Show the plot
    # plt.show()
    return extract_summary(G, min_score)


def visualize_graph_pyvis(G):
    # Create a PyVis network
    net = Network(notebook=True)

    # Add nodes and edges to the network
    for node in G.nodes():
        net.add_node(node)

    for edge in G.edges(data=True):
        node1, node2, attributes = edge
        similarity = attributes["similarity"]
        if similarity > 0.7:
            color = "green"
        else:
            color = "gray"
        net.add_edge(node1, node2, value=similarity, color=color)

    # Show the network
    net.show("graph.html")


'''
# Assume G is your graph with edges having a "similarity" attribute
G = nx.Graph()
G.add_nodes_from(["A", "B", "C", "D"])
G.add_edges_from([("A", "B", {"similarity": 0.9}), ("A", "C", {"similarity": 0.6}),
                  ("B", "D", {"similarity": 0.8}), ("C", "D", {"similarity": 0.3})])

# Visualize the graph
visualize_graph(G)

# Visualize the graph using PyVis
visualize_graph_pyvis(G)
'''